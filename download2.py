import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd

if not mt5.initialize():
    print(mt5.last_error())
    quit()

rates = mt5.copy_rates_from_pos(
    "XAUUSD",
    mt5.TIMEFRAME_M1,
    0,
    99999
)
print(rates is None)
print(mt5.last_error())
df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s')

df.to_parquet('data/forex_cfd/XAUUSD_M1.parquet')

mt5.shutdown()