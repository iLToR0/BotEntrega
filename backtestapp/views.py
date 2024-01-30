import logging
from django.shortcuts import render
from backtestapp.exeptions.NoTradesExeption import NoTradesException
from backtestapp.services.BackTestManager import BacktestManager
from backtestapp.services.Backtestmanager2 import BacktestManager2
from .strategy import ThreeCandlePatternStrategy
from .models import *
from .forms import StrategyParametersForm
from django.template import RequestContext
from .forms import StrategyParameters2Form
from .MauriStrategy import MauricioStrategy
from datetime import datetime
import backtrader as bt
import pandas as pd
import os


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

def input_page2(request):
    
    if request.method == 'POST':
        form = StrategyParameters2Form(request.POST)
        if form.is_valid():
            try:
 
                strategy = MauricioStrategy

                backtest_manager = BacktestManager2(form, strategy)
                
                results = backtest_manager.run_backtest()
                return render(request, 'results.html',results)
            
            except NoTradesException as e:

                # Manejar la excepción y renderizar la plantilla 'exception.html'
                return render(request, 'exception.html', {'error_message': str(e)})
    else:
        form = StrategyParameters2Form()
    return render(request, 'input_page2.html', {'form': form})
   


def home(request):
      return render(request, 'home.html')
