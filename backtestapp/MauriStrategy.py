import math
import backtrader as bt
import pandas as pd
from datetime import datetime, timedelta, time
import numpy as np


class MauricioStrategy(bt.Strategy):

    def __init__(self, indicatorResults, TipoTK, ValorTK, StopLoss, StartHour, EndHour):

        self.indicatorResults = indicatorResults

        self.ema200 = bt.indicators.ExponentialMovingAverage(
            self.data.close, period=200
        )
        self.ema20 = bt.indicators.ExponentialMovingAverage(
            self.data.close, period=20
        )
        self.bf = 1
        self.tipoTK = TipoTK
        self.valorTK = ValorTK
        self.stopLoss = StopLoss
        self.vela = 0
        self.valorInicialCartera = 0
        self.valorFinalCartera = 0
        self.order = {}
        self.id = 0
        self.lastDay = None
        self.startHour = StartHour
        self.endHour = EndHour
        self.flagBuyEnabled = False

        self.flagSellEnabled = False

    def start(self):
        self.valorInicialCartera = self.broker.getvalue()

    def stop(self):
        self.valorFinalCartera = self.broker.getvalue()

    def next(self):

        fechaHoy = self.data.datetime.datetime()

        if self.startHour <= fechaHoy.time() < self.endHour:
            if self.notHaveOpenedPosition():
                self.checkSignalBuy()
                self.checkSignalSell()

    def notify_order(self, order):
        s = order.Status
        if order.status in [order.Completed]:
            size = self.position.size
            print(size)
            print(
                f"Venta ejecutada - Precio: {order.executed.price}, Comisión: {order.executed.comm}")

    def checkOrder(self, makeOrder):
        precio = self.data.open[1]
        checkDistance = abs(precio - self.ema200[0])
        fixedSl = self.stopLoss - 1
        if checkDistance <= fixedSl:

            makeOrder(precio)

    def makeBuyOrder(self, precio):
        precioStop = precio - self.stopLoss
        takeProfitBuy = self.calcular_TK_Buy(
            precio, self.tipoTK, self.valorTK, self.stopLoss)
        self.order[self.id] = self.buy_bracket(tradeid=self.id,
                                               exectype=bt.Order.Market,
                                               stopprice=precioStop,
                                               limitprice=takeProfitBuy
                                               )
        self.id += 1
        self.printBuyOrder(precio, precioStop, takeProfitBuy)

    def makeSellOrder(self, precio):
        precioStop = precio + self.stopLoss
        takeProfitSell = self.calcular_TK_Sell(
            precio, self.tipoTK, self.valorTK, self.stopLoss)
        self.order[self.id] = self.sell_bracket(tradeid=self.id,
                                                exectype=bt.Order.Market, stopprice=precioStop, limitprice=takeProfitSell)
        self.id += 1
        self.printSellOrder(precio, precioStop, takeProfitSell)

    def printBuyOrder(self, precio, precioStop, takeProfitBuy):

        print(f"compra ejecutada - Precio: {precio}")
        print(f"compra ejecutada - SL: {precioStop}")
        print(f"compra ejecutada - TK: {takeProfitBuy}")

    def printSellOrder(self, precio, precioStop, takeProfitSell):

        print(f"venta ejecutada - Precio: {precio}")
        print(f"venta ejecutada - SL: {precioStop}")
        print(f"venta ejecutada - TK: {takeProfitSell}")

    def checkSignalBuy(self):
        if self.ema20 > self.ema200:

            if self.flagBuyEnabled == False and self.ema200 <= self.data.high[0] and self.data.low[0] <= self.ema200[0] and self.checkBunkerFundColorForBuyOnOpeningCandle():
                self.flagBuyEnabled = True

            elif self.flagBuyEnabled == True and self.data.close[0] > self.ema200:
                self.flagBuyEnabled = False
                if self.checkBunkerFundColorForBuyOnClosingCandle():

                    self.checkOrder(self.makeBuyOrder)
        elif self.flagBuyEnabled == True:
            self.flagBuyEnabled = False

    def checkSignalSell(self):
        if self.ema20 < self.ema200:

            if self.flagSellEnabled == False and self.ema200 >= self.data.low[0] and self.data.high[0] >= self.ema200[0] and self.checkBunkerFundColorForSellOnOpeningCandle():
                self.flagSellEnabled = True

            elif self.flagSellEnabled == True and self.data.close[0] < self.ema200:
                self.flagSellEnabled = False
                if self.checkBunkerFundColorForSellOnClosingCandle():
                    self.checkOrder(self.makeSellOrder)
        elif self.flagSellEnabled == True:
            self.flagSellEnabled = False

    def checkBunkerFundColorForSellOnClosingCandle(self):
        current_date = self.data.datetime.datetime()
        color = self.indicatorResults[self.indicatorResults['datetime']
                                      == current_date]['color'].iloc[0]
        return color in ["red", "white"]

    def checkBunkerFundColorForSellOnOpeningCandle(self):
        current_date = self.data.datetime.datetime()
        color = self.indicatorResults[self.indicatorResults['datetime']
                                      == current_date]['color'].iloc[0]
        return color in ["green", "white", "blue"]

    def checkBunkerFundColorForBuyOnClosingCandle(self):
        current_date = self.data.datetime.datetime()
        color = self.indicatorResults[self.indicatorResults['datetime']
                                      == current_date]['color'].iloc[0]
        return color in ["green", "blue"]

    def checkBunkerFundColorForBuyOnOpeningCandle(self):
        current_date = self.data.datetime.datetime()
        color = self.indicatorResults[self.indicatorResults['datetime']
                                      == current_date]['color'].iloc[0]
        return color in ["red", "white", "blue"]

    def calcular_TK_Buy(self, precio, tipoDeTk, ValorTK, recorridoStop):

        if tipoDeTk == 'P':
            # Calcular precio, stop loss y take profit cuando tipoDeTk es 'P'
            nuevo_tp = precio + ValorTK

        elif tipoDeTk == 'R':
            # Calcular precio, stop loss y take profit cuando tipoDeTk es 'R'
            nuevo_tp = precio + (ValorTK * recorridoStop)

        return nuevo_tp

    def calcular_TK_Sell(self, precio, tipoDeTk, ValorTK, recorridoStop):

        if tipoDeTk == 'P':
            # Calcular precio, stop loss y take profit cuando tipoDeTk es 'P'
            nuevo_tp = precio - ValorTK

        elif tipoDeTk == 'R':
            # Calcular precio, stop loss y take profit cuando tipoDeTk es 'R'
            nuevo_tp = precio - (ValorTK * recorridoStop)

        return nuevo_tp

    def notHaveOpenedPosition(self):
        return self.position.size >= 0 and self.position.size <= 0
