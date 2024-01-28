# backtestapp/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='inicio'),
    path('input/', views.input_page, name='input_page'),
    path('', views.home, name='inicio'),
    path('input2/', views.input_page2, name='input_page2'),
    
    
    
]
