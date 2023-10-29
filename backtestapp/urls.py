# backtestapp/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='inicio'),
    path('input/', views.input_page, name='input_page'),
    
    
]
