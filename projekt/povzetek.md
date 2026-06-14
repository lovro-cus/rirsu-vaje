# Projektna naloga — napovedovanje PM10 z rekurentno nevronsko mrežo

## Cilj
Čim natančneje napovedati naslednjo vrednost parametra **PM10** (kakovost zraka) iz
multivariatne urne časovne vrste meritev, ter rešitev ponuditi kot REST API v Docker sliki.

## Vsebina oddaje
```
projekt/
├── projekt.ipynb           # celoten potek: obdelava, učenje, ovrednotenje (z izhodi)
├── prep_projekt.py         # SKUPNI modul za predprocesiranje (uporabljata notebook in storitev)
├── dataset_E408.csv        # podatki
└── service/                # spletna storitev
    ├── app.py              # Flask: POST /predict
    ├── prep_projekt.py     # kopija skupnega modula
    ├── test_api.py         # 3 testni zahtevki
    ├── requirements.txt
    ├── Dockerfile
    └── models/             # model_pm10.keras + scalers_pm10.pkl
```

## 1. Obdelava in inženiring podatkov (`prep_projekt.build_features`)
- **Manjkajoče vrednosti:** numerične zapolnimo s **časovno interpolacijo** + mediana
  (PM10 ima 179, ostale značilnice ~215 manjkajočih).
- **Kodiranje kategoričnih:** `clouds` ordinalno (jasno→oblačno = 0..3),
  `wind_direction` (8 kompasnih smeri) pretvorjeno v **sin/cos** kota.
- **Časovne značilnice:** ura (sin/cos), dan v tednu, mesec, vikend.
- **Popravljanje izkrivljenosti:** desno-izkrivljene značilnice (PM10, PM2.5, rain,
  wind_speed; skewness 1.5–10.8) transformirane z **log1p**.
- **Izbira značilnic:** pregled korelacije s PM10 (najmočneje koreliran PM2.5);
  obdržanih vseh 15 značilnic, ker jih RNN sama tehta in je množica obvladljiva.
- **Normalizacija:** `StandardScaler` (ločeno za značilnice in cilj), naučen **samo na učnem letu**.

## 2. Priprava časovnih oken
- **Velikost okna = 24 ur (1 dan)** — znotraj omejitve ≤ 1 teden; zajame dnevni cikel onesnaženja.
- Multivariatna okna oblike `(n, 24, 15)`.
- **Delitev:** učenje na **prvem letu** meritev (prvih 8760 ur), test na preostanku.
  - `X_train: (8736, 24, 15)`, `X_test: (5340, 24, 15)`.

## 3. Model in razvoj
- Arhitektura: `LSTM(64, return_sequences) → Dropout(0.2) → LSTM(32) → Dense(16) → Dense(1)`.
- Optimizator `adam`, izguba MSE, `EarlyStopping` (patience=8) za preprečitev preprileganja.
- Pot razvoja: izbrana je bila dvoslojna LSTM arhitektura (zajem dnevnih vzorcev);
  hiperparametri (velikost mreže 64/32, dropout 0.2, batch 64, okno 24) so bili izbrani
  eksperimentalno z opazovanjem validacijske izgube.

## 4. Rezultati (testno obdobje)
| Metrika | Vrednost |
|---------|----------|
| MAE  | **2.52** |
| MAPE | **22.0 %** |
| MSE  | **13.95** |
| EVS  | **0.72** |

Model pojasni ~72 % variance PM10 in se v povprečju zmoti za ~2.5 enote — dober rezultat
za urno napovedovanje onesnaženosti, kjer so prisotni nepredvidljivi sunki.

## 5. Spletna storitev
- **POST `/predict`** sprejme okno meritev (seznam ≥24 vrstic z istimi stolpci kot zbirka) v JSON;
  vrne `{"prediction": <PM10>}`.
- Storitev uporabi **isti `prep_projekt`** in **iste scalerje** kot učenje → konsistentno predprocesiranje.

### Zagon lokalno
```bash
# učenje (zgradi model + scalerje)
.venv/Scripts/python -m nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.kernel_name=rirsu projekt/projekt.ipynb
# storitev
cd projekt/service && python app.py        # teče na portu 5001
python test_api.py                         # 3 testni zahtevki
```
### Zagon prek Dockerja
```bash
cd projekt/service
docker build -t projekt-pm10 .
docker run -p 5001:5001 projekt-pm10
```

### Primer zahtevka
```jsonc
POST /predict
{"data": [ {"datetime":"2025-..","PM10":12,"PM2.5":8,"temperature":14,"rain":0,
            "pressure":1007,"precipitation":0,"wind_speed":6,"clouds":"oblačno",
            "wind_direction":"SZ"}, ... (24 vrstic) ... ]}
// odgovor: {"prediction": 9.07}
```

## Opomba o dodatnem delu
Implementiran je **osnovni del** (najvišja ocena 8). Dodatni del (metoda iz znanstvenega
članka in primerjava) ni vključen — po želji ga je mogoče dodati kot ločen eksperiment.
