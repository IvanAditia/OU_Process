import pandas as pd
import numpy as np
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
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

data['buy_entry'] = (
	(data['mean_20']  > data['mean_50']) &
	(data['adx'] > 20) &
	(data['stoch_k_14'] < 20) &
	(data['stoch_d_3'] < 20) &
	(data['stoch_k_14'] > data['stoch_d_3'])
)

data['sell_entry'] = (
	(data['mean_20']  < data['mean_50']) &
	(data['adx'] > 20) &
	(data['stoch_k_14'] > 80) &
	(data['stoch_d_3'] > 80) &
	(data['stoch_k_14'] < data['stoch_d_3'])
)

contract_size = 1
initial_balance = 20
risk_percent = 10
fee_perlot = 3
leverage = 500
lot = 0.01
balance = initial_balance
trades = []
position = None
equity_curve = []

for i in range(len(data)-1):
	row = data.iloc[i]
	equity_curve.append(balance)
	
	if balance <=0:
		break
	elif balance >= 100 and balance <=999:
		risk_percent = 5
	elif balance >= 1000:
		risk_percent = 1
	
	if position is None:
		price = data.iloc[i + 1]['open']
		
		if row['buy_entry']:
			entry_price = price
			sl = entry_price - row['sd']
			sl_distance = abs(entry_price - sl)
			tp = (sl_distance * 2) + entry_price
			risk = balance * risk_percent / 100
			lot = risk/(sl_distance * contract_size)
			if lot < 0.01:
				lot = 0.01
			elif lot > 500:
				lot = 500
			lot = max(0.01, round(lot,2))	
			margin = (entry_price * contract_size * lot) / leverage
			if margin > balance:
				continue
			position = ({
				'side' : 'BUY',
				'entry' : entry_price,
				'sl' : sl,
				'tp' : tp, 
				'lot' : lot,
			})
			
		elif row['sell_entry']:
			entry_price = price
			sl = entry_price + row['sd']
			sl_distance = abs(entry_price - sl)
			tp = entry_price - (sl_distance * 2)
			risk = balance * risk_percent / 100
			lot = risk/(sl_distance * contract_size)
			if lot < 0.01:
				lot = 0.01
			elif lot > 500:
				lot = 500
			lot = max(0.01, round(lot,2))	
			margin = (entry_price * contract_size * lot) / leverage
			if margin > balance:
				continue
			
			position = ({
				'side' : 'SELL',
				'entry' : entry_price,
				'sl' : sl,
				'tp' : tp, 
				'lot' : lot,
			})
	else:
		high = row['high']
		low = row['low']
		exit_price = None
		reason = None
		
		if position['side'] == 'BUY':
			if low <= position['sl']:
				exit_price = position['sl']
				reason = 'SL'
			
			elif high  >= position['tp']:
				exit_price = position['tp']
				reason = 'TP'
				
			if exit_price:
				pnl = (exit_price - position['entry']) * position['lot']  * contract_size
				fee = fee_perlot * position['lot'] * 2
				balance -= fee
				balance += pnl
				trades.append({
					'side' : 'BUY',
					'entry' : position['entry'],
					'exit' : exit_price,
					'lot' : position['lot'],
					'pnl' : pnl,
					'fee' : fee,
					'balance' : balance,
					'reason' : reason
				})
				
				position = None
				
		elif position['side']  == 'SELL':
			if high  >= position['sl']:
				exit_price = position['sl']
				reason = 'SL'
				
			elif low <= position['tp']:
				exit_price = position['tp']
				reason = 'TP'
				
			if exit_price:
				pnl = (position['entry'] - exit_price) * position['lot'] * contract_size
				fee = fee_perlot * position['lot'] * 2
				balance -= fee
				balance += pnl
				trades.append({
					'side' : 'SELL',
					'entry' : position['entry'],
					'exit' : exit_price,
					'lot' : position['lot'],
					'pnl' : pnl,
					'fee' : fee,
					'balance'  : balance,
					'reason' : reason
				})
				position = None
				

trade = pd.DataFrame(trades)

print(trade)

if len(trade):
	win = (trade['reason'] == 'TP').sum()
	loss = (trade['reason'] == 'SL').sum()
	
	print(f'TP            : {win}')
	print(f'SL            : {loss}')
	print(f'Win Rate      : {win/len(trade)*100:.2f}%')
	
	print(f'Total Pnl     : {trade["pnl"].sum():.2f}')
	print(f'Modal 		  : {initial_balance:.2f}')
	print(f'Final Balance : {balance:.2f}')
	
	print('Average Win    : ', trade.loc[trade.pnl > 0, 'pnl'].mean())
	print('Average Loss   : ', trade.loc[trade.pnl < 0, 'pnl'].mean())
	print('Profit Factor  : ',
		trade.loc[trade.pnl > 0, 'pnl'].sum() / 
		abs(trade.loc[trade.pnl < 0, 'pnl'].sum())
	)
	
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(equity_curve)
plt.title('Equity Curve')
plt.grid(True)
plt.show()
