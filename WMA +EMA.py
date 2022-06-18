import pandas as pd
import yfinance as yf
import talib as ta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


ticker="GOOG"
df=yf.download(ticker,"2018-1-1")

cash=10000
commission=0.002


#Backtesting
class moving_averages(Strategy):

    t1=85
    t2=75
    t_ema=5

    def init(self):

        self.wma1=self.I(ta.WMA,self.data.Close, self.t1)
        self.wma2=self.I(ta.WMA,self.data.Close, self.t2)
        self.ema=self.I(ta.EMA, self.data.Close, self.t_ema)

    def next(self):

        if crossover(self.ema, self.wma1) and crossover(self.ema, self.wma2):

            self.buy()

        elif crossover(self.wma1, self.ema) and crossover(self.wma2, self.ema):

            self.sell()

bt=Backtest(df, moving_averages, cash=10000, commission=0.002, exclusive_orders=True, trade_on_close=True)
output=bt.run()
bt.plot()

print(output)