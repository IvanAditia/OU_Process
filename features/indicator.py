import ta

def mean(data, period, source='close'):
	data[f'mean_{period}'] = data[source].rolling(period).mean()
	return data
	
def sd(data, period, source='close'):
	data[f'sd'] = data[source].rolling(period).std()
	return data
	
def adx(data, period, high='high', low='low', close='close'):
	data['adx'] = ta.trend.ADXIndicator(
		high=data[high],
		low=data[low],
		close=data[close],
		window=period
	).adx()
	return data
	
def stochastic(data, period, smooth_period, high='high', low='low', close='close'):
	stoch = ta.momentum.StochasticOscillator(
		high=data[high],
		low=data[low],
		close=data[close],
		window = period,
		smooth_window = smooth_period
	)
	data[f'stoch_k_{period}'] = stoch.stoch()
	data[f'stoch_d_{smooth_period}'] = stoch.stoch_signal()
	return data
	
