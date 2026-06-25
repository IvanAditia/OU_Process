import pandas as pd
import numpy as np
import ta
import matplotlib as mpl
import matplotlib.pyplot as plt

df = pd.read_parquet('data/forex_cfd/XAUUSD_M1.parquet')

df['mean'] = df['close'].rolling(20).mean()
df['sd'] = df['close'].rolling(20).std()
df['adx'] = ta.trend.ADXIndicator(
    high=df['high'],
    low=df['low'],
    close=df['close'],
    window=20
).adx()

X = df['close']
y = df['close'].shift(1)

df['log_price'] = X - y

df = df.dropna().copy()


fig, ax = plt.subplots()
ax.plot(df['time'], df['log_price'], color='green')

plt.show()
