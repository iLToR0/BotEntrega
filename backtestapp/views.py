from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
import backtrader as bt
from .strategy import ThreeCandlePatternStrategy
from .models import *
import pandas as pd
from django.http import HttpRequest
from django.views import View
from .forms import StrategyParametersForm



# Create your views here.

def ejecutar_backtest(request):
    #if __name__ == "__main__":
        cerebro = bt.Cerebro()

    # Agregar un feed de datos (puedes usar tus propios datos aquí)
        archivo_csv = 'dataMonth.csv'

    # Cargar los datos en un DataFrame de pandas
        df = pd.read_csv(archivo_csv, sep=';', header=None, names=['datetime', 'open', 'high', 'low', 'close', 'volume'])

    # Añadir milisegundos a la columna 'datetime'
        df['datetime'] = pd.to_datetime(df['datetime'], format='%d%m%Y %H%M%S')

    # Establecer la columna 'datetime' como índice de tiempo
        df.set_index('datetime', inplace=True)
        df = df[::-1]

    # Convertir las columnas numéricas a tipo float
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)

        data_feed = bt.feeds.PandasData(dataname=df)

        cerebro.adddata(data_feed)

    # Agregar la estrategia al cerebro
        cerebro.addstrategy(ThreeCandlePatternStrategy)
        broker = bt.brokers.BrokerBack()
        broker.setcash(10000000.00)
        cerebro.setbroker(broker)
    
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='misanalisis')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='midrawdown')
        #print(data_feed)

    

    # Ejecutar el backtest
        thestrats = cerebro.run()
        thestrat = thestrats[0]
    
    
        print("Picos detectados:")
        

        for peak in cerebro.runstrats[0][0].resistenciaBuy:
            print(f"Pico: {peak:.2f}")

        print(cerebro.runstrats[0][0].valorInicialCartera)
        print(cerebro.runstrats[0][0].valorFinalCartera)

        calculo = (cerebro.runstrats[0][0].valorFinalCartera - cerebro.runstrats[0][0].valorInicialCartera) / cerebro.runstrats[0][0].valorInicialCartera * 100
        print(calculo)
    
        print('estadisticas:', thestrat.analyzers.misanalisis.print())
        print('drawdown:', thestrat.analyzers.midrawdown.print())

        #cerebro.plot(style="candlestick")
        return render(request, 'resultados.html',{    
                                                   'drawdown': thestrat.analyzers.midrawdown.get_analysis(), 
                                                   'misanalisis': thestrat.analyzers.misanalisis.get_analysis()})


def input_page(request):
    if request.method == 'POST':
        form = StrategyParametersForm(request.POST)
        if form.is_valid():
            # Obtén los valores del formulario
           
            ValorTK = form.cleaned_data['valorTK']
            StartHour = form.cleaned_data['startHour']
            EndHour = form.cleaned_data['endHour']
            fechaDesde = form.cleaned_data['fechaDesde']
            fechaHasta = form.cleaned_data['fechaHasta']
            tipoTK = form.cleaned_data['tipoTK']


            # Crear un objeto cerebro de backtrader
            cerebro = bt.Cerebro()
        

            def no_hay_datos_disponibles(df, fechaDesde, fechaHasta,request):
                fechaDesde = pd.to_datetime(fechaDesde)
                fechaHasta = pd.to_datetime(fechaHasta)
                return ((df.index.min() >= fechaDesde) or (df.index.max() <= fechaHasta))

                
            def fechaIgual (fechaDesde, fechaHasta,request):
                fechaDesde = pd.to_datetime(fechaDesde)
                fechaHasta = pd.to_datetime(fechaHasta)
                if fechaDesde == fechaHasta:
                    return True
                else:
                    return False

            if fechaIgual(fechaDesde, fechaHasta,request) == True:
                errorFechaIgual = "Las fechas no pueden ser iguales. Por favor, cambie las fechas."
                return render(request, 'input_page.html', {'form': form, 'error_message': errorFechaIgual})

        
            


            archivo_csv = 'dataKitInicial.csv'

            # Cargar los datos en un DataFrame de pandas
            df = pd.read_csv(archivo_csv, sep=';', header=None, names=['datetime', 'open', 'high', 'low', 'close', 'volume'])

            # Añadir milisegundos a la columna 'datetime'
            df['datetime'] = pd.to_datetime(df['datetime'], format='%d%m%Y %H%M%S')

            # Establecer la columna 'datetime' como índice de tiempo
            df.set_index('datetime', inplace=True)

            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            
            
            
            fecha_desde = fechaDesde
            fecha_hasta = fechaHasta

            if no_hay_datos_disponibles(df, fechaDesde, fechaHasta, request) == True:

                error_message = "No hay datos disponibles para las fechas ingresadas. Por favor, cambie las fechas. ("+ df.index.min() + "-" + df.index.max() + ")"
                return render(request, 'input_page.html', {'form': form, 'error_message': error_message})

            df = df.loc[fecha_desde:fecha_hasta]

            # Convertir las columnas numéricas a tipo float
            df['open'] = df['open'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            df['close'] = df['close'].astype(float)
            df['volume'] = df['volume'].astype(float)

            data_feed = bt.feeds.PandasData(dataname=df, timeframe=bt.TimeFrame.Minutes)

            cerebro.adddata(data_feed)


            cerebro.addstrategy(ThreeCandlePatternStrategy,  tipoTK, ValorTK, StartHour, EndHour)

            cerebro.addsizer(bt.sizers.FixedSize, stake=20)
            broker = bt.brokers.BrokerBack(checksubmit=False)
            broker.setcommission(commission=0.125, margin=1)
            broker.setcash(100000.00)
            cerebro.setbroker(broker)
            

            cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='misanalisis')
            cerebro.addanalyzer(bt.analyzers.DrawDown, _name='midrawdown')

            
            # Ejecutar el backtest
            
            
            thestrats = cerebro.run()
            thestrat = thestrats[0]




            # Procesar los resultados y análisis
            

            print('estadisticas:', thestrat.analyzers.misanalisis.print())
            print('drawdown:', thestrat.analyzers.midrawdown.print())


            trade_analysis = thestrat.analyzers.misanalisis.get_analysis()
            drawDown_analysis = thestrat.analyzers.midrawdown.get_analysis()

            lenDrawDown =drawDown_analysis['len'] 
            drawdown = round(drawDown_analysis['drawdown'],2)
            moneydraw = drawDown_analysis['moneydown']

            drawMax = drawDown_analysis['max']['len']
            drawMaxPerc = round(drawDown_analysis['max']['drawdown'],2)
            moneydrowMax = drawDown_analysis['max']['moneydown']
            total_trades = trade_analysis['total']['total']

            won_longest = trade_analysis['streak']['won']['longest']


            lost_longest = trade_analysis['streak']['lost']['longest']
            wins = trade_analysis['won']['total']
            losts = trade_analysis['lost']['total']
            longTotal = trade_analysis['long']['total']
            shortTotal = trade_analysis['short']['total']
            longWins = trade_analysis['long']['won']
            longLost = trade_analysis['long']['lost']
            shortWins = trade_analysis['short']['won']
            shortLost = trade_analysis['short']['lost']
            recorridoEnOperaciones = trade_analysis['len']['total']
            promedioVelasOperacion = round(trade_analysis['len']['average'],2)
            
            maxVelasOperacion = trade_analysis['len']['max']
            minVelasOperacion = trade_analysis['len']['min']
            recorridoOperacionesGanadas = trade_analysis['len']['won']['total']
            promedioVelasOperacionGanadas = round(trade_analysis['len']['won']['average'],2)
            maxVelasOperacionGanadas = trade_analysis['len']['won']['max']
            minVelasOperacionGanadas = trade_analysis['len']['won']['min']
            recorridoOperacionesPerdidas = trade_analysis['len']['lost']['total']
            promedioVelasOperacionPerdidas = round(trade_analysis['len']['lost']['average'],2)
            maxVelasOperacionPerdidas = trade_analysis['len']['lost']['max']
            minVelasOperacionPerdidas = trade_analysis['len']['lost']['min']
            long_total = trade_analysis['len']['long']['total']
            long_average = trade_analysis['len']['long']['average']
            long_max = trade_analysis['len']['long']['max']
            long_min = trade_analysis['len']['long']['min']
            pnl = trade_analysis['pnl']['net']['total']
            pnlWins = trade_analysis['won']['pnl']['total']
            pnlLosts= trade_analysis['lost']['pnl']['total']
            pnlLongs = trade_analysis['long']['pnl']['total']
            pnlShort = trade_analysis['short']['pnl']['total']
            pnlLongWins = trade_analysis['long']['pnl']['won']['total']
            pnlLongLosts = trade_analysis['long']['pnl']['lost']['total']
            pnlShortWins = trade_analysis['short']['pnl']['won']['total']
            pnlShortLosts = trade_analysis['short']['pnl']['lost']['total']

            long_won_total = trade_analysis['len']['long']['won']['total']
            long_won_average = trade_analysis['len']['long']['won']['average']
            long_won_max = trade_analysis['len']['long']['won']['max']
            long_won_min = trade_analysis['len']['long']['won']['min']

            long_lost_total = trade_analysis['len']['long']['lost']['total']
            long_lost_average = trade_analysis['len']['long']['lost']['average']
            long_lost_max = trade_analysis['len']['long']['lost']['max']
            long_lost_min = trade_analysis['len']['long']['lost']['min']

            # Estadísticas para "short"
            short_total = trade_analysis['len']['short']['total']
            short_average = round(trade_analysis['len']['short']['average'],2)
            short_max = trade_analysis['len']['short']['max']
            short_min = trade_analysis['len']['short']['min']

            short_won_total = trade_analysis['len']['short']['won']['total']
            short_won_average = trade_analysis['len']['short']['won']['average']
            short_won_max = trade_analysis['len']['short']['won']['max']
            short_won_min = trade_analysis['len']['short']['won']['min']

            short_lost_total = trade_analysis['len']['short']['lost']['total']
            short_lost_average = trade_analysis['len']['short']['lost']['average']
            short_lost_max = trade_analysis['len']['short']['lost']['max']
            short_lost_min = trade_analysis['len']['short']['lost']['min']


            print('total trades:', total_trades)
          



            # Redirige a la página de resultados
            return render(request, 'results.html',{
                                                 'lendraw':lenDrawDown,
                                                 'drawdown':drawdown,
                                                 'moneydown':moneydraw,
                                                 'lenMax':drawMax,
                                                 'drawMax':drawMaxPerc,
                                                 'moneyMax':moneydrowMax,    
                                                 'totaltrades':total_trades,
                                                 'rachaganadora': won_longest,
                                                 'rachaperdedora': lost_longest,
                                                 'totalganados' : wins,
                                                 'totalperdidos':losts,
                                                 'longTotal':longTotal,
                                                 'shortTotal':shortTotal,
                                                 'longWins':longWins,
                                                 'longLost':longLost,
                                                 'shortWins':shortWins,
                                                 'shortLost':shortLost,
                                                 'recorridoEnOperaciones':recorridoEnOperaciones,
                                                 'promedioVelasOperacion':promedioVelasOperacion,
                                                 'maxvelasOperacion':maxVelasOperacion,
                                                 'minvelasOperacion':minVelasOperacion,
                                                 'recorridoOperacionesGanadas':recorridoOperacionesGanadas,
                                                 'promedioVelasOperacionGanadas':promedioVelasOperacionGanadas,
                                                 'maxvelasOperacionGanadas':maxVelasOperacionGanadas,
                                                 'minvelasOperacionGanadas':minVelasOperacionGanadas,
                                                 'recorridoOperacionesPerdidas':recorridoOperacionesPerdidas,
                                                 'promedioVelasOperacionPerdidas':promedioVelasOperacionPerdidas,
                                                 'maxvelasOperacionPerdidas':maxVelasOperacionPerdidas,
                                                 'minvelasOperacionPerdidas':minVelasOperacionPerdidas,
                                                 'long_total': long_total,
                                                 'long_average': long_average,
                                                 'long_max': long_max,
                                                 'long_min': long_min,
                                                 'long_won_total': long_won_total,
                                                 'long_won_average': long_won_average,
                                                 'long_won_max': long_won_max,
                                                 'long_won_min': long_won_min,
                                                 'long_lost_total': long_lost_total,
                                                 'long_lost_average': long_lost_average,
                                                 'long_lost_max': long_lost_max,
                                                 'long_lost_min': long_lost_min,
                                                 'short_total': short_total,
                                                 'short_average': short_average,
                                                 'short_max': short_max,
                                                 'short_min': short_min,
                                                 'short_won_total': short_won_total,
                                                 'short_won_average': short_won_average,
                                                 'short_won_max': short_won_max,
                                                 'short_won_min': short_won_min,
                                                 'short_lost_total': short_lost_total,
                                                 'short_lost_average': short_lost_average,
                                                 'short_lost_max': short_lost_max,
                                                 'short_lost_min': short_lost_min,
                                                 'pnl':pnl,
                                                 'pnlwins':pnlWins,
                                                 'pnlLosts':pnlLosts,
                                                 'pnllong':pnlLongs,
                                                 'pnlShort':pnlShort,
                                                 'pnlLongWins':pnlLongWins,
                                                 'pnlLongLosts':pnlLongLosts,
                                                 'pnlShortWins':pnlShortWins,
                                                 'pnlShortLosts':pnlShortLosts,



                                                 
                                                
                                                

                                                 'midrawdown': thestrat.analyzers.midrawdown.get_analysis()})
    else:
        form = StrategyParametersForm()
    return render(request, 'input_page.html', {'form': form})

    
   


def home(request):
      return render(request, 'home.html')

