# backtestapp/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('ejecutar', views.ejecutar_backtest, name='ejecutar_backtest'),
    path('', views.home, name='inicio'),
    path('input/', views.input_page, name='input_page'),
    
    
]
