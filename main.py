import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import mplfinance as mpl
from features import mean, sd, adx, body, bullish, bearish, stochastic
from data import DATA_PATH

data = pd.read_parquet(DATA_PATH['gold'])

data = mean(data, 14)
data = mean(data, 20)
data = mean(data, 50)
data = sd(data, 14)
data = adx(data, 20)
data = stochastic(data, 14, 3)

data = data.dropna().copy()

results = []

data['valid'] = (
	(data['mean_14'] > data['mean_20']) &
	(data['mean_20'] > data['mean_50'])
)

for i in range(len(data)):
	row = data.iloc[i]
	
	if row['valid'].any():
		results.append({
			'time' : row['time'],
			'open' : row['open'],
			'high' : row['high'],
			'low' : row['low'],
			'close' : row['close'],
			'volume' : row['tick_volume']
		})


result = pd.DataFrame(results)


