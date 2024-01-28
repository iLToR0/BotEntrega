from datetime import timedelta
import pandas as pd
import backtrader as bt

class DataManager:

    def __init__(self, archivo):
        self.archivo_csv = archivo

    def get_data(self, fecha_desde, fecha_hasta, time_frame):
        
        # Cargar los datos en un DataFrame de pandas
        df = pd.read_csv(self.archivo_csv, sep=';', header=None, names=['datetime', 'open', 'high', 'low', 'close', 'volume'])

        # Añadir milisegundos a la columna 'datetime'
        df['datetime'] = pd.to_datetime(df['datetime'], format='%d%m%Y %H%M%S')

        # Establecer la columna 'datetime' como índice de tiempo
        df.set_index('datetime', inplace=True)

        df.index = pd.to_datetime(df.index)
        df = df.sort_index()


        df = df.loc[fecha_desde:fecha_hasta]
        
        # Convertir las columnas numéricas a tipo float
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)

        data_feed = bt.feeds.PandasData(dataname=df, timeframe=time_frame)

        return data_feed
    

def no_hay_datos_disponibles(df, fechaDesde, fechaHasta):
    fechaDesde = pd.to_datetime(fechaDesde)
    fechaHasta = pd.to_datetime(fechaHasta)
    return ((df.index.min().date() > fechaDesde.date()) or (df.index.max() + timedelta(days=1)).date() < fechaHasta.date())



           # if fechaIgual(fechaDesde, fechaHasta,request) == True:
           #     error_message = "Las fechas no pueden ser iguales. Por favor, cambie las fechas."
            #    return render(request, 'input_page.html', {'form': form, 'error_message': error_message})