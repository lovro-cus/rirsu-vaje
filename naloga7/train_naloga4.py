"""Ucenje in serializacija REGRESIJSKEGA modela iz NALOGE 4 (obvezni del).

Podatkovna zbirka: Seoul Bike Sharing (`bike_data.csv`, zbirka iz naloge 1).
Cilj: napoved stevila izposojenih koles `rented_bike_count`.

Skripta zgradi nevronsko mrezo (Keras), jo nauci ter serializira:
  - model_naloga4.keras  (model)
  - prep_naloga4.pkl      (scaler + vrstni red znacilnic + kodirne preslikave)
v mapo naloga7/models/.
"""
import os, pickle
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (mean_absolute_error, mean_squared_error,
                             explained_variance_score, mean_absolute_percentage_error)

np.random.seed(1234); tf.random.set_seed(1234)

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, '..', 'naloga1', 'bike_data.csv')
MODELS = os.path.join(HERE, 'models')
os.makedirs(MODELS, exist_ok=True)

# Fiksne kodirne preslikave kategoricnih znacilnic (da je inferenca v API-ju deterministicna)
SEASONS = {'Spring': 0, 'Summer': 1, 'Autumn': 2, 'Winter': 3}
HOLIDAY = {'No Holiday': 0, 'Holiday': 1}
WORK    = {'No': 0, 'Yes': 1}

# Vrstni red znacilnic, ki ga model pricakuje na vhodu
FEATURES = ['day', 'month', 'year', 'hour', 'temperature', 'humidity', 'wind_speed',
            'visibility', 'dew_point_temperature', 'solar_radiation', 'rainfall',
            'snowfall', 'seasons', 'holiday', 'work_hours']


def pripravi(df):
    """Obdelava podatkov: razbitje datuma, zapolnitev manjkajocih, kodiranje kategorij."""
    df = df.copy()
    # datum dd/mm/yyyy -> day, month, year
    df[['day', 'month', 'year']] = df['date'].str.split('/', expand=True).astype(int)
    df.drop('date', axis=1, inplace=True)
    # kodiranje kategoricnih znacilnic
    df['seasons'] = df['seasons'].map(SEASONS)
    df['holiday'] = df['holiday'].map(HOLIDAY)
    df['work_hours'] = df['work_hours'].map(WORK)
    # zapolnitev morebitnih manjkajocih numericnih vrednosti s povprecjem
    df = df.fillna(df.mean(numeric_only=True))
    return df


def main():
    df = pripravi(pd.read_csv(CSV))
    X = df[FEATURES].values.astype('float32')
    y = df['rented_bike_count'].values.astype('float32')

    # delitev na ucno/testno (30 % test, random_state 1234 kot v nalogi 1)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=1234)

    # standardizacija vhodnih znacilnic (scaler naucimo le na ucni mnozici)
    scaler = StandardScaler().fit(Xtr)
    Xtr_s, Xte_s = scaler.transform(Xtr), scaler.transform(Xte)

    def oceni(ime, yp):
        print(f'{ime:8s} MAE={mean_absolute_error(yte,yp):.2f}  '
              f'MSE={mean_squared_error(yte,yp):.1f}  '
              f'EVS={explained_variance_score(yte,yp):.4f}')
        return explained_variance_score(yte, yp)

    # --- model A: nevronska mreza (Keras) ---
    nn = Sequential([Input(shape=(len(FEATURES),)),
                     Dense(128, activation='relu'), Dense(64, activation='relu'),
                     Dense(32, activation='relu'), Dense(1)])
    nn.compile(optimizer='adam', loss='mse')
    nn.fit(Xtr_s, ytr, validation_split=0.1, epochs=80, batch_size=64, verbose=0)
    evs_nn = oceni('NN', nn.predict(Xte_s, verbose=0).flatten())

    # --- model B: XGBoost regresor (ansambelska metoda iz nalog 3/4) ---
    xgb = XGBRegressor(n_estimators=400, max_depth=6, learning_rate=0.05,
                       random_state=1234, n_jobs=-1)
    xgb.fit(Xtr_s, ytr)
    evs_xgb = oceni('XGBoost', xgb.predict(Xte_s))

    # izberemo NAJBOLJSI model (najvisji EVS) in ga serializiramo
    prep = {'scaler': scaler, 'features': FEATURES,
            'seasons': SEASONS, 'holiday': HOLIDAY, 'work': WORK}
    if evs_xgb >= evs_nn:
        prep['model_type'] = 'xgboost'
        prep['model'] = xgb
        print('Izbran model: XGBoost')
    else:
        prep['model_type'] = 'keras'
        nn.save(os.path.join(MODELS, 'model_naloga4.keras'))
        print('Izbran model: NN (Keras)')
    with open(os.path.join(MODELS, 'prep_naloga4.pkl'), 'wb') as f:
        pickle.dump(prep, f)
    print('Shranjeno v', MODELS)


if __name__ == '__main__':
    main()
