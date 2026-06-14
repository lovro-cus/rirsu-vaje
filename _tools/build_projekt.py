"""Generator notebooka za PROJEKTNO NALOGO - napoved PM10 z rekurentno NM."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from nbbuild import build

C = []
md = lambda s: C.append(("md", s))
code = lambda s: C.append(("code", s))

md("""# Projektna naloga - napovedovanje PM10 z rekurentnimi nevronskimi mrezami

Cilj: cim natancneje napovedati naslednjo vrednost parametra **PM10** (kvaliteta zraka)
iz multivariatne casovne vrste meritev.

Vsebina notebooka:
1. Obdelava in procesiranje podatkov (manjkajoce vrednosti, izkrivljenost, inzeniring in izbira znacilnic, normalizacija).
2. Priprava casovnih oken in delitev na ucno (prvo leto) in testno obdobje.
3. Izgradnja in ucenje rekurentne nevronske mreze (LSTM).
4. Ovrednotenje (MAE, MAPE, MSE, EVS) in izris napovedi.
5. Serializacija modela in scalerjev za spletno storitev.""")

code("""# Uvoz knjiznic + skupni modul za predprocesiranje (uporabljen tudi v storitvi)
import numpy as np, pandas as pd, pickle, warnings
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (mean_absolute_error, mean_squared_error,
                             explained_variance_score, mean_absolute_percentage_error)
import prep_projekt as pp
warnings.filterwarnings('ignore')
np.random.seed(1234); tf.random.set_seed(1234)
print('TF', tf.__version__)""")

md("""## 1. Nalaganje in pregled podatkov""")
code("""# Nalaganje surovih podatkov in osnovni pregled
df = pd.read_csv('dataset_E408.csv')
df['datetime'] = pd.to_datetime(df['datetime'])
df = df.sort_values('datetime').reset_index(drop=True)
print('Oblika:', df.shape)
print('Obdobje:', df['datetime'].min(), '->', df['datetime'].max())
print('Frekvenca: urne meritve')
df.head()""")

code("""# Izris ciljne spremenljivke PM10 skozi cas
plt.figure(figsize=(15,4))
plt.plot(df['datetime'], df['PM10'], linewidth=0.5)
plt.title('PM10 skozi cas'); plt.xlabel('cas'); plt.ylabel('PM10'); plt.tight_layout(); plt.show()""")

code("""# Pregled manjkajocih vrednosti
print('Manjkajoce vrednosti po stolpcih:')
print(df.isnull().sum())""")

code("""# Pregled IZKRIVLJENOSTI numericnih znacilnic (kateri stolpci so desno-izkrivljeni)
num = ['PM10','PM2.5','temperature','rain','pressure','precipitation','wind_speed']
print('Izkrivljenost (skewness):')
print(df[num].skew().sort_values(ascending=False))""")

md("""## 2. Obdelava podatkov

Vsa obdelava je zbrana v modulu `prep_projekt.build_features`, ki:
- **zapolni manjkajoce vrednosti** (casovna interpolacija + mediana),
- **kodira kategoricne** znacilnice (`clouds` ordinalno, `wind_direction` v `sin/cos`),
- doda **casovne ciklicne znacilnice** (ura, dan, mesec, vikend),
- **popravi izkrivljenost** desno-izkrivljenih znacilnic (`log1p`: PM10, PM2.5, rain, wind_speed).""")
code("""# Gradnja znacilnic prek skupnega modula
X_df, y_ser = pp.build_features(df)
print('Znacilnice:', list(X_df.columns))
print('Oblika X:', X_df.shape, ' brez NaN:', X_df.isnull().sum().sum()==0)
X_df.head()""")

md("""## 3. Izbira znacilnic

Pogledamo korelacijo posameznih znacilnic s ciljno vrednostjo PM10 (po log1p transformaciji).""")
code("""# Korelacija znacilnic s ciljno log-vrednostjo PM10 (PM10_l)
kor = X_df.corrwith(X_df['PM10_l']).drop('PM10_l').sort_values(key=abs, ascending=False)
plt.figure(figsize=(10,4))
kor.plot(kind='bar'); plt.title('Korelacija znacilnic s PM10 (log)'); plt.ylabel('Pearson r')
plt.tight_layout(); plt.show()
print(kor)
print('\\nOpomba: najmocneje koreliran je PM2.5; ohranimo vse znacilnice, saj rekurentna '
      'mreza sama izlusci uporabne vzorce, mnozica znacilnic pa je obvladljiva (15).')""")

md("""## 4. Delitev na ucno/testno obdobje in normalizacija

Model ucimo na **prvem letu meritev** (prvih 8760 urnih meritev), preostanek je testno obdobje.
Normalizacija (`StandardScaler`) je naucena **samo na ucnem obdobju** (brez puscanja informacij).""")
code("""# Delitev: prvo leto = ucno obdobje
TRAIN_LEN = 8760           # 365 dni * 24 ur
WINDOW = 24                # velikost okna = 1 dan (<= 1 teden, kot zahteva navodilo)

# scalerji naucimo SAMO na ucnem delu
feat_scaler = StandardScaler().fit(X_df.values[:TRAIN_LEN])
targ_scaler = StandardScaler().fit(y_ser.values[:TRAIN_LEN].reshape(-1,1))

X_scaled = feat_scaler.transform(X_df.values)
y_scaled = targ_scaler.transform(y_ser.values.reshape(-1,1)).flatten()""")

code("""# Gradnja multivariatnih oken in delitev na ucno/testno glede na indeks cilja
Xw, yw = pp.make_windows(X_scaled, y_scaled, WINDOW)
# indeks cilja okna i je (i + WINDOW); meja med ucno in testno mnozico je TRAIN_LEN
meja = TRAIN_LEN - WINDOW
X_train, y_train = Xw[:meja], yw[:meja]
X_test,  y_test  = Xw[meja:], yw[meja:]
print('X_train:', X_train.shape, 'y_train:', y_train.shape)
print('X_test :', X_test.shape,  'y_test :', y_test.shape)""")

md("""## 5. Izgradnja in ucenje modela (LSTM)

Arhitektura: dva sloja LSTM (64 in 32 enot) + Dropout + polno povezana sloja.
Hiperparametre (velikost mreze, dropout, ucno stopnjo) smo izbrali eksperimentalno;
uporabimo `EarlyStopping` za preprecitev preprileganja.""")
code("""# Gradnja in ucenje rekurentne nevronske mreze
model = Sequential([
    Input(shape=(WINDOW, X_train.shape[2])),
    LSTM(64, return_sequences=True),
    Dropout(0.2),
    LSTM(32),
    Dense(16, activation='relu'),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')
es = EarlyStopping(patience=8, restore_best_weights=True)
hist = model.fit(X_train, y_train, validation_split=0.15,
                 epochs=60, batch_size=64, callbacks=[es], verbose=0)
print('Koncni val_loss:', round(hist.history['val_loss'][-1],4), '| epoh:', len(hist.history['loss']))""")

code("""# Izris zgodovine ucenja
plt.figure(figsize=(8,4))
plt.plot(hist.history['loss'], label='train loss')
plt.plot(hist.history['val_loss'], label='val loss')
plt.title('Zgodovina ucenja LSTM'); plt.xlabel('epoha'); plt.ylabel('MSE'); plt.legend()
plt.tight_layout(); plt.show()""")

md("""## 6. Ovrednotenje na testnih podatkih

Napovedi in prave vrednosti pretvorimo nazaj v izvirno skalo PM10 ter izracunamo
metrike **MAE, MAPE, MSE, EVS**.""")
code("""# Napoved + inverzna standardizacija + metrike
y_pred_s = model.predict(X_test, verbose=0).flatten()
y_pred = targ_scaler.inverse_transform(y_pred_s.reshape(-1,1)).flatten()
y_true = targ_scaler.inverse_transform(y_test.reshape(-1,1)).flatten()

print('--- Metrike na testnih podatkih ---')
print(f'MAE : {mean_absolute_error(y_true, y_pred):.3f}')
print(f'MAPE: {mean_absolute_percentage_error(y_true, y_pred)*100:.2f} %')
print(f'MSE : {mean_squared_error(y_true, y_pred):.3f}')
print(f'EVS : {explained_variance_score(y_true, y_pred):.4f}')""")

code("""# Graf pravih in napovedanih vrednosti PM10 (prvih 500 testnih tock)
plt.figure(figsize=(15,4))
plt.plot(y_true[:500], label='prave', linewidth=1)
plt.plot(y_pred[:500], label='napovedane', linewidth=1)
plt.title('PM10 - prave vs napovedane (testno obdobje)'); plt.xlabel('cas'); plt.ylabel('PM10'); plt.legend()
plt.tight_layout(); plt.show()""")

md("""## 7. Serializacija za spletno storitev

Shranimo model in oba scalerja ter konfiguracijo (velikost okna, vrstni red znacilnic).""")
code("""# Shranjevanje modela in scalerjev v mapo service/models
import os
os.makedirs('service/models', exist_ok=True)
model.save('service/models/model_pm10.keras')
with open('service/models/scalers_pm10.pkl','wb') as f:
    pickle.dump({'feat_scaler': feat_scaler, 'targ_scaler': targ_scaler,
                 'window': WINDOW, 'features': pp.FEATURES}, f)
print('Shranjeno: service/models/model_pm10.keras, scalers_pm10.pkl')""")

out = os.path.join(os.path.dirname(__file__), '..', 'projekt', 'projekt.ipynb')
build(os.path.abspath(out), C, kernel_name='rirsu')
print('Zgrajen notebook:', os.path.abspath(out), 'st. celic:', len(C))
