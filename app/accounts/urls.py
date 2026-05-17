from django.urls import path, include
from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', include('django.contrib.auth.urls')),  # Django 내장 로그인/로그아웃 등
]