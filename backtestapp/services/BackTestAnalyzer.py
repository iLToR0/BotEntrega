class BacktestAnalyzer:

    @staticmethod
    def process_backtest_results(thestrat):
        
        trade_analysis = thestrat.analyzers.misanalisis.get_analysis()
        drawdown_analysis = thestrat.analyzers.midrawdown.get_analysis()

        trade_results = BacktestAnalyzer.process_trade_analysis(trade_analysis)
        drawdown_results = BacktestAnalyzer.process_drawdown_analysis(drawdown_analysis)
        
        # Combinar los resultados en un solo diccionario
        results = {**trade_results, **drawdown_results}
        return results

    @staticmethod
    def process_drawdown_analysis(drawDown_analysis):
        # Procesa el análisis de drawdown aquí
        drawdown_results = {
            'lendraw': drawDown_analysis['len'] ,
            'drawdown': round(drawDown_analysis['drawdown'],2),
            'moneydown': drawDown_analysis['moneydown'],
            'lenMax': drawDown_analysis['max']['len'],
            'drawMax': round(drawDown_analysis['max']['drawdown'],2),
            'moneyMax': drawDown_analysis['max']['moneydown'],  
        }
        return drawdown_results

    @staticmethod
    def process_trade_analysis(trade_analysis):
        # Procesa el análisis de operaciones aquí
        print(trade_analysis)
        trade_results = {
                'totaltrades': trade_analysis['total']['total'],
                'rachaganadora': trade_analysis['streak']['won']['longest'],
                'rachaperdedora': trade_analysis['streak']['lost']['longest'],
                'totalganados': trade_analysis['won']['total'],
                'totalperdidos': trade_analysis['lost']['total'],
                'longTotal': trade_analysis['long']['total'],
                'shortTotal': trade_analysis['short']['total'],
                'longWins': trade_analysis['long']['won'],
                'longLost': trade_analysis['long']['lost'],
                'shortWins': trade_analysis['short']['won'],
                'shortLost': trade_analysis['short']['lost'],
                'recorridoEnOperaciones': trade_analysis['len']['total'],
                'promedioVelasOperacion': round(trade_analysis['len']['average'], 2),
                'maxvelasOperacion': trade_analysis['len']['max'],
                'minvelasOperacion': trade_analysis['len']['min'],
                'recorridoOperacionesGanadas': trade_analysis['len']['won']['total'],
                'promedioVelasOperacionGanadas': round(trade_analysis['len']['won']['average'], 2),
                'maxvelasOperacionGanadas': trade_analysis['len']['won']['max'],
                'minvelasOperacionGanadas': trade_analysis['len']['won']['min'],
                'recorridoOperacionesPerdidas': trade_analysis['len']['lost']['total'],
                'promedioVelasOperacionPerdidas': round(trade_analysis['len']['lost']['average'], 2),
                'maxvelasOperacionPerdidas': trade_analysis['len']['lost']['max'],
                'minvelasOperacionPerdidas': trade_analysis['len']['lost']['min'],
                'long_total': trade_analysis['len']['long']['total'],
                'long_average': trade_analysis['len']['long']['average'],
                'long_max': trade_analysis['len']['long']['max'],
                'long_min': trade_analysis['len']['long']['min'],
                'long_won_total': trade_analysis['len']['long']['won']['total'],
                'long_won_average': trade_analysis['len']['long']['won']['average'],
                'long_won_max': trade_analysis['len']['long']['won']['max'],
                'long_won_min': trade_analysis['len']['long']['won']['min'],
                'long_lost_total': trade_analysis['len']['long']['lost']['total'],
                'long_lost_average': trade_analysis['len']['long']['lost']['average'],
                'long_lost_max': trade_analysis['len']['long']['lost']['max'],
                'long_lost_min': trade_analysis['len']['long']['lost']['min'],
                'short_total': trade_analysis['len']['short']['total'],
                'short_average': round(trade_analysis['len']['short']['average'], 2),
                'short_max': trade_analysis['len']['short']['max'],
                'short_min': trade_analysis['len']['short']['min'],
                'short_won_total': trade_analysis['len']['short']['won']['total'],
                'short_won_average': trade_analysis['len']['short']['won']['average'],
                'short_won_max': trade_analysis['len']['short']['won']['max'],
                'short_won_min': trade_analysis['len']['short']['won']['min'],
                'short_lost_total': trade_analysis['len']['short']['lost']['total'],
                'short_lost_average': trade_analysis['len']['short']['lost']['average'],
                'short_lost_max': trade_analysis['len']['short']['lost']['max'],
                'short_lost_min': trade_analysis['len']['short']['lost']['min'],
                'pnl': trade_analysis['pnl']['net']['total'],
                'pnlwins': trade_analysis['won']['pnl']['total'],
                'pnlLosts': trade_analysis['lost']['pnl']['total'],
                'pnllong': trade_analysis['long']['pnl']['total'],
                'pnlShort': trade_analysis['short']['pnl']['total'],
                'pnlLongWins': trade_analysis['long']['pnl']['won']['total'],
                'pnlLongLosts': trade_analysis['long']['pnl']['lost']['total'],
                'pnlShortWins': trade_analysis['short']['pnl']['won']['total'],
                'pnlShortLosts': trade_analysis['short']['pnl']['lost']['total'],
                'long_won_total': trade_analysis['len']['long']['won']['total'],
                'long_won_average': trade_analysis['len']['long']['won']['average'],
                'long_won_max': trade_analysis['len']['long']['won']['max'],
                'long_won_min': trade_analysis['len']['long']['won']['min'],
                'long_lost_total': trade_analysis['len']['long']['lost']['total'],
                'long_lost_average': trade_analysis['len']['long']['lost']['average'],
                'long_lost_max': trade_analysis['len']['long']['lost']['max'],
                'long_lost_min': trade_analysis['len']['long']['lost']['min'],
        }
        return trade_results
