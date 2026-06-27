import math
from typing import Dict, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ta

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

MIN_LOT = 0.01
LOT_STEP = 0.01

def normalize_lot(lot):
    lot = math.floor(lot / LOT_STEP) * LOT_STEP
    return max(MIN_LOT, round(lot, 2))

initial_balance = 10.00
contract_size = 1
balance = initial_balance
risk_percent = 0.1
trades = []
equity_curve = []
position = None

for i in range(len(df)-1):
    if balance <= 0:
        print('modal habis')
        break

    if balance >= 100:
        risk_percent = 0.01

    row = df.iloc[i]
    next_row = df.iloc[i + 1]
    equity_curve.append(balance)

    # entry
    if position is None:

        risk = balance * risk_percent

        #buy
        if row['zscore'] < -1.3:
            entry = next_row['open']
            sl = entry - row['sd_price']
            sl_distance = abs(entry-sl)
            if sl_distance <= 0:
                continue
            lot = risk / (sl_distance * contract_size)
            lot = normalize_lot(lot)
            rugi = sl_distance * lot * contract_size
            if rugi > risk:
                continue
            position = {
                'side' : 'BUY',
                'entry' : entry,
                'sl': sl,
                'lot' : lot,
                'entry_bar' : i + 1
            }

        # sell
        elif row['zscore'] > 1.3:
            entry = next_row['open']
            sl = entry  + row['sd_price']
            sl_distance = abs(sl-entry)
            if sl_distance <= 0:
                continue
            lot = risk / (sl_distance * contract_size)
            lot = normalize_lot(lot)
            rugi = sl_distance * lot * contract_size
            if rugi > risk:
                continue
            position = {
                'side' : 'SELL',
                'entry' : entry,
                'sl' : sl,
                'lot' : lot,
                'entry_bar' : i + 1
            }

    else:
        if i <= position['entry_bar']:
            continue
        high = row['high']
        low = row['low']
        exit_price = None
        reason = None

        # buy
        if position['side'] == 'BUY':
            if low <= position['sl']:
                exit_price = position['sl']
                reason = 'SL'
            elif row['zscore'] >= -0.006:
                exit_price = row['close']
                reason = 'TP'

            if exit_price:
                pnl = (exit_price - position['entry']) * contract_size * position['lot']

                balance += pnl
                trades.append({
                    'side': 'BUY',
                    'entry' : position['entry'],
                    'exit' : exit_price,
                    'lot' : position['lot'],
                    'pnl' : pnl,
                    'reason' : reason,
                    'balance': balance
                })
                position = None

        elif position['side'] == 'SELL':
            if high >= position['sl']:
                exit_price = position['sl']
                reason = 'SL'

            elif row['zscore'] <= -0.006:
                exit_price = row['close']
                reason = 'TP'

            if exit_price:
                pnl = (position['entry'] - exit_price) * contract_size * position['lot']
                balance += pnl

                trades.append({
                    'side' : 'SELL',
                    'entry': position['entry'],
                    'exit' : exit_price,
                    'lot' : position['lot'],
                    'pnl' : pnl,
                    'reason' : reason,
                    'balance' : balance
                })

                position = None

# hasil
trade = pd.DataFrame(trades)

trade.to_excel('data/hasilbacktest.xlsx')

print(trade)

print()

print("============== SUMMARY ==============")
print(f"Total Trade : {len(trade)}")

if len(trade):

    win = (trade["reason"] == "TP").sum()
    loss = (trade["reason"] == "SL").sum()

    print(f"TP          : {win}")
    print(f"SL          : {loss}")
    print(f"Win Rate    : {win/len(trade)*100:.2f}%")

    print(f"Total PnL   : {trade['pnl'].sum():.2f}")
    print(f"Final Bal   : {balance:.2f}")

# =========================
# Equity Curve
# =========================

plt.figure(figsize=(12,5))
plt.plot(equity_curve)
plt.title("Equity Curve")
plt.grid(True)
plt.show()