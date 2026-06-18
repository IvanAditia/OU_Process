import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_parquet('data/ETHUSDT_Dataset.parquet')
df.columns=(
    [
        'time',
        'open',
        'high',
        'low',
        'close'
    ]
)

df['close'] = df['close'].astype(float)

df['log_return'] = np.log(df['close']).diff()
df = df.dropna(subset=['log_return']).copy()
x = df['time']
y = df['log_return']

plt.figure(figsize=(15,6))
plt.plot(x, y)
plt.show()