import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta

df  = pd.read_parquet('data/ETHUSDT_2020.parquet')

df = df[
    [
        'openTime',
        'open',
        'high',
        'low',
        'close',
        'volume',
        'closeTime'
    ]
]

df['volume'] = df['volume'].astype(float)
df['close'] = df['close'].astype(float)
df['high'] = df['high'].astype(float)
df['low'] = df['low'].astype(float)
df['adx'] = ta.trend.ADXIndicator(
        high=df['high'],
        low=df['low'],
        close=df['close'],
        window=14
    ).adx()

df['volume_mean'] = df['volume'].rolling(50).mean()
df['mean'] = df['close'].rolling(50).mean()
df['sd'] = df['close'].rolling(14).std()
df = df.dropna().copy()

window = 100
inital_balance = 20
leverage = 10
taker_fee = 0.0005

position = None
balance = inital_balance
equity_curve = []
trades = []
risk = 1

for i in range(window, len(df)):
    row = df.iloc[i]
    close = row['close']
    volume = row['volume']
    volume_mean = row['volume_mean']
    sd = row['sd']
    mean = row['mean']
    adx = row['adx']

    entry_long = (
        (close > mean) &
        (volume > volume_mean) &
        (adx > 25)
    )
    entry_short = (
        (close < mean) &
        (volume > volume_mean) & 
        (adx > 25)
    )
    equity_curve.append(balance)

    # entry
    if position is None:

        price = row['close']
        # long
        if entry_long.any():
            entry = price
            if pd.isna(sd.any()):
                continue
            sl = entry - sd
            tp = entry + (2 * sd)
            stop_distance = entry - sl
            qty = risk / stop_distance
            notional = qty * entry
            margin = notional / leverage
            if margin > balance:
                continue
            fee = notional * taker_fee
            balance -= fee
            position= {
                'side' : 'Long',
                'entry' : entry,
                'sl' : sl,
                'tp' : tp,
                'qty' : qty,
                'margin' : margin,
                'entry_index' : i
            }

        elif entry_short.any():
            entry = price
            if pd.isna(sd.any()):
                continue
            sl = entry + sd
            tp = entry - (2 * sd)
            stop_distance = sl - entry
            qty = risk / stop_distance
            notional = qty * entry
            margin = notional / leverage
            if margin > balance:
                continue
            fee = notional * taker_fee
            balance -= fee
            position= {
                'side' : 'Short',
                'entry' : entry,
                'sl' : sl,
                'tp' : tp,
                'qty' : qty,
                'margin' : margin,
                'entry_index' : i
            }

    # manage posisi
    else:
        high = row['high']
        low = row['low']
        exit_price = None
        reason = None

        # Long
        if position['side'] == 'Long':
            if low <= position['sl']:
                exit_price = position['sl']
                reason = 'SL'

            elif high >= position['tp']:
                exit_price = position['tp']
                reason = 'TP'

            if exit_price:
                pnl = (
                    exit_price - position['entry']
                ) * position['qty']
                fee = (
                    exit_price * position['qty']
                ) * taker_fee
                pnl -= fee
                balance += pnl
                trades.append({
                    'side' : 'Long',
                    'entry' : position['entry'],
                    'exit' : exit_price,
                    'qty' : position['qty'],
                    'pnl' : pnl,
                    'reason' : reason
                })
                position = None
        
        elif position['side'] == 'Short':
            if high >= position['sl']:
                exit_price = position['sl']
                reason = 'SL'

            elif low <= position['tp']:
                exit_price = position['tp']
                reason = 'TP'

            if exit_price:
                pnl = (
                    exit_price - position['entry']
                ) * position['qty']
                fee = (
                    exit_price * position['qty']
                ) * taker_fee
                pnl -= fee
                balance += pnl
                trades.append({
                    'side' : 'Short',
                    'entry' : position['entry'],
                    'exit' : exit_price,
                    'qty' : position['qty'],
                    'pnl' : pnl,
                    'reason' : reason
                })
                position = None


# result

trade = pd.DataFrame(trades)
print((trade['reason'] == 'TP').sum())
print((trade['reason'] == 'SL').sum())
print(balance)