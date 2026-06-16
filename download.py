from http import client
from symtable import Symbol
import pandas as pd
from binance.client import Client
import os
from dotenv import load_dotenv


load_dotenv()

df = pd.read_parquet('data/BTCUSDT_FULL_FUNDING.parquet')

start = df['fundingTime'].min()
end = df['fundingTime'].max()
api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')

client = Client(api_key, secret_key)

print('Download dimulai...')
klines = client.futures_historical_klines(
    'BTCUSDT',
    Client.KLINE_INTERVAL_8HOUR,
    str(start),
    str(end)
)
data = pd.DataFrame(klines)
data.to_parquet('data/BTCUSDT_OHLC.parquet')
print('Download selesai...')