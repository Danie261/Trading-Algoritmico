import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import matplotlib.gridspec as gd
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
df["High"]=data["High"]
df["Low"]=data["Low"]


#Cálculo 'RSI'
t_rsi=14

df["Diff"]=df["Close"].diff(1)

def var():
    var_pos=[]
    var_neg=[]
    for i in range(len(df)):
        if df["Diff"][i]>0:
            var_pos+=[df["Diff"][i]]
            var_neg+=[0]
        elif df["Diff"][i]<0:
            var_neg+=[abs(df["Diff"][i])]
            var_pos+=[0]
        else:
            var_pos+=[0]
            var_neg+=[0]
    return var_pos,var_neg
pos,neg=var()

df["Var+"]=pos
df["Var-"]=neg

df["Prom+"]=df["Var+"].ewm(span=t_rsi,adjust=False, min_periods=t_rsi).mean()
df["Prom-"]=df["Var-"].ewm(span=t_rsi,adjust=False, min_periods=t_rsi).mean()

df["RS"]=df["Prom+"]/df["Prom-"]

df["RSI"]=100-(100/(1+df["RS"]))


#Plotting 
plt.figure(figsize=(17,11))
plt.subplot(211)
plt.plot(df['Close'], label="Stock Price")
plt.title(f"{longname} Stock Price")
plt.legend(loc="upper left")

plt.subplot(212)
plt.title("RSI chart")
plt.plot(df["RSI"])
plt.xlabel("Date")
plt.fill_between(df.index, df["RSI"], 70, where=df["RSI"]>70, color="lightcoral")
plt.fill_between(df.index, df["RSI"], 30, where=df["RSI"]<30, color="lightgreen")
plt.axhline(30, linestyle='--', color="black",alpha=0.8)
plt.axhline(50, linestyle="--", color="black", alpha=0.5)
plt.axhline(70, linestyle='--', color="black",alpha=0.8)

plt.show()


#Comparación con TA-Lib
da=pd.DataFrame()
da["RSI"]=df["RSI"]

da["RSI (TA-Lib)"]=ta.RSI(df["Close"], t_rsi)
da["Diff"]=da["RSI"]-da["RSI (TA-Lib)"]
da.dropna(inplace=True)


#Plotting
plt.title("RSI Comparison")
plt.plot(da["RSI"], label="RSI")
plt.plot(da["RSI (TA-Lib)"], label="RSI (TA-Lib)")
plt.xlabel("Date")
plt.legend(loc="upper left")
plt.axhline(30, linestyle='--', color="black",alpha=0.8)
plt.axhline(50, linestyle="--", color="black", alpha=0.5)
plt.axhline(70, linestyle='--', color="black",alpha=0.8)

plt.show()
print(da.head(20))
