import pandas as pd
from binance.client import Client
import os
from dotenv import load_dotenv
import time


load_dotenv()

api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')

client = Client(api_key, secret_key)

start = pd.to_datetime('2020-01-01')
end = pd.to_datetime('2026-05-31')

start_ms = int(start.timestamp() * 1000)
end_ms = int(end.timestamp() * 1000)

symbol = 'ETHUSDT'

all_data = []

while start_ms < end_ms:
    data = client.futures_funding_rate(
        symbol = symbol,
        startTime = start_ms,
        endTime = end_ms,
        limit = 1000
    )

    if not data:
        break

    all_data.extend(data)

    start_ms = data[-1]['fundingTime'] + 1

    time.sleep(0.2)

df = pd.DataFrame(all_data)

df['fundingTime'] = pd.to_datetime(df['fundingTime'], unit='ms')
df['fundingRate'] = df['fundingRate'].astype(float)

df = df.sort_values('fundingTime')

print(df.tail())

# df.to_parquet('data/ETHUSDT_FUNDING.parquet')
