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
df=yf.download(ticker,"2021-8-1")#mas corto para que se vea mejor

df["Index"]=range(len(df))
n=10


#Cálculo 'AROON'
class aroon():
    def a_up(self):
        a=df["High"].rolling(n).max()
        dif=[]
        aup=[]
        for i in range(len(df)):
            index=0
            if i<n:
                dif+=[np.nan]
                aup+=[np.nan]
            else:
                for j in range(i,i-n,-1):
                    if df["High"][j]==a[i]:
                        index=df["Index"][j]
                dif+=[i-index]
                aup+=[int(((n-(i-index))/n)*100)]
        return aup

    def a_down(self):
        a=df["Low"].rolling(n).min()
        dif=[]
        adown=[]
        for i in range(len(df)):
            index=0
            if i<n:
                dif+=[np.nan]
                adown+=[np.nan]
            else:
                for j in range(i,i-n,-1):
                    if df["Low"][j]==a[i]:
                        index=df["Index"][j]
                dif+=[i-index]
                adown+=[int(((n-(i-index))/n)*100)]
        return adown, dif

x=aroon()       
df["AROON Up"]=x.a_up()        
df["AROON Down"], df["dif"]=x.a_down()


#Algoritmo de c/v
def signals():
    b=[]
    s=[]
    for i in range(len(df)):
        if i==0:
            b+=[np.nan]
            s+=[np.nan]
        elif df["AROON Up"][i-1]<df["AROON Down"][i-1] and df["AROON Up"][i]>df["AROON Down"][i]:
            b+=[df["Close"][i]]
            s+=[np.nan]
        elif df["AROON Up"][i-1]>df["AROON Down"][i-1] and df["AROON Up"][i]<df["AROON Down"][i]:
            b+=[np.nan]
            s+=[df["Close"][i]]
        else:
            b+=[np.nan]
            s+=[np.nan]
    return b, s

df["Buy"], df["Sell"]=signals()


#Plotting
plt.figure(figsize=(17,11))
plt.subplot(211)
plt.plot(df["Close"], label="Stock Price", alpha=0.7)
plt.scatter(df.index, df["Buy"], label="Buy Price", marker="^", color="green")
plt.scatter(df.index, df["Sell"], label="Sell Price", marker="v", color="red")
plt.title(f"{longname} Stock Price")
plt.legend(loc="upper left")


plt.subplot(212)
plt.plot(df["AROON Up"], label="AROON Up")
plt.plot(df["AROON Down"], label="AROON Down")
plt.axhline(50, color="black", lw=0.5)
plt.axhline(70, color="black", lw=0.5)
plt.axhline(30, color="black", lw=0.5)
plt.title("AROON Chart")
plt.xlabel("Date")
plt.legend(loc="upper left")

plt.show()


#Comparación con TA-Lib ¿xq algunas me dan mal?(aroon down)
da=pd.DataFrame()

da["AROON Down"]=df["AROON Down"]
da["AROON Up"]=df["AROON Up"]

da["AROON Down (TA-Lib)"], da["AROON Up (TA-Lib)"]=ta.AROON(df["High"], df["Low"], n)
da.dropna(inplace=True)


#Plotting
plt.figure(figsize=(17,11))
plt.subplot(211)
plt.plot(da["AROON Up"], label="AROON Up")
plt.plot(da["AROON Down"], label="AROON Down")
plt.axhline(50, color="black", lw=0.5)
plt.title("AROON Chart")
plt.legend(loc="upper left")

plt.subplot(212)
plt.plot(da["AROON Up (TA-Lib)"], label="AROON Up (TA-Lib)")
plt.plot(da["AROON Down (TA-Lib)"], label="AROON Down (TA-Lib)")
plt.axhline(50, color="black", lw=0.5)
plt.title("AROON (TA-Lib) Chart")
plt.legend(loc="upper left")
plt.xlabel("Date")

plt.show()
print(da.head(20))