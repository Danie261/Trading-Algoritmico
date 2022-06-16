import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import talib as ta
import seaborn as sns
sns.set()


#company=input("Introduce el ticker de la compañía deseada: ")
ticker="TSLA"
info=yf.Ticker(ticker).info
longname=info["longName"]
if "," in longname:
    longname=longname.replace(",","")
df=yf.download(ticker,"2020-6-1")


#Cálculo 'Tenkan-sen'
max_9=df["High"].rolling(9).max()
min_9=df["Low"].rolling(9).min()
df["Tenkan-Sen"]=((max_9+min_9)/2)


#Cálculo 'Kijun-sen'
max_26=df["High"].rolling(26).max()
min_26=df["Low"].rolling(26).min()
df["Kijun-Sen"]=((max_26+min_26)/2)


#Cálculo 'Senkou Span A'
df["Senkou Span A"]=((df["Tenkan-Sen"]+df["Kijun-Sen"])/2).shift(26)


#Cálculo 'Senkou Span B'
max_52=df["High"].rolling(52).max()
min_52=df["Low"].rolling(52).min()
df["Senkou Span B"]=((max_52+min_52)/2).shift(26)


#Cálculo 'Chikou Span'
df["Chikou Span"]=df["Close"].shift(-26)


#Algoritmo de c/v
def signals():
    b=[]
    s=[]
    for i in range(len(df)):
        if i==0:
            b+=[np.nan]
            s+=[np.nan]
        elif df["Tenkan-Sen"][i-1]<df["Kijun-Sen"][i-1] and df["Tenkan-Sen"][i]>df["Kijun-Sen"][i]:
            b+=[df["Close"][i]]
            s+=[np.nan]
        elif df["Tenkan-Sen"][i-1]>df["Kijun-Sen"][i-1] and df["Tenkan-Sen"][i]<df["Kijun-Sen"][i]:
            b+=[np.nan]
            s+=[df["Close"][i]]
        else:
            b+=[np.nan]
            s+=[np.nan]
    return b, s

df["Buy"], df["Sell"]=signals()


#Plotting
plt.figure(figsize=(17,11))
plt.plot(df["Close"], label="Stock Price", lw=1.3)
plt.plot(df["Tenkan-Sen"], lw=0.9, label="Tenkan-Sen", color="pink")
plt.plot(df["Kijun-Sen"], lw=0.9, label="Kijun-Sen", color="brown")
plt.plot(df["Senkou Span A"], lw=0.9, label="Senkou Span A", color="green")
plt.plot(df["Senkou Span B"], lw=0.9, label="Senkou Span B", color="red")
plt.plot(df["Chikou Span"], lw=0.9, label="Chikou Span", color="darkblue")
plt.legend(loc="upper left")
plt.title(f"Ichimoku Cloud for {longname}")
plt.fill_between(df.index, df["Senkou Span A"], df["Senkou Span B"], where=df["Senkou Span A"]>df["Senkou Span B"], color="lightgreen")
plt.fill_between(df.index, df["Senkou Span A"], df["Senkou Span B"], where=df["Senkou Span A"]<df["Senkou Span B"], color="lightcoral")
plt.xlabel("Date")

plt.show()

plt.figure(figsize=(17,11))
plt.plot(df["Close"], label="Stock Price", alpha=0.8)
plt.plot(df["Tenkan-Sen"], lw=0.9, label="Tenkan-Sen", color="pink", alpha=0.2)
plt.plot(df["Kijun-Sen"], lw=0.9, label="Kijun-Sen", color="brown", alpha=0.2)
plt.plot(df["Senkou Span A"], lw=0.9, label="Senkou Span A", color="green", alpha=0.2)
plt.plot(df["Senkou Span B"], lw=0.9, label="Senkou Span B", color="red", alpha=0.2)
plt.plot(df["Chikou Span"], lw=0.9, label="Chikou Span", color="darkblue", alpha=0.2)
plt.scatter(df.index, df["Buy"], label="Buy Price", marker="^", color="green")
plt.scatter(df.index, df["Sell"], label="Sell Price", marker="v", color="red")
plt.legend(loc="upper left")
plt.title(f"Ichimoku Cloud TK Cross Strategy for {longname}")
plt.fill_between(df.index, df["Senkou Span A"], df["Senkou Span B"], where=df["Senkou Span A"]>df["Senkou Span B"], color="lightgreen")
plt.fill_between(df.index, df["Senkou Span A"], df["Senkou Span B"], where=df["Senkou Span A"]<df["Senkou Span B"], color="lightcoral")
plt.xlabel("Date")

plt.show()
