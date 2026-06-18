import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

df  = pd.read_parquet('data/ETHUSDT_FUNDING.parquet')

data = df['fundingRate']

window = 100

df['zscore'] = np.nan

for i in range(window, len(df)):
        train = df.iloc[i-window:i].copy()

        # membuat data
        train['Xt'] = train['fundingRate']
        train['Xt1'] = train['fundingRate'].shift(-1)
        
        train = train.dropna(subset=['Xt', 'Xt1']).copy()

        X = train[['Xt']]
        y = train['Xt1']

        # membuat model regresi
        model = LinearRegression()
        model.fit(X, y)

        # mengambil intersept dan phi(b)
        a = model.intercept_
        b = model.coef_[0]

        if b <= 0 or b >= 1:
            continue

        # menghitung rata-rata(mu)
        mu = a / (1 - b)

        # menghitung residual(epsilon) = error regresi
        residuals = y - model.predict(X)

        # menghitung sigma(standar deviasi)
        sigma = residuals.std()
        sigma_eq = sigma / np.sqrt(1 - b**2)

        # menghitung theta
        theta = -np.log(b)

        # menghitung half-life
        hl = np.log(2) / theta

        # menghitung Z-Score
        current = df.iloc[i]['fundingRate'] #data saat ini
        zscore = (current - mu ) / sigma_eq

        df.loc[df.index[i], 'zscore']  = zscore


df['markPrice'] = pd.to_numeric(
    df['markPrice'],
    errors='coerce'
)

df['future_return'] = (
        df['markPrice'].shift(-24) / df['markPrice'] - 1
)
bins = [-999,-3,-2,-1,0,1,2,3,999]

df['bucket'] = pd.cut(df['zscore'], bins)

result = (
    df.groupby('bucket')['future_return']
    .mean()
)

print(result)