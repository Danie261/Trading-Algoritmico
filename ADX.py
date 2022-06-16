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


#Cálculo 'ATR'
class calculo_ATR:
    t=14

    def tr(self):
        tr=[]
        for i in range(len(df)):
            if i!=0:
                a=df["High"][i]-df["Low"][i]
                b=abs(df["High"][i]-df["Close"][i-1])
                c=abs(df["Low"][i]-df["Close"][i-1])
                tr+=[max(a,b,c)]
            else:
                tr+=[np.nan]
        return tr

    def a_tr(self):
        atr=[]
        atr_0=0
        for i in range(len(df)):
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


#Cálculo '+DM y -DM'
def dms():
    pos_dm=[]
    neg_dm=[]
    for i in range(len(df)):
        if i!=0:
            upmove=df["High"][i]-df["High"][i-1]
            downmove=df["Low"][i]-df["Low"][i-1]
            if upmove>downmove:
                if upmove>0:
                    pos_dm+=[upmove]
                    neg_dm+=[0]
                else:
                    pos_dm+=[0]
                    neg_dm+=[0]
            elif upmove<downmove:
                if downmove>0:
                    neg_dm+=[downmove]
                    pos_dm+=[0]
                else:
                    neg_dm+=[0]
                    pos_dm+=[0]
            else:
                pos_dm+=[0]
                neg_dm+=[0]
        else:
            pos_dm+=[np.nan]
            neg_dm+=[np.nan]
    return pos_dm, neg_dm

df["+DM"], df["-DM"]=dms()

del(df["Open"],df["Adj Close"], df["Volume"])


#Cálculo '+DI y -DI'
t=14
def dis():
    pos_di=[]
    neg_di=[]
    a=df["+DM"].ewm(span=t,adjust=False, min_periods=t).mean()
    b=df["-DM"].ewm(span=t,adjust=False, min_periods=t).mean()

    for i in range(len(df)):
        if i>t-1:
            pos_di+=[(a[i]/df["ATR"][i])*100]
            neg_di+=[abs((b[i]/df["ATR"][i])*100)]
        else:
            pos_di+=[np.nan]
            neg_di+=[np.nan]

    return pos_di, neg_di

df["+DI"], df["-DI"]=dis()


#Cálculo 'DX'
def dx():#dmi
    dx=[]
    for i in range(len(df)):
        if i>t-1:
            dx+=[abs((df["+DI"][i]-df["-DI"][i])/(df["+DI"][i]+df["-DI"][i]))*100]
        else:
            dx+=[np.nan]
    return dx

df["DX"]=dx()
df.dropna(inplace=True)


#Cálculo de 'ADX'
def adx():
    adx=[]
    for i in range(len(df)):
        if len(adx)==0:
            adx_0=0
            for j in range(1, t+1):
                adx_0+=df["DX"][j]
            adx+=[adx_0/t]
        
        elif len(adx)==1:
            adx+=[(adx[0]*(t-1)+df["DX"][i])/t]
        else:
            adx+=[(adx[i-1]*(t-1)+df["DX"][i])/t]
    return adx

df["ADX"]=adx()


#Algoritmo de c/v
def signals():
    b=[]
    s=[]
    condition=0
    for i in range(len(df)):
        if df["ADX"][i-1]<25 and df["ADX"][i]>25 and df["+DI"][i]>df["-DI"][i]:
            if condition!=1:
                b+=[df["Close"][i]]
                s+=[np.nan]
                condition=1
                
            else:
                b+=[np.nan]
                s+=[np.nan]
                
        elif df["ADX"][i-1]<25 and df["ADX"][i]>25 and df["-DI"][i]>df["+DI"][i]:
            if condition!=-1:
                b+=[np.nan]
                s+=[df["Close"][i]]
                condition=-1
                
            else:
                b+=[np.nan]
                s+=[np.nan]
                
        else:
            b+=[np.nan]
            s+=[np.nan]
            
    return b, s

b,s=signals()


#Plotting
plt.figure(figsize=(17,11))
plt.subplot(211)
plt.plot(df["Close"], label="Stock Price", alpha=0.8)
plt.scatter(df.index, b, label="Buy Price", marker="^", color="green")
plt.scatter(df.index, s, label="Sell Price", marker="v", color="red")
plt.title(f"{longname} Stock Price")
plt.legend(loc="upper left")

plt.subplot(212)
plt.plot(df["ADX"], color="darkblue", label="ADX", alpha=0.5)
plt.plot(df["+DI"], color="green", label="+DI")
plt.plot(df["-DI"], color="red", label="-DI")
plt.axhline(25, color="black", linestyle ="--")
plt.xlabel("Date")
plt.legend(loc="upper left")
plt.title("ADX Chart")

plt.show()


        


