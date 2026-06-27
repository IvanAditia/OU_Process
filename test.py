import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

df = pd.read_parquet('data/forex_cfd/XAUUSD_M1.parquet')

buy_candle = (
    (df['open'].shift(2) < df['close'].shift(2)) &
    (df['open'].shift(1) < df['close'].shift(1)) &
    (df['open'] < df['close'])
)

df = df.dropna().copy()

results = []

for i in range(len(df)):
    row = df.iloc[i-2]

    if buy_candle.iloc[i]:
        time = row['time']
        open = row['open']
        high = row['high']
        low = row['low']
        close = row['close']
        volume = row['tick_volume']

        results.append({
            'time': time,
            'open': open,
            'high': high,
            'low' : low,
            'close' : close,
            'volume' : volume
        })

result = pd.DataFrame(results)

fig, ax = plt.subplots()
ax.plot(result['volume'])
ax.plot(df['tick_volume'])

plt.show()