from django.db import models
from django.contrib.auth.models import User


class LottoDrawing(models.Model):
    """회차별 추첨 결과 모델"""
    
    round_no = models.PositiveIntegerField(
        unique=True,
        verbose_name='회차 번호'
    )
    draw_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='추첨 일시'
    )
    num1 = models.PositiveSmallIntegerField(verbose_name='당첨번호 1')
    num2 = models.PositiveSmallIntegerField(verbose_name='당첨번호 2')
    num3 = models.PositiveSmallIntegerField(verbose_name='당첨번호 3')
    num4 = models.PositiveSmallIntegerField(verbose_name='당첨번호 4')
    num5 = models.PositiveSmallIntegerField(verbose_name='당첨번호 5')
    num6 = models.PositiveSmallIntegerField(verbose_name='당첨번호 6')
    bonus = models.PositiveSmallIntegerField(verbose_name='보너스 번호')

    class Meta:
        verbose_name = '추첨 결과'
        verbose_name_plural = '추첨 결과 목록'
        ordering = ['-round_no']  # 최신 회차가 먼저

    def __str__(self):
        return f"제{self.round_no}회차"

    def get_winning_numbers(self):
        """당첨 번호 6개를 리스트로 반환"""
        return [self.num1, self.num2, self.num3, self.num4, self.num5, self.num6]


class LottoTicket(models.Model):
    """구매한 복권 정보 모델"""
    
    PURCHASE_TYPE_CHOICES = [
        ('manual', '수동'),
        ('auto', '자동'),
    ]
    
    RANK_CHOICES = [
        (1, '1등'),
        (2, '2등'),
        (3, '3등'),
        (4, '4등'),
        (5, '5등'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name='구매자'
    )
    drawing = models.ForeignKey(
        LottoDrawing,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets',
        verbose_name='참여 회차'
    )
    
    # 선택한 6개 숫자
    num1 = models.PositiveSmallIntegerField()
    num2 = models.PositiveSmallIntegerField()
    num3 = models.PositiveSmallIntegerField()
    num4 = models.PositiveSmallIntegerField()
    num5 = models.PositiveSmallIntegerField()
    num6 = models.PositiveSmallIntegerField()
    
    purchase_type = models.CharField(
        max_length=10,
        choices=PURCHASE_TYPE_CHOICES,
        verbose_name='구매 방식'
    )
    purchase_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='구매 일시'
    )
    rank = models.PositiveSmallIntegerField(
        choices=RANK_CHOICES,
        null=True,
        blank=True,
        verbose_name='당첨 등수'
    )

    class Meta:
        verbose_name = '구매 복권'
        verbose_name_plural = '구매 복권 목록'
        ordering = ['-purchase_date']

    def __str__(self):
        return f"{self.user.username} - {self.get_numbers_display()}"

    def get_numbers(self):
        """선택한 6개 번호를 리스트로 반환"""
        return [self.num1, self.num2, self.num3, self.num4, self.num5, self.num6]
    
    def get_numbers_display(self):
        """번호를 문자열로 보기 좋게 반환"""
        nums = sorted(self.get_numbers())
        return ', '.join(str(n) for n in nums)