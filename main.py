from turtle import position
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from sklearn.linear_model import LinearRegression
import numpy as np

df  = pd.read_parquet('data/ETHUSDT_FUNDING.parquet')

data = df['fundingRate']
adf_test = adfuller(data)

adf = adf_test[0]
pvalue = adf_test[1]

if adf < -3 and pvalue < 0.05:
    print('Data stationary')

    # risk
    initial_balance = 20.0
    risk = 0.01
    leverage = 10
    max_position = 5
    max_risk = 0.05
    taker_fee = 0.0005

    # param
    position = 0
    balance = initial_balance
    equity_curve = []
    trades = []
    risk = balance * risk
    window  = 100

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

        if b < 0:
            continue

        # menghitung rata-rata(mu)
        mu = a / (1 - b)

        # menghitung residual(epsilon) = error regresi
        residuals = y - model.predict(X)

        # menghitung sigma(standar deviasi)
        sigma = residuals.std()

        # menghitung Z-Score
        current = df.iloc[i]['fundingRate'] #data saat ini
        zscore = (current - mu ) / sigma

        df.loc[df.index[i], 'zscore']  = zscore
        
        df['signal'] = 0

        df.loc[df['zscore'] > 2, 'signal'] = -1
        df.loc[df['zscore'] < -2, 'signal'] = 1

        equity_curve.append(balance)

        # entry
        if position == 0:
            s = df['signal']
            # long
            if s == 1:
                entry = df['close']


else:
    print('Data tidak stationary')
