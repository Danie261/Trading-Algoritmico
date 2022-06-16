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


#Cálculo de 'ATR'
class calculo_ATR:
    t=10

    def tr(self):
        tr=[]
        for i in range(len(data)):
            if i!=0:
                a=data["High"][i]-data["Low"][i]
                b=abs(data["High"][i]-df["Close"][i-1])
                c=abs(data["Low"][i]-df["Close"][i-1])
                tr+=[max(a,b,c)]
            else:
                tr+=[np.nan]
        return tr

    def a_tr(self):
        atr=[]
        atr_0=0
        for i in range(len(data)):
            if len(atr)==0:
                for j in range(1,self.t+1):
                    atr_0+=t_r[j]
                atr+=[atr_0/self.t]
            elif len(atr)==1:
                atr+=[(atr[0]*(self.t-1)+t_r[i])/self.t]
            else:
                atr+=[(atr[i-1]*(self.t-1)+t_r[i])/self.t]
        return atr

x=calculo_ATR()
t_r=x.tr()
df["ATR"]=x.a_tr()


#Cálculo 'Middle Band'
t=20
df["Middle"]=df["Close"].ewm(span=t,adjust=False, min_periods=t).mean()


#Cálculo de 'Upper Band' y 'Lower Band'
df["Upper"]=df["Middle"]+2*df["ATR"]
df["Lower"]=df["Middle"]-2*df["ATR"]


#Algoritmo de c/v
def signals():
    c=[]
    v=[]
    condition=0
    for i in range(len(df)):
        if i<(len(df)-3):
            if df["Close"][i]>df["Upper"][i] and condition!=1:
                if df["Close"][i+2]>df["Upper"][i+2]:
                    c+=[np.nan]
                    v+=[np.nan]
                    condition=0
                else:
                    c+=[df["Close"][i+1]]
                    v+=[np.nan]
                    condition=1
            elif df["Close"][i]<df["Lower"][i] and condition!=-1:
                if df["Close"][i+2]<df["Upper"][i+2]:
                    c+=[np.nan]
                    v+=[np.nan]
                    condition=0
                else:
                    c+=[np.nan]
                    v+=[df["Close"][i+1]]
                    condition=-1
            else:
                c+=[np.nan]
                v+=[np.nan]
                condition=0
        else:
            c+=[np.nan]
            v+=[np.nan]
    return c,v

df["Sell"], df["Buy"]=signals()


#Plotting
plt.figure(figsize=(17,11))
plt.subplot(211)
plt.title(f"Keltner Channel for {longname}")
plt.plot(df["Middle"], linestyle="--")
plt.plot(df["Close"], label="Stock Price", alpha=0.4, color="black")
plt.plot(df["Upper"], label="Upper Band", color="darkblue")
plt.plot(df["Lower"], label="Lower Band", color="red")
plt.fill_between(df.index, df["Lower"], df["Upper"], where=df["Upper"]>df["Lower"], color="lightgreen")
plt.scatter(df.index, df["Buy"], label="Buy Price", marker="^", color="green")
plt.scatter(df.index, df["Sell"], label="Sell Price", marker="v", color="red")
plt.legend(loc="upper left")

plt.subplot(212)
plt.title("Average True Range")
plt.plot(df["ATR"], label="Average True Range")
plt.xlabel("Date")
plt.legend(loc="upper left")

plt.show()


#Comparación con TA-Lib (Hay diferencia al principio que tiende a cero)
da=pd.DataFrame()

da["ATR"]=df["ATR"]
da["ATR (TA-Lib)"]=ta.ATR(data["High"], data["Low"], df["Close"], 10)

da.dropna(inplace=True)

plt.figure(figsize=(17,11))
plt.subplot(211)
plt.title("Average True Range")
plt.plot(da["ATR"], label="Average True Range")
plt.legend(loc="upper left")

plt.subplot(212)
plt.title("Average True Range (TA-lib)")
plt.plot(da["ATR (TA-Lib)"], label="Average True Range (TA-Lib)", color="brown")
plt.xlabel("Date")
plt.legend(loc="upper left")

plt.show()
print(da.tail(20))
