from django.shortcuts import render
from backtestapp.services.BackTestManager import BacktestManager
from .strategy import ThreeCandlePatternStrategy
from .models import *
from .forms import StrategyParametersForm
from django.template import RequestContext
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
