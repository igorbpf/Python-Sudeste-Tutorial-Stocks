from datetime import date, timedelta
import os
from sklearn.neighbors import KNeighborsRegressor
import numpy as np
import pandas as pd

def complete_missing_values(df):
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)
    return df

def sma(df, window=20):
    sma = df.rolling(window).mean()
    return complete_missing_values(sma)

def bollinger_band(df, window=20):
    sma = df.rolling(window).mean()
    sma = complete_missing_values(sma)
    up_bb = sma + 2 * complete_missing_values(df.rolling(window).std())
    do_bb = sma - 2 * complete_missing_values(df.rolling(window).std())
    return up_bb, do_bb

def volatilidade(df, window=20):
    vol = df.rolling(window).std()
    return complete_missing_values(vol)

def normalize(df):
    df = df/df.ix[0]
    return df


def get_stock(names=['^BVSP'], start_date=date(1990,1,1), end_date=date(2017,5,2)):

    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index=dates, )

    data_dir = '../data/'

    if '^BVSP' not in names:
        names.append('^BVSP')

    for name in names:
        name_location = os.path.join(data_dir,name)
        df_temp = pd.read_csv(name_location + '.csv', index_col='Date', parse_dates=True)
        df = df.join(df_temp['Adj Close'], how='left')
        df = df.rename(columns={'Adj Close': name})
        if '^BVSP' in df.columns.values:
            df.dropna(subset=['^BVSP'], inplace=True)

    return complete_missing_values(df)


def confidence(regressor, features):

    distance, _ = regressor.kneighbors(features)
    mean = distance.mean()
    std = distance.std()

    alpha = 1

    firstp = (mean + std)/alpha
    firstn = (mean - std)/alpha
    secondp = (mean + 2*std)/alpha
    secondn = (mean - 2*std)/alpha
    inFirstDev = []
    inSecondDev = []
    outSecondDev = []

    for array in distance:
        for point in array:
            if point <= firstp and point >= firstn:
                inFirstDev.append(point)
            elif (point <= secondp and point >= firstp) or (point >= secondn and point <= firstn):
                inSecondDev.append(point)
            else:
                outSecondDev.append(point)
    conf = 0

    if len(inFirstDev) == 3:
        conf = 5
    elif len(inFirstDev) == 2 and len(inSecondDev) == 1:
        conf = 4
    elif len(inFirstDev) == 1 and len(inSecondDev) == 2:
        conf = 3
    elif len(inFirstDev) == 2 and len(outSecondDev) == 1:
        conf = 3
    elif len(inSecondDev) == 3:
        conf = 2
    else:
        conf = 1

    return conf


def get_future(symbol, forecast, rollback, index):

    df = get_stock([symbol])

    ind = []

    for i in index:
        if i[0] == 'Volatilidade':
            df['volatilidade'] = volatilidade(df[[symbol]], i[1])
            ind.append('volatilidade')

        if i[0] == 'BB':
            df['bb up'], df['bb down'] = bollinger_band(df[[symbol]], i[1])
            ind.append('bb up')
            ind.append('bb down')

        if i[0] == 'SMA':
            df['sma'] = sma(df[[symbol]], i[1])
            ind.append('sma')


    df['shift'] = df[symbol].shift(-forecast)

    neigh = KNeighborsRegressor(n_neighbors = 3)


    X = df[ind].as_matrix()[-1]

    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    df = complete_missing_values(df)

    features = df[ind].ix[-rollback:]

    label = df['shift'].ix[-rollback:]

    X_train = features.as_matrix()
    y_train = label



    neigh.fit(X_train,y_train)

    X = X.reshape(1,-1)
    price = neigh.predict(X)

    conf = confidence(neigh, X)

    return round(price[0],2) , conf
