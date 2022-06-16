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
data=yf.download(ticker,"2020-6-1")

df=pd.DataFrame()
df["Close"]=data["Close"]


#Cálculo 'Middle Band'
t=20
df["SMA"]=df["Close"].rolling(t).mean()


#Cálculo 'Upper Band'
stdev=df["Close"].rolling(t).std()
df["Upper"]=df["SMA"]+2*stdev


#Cálculo 'Lower Band'
df["Lower"]=df["SMA"]-2*stdev


#Algoritmo de c/v
def signals():
    b=[]
    s=[]
    condition=0
    for i in range(len(df)):
        if i<(len(df)-3):
            if df["Close"][i]>df["Upper"][i] and condition!=1:
                if df["Close"][i+2]>df["Upper"][i+2]:
                    b+=[np.nan]
                    s+=[np.nan]
                    condition=0
                else:
                    b+=[np.nan]
                    s+=[df["Close"][i+1]]
                    condition=1
            elif df["Close"][i]<df["Lower"][i] and condition!=-1:
                if df["Close"][i+2]<df["Lower"][i+2]:
                    b+=[np.nan]
                    s+=[np.nan]
                    condition=0
                else:
                    b+=[df["Close"][i+1]]
                    s+=[np.nan]
                    condition=-1
            else:
                b+=[np.nan]
                s+=[np.nan]
                condition=0
        else:
            b+=[np.nan]
            s+=[np.nan]
    return b,s
    
df["Buy"], df["Sell"]=signals()


#Plotting
plt.figure(figsize=(17,11))
plt.plot(df["SMA"], label="Middle Band", linestyle="--")
plt.title(f"Bollinger Bands for {longname}")
plt.plot(df["Close"], label="Stock Price", alpha=0.4, color="black")
plt.plot(df["Upper"], label="Upper Band", color="darkblue")
plt.plot(df["Lower"], label="Lower Band", color="red")
plt.fill_between(df.index, df["Lower"], df["Upper"], where=df["Upper"]>df["Lower"], color="lightgreen")
plt.scatter(df.index, df["Buy"], label="Buy Price", marker="^", color="green")
plt.scatter(df.index, df["Sell"], label="Sell Price", marker="v", color="red")
plt.legend(loc="upper left")
plt.xlabel("Date")

plt.show()


#Comparación con TA-Lib
da=pd.DataFrame()
da["Upper"]=df["Upper"]
da["Lower"]=df["Lower"]

da["Upper (TA-Lib)"], middle, da["Lower (TA-Lib)"]=ta.BBANDS(df["Close"], t, 2, 2)

da.dropna(inplace=True)

plt.figure(figsize=(17,11))
plt.title("Bollinger Bands Comparison")
plt.plot(da["Upper"], label="Upper Band", color="darkblue")
plt.plot(df["Close"], label="Stock Price", alpha=0.4)
plt.plot(df["SMA"], label="Middle Band", linestyle="--")
plt.plot(da["Lower"], label="Lower Band", color="red")
plt.plot(da["Upper (TA-Lib)"], label="Upper Band (TA-Lib)", linestyle="--")
plt.plot(middle, label="Middle Band (TA-Lib)", linestyle="--")
plt.plot(da["Lower (TA-Lib)"], label="Lower Band (TA-Lib)", linestyle="--")
plt.xlabel("Date")
plt.fill_between(da.index, da["Lower"], da["Upper"], where=da["Upper"]>da["Lower"], color="lightgreen")
plt.legend(loc="upper left")

plt.show()
print(da.head(10))

