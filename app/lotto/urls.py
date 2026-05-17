from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('buy/', views.buy, name='buy'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),

    # 관리자 기능
    path('manage/drawing/', views.admin_drawing, name='admin_drawing'),
    path('manage/sales/', views.admin_sales, name='admin_sales'),

    path(
        'manage/winners/',
        views.admin_winners,
        name='admin_winners'
    ),

    path(
        'manage/winners/<int:round_no>/',
        views.admin_winners,
        name='admin_winners'
    ),
]