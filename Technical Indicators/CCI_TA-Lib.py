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


#Cálculo de 'CCI'
t=14
ty_p=(df["Close"]+df["High"]+df["Low"])/3

sma_typ=ty_p.rolling(t).mean()
st_dev=ty_p.rolling(t).std()

df["CCI"]=(ty_p-sma_typ)/(0.015*st_dev)


#Plotting
plt.figure(figsize=(17,11))
plt.subplot(211)
plt.plot(df['Close'], label="Stock Price")
plt.title(f"{longname} Stock Price")
plt.legend(loc="upper left")

plt.subplot(212)
plt.title("CCI chart")
plt.plot(df["CCI"])
plt.xlabel("Date")
plt.fill_between(df.index, df["CCI"], 100, where=df["CCI"]>100, color="lightcoral")
plt.fill_between(df.index, df["CCI"], -100, where=df["CCI"]<-100, color="lightgreen")
plt.axhline(100, linestyle='--', color="black",alpha=0.8)
plt.axhline(-100, linestyle='--', color="black",alpha=0.8)

plt.show()


#Comparación con TA-Lib (sigue mismo patrón)
da=pd.DataFrame()
da["CCI"]=df["CCI"]

da["CCI (TA-Lib)"]=ta.CCI(df["High"], df["Low"], df["Close"], t)


#Plotting
plt.figure(figsize=(17,11))
plt.subplot(211)
plt.plot(df["CCI"], label="CCI")
plt.title("CCI Comparison")
plt.legend(loc="upper left")
plt.axhline(100, linestyle='--', color="black",alpha=0.8)
plt.axhline(-100, linestyle='--', color="black",alpha=0.8)


plt.subplot(212)
plt.title("CCI TA-Lib")
plt.plot(da["CCI (TA-Lib)"], label="CCI (TA-Lib)")
plt.xlabel("Date")
plt.legend(loc="upper left")
plt.axhline(100, linestyle='--', color="black",alpha=0.8)
plt.axhline(-100, linestyle='--', color="black",alpha=0.8)

plt.show()
print(da.tail(20))