import backtrader as bt
from backtestapp.services.BackTestAnalyzer import BacktestAnalyzer
from backtestapp.services.DataManager import DataManager


class BacktestManager:

    def __init__(self, form, archivo_csv, strategy):
        self.archivo_csv = archivo_csv
        self.strategy = strategy
        self.get_formFields(form)

    def run_backtest(self):
        # Procesar los valores del formulario y crear un objeto cerebro

        cerebro = bt.Cerebro()

        data_feed = self._get_data_feed()
        cerebro.adddata(data_feed)

        self.add_strategy(self.strategy, cerebro)

        # Configurar el broker y los analizadores
        self._setup_broker(cerebro)
        self._add_analyzers(cerebro)

        # Ejecutar el backtest
        thestrats = cerebro.run()
        thestrat = thestrats[0]

        # Procesar los resultados

        results = BacktestAnalyzer.process_backtest_results(thestrat)
        
        return results

    def _get_data_feed(self):
        # Obtener los datos del archivo CSV
        dataManager = DataManager(self.archivo_csv)
        
        data_feed = dataManager.get_data(self.fechaDesde, self.fechaHasta, bt.TimeFrame.Minutes)
        return data_feed

    def add_strategy(self, strategy, cerebro):
        # Crear una estrategia personalizada basada en los valores del formulario

        cerebro.addstrategy(strategy, self.tipoTK, self.valorTK, self.startHour, self.endHour)

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
        self.startHour = form.cleaned_data['startHour']
        self.endHour = form.cleaned_data['endHour']
        self.tipoTK = form.cleaned_data['tipoTK']