"""Test spletne storitve projektne naloge. Storitev mora teci (python app.py).
Pripravi 3 razlicne zahtevke iz realnih podatkov in izpise napovedi."""
import requests
import pandas as pd

BASE = 'http://127.0.0.1:5001'
WINDOW = 24
STOLPCI = ['datetime','PM10','PM2.5','temperature','rain','pressure',
           'precipitation','wind_speed','clouds','wind_direction']


def okno(df, start):
    return df.iloc[start:start+WINDOW][STOLPCI].to_dict(orient='records')


if __name__ == '__main__':
    df = pd.read_csv('../dataset_E408.csv')
    df['datetime'] = df['datetime'].astype(str)
    # 3 razlicni zahtevki iz razlicnih obdobij
    for i, start in enumerate([9000, 11000, 13000], 1):
        r = requests.post(f'{BASE}/predict', json={'data': okno(df, start)})
        prava = df.iloc[start+WINDOW]['PM10']
        print(f'zahtevek {i}: {r.status_code} {r.json()}  (prava naslednja PM10 = {prava})')
