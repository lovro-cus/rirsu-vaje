"""Skupni modul za obdelavo podatkov projektne naloge (napoved PM10).

Funkcijo `build_features` uporabljata tako ucni notebook kot spletna storitev,
da je predprocesiranje IDENTICNO pri ucenju in pri napovedovanju.

Koraki obdelave:
  - pretvorba in razvrstitev po casu
  - zapolnitev manjkajocih vrednosti (interpolacija + mediana)
  - kodiranje kategoricnih znacilnic (clouds ordinalno, wind_direction -> sin/cos)
  - casovne znacilnice (ura/dan/mesec kot ciklicne + vikend)
  - popravljanje izkrivljenosti desno-izkrivljenih znacilnic (log1p)
"""
import numpy as np
import pandas as pd

# ordinalna preslikava oblacnosti (od jasno do oblacno)
CLOUDS = {'jasno': 0, 'delno oblačno': 1, 'pretežno oblačno': 2, 'oblačno': 3}
# smeri vetra v kotne stopinje (kompas, slovenske kratice)
WIND_DEG = {'S': 0, 'SV': 45, 'V': 90, 'JV': 135, 'J': 180, 'JZ': 225, 'Z': 270, 'SZ': 315}

# koncni vrstni red numericnih znacilnic, ki jih model uporablja
FEATURES = ['PM10_l', 'PM2.5_l', 'temperature', 'pressure', 'precipitation',
            'rain_l', 'wind_speed_l', 'clouds_ord', 'wd_sin', 'wd_cos',
            'hour_sin', 'hour_cos', 'dow', 'month', 'is_weekend']
TARGET = 'PM10'


def build_features(df):
    """Sprejme surov DataFrame in vrne (X_features_df, y_target_series)."""
    df = df.copy()
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime').reset_index(drop=True)

    # --- zapolnitev manjkajocih numericnih vrednosti ---
    num = ['PM10', 'PM2.5', 'temperature', 'rain', 'pressure', 'precipitation', 'wind_speed']
    for c in num:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    # casovna interpolacija, nato zapolnitev robov in morebitnih ostankov z mediano
    df[num] = df[num].interpolate(method='linear', limit_direction='both')
    df[num] = df[num].fillna(df[num].median())

    # --- kategoricne znacilnice ---
    df['clouds_ord'] = df['clouds'].map(CLOUDS).fillna(0)
    deg = df['wind_direction'].map(WIND_DEG)
    rad = np.deg2rad(deg)
    df['wd_sin'] = np.sin(rad).fillna(0.0)   # manjkajoco smer obravnavamo kot nevtralno (0)
    df['wd_cos'] = np.cos(rad).fillna(0.0)

    # --- casovne (ciklicne) znacilnice ---
    h = df['datetime'].dt.hour
    df['hour_sin'] = np.sin(2 * np.pi * h / 24)
    df['hour_cos'] = np.cos(2 * np.pi * h / 24)
    df['dow'] = df['datetime'].dt.dayofweek
    df['month'] = df['datetime'].dt.month
    df['is_weekend'] = (df['dow'] >= 5).astype(int)

    # --- popravljanje izkrivljenosti (log1p za desno-izkrivljene znacilnice) ---
    df['PM10_l'] = np.log1p(df['PM10'])
    df['PM2.5_l'] = np.log1p(df['PM2.5'])
    df['rain_l'] = np.log1p(df['rain'].clip(lower=0))
    df['wind_speed_l'] = np.log1p(df['wind_speed'].clip(lower=0))

    return df[FEATURES].astype('float32'), df[TARGET].astype('float32')


def make_windows(X, y, window):
    """Razdeli zaporedje znacilnic na multivariatna okna dolzine `window`;
    cilj je naslednja vrednost PM10 po oknu."""
    Xs, ys = [], []
    Xv = np.asarray(X, dtype='float32')
    yv = np.asarray(y, dtype='float32')
    for i in range(len(Xv) - window):
        Xs.append(Xv[i:i + window])
        ys.append(yv[i + window])
    return np.array(Xs), np.array(ys)
