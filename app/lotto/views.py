from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LottoDrawing, LottoTicket
from .forms import ManualLottoForm
from .utils import generate_auto_numbers, validate_manual_numbers


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
            # 자동 번호 생성
            numbers = generate_auto_numbers()
            ticket = LottoTicket.objects.create(
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
                ticket = LottoTicket.objects.create(
                    user=request.user,
                    num1=numbers[0], num2=numbers[1], num3=numbers[2],
                    num4=numbers[3], num5=numbers[4], num6=numbers[5],
                    purchase_type='manual'
                )
                messages.success(request, f'수동 번호로 구매가 완료되었습니다! 선택된 번호: {", ".join(map(str, sorted(numbers)))}')
                return redirect('my_tickets')
            else:
                # 폼 에러 시 다시 렌더링
                return render(request, 'lotto/buy.html', {'manual_form': form})
    
    # GET 요청
    form = ManualLottoForm()
    return render(request, 'lotto/buy.html', {'manual_form': form})


@login_required
def my_tickets(request):
    """내 구매 내역"""
    tickets = LottoTicket.objects.filter(user=request.user).order_by('-purchase_date')
    return render(request, 'lotto/my_tickets.html', {'tickets': tickets})