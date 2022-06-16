import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import yfinance as yf
import seaborn as sns
sns.set()


df=yf.download("TSLA", "2020-6-1", "2022-3-25")


#Plotting
plt.figure(figsize=(17,11))
plt.title(f"Tesla Stock Price")
plt.plot(df["Close"], label="Stock Price")
plt.legend(loc="upper left")
plt.xlabel("Date")

plt.show()


#Establecemos la Swing
df1=yf.download("TSLA", "2021-3-15", "2022-3-25")
maximum=df1["Close"].max()
minimum=df1["Close"].min()


#Algoritmo para establecer los límites de la Swing
def ptos():
    a=[]
    b=[]
    c=[]
    p=[]
    x=0
    for i in range(len(df1)):
        if df1["Close"][i]==maximum:
            a+=[df1["Close"][i]]
            b+=[np.nan]
            for j in range(i+1,len(df1)):
                p+=[df1["Close"][j]]
            x=min(p)
        elif df1["Close"][i]==minimum:
            b+=[df1["Close"][i]]
            a+=[np.nan]
        else:
            a+=[np.nan]
            b+=[np.nan]

    for i in range(len(df1)):
        if df1["Close"][i]==x:
            c+=[x]
        else:
            c+=[np.nan]
    return a, b, c

df1["Máximo"], df1["Mínimo"], df1["Pullback"]=ptos()


#Establecemos los distintos niveles
level_1=maximum-(0.236*(maximum-minimum))
level_2=maximum-(0.382*(maximum-minimum))
level_3=maximum-(0.5*(maximum-minimum))
level_4=maximum-(0.618*(maximum-minimum))
level_5=maximum-(0.784*(maximum-minimum))


#Plotting
plt.figure(figsize=(17,11))
plt.title(f"Tesla Stock Price")
plt.plot(df1["Close"], label="Stock Price", alpha=0.7)
plt.suptitle("Fibonacci Retracement", y=0.94, x=0.51)
plt.axhline(maximum, xmin=0.612, xmax=0.95, linestyle="--", alpha=0.5, color="black")
plt.axhline(level_1, xmin=0.612, xmax=0.95, linestyle="--", alpha=0.6, color="darkgreen")
plt.axhline(level_2, xmin=0.612, xmax=0.95, linestyle="--", alpha=0.6, color="green")
plt.axhline(level_3, xmin=0.612, xmax=0.95, linestyle="dotted", alpha=0.5, color="black")
plt.axhline(level_4, xmin=0.612, xmax=0.95, linestyle="--", alpha=0.6, color="green")
plt.axhline(level_5, xmin=0.612, xmax=0.95, linestyle="--", alpha=0.6, color="darkgreen")
plt.axhline(minimum, xmin=0.612, xmax=0.95, linestyle="--", alpha=0.5, color="black")
plt.scatter(df1.index, df1["Máximo"], label="Swing Max (2021-11-03)", color="red")
plt.scatter(df1.index, df1["Mínimo"], label="Swing Min (2020-3-23)", color="green")
plt.scatter(df1.index, df1["Pullback"], label="Swing Pullback", color="black")
plt.legend(loc="upper left")
plt.xlabel("Date")

plt.show()