from binance.client import Client
import pandas as pd
import os
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')

client = Client(api_key, secret_key)

os.makedirs('data', exist_ok=True)

periods  = [
    (2020, '1 Jan, 2020', '31 Dec, 2020'),
    (2021, '1 Jan, 2021', '31 Dec, 2021'),
    (2022, '1 Jan, 2022', '31 Dec, 2022'),
    (2023, '1 Jan, 2023', '31 Dec, 2023'),
    (2024, '1 Jan, 2024', '31 Dec, 2024'),
    (2025, '1 Jan, 2025', '31 Dec, 2025'),
]

symbol = 'ETHUSDT'


# 🔁 FUNCTION WITH RETRY
def get_futures_klines_with_retry(symbol, interval, start, end, max_retries=10):
    attempt = 0

    while attempt < max_retries:
        try:
            data = client.futures_historical_klines(
                symbol,
                interval,
                start,
                end
            )
            return data

        except Exception as e:
            attempt += 1

            wait_time = min(2 ** attempt, 60)  # exponential backoff max 60s

            print(f"[Retry {attempt}/{max_retries}] Error: {e}")
            print(f"Waiting {wait_time} seconds...")

            time.sleep(wait_time)

    raise Exception("Max retries reached, gagal ambil data.")


for year, start, end in periods:
    print(f"\nDownload {year}...")

    kline = get_futures_klines_with_retry(
        symbol,
        Client.KLINE_INTERVAL_1MINUTE,
        start,
        end
    )

    df = pd.DataFrame(kline, columns=[
        'openTime',
        'open',
        'high',
        'low',
        'close',
        'volume',
        'closeTime',
        'quote_asset_volume',
        'trades',
        'taker_buy_base_asset_volume',
        'taker_buy_quote_asset_volume',
        'ignore'
    ])

    df['openTime'] = pd.to_datetime(df['openTime'], unit='ms')
    df['closeTime'] = pd.to_datetime(df['closeTime'], unit='ms')

    file_path = f'data/ETHUSDT_{year}.parquet'
    df.to_parquet(file_path)

    print(f"Total candle: {len(df)} saved -> {file_path}")

print("\nDownload selesai 🚀")