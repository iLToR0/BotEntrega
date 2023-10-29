from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
import backtrader as bt
from backtestapp.services.BackTestManager import BacktestManager

from backtestapp.services.DataService import DataService
from .strategy import ThreeCandlePatternStrategy
from .models import *
import pandas as pd
from django.http import HttpRequest
from django.views import View
from .forms import StrategyParametersForm
from datetime import timedelta




def input_page(request):
    if request.method == 'POST':
        form = StrategyParametersForm(request.POST)
        if form.is_valid():
            
            archivo_csv = 'dataKitInicial.csv'
            strategy = ThreeCandlePatternStrategy

            backtest_manager = BacktestManager(form, archivo_csv, strategy)
            
            results = backtest_manager.run_backtest()
            return render(request, 'results.html',results)
    else:
        form = StrategyParametersForm()
    return render(request, 'input_page.html', {'form': form})

    
   


def home(request):
      return render(request, 'home.html')
