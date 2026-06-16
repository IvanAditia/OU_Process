import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_parquet('data/BTCUSDT_FULL_FUNDING.parquet')

x = df['fundingTime']
y = df['fundingRate']

plt.figure(figsize=(15,6))
plt.plot(x, y)
plt.show()