from django.contrib import admin
from .models import LottoDrawing, LottoTicket


@admin.register(LottoDrawing)
class LottoDrawingAdmin(admin.ModelAdmin):
    """추첨 결과 관리자 페이지"""
    list_display = ['round_no', 'draw_date', 'get_winning_numbers_display', 'bonus']
    list_filter = ['draw_date']
    search_fields = ['round_no']
    ordering = ['-round_no']

    def get_winning_numbers_display(self, obj):
        """당첨 번호를 보기 좋게 표시"""
        nums = sorted(obj.get_winning_numbers())
        return ', '.join(str(n) for n in nums)
    
    get_winning_numbers_display.short_description = '당첨 번호'


@admin.register(LottoTicket)
class LottoTicketAdmin(admin.ModelAdmin):
    """구매 복권 관리자 페이지"""
    list_display = ['id', 'user', 'get_numbers_display', 'purchase_type', 'purchase_date', 'drawing', 'rank']
    list_filter = ['purchase_type', 'rank', 'purchase_date', 'drawing']
    search_fields = ['user__username']
    ordering = ['-purchase_date']
    readonly_fields = ['purchase_date']