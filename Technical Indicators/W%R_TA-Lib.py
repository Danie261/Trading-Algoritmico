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


#Cálculo de 'Williams % Range'
t=21
max_14=df["High"].rolling(t).max()
min_14=df["Low"].rolling(t).min()
wr=(-(max_14-df["Close"])/(max_14-min_14))*100
df["W%R"]=wr

df.dropna(inplace=True)


#Plotting
plt.figure(figsize=(17,11))
plt.subplot(211)
plt.plot(df["Close"], label="Stock Price")
plt.title(f"{longname} Stock Price")
plt.legend(loc="upper left")
plt.grid()

plt.subplot(212)
plt.title("Williams % Range Chart")
plt.plot(df["W%R"])
plt.axhline(-20, linestyle="--", alpha=0.8, color="black")
plt.axhline(-50, linestyle="--", alpha=0.5, color="black")
plt.axhline(-80, linestyle="--", alpha=0.8, color="black")
plt.fill_between(df.index, df["W%R"], -20, where=df["W%R"]>-20, color="coral")
plt.fill_between(df.index, df["W%R"], -80, where=df["W%R"]<-80, color="lightgreen")
plt.xlabel("Date")

plt.show()


#Comparación con TA-Lib
da=pd.DataFrame()
da["W%R"]=df["W%R"]

da["W%R (TA-Lib)"]=ta.WILLR(df["High"], df["Low"], df["Close"],21)
da.dropna(inplace=True)


plt.figure(figsize=(10,5))
plt.title("W%R Comparison")
plt.plot(da["W%R"], label="W%R")
plt.plot(da["W%R (TA-Lib)"], label="W%R (TA-Lib)")
plt.xlabel("Date")
plt.legend(loc="upper left")
plt.axhline(-20, linestyle="--", alpha=0.8, color="black")
plt.axhline(-50, linestyle="--", alpha=0.5, color="black")
plt.axhline(-80, linestyle="--", alpha=0.8, color="black")
plt.xlabel("Date")

plt.show()
print(da.head(20))

