import pandas as pd

kline_df = pd.read_parquet('data/BTCUSDT_OHLC.parquet')
kline_df = kline_df[
    [0, 1, 2, 3, 4]
]
kline_df.columns = [
    'openTime',
    'open',
    'high',
    'low',
    'close'
]

kline_df['openTime'] = pd.to_datetime(
    kline_df['openTime'],
    unit='ms'
)

funding_df = pd.read_parquet('data/BTCUSDT_FULL_FUNDING.parquet')
funding_df = funding_df[
    ['fundingTime', 'fundingRate']
]
funding_df['fundingTime'] = funding_df['fundingTime'].dt.floor('s')

df = funding_df.merge(
    kline_df,
    left_on='fundingTime',
    right_on='openTime',
    how='inner'
)

df.to_parquet('data/BTCUSDT_FINAL_DATA.parquet')