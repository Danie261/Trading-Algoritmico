import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import talib as ta


#company=input("Introduce el ticker de la compañía deseada: ")
ticker="TSLA"
info=yf.Ticker(ticker).info
longname=info["longName"]
if "," in longname:
    longname=longname.replace(",","")
data=yf.download(ticker,"2020-6-1")["Close"]

df=pd.DataFrame()
df["Close"]=data


#Cálculo de 'EMA'
t_slow=26
t_fast=12
t_signal=9
df["EMA Slow"]=df["Close"].ewm(span=t_slow,adjust=False, min_periods=t_slow).mean()
df["EMA Fast"]=df["Close"].ewm(span=t_fast,adjust=False, min_periods=t_fast).mean()

#Cálculo de 'MACD'
df["MACD"]=df["EMA Fast"]-df["EMA Slow"]

#Cálculo de 'Signal'
df["Signal"]=df["MACD"].ewm(span=t_signal ,adjust=False, min_periods=t_signal).mean()

#Cálculo de 'Histograma'
df["Hist"]=df["MACD"]-df["Signal"]


#Algoritmo de c/v
def signals():
    b=[]
    s=[]
    for i in range(len(df)):
        if i!=0:
            if df["MACD"][i-1]<0 and df["MACD"][i]>0:
                b+=[df["Close"][i]]
                s+=[np.nan]
            elif df["MACD"][i-1]>0 and df["MACD"][i]<0:
                b+=[np.nan]
                s+=[df["Close"][i]]
            else:
                b+=[np.nan]
                s+=[np.nan]
        else:
            b+=[np.nan]
            s+=[np.nan]
    return b,s

df["Buy"],df["Sell"]=signals()


#Plotting
plt.figure(figsize=(17,11))
plt.subplot(211)
plt.plot(df["Close"], label="Stock Price", alpha=0.7)
plt.scatter(df.index, df["Buy"], label="Buy Price", marker="^", color="green")
plt.scatter(df.index, df["Sell"], label="Sell Price", marker="v", color="red")
plt.title(f"{longname} Stock Price")
plt.legend(loc="upper left")
plt.grid()

plt.subplot(212)
plt.plot(df["Signal"], color="red", linestyle="--", label="Signal")
plt.plot(df["MACD"], color="darkblue", label="MACD")
plt.bar(df.index, df["Hist"], color="black")
plt.axhline(0, color="black", lw=0.5)
plt.title("MACD Chart")
plt.xlabel("Date")
plt.legend(loc="upper left")
plt.grid()

plt.show()


#Comparación con TA-Lib
da=pd.DataFrame()

da["MACD"]=df["MACD"]
da["Signal"]=df["Signal"]
da["Hist"]=df["Hist"]

da["MACD (TA-Lib)"], da["Signal (TA-Lib)"], da["Hist (TA-Lib)"]=ta.MACD(df["Close"], t_fast, t_slow, t_signal)#--->al principio hay diferencia pero tiende a cero
da.dropna(inplace=True)


#Plotting
plt.figure(figsize=(17,11))
plt.subplot(211)
plt.plot(da["Signal"], color="red", linestyle="--", label="Signal")
plt.plot(da["MACD"], color="darkblue", label="MACD")
plt.bar(da.index, da["Hist"], color="black")
plt.axhline(0, color="black", lw=0.5)
plt.title("MACD Chart")
plt.legend(loc="upper left")
plt.grid()

plt.subplot(212)
plt.plot(da["Signal (TA-Lib)"], color="red", linestyle="--", label="Signal (TA-Lib)")
plt.plot(da["MACD (TA-Lib)"], color="darkblue", label="MACD (TA-Lib)")
plt.bar(da.index, da["Hist (TA-Lib)"], color="black")
plt.axhline(0, color="black", lw=0.5)
plt.title("MACD (TA-Lib) Chart")
plt.legend(loc="upper left")
plt.xlabel("Date")
plt.grid()

plt.show()
print(da.tail(10))
