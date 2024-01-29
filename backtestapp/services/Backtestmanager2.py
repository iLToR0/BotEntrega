import backtrader as bt
from backtestapp.services.BackTestAnalyzer import BacktestAnalyzer
import pandas as pd



class BacktestManager2:

    def __init__(self, form, strategy):
        #self.archivo_csv = archivo_csv
        #self.indicatorResults = indicatorResults
        self.strategy = strategy
        
        self.get_formFields(form)

    def run_backtest(self):
        # Procesar los valores del formulario y crear un objeto cerebro

        cerebro = bt.Cerebro()

        
        data_feed = self._get_data_feed(fecha_desde=self.fechaDesde, fecha_hasta=self.fechaHasta, time_frame=bt.TimeFrame.Minutes)
        indicatorResultsDF = self._get_indicator_DF()

        cerebro.adddata(data_feed)

        self.add_strategy(self.strategy, cerebro,indicatorResultsDF)

        # Configurar el broker y los analizadores
        self._setup_broker(cerebro)
        self._add_analyzers(cerebro)

        # Ejecutar el backtest
        thestrats = cerebro.run()
        thestrat = thestrats[0]

        # Procesar los resultados

        results = BacktestAnalyzer.process_backtest_results(thestrat)
        
        return results

    def _get_data_feed(self, fecha_desde,fecha_hasta,time_frame):
        archivoCSV = 'DataCompletaYear2min.csv'
        df = pd.read_csv(archivoCSV, sep=';', header=None, names=['datetime', 'open', 'high', 'low', 'close', 'volume'],skip_blank_lines=True)
        df = df.dropna()
        
        # Añadir milisegundos a la columna 'datetime'
        df['datetime'] = pd.to_datetime(df['datetime'], format='%d/%m/%Y %H:%M:%S')

        # Establecer la columna 'datetime' como índice de tiempo
        df.set_index('datetime', inplace=True)

        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        print("longtidu de data:", len(df))

        df = df.loc[fecha_desde:fecha_hasta]
        
        # Convertir las columnas numéricas a tipo float
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)

        data_feed = bt.feeds.PandasData(dataname=df, timeframe=time_frame)
        

        return data_feed
        

    def _get_indicator_DF(self):
        resultados = 'resultsIndicator.csv'
        indicatorResults = pd.read_csv(resultados, sep=',', header=None, names=[
                        'datetime', 'fundtrend', 'bullbearline', 'bankerentry', 'color'])
        
        indicatorResults['datetime'] = pd.to_datetime(indicatorResults['datetime'], format="%Y-%m-%d %H:%M:%S")
        return indicatorResults

    def add_strategy(self, strategy, cerebro,indicatorResults):
        # Crear una estrategia personalizada basada en los valores del formulario
        cerebro.addstrategy(strategy,indicatorResults, self.tipoTK, self.valorTK,self.stopLoss,self.startHour, self.endHour)

    def _setup_broker(self, cerebro):
        # Configurar el broker
        broker = bt.brokers.BrokerBack(checksubmit=False)
        broker.setcommission(commission=0.125, margin=1)
        cerebro.addsizer(bt.sizers.FixedSize, stake=20)
        broker.setcash(100000.00)
        cerebro.setbroker(broker)

    def _add_analyzers(self, cerebro):
        # Agregar analizadores al cerebro
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='misanalisis')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='midrawdown')
    
    def get_formFields(self, form):
        self.fechaDesde = form.cleaned_data['fechaDesde']
        self.fechaHasta = form.cleaned_data['fechaHasta']
        self.valorTK = form.cleaned_data['valorTK']
        self.stopLoss = form.cleaned_data['stopLoss']
        self.startHour = form.cleaned_data['startHour']
        self.endHour = form.cleaned_data['endHour']
        self.tipoTK = form.cleaned_data['tipoTK']
