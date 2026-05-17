from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import LottoDrawing, LottoTicket
from .forms import ManualLottoForm
from .utils import generate_auto_numbers, perform_drawing, check_rank
from .decorators import staff_required


def home(request):
    """메인 페이지 - 최근 당첨 번호 표시"""
    latest_drawing = LottoDrawing.objects.first()
    context = {
        'latest_drawing': latest_drawing,
    }
    return render(request, 'lotto/home.html', context)


@login_required
def buy(request):
    """복권 구매 페이지"""
    if request.method == 'POST':
        purchase_type = request.POST.get('purchase_type')
        
        if purchase_type == 'auto':
            numbers = generate_auto_numbers()
            LottoTicket.objects.create(
                user=request.user,
                num1=numbers[0], num2=numbers[1], num3=numbers[2],
                num4=numbers[3], num5=numbers[4], num6=numbers[5],
                purchase_type='auto'
            )
            messages.success(request, f'자동 번호로 구매가 완료되었습니다! 선택된 번호: {", ".join(map(str, numbers))}')
            return redirect('my_tickets')
        
        elif purchase_type == 'manual':
            form = ManualLottoForm(request.POST)
            if form.is_valid():
                numbers = form.get_numbers()
                LottoTicket.objects.create(
                    user=request.user,
                    num1=numbers[0], num2=numbers[1], num3=numbers[2],
                    num4=numbers[3], num5=numbers[4], num6=numbers[5],
                    purchase_type='manual'
                )
                messages.success(request, f'수동 번호로 구매가 완료되었습니다! 선택된 번호: {", ".join(map(str, sorted(numbers)))}')
                return redirect('my_tickets')
            else:
                return render(request, 'lotto/buy.html', {'manual_form': form})
    
    form = ManualLottoForm()
    return render(request, 'lotto/buy.html', {'manual_form': form})


@login_required
def my_tickets(request):
    """내 구매 내역"""
    tickets = LottoTicket.objects.filter(user=request.user).order_by('-purchase_date')
    return render(request, 'lotto/my_tickets.html', {'tickets': tickets})


# ========== 관리자 기능 ==========

@staff_required
def admin_drawing(request):
    """추첨 실행 페이지 (관리자 전용)"""
    drawings = LottoDrawing.objects.all().order_by('-round_no')
    
    if request.method == 'POST':
        # 추첨되지 않은 티켓 개수 확인
        pending_tickets = LottoTicket.objects.filter(drawing__isnull=True)
        pending_count = pending_tickets.count()
        
        if pending_count == 0:
            messages.warning(request, '추첨할 티켓이 없습니다. 먼저 티켓 구매가 이루어져야 합니다.')
            return redirect('admin_drawing')
        
        # 다음 회차 번호 계산
        last_drawing = LottoDrawing.objects.first()
        next_round = (last_drawing.round_no + 1) if last_drawing else 1
        
        # 추첨 실행
        winning_numbers, bonus_number = perform_drawing()
        
        # 추첨 결과 저장
        new_drawing = LottoDrawing.objects.create(
            round_no=next_round,
            num1=winning_numbers[0], num2=winning_numbers[1], num3=winning_numbers[2],
            num4=winning_numbers[3], num5=winning_numbers[4], num6=winning_numbers[5],
            bonus=bonus_number
        )
        
        # 모든 추첨 대기 티켓의 등수 판정 및 업데이트
        for ticket in pending_tickets:
            ticket_numbers = ticket.get_numbers()
            rank = check_rank(ticket_numbers, winning_numbers, bonus_number)
            ticket.drawing = new_drawing
            ticket.rank = rank
            ticket.save()
        
        messages.success(
            request,
            f'제{next_round}회차 추첨 완료! '
            f'당첨번호: {", ".join(map(str, winning_numbers))} + 보너스 {bonus_number} | '
            f'{pending_count}개의 티켓에 대해 당첨 판정 완료.'
        )
        return redirect('admin_winners', round_no=next_round)
    
    # 추첨 대기 중인 티켓 수
    pending_count = LottoTicket.objects.filter(drawing__isnull=True).count()
    
    return render(request, 'lotto/admin_drawing.html', {
        'drawings': drawings,
        'pending_count': pending_count,
    })


@staff_required
def admin_sales(request):
    """판매 내역 통계 (관리자 전용)"""
    # 전체 통계
    total_tickets = LottoTicket.objects.count()
    auto_count = LottoTicket.objects.filter(purchase_type='auto').count()
    manual_count = LottoTicket.objects.filter(purchase_type='manual').count()
    
    # 회차별 통계
    drawings_with_stats = []
    for drawing in LottoDrawing.objects.all().order_by('-round_no'):
        tickets = LottoTicket.objects.filter(drawing=drawing)
        drawings_with_stats.append({
            'drawing': drawing,
            'total': tickets.count(),
            'auto': tickets.filter(purchase_type='auto').count(),
            'manual': tickets.filter(purchase_type='manual').count(),
        })
    
    # 추첨 대기 티켓
    pending_tickets = LottoTicket.objects.filter(drawing__isnull=True)
    
    # 사용자별 구매량 TOP 10
    from django.contrib.auth.models import User
    top_users = User.objects.annotate(
        ticket_count=Count('tickets')
    ).filter(ticket_count__gt=0).order_by('-ticket_count')[:10]
    
    return render(request, 'lotto/admin_sales.html', {
        'total_tickets': total_tickets,
        'auto_count': auto_count,
        'manual_count': manual_count,
        'drawings_with_stats': drawings_with_stats,
        'pending_count': pending_tickets.count(),
        'top_users': top_users,
    })


@staff_required
def admin_winners(request, round_no=None):
    """당첨자 내역 (관리자 전용)"""
    if round_no:
        drawing = get_object_or_404(LottoDrawing, round_no=round_no)
    else:
        drawing = LottoDrawing.objects.first()  # 최근 회차
    
    if not drawing:
        return render(request, 'lotto/admin_winners.html', {
            'drawing': None,
            'all_drawings': [],
        })
    
    # 등수별 당첨자 정리
    winners_by_rank = {}
    for rank in [1, 2, 3, 4, 5]:
        winners = LottoTicket.objects.filter(
            drawing=drawing,
            rank=rank
        ).select_related('user').order_by('purchase_date')
        winners_by_rank[rank] = winners
    
    # 낙첨 카운트
    losers_count = LottoTicket.objects.filter(
        drawing=drawing,
        rank__isnull=True
    ).count()
    
    # 회차 선택용
    all_drawings = LottoDrawing.objects.all().order_by('-round_no')
    
    return render(request, 'lotto/admin_winners.html', {
        'drawing': drawing,
        'winners_by_rank': winners_by_rank,
        'losers_count': losers_count,
        'all_drawings': all_drawings,
    })