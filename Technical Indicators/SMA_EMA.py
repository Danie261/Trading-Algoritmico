import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import yfinance as yf
import talib as ta
import seaborn as sns
sns.set()


#company=input("Introduce el ticker de la compañía deseada: ")
ticker="TSLA"
info=yf.Ticker(ticker).info
longname=info["longName"]
if "," in longname:
    longname=longname.replace(",","")
data=yf.download(ticker,"2020-6-1")["Close"]
df=pd.DataFrame()
df["Close"]=data


#Cálculo de 'SMA'
t_fast=30
t_slow=100
df["SMA Fast"]=df["Close"].rolling(t_fast).mean()
df["SMA Slow"]=df["Close"].rolling(t_slow).mean()


#Cálculo de 'EMA' 
df["EMA Fast"]=df["Close"].ewm(span=t_fast,adjust=False, min_periods=t_fast).mean()
df["EMA Slow"]=df["Close"].ewm(span=t_slow,adjust=False, min_periods=t_slow).mean()


#Algoritmo de c/v
def signals(Type):
    compra=[]
    venta=[]
    for i in range(len(df)):
        if i!=0:
            if df[f"{Type} Fast"][i-1]<df[f"{Type} Slow"][i-1] and df[f"{Type} Fast"][i]>df[f"{Type} Slow"][i]:
                compra+=[df["Close"][i]]
                venta+=[np.nan]
                    
            elif df[f"{Type} Fast"][i-1]>df[f"{Type} Slow"][i-1] and df[f"{Type} Fast"][i]<df[f"{Type} Slow"][i]:
                venta+=[df["Close"][i]]
                compra+=[np.nan]
            else:
                compra+=[np.nan]
                venta+=[np.nan]
        else:
            compra+=[np.nan]
            venta+=[np.nan]
    return compra,venta


#Plotting
def chart(x,a,b):

    plt.figure(figsize=(17,11))
    plt.plot(df["Close"], label="Stock Price", lw=0.7)
    plt.plot(df[f"{x} Fast"],label=f"{x} {a}",alpha=0.9)
    plt.plot(df[f"{x} Slow"], label=f"{x} {b}", alpha=0.9)
    plt.scatter(df.index, df["Buy"], label="Buy Price", marker="^", color="green")
    plt.scatter(df.index, df["Sell"], label="Sell Price", marker="v", color="red")
    plt.title(f"{longname} Stock Price")
    plt.xlabel("Date")
    plt.legend(loc="upper left")

    plt.show()

a_buy, a_sell=signals("SMA")
df["Buy"]=a_buy
df["Sell"]=a_sell

chart("SMA", t_fast, t_slow)


#Plotting 
a_buy, a_sell=signals("EMA")
df["Buy"]=a_buy
df["Sell"]=a_sell

chart("EMA", t_fast, t_slow)


##Comparación con TA-Lib---->pequeña diferencia al principio que tiende a '0'
da=pd.DataFrame()

t=10

da["SMA (TA-Lib)"]=ta.SMA(df["Close"],t)
da["SMA"]=df["Close"].rolling(t).mean()
da["EMA"] = ta.EMA(df["Close"],t)
da["EMA (TA-Lib)"]=df["Close"].ewm(span=t,adjust=False, min_periods=t).mean()

da.dropna(inplace=True)


#Plotting
plt.figure(figsize=(17,11))
plt.subplot(211)
plt.plot(df["Close"], label="Stock Price", lw=0.5) 
plt.plot(da["SMA"], label="SMA")
plt.plot(da["SMA (TA-Lib)"], label="SMA (TA-Lib)")
plt.legend(loc="upper left")
plt.title("SMA Comparison")

plt.subplot(212)
plt.plot(df["Close"], label="Stock Price", lw=0.5) 
plt.plot(da["EMA"], label="EMA")
plt.plot(da["EMA (TA-Lib)"], label="EMA (TA-Lib)")
plt.legend(loc="upper left")
plt.title("EMA Comparison")
plt.xlabel("Date")

plt.show()
print(da.tail(20))











