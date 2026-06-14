"""Testiranje REST API spletne storitve naloge 7 (vse tri konecne tocke).
Pred zagonom mora teci storitev (python app.py). Zazene: python test_api.py
"""
import base64, io, json
import requests
import numpy as np
import pandas as pd
from PIL import Image

BASE = 'http://127.0.0.1:5000'


def test_naloga4():
    # en primerek v obliki surovih znacilnic (Seoul bike)
    primerek = {
        'day': 1, 'month': 12, 'year': 2017, 'hour': 18, 'temperature': -3.5,
        'humidity': 40, 'wind_speed': 1.5, 'visibility': 2000,
        'dew_point_temperature': -15.0, 'solar_radiation': 0.0,
        'rainfall': 0.0, 'snowfall': 0.0, 'seasons': 'Winter',
        'holiday': 'No Holiday', 'work_hours': 'Yes'}
    r = requests.post(f'{BASE}/predict/naloga4', json=primerek)
    print('naloga4 ->', r.status_code, r.json())


def test_naloga6():
    # 186 zaporednih vrednosti available_bike_stands iz realne zbirke
    df = pd.read_csv('../naloga6/mbajk.csv')
    df['date'] = pd.to_datetime(df['date'])
    serija = df.sort_values('date')['available_bike_stands'].values[:186].tolist()
    r = requests.post(f'{BASE}/predict/naloga6', json={'data': serija})
    print('naloga6 ->', r.status_code, r.json())


def test_naloga5():
    # nalozimo eno realno sliko in jo posljemo kot base64
    import glob
    fp = glob.glob('../naloga5/shapes/triangles/*.png')[0]
    with open(fp, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    r = requests.post(f'{BASE}/predict/naloga5', json={'image': b64})
    print('naloga5 ->', r.status_code, r.json(), '(pricakovano: triangles)')


if __name__ == '__main__':
    test_naloga4()
    test_naloga6()
    test_naloga5()
