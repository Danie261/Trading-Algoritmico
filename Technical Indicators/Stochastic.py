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


#Cálculo de 'Fast %K'
t_k=14
t_d=3
max_14=df["High"].rolling(t_k).max()
min_14=df["Low"].rolling(t_k).min()

k=((df["Close"]-min_14)/(max_14-min_14))*100


#Cálculo de 'Fast %D'
d=k.rolling(t_d).mean()


#Cálculo de 'Slow %K'
slow_k=k.rolling(t_d).mean()


#Cálculo de 'Slow %D'
slow_d=slow_k.rolling(t_d).mean()


#Plotting
def chart(x):
    plt.figure(figsize=(17,11))
    plt.subplot(211)
    plt.plot(df["Close"], label="Close Price")
    plt.title(f"{longname} Stock Price")
    plt.legend(loc="upper left")

    plt.subplot(212)
    plt.title(f"{x} Stochastic Oscillator")
    plt.axhline(20, linestyle="--", alpha=0.6, color="black")
    plt.axhline(50, linestyle="--", alpha=0.4, color="black")
    plt.axhline(80, linestyle="--", alpha=0.6, color="black")
    if x=="Fast":
        plt.plot(k, label="Fast %K")
        plt.plot(d, label="Fast %D")
        plt.fill_between(df.index, k, 20, where=k<20, color="lightgreen")
        plt.fill_between(df.index, k, 80, where=k>80, color="lightcoral")
    else:
        plt.plot(slow_k, label="Slow %K")
        plt.plot(slow_d, label="Slow %D")
        plt.fill_between(df.index, slow_k, 20, where=slow_k<20, color="lightgreen")
        plt.fill_between(df.index, slow_k, 80, where=slow_k>80, color="lightcoral")

    plt.xlabel("Date")
    plt.legend(loc="upper left")

    plt.show()

#Fast
chart("Fast")

#Slow
chart("Slow")


#Comparación con TA-Lib
da=pd.DataFrame()

da["Slow %K"]=slow_k
da["Slow %D"]=slow_d
da["Slow %K (TA-Lib)"], da["Slow %D (TA-Lib)"]=ta.STOCH(df["High"], df["Low"], df["Close"], t_k, t_d)
da["Fast %K"]=k
da["Fast %D"]=d
da["Fast %K (TA-Lib)"], da["Fast %D (TA-Lib)"]=ta.STOCHF(df["High"], df["Low"], df["Close"], t_k, t_d)
da.dropna(inplace=True)


#Plotting
def chart_ta(y):

    plt.figure(figsize=(17,11))
    plt.subplot(211)
    plt.title(f"{y} Stochastic Oscillator")
    plt.axhline(20, linestyle="--", alpha=0.6, color="black")
    plt.axhline(50, linestyle="--", alpha=0.4, color="black")
    plt.axhline(80, linestyle="--", alpha=0.6, color="black")

    if y=="Fast":

        plt.plot(k, label="Fast %K") 
        plt.plot(d, label="Fast %D")

    else:

        plt.plot(slow_k, label="Slow %K") 
        plt.plot(slow_d, label="Slow %D")
    
    plt.legend(loc="upper left")


    plt.subplot(212)
    plt.title(f"{y} Stochastic Oscillator (TA-Lib)")
    plt.axhline(20, linestyle="--", alpha=0.6, color="black")
    plt.axhline(50, linestyle="--", alpha=0.4, color="black")
    plt.axhline(80, linestyle="--", alpha=0.6, color="black")

    if y=="Fast":

        plt.plot(da["Fast %K (TA-Lib)"], label="Fast %K (TA-Lib)") 
        plt.plot(da["Fast %D (TA-Lib)"], label="Fast &D (TA-Lib)")

    else:

        plt.plot(da["Slow %K (TA-Lib)"], label="Slow %K (TA-Lib)") 
        plt.plot(da["Slow %D (TA-Lib)"], label="Slow %D (TA-Lib)")

    plt.legend(loc="upper left")
    plt.xlabel("Date")

    plt.show()

#Fast
chart_ta("Fast")

#Slow
chart_ta("Slow")

print(da.head(10))

