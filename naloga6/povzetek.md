# Naloga 6 — Rekurentne nevronske mreže (RNN / GRU / LSTM)

## Cilj
Napovedovanje **naslednje vrednosti** v časovni vrsti izposoje koles
(`available_bike_stands`) z uporabo treh tipov rekurentnih nevronskih mrež.
Obvezni del obravnava **univariatno** vrsto, dodatni del **multivariatno**.

## Zagon
```bash
# iz korenske mape projekta (kjer je .venv)
.venv/Scripts/python -m nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.kernel_name=rirsu naloga6/naloga6.ipynb
```
Notebook ob koncu shrani najboljši univariatni model `model_naloga6.keras` in
`scaler_naloga6.pkl` (uporabljena v nalogi 7).

## Obvezni del — potek (univariatno)
1. **Nalaganje + sortiranje** zapisov po času (`date`).
2. **Izris** grafa `available_bike_stands` skozi čas.
3. **Filtriranje** zgolj ciljne značilnice in pretvorba v `numpy` polje.
4. **Delitev na učno/testno** in **standardizacija** (`StandardScaler`, naučen le na učni množici).
   - Da dobimo predpisane oblike, je test = zadnjih `1302 + 186 = 1488` vrednosti,
     učna = prvih `26181` vrednosti.
5. **Okna velikosti 186** (korak 1): vsako okno (186 vrednosti) je vhod `X`, naslednja vrednost je `y`.
   - `X_train: (25995, 186)`, `X_test: (1302, 186)` — natanko kot v navodilih.
   - Preoblikovanje v `(primerki, koraki, vrednosti) = (n, 1, 186)`.
6. **Tri arhitekture** (vsaka: 2 rekurentna sloja po 32 enot → Dense(16) → Dense(1)):
   - RNN (`SimpleRNN`), GRU, LSTM.
7. **Učenje** 25 epoh, optimizator `adam`, izguba `MSE`; shranjene zgodovine učenja.
8. **Izris** krivulj učenja (train/val loss) za vse tri modele.
9. **Ovrednotenje**: napoved → **inverzna standardizacija** → metrike **MAE, MAPE, MSE, EVS**.
10. **Graf** pravih vs. napovedanih vrednosti za vsak model.

### Doseženi rezultati (univariatno)
| Model | MAE | MSE | EVS |
|-------|-----|-----|-----|
| RNN  | ~1.31 | ~3.03 | ~0.944 |
| GRU  | ~1.32 | ~3.07 | ~0.944 |
| LSTM | ~1.33 | ~3.10 | ~0.944 |

> **Opomba o MAPE:** ker `available_bike_stands` pogosto znaša 0, je MAPE
> (deljenje z 0) numerično nestabilen in zato neuporaben — zanesljive so MAE, MSE in EVS.

## Dodatni del — potek (multivariatno)
- Vključene značilnice: `available_bike_stands` (cilj, stolpec 0), `apparent_temperature`,
  `dew_point`, `precipitation_probability`, `surface_pressure`.
- **Manjkajoče vrednosti** (`precipitation_probability`) zapolnjene z **Random Forest regresorjem**.
- Enaka delitev/standardizacija; multivariatna okna `(25995, 186, 5)` → preoblikovanje v `(25995, 5, 186)`.
- Iste tri arhitekture (vhod `(5, 186)`); inverzna transformacija samo nad ciljnim stolpcem.

### Doseženi rezultati (multivariatno)
| Model | MAE | MSE | EVS |
|-------|-----|-----|-----|
| RNN  | ~2.10 | ~6.57 | ~0.879 |
| GRU  | ~1.89 | ~5.57 | ~0.900 |
| LSTM | ~1.96 | ~5.95 | ~0.903 |

## Ugotovitve za zagovor
- Vse tri arhitekture dosežejo zelo podobno uspešnost; **univariatni** pristop tu deluje
  nekoliko bolje (manjši MAE), ker so dodatne meteorološke značilnice za napoved naslednje
  vrednosti šibko informativne in vnašajo šum.
- Najboljši univariatni model (najnižji MAE — RNN) je serializiran za REST storitev (naloga 7).
- Reševanje točnih predpisanih oblik (`1, 186` oz. `5, 186`) je doseženo z natančno izbiro mej delitve.
