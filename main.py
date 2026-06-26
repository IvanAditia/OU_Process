import pandas as pd
import numpy as np
import ta
import matplotlib as mpl
import matplotlib.pyplot as plt

df = pd.read_parquet('data/forex_cfd/XAUUSD_M1.parquet')

df['sd_price'] = df['close'].rolling(100).std()

df['log_price'] = np.log(df['close'])

X = df['log_price']
y = df['log_price'].shift(1)

df['price'] = X - y

window = 100
df['mean'] = df['price'].rolling(window).mean()
df['sd'] = df['price'].rolling(window).std()

df['zscore'] = (
    df['price'] - df['mean']
) /  df['sd']

df = df.dropna().copy()

quantile = df['zscore'].quantile(
    [0.01,0.05,0.25,0.50,0.75,0.95,0.99]
)

total = len(df)

buy = (df['zscore'] < -1).sum()
sell = (df['zscore'] > 1).sum()

print(quantile)
print(f"Total data      : {total}")
print(f"Buy signal      : {buy} ({buy/total*100:.2f}%)")
print(f"Sell signal     : {sell} ({sell/total*100:.2f}%)")
print(f"Total signal    : {buy+sell} ({(buy+sell)/total*100:.2f}%)")

initial_balance = 10.00
balance = initial_balance
risk = 1
trades = []
position = None

for i in range(len(df)):
    row = df.iloc[i]
    close = row['close']
    
    # entry
    if position is None:

        #buy
        if row['zscore'] < -1.5:
            price = close
            sl = price - df['sd_price']
            tp = (row['zscore'] == 0)
            lot = 
        
