import backtrader as bt
import pandas as pd
from datetime import datetime, timedelta,time


class ThreeCandlePatternStrategy(bt.Strategy):
        
    
   
    def __init__(self,tipoTK,valorTK,StartHour,EndHour):

        
        self.resistenciaSell = []  # Lista para almacenar los picos de las resistenciaSell y sus marcas de tiempo
        self.resistenciaBuy = []
        self.resistenciasAEliminar = []
        self.valor_contrato = 20
        self.tipoTK  = tipoTK
        self.valorTK = valorTK
        self.vela = 0
        self.valorInicialCartera = 0
        self.valorFinalCartera=0
        self.order = {}
        self.id = 0
        self.lastDay = None
        self.startHour = StartHour
        self.endHour = EndHour
        
        
    def start(self):
        self.valorInicialCartera = self.broker.getvalue()
        
    
    def stop(self):
        self.valorFinalCartera = self.broker.getvalue()
        
        

    def next(self):
        
        #esto solo saltea las primeras 3 lineas
        if len(self.data) < 3:
            return
        
        self.vela += 1
        fechaHoy = self.data.datetime.datetime()  
        

        if self.startHour <= fechaHoy.time() < self.endHour:

            self.marcarResistencias()
            
            
            #Sell
            self.analizarSell()     
            self.analizarBuy()
            

        self.cleanResistenciasPerDay(fechaHoy)

    def cleanResistenciasPerDay(self, fechaHoy):
        
        if self.lastDay and fechaHoy.day != self.lastDay.day:
            self.resistenciaBuy = []
            self.resistenciaSell = []
            
        self.lastDay=fechaHoy        
                                

    def analizarSell(self):
        #define si ya se abrio una posicion en esta vela
        self.operacionAbiertaVelaActual = False

        for resistencia in self.resistenciaSell.copy():

                if self.velaActualEnContacto(resistencia) and self.colorVelaActual() < 0:

                    if self.notHaveOpenedBuy():
                        self.makeEqualSellOrder()

                    self.resistenciaSell.remove(resistencia)

                elif self.velaAnteriorEnContacto(resistencia) and (not self.velaActualEnContacto(resistencia)):
                    #revisar que la condicion sea correcta
                    self.resistenciaSell.remove(resistencia)   

    def analizarBuy(self):
        #define si ya se abrio una posicion en esta vela
        self.operacionAbiertaVelaActual = False

        for resistencia in self.resistenciaBuy.copy():

                if self.velaActualEnContacto(resistencia) and self.colorVelaActual() > 0:
                    
                    if self.notHaveOpenedSell():
                        self.makeEqualBuyOrder()

                    self.resistenciaBuy.remove(resistencia)

                elif self.velaAnteriorEnContacto(resistencia) and (not self.velaActualEnContacto(resistencia)):
                    #revisar que la condicion sea correcta
                    self.resistenciaBuy.remove(resistencia)    

    def notify_order(self, order):
        s = order.Status
       # print(s[order.status])
        if order.status in [order.Completed]:
            size = self.position.size
           #   print(f"Venta ejecutada - Precio: {order.executed.price}, Comisión: {order.executed.comm}")

    def makeEqualBuyOrder(self):
        if self.operacionAbiertaVelaActual == False:
            precio = self.data.open[1]
            stoplossBuy = self.data.low[0] - 0.5
            recorridoStop = precio - stoplossBuy
            takeProfit = self.calcular_TK_Buy(precio, self.tipoTK, self.valorTK, recorridoStop)                    
            self.order[self.id]=self.buy_bracket(tradeid=self.id,
                                    exectype=bt.Order.Market,
                                    stopprice= stoplossBuy,
                                    limitprice=takeProfit)
            print(f"compra ejecutada - Precio: {precio}")
            print(f"compra ejecutada - SL: {stoplossBuy}")
            print(f"compra ejecutada - TK: {takeProfit}")

            self.operacionAbiertaVelaActual = True
            self.id += 1

    def makeEqualSellOrder(self):
        if self.operacionAbiertaVelaActual == False:

            precio = self.data.open[1]
            stoplossBuy = self.data.high[0] + 0.5
            recorridoStop = stoplossBuy - precio
            takeProfit = self.calcular_TK_Sell(precio, self.tipoTK, self.valorTK, recorridoStop)  

            self.order[self.id]=self.sell_bracket(tradeid=self.id,
                                        exectype=bt.Order.Market, stopprice=stoplossBuy, limitprice=takeProfit)
            print(f"venta ejecutada - Precio: {precio}")
            print(f"venta ejecutada - SL: {stoplossBuy}")
            print(f"venta ejecutada - TK: {takeProfit}")
            self.operacionAbiertaVelaActual = True
            self.id += 1

    def calcular_TK_Buy(self, precio, tipoDeTk, ValorTK, recorridoStop):

        if tipoDeTk == 'P':
            # Calcular precio, stop loss y take profit cuando tipoDeTk es 'P'
            nuevo_tp = precio + ValorTK

        elif tipoDeTk == 'R':
            # Calcular precio, stop loss y take profit cuando tipoDeTk es 'R'
            nuevo_tp = precio + (ValorTK * recorridoStop)
        # Tipo de TK no válido

        return nuevo_tp

    def calcular_TK_Sell(self, precio, tipoDeTk, ValorTK, recorridoStop):

        if tipoDeTk == 'P':
            # Calcular precio, stop loss y take profit cuando tipoDeTk es 'P'
            nuevo_tp = precio - ValorTK

        elif tipoDeTk == 'R':
            # Calcular precio, stop loss y take profit cuando tipoDeTk es 'R'
            nuevo_tp = precio - (ValorTK * recorridoStop)
       

        return nuevo_tp
    
    def notHaveOpenedBuy(self):
        return self.position.size <= 0
    
    def notHaveOpenedSell(self):
        return self.position.size >= 0

    def marcarResistencias(self):
        
        shadow_high3, shadow_low3 = self.data.high[-3], self.data.low[-3]
        shadow_high2, shadow_low2 = self.data.high[-2], self.data.low[-2]
        shadow_high1, shadow_low1 = self.data.high[-1], self.data.low[-1]

        # Verificar si la sombra de la vela central es más alta que las dos velas adyacentes
        self.marcarResistenciasSell(shadow_high3, shadow_high2, shadow_high1)
        self.marcarResistenciasBuy(shadow_low3, shadow_low2, shadow_low1)


    def marcarResistenciasSell(self, shadow_high3, shadow_high2, shadow_high1):
        if shadow_high2 > shadow_high3 and shadow_high2 > shadow_high1:
            resistenciaSell = shadow_high2 + 0.25
            # Almacenar el pico high de la vela central en la lista
            self.resistenciaSell.append(resistenciaSell)

    def marcarResistenciasBuy(self, shadow_low3, shadow_low2, shadow_low1):
        if shadow_low2 < shadow_low3 and shadow_low2 < shadow_low1:
            resistenciaBuy = shadow_low2 - 0.25
            # Almacenar el pico high de la vela central en la lista
            self.resistenciaBuy.append(resistenciaBuy)

    def velaAnteriorEnContacto(self, resistencia):
        return self.data.high[-1] >= resistencia and self.data.low[-1] <= resistencia

    def velaActualEnContacto(self, resistencia):
        return self.data.high[0] >= resistencia and self.data.low[0] <= resistencia
        
    def colorVelaAnterior(self):
        return self.data.close[-1] - self.data.open[-1]
    
    def colorVelaActual(self):
        return self.data.close[0] - self.data.open[0]
