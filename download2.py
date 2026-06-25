import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd

if not mt5.initialize():
    print(mt5.last_error())
    quit()

rates_silver = mt5.copy_rates_from_pos(
    "XAGUSD.pc",
    mt5.TIMEFRAME_M1,
    0,
    99999
)
rates_gold = mt5.copy_rates_from_pos(
    "XAUUSD.pc",
    mt5.TIMEFRAME_M1,
    0,
    99999
)
print(rates_silver is None)
print(rates_gold is None)
print(mt5.last_error())
df_silver = pd.DataFrame(rates_silver)
df_gold = pd.DataFrame(rates_gold)
df_silver['time'] = pd.to_datetime(df_silver['time'], unit='s')
df_gold['time'] = pd.to_datetime(df_gold['time'], unit='s')

df_silver.to_parquet('data/forex_cfd/XAGUSD_M1.parquet')
df_gold.to_parquet('data/forex_cfd/XAUUSD_M1.parquet')

mt5.shutdown()