import pandas as pd
import numpy as np
import ta
import matplotlib.pyplot as plt


df_silver = pd.read_parquet('data/forex_cfd/XAGUSD_M1.parquet')
df_gold = pd.read_parquet('data/forex_cfd/XAUUSD_M1.parquet')

print(df_silver)
print(df_gold)