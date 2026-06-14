# Naloga 7 — REST API spletna storitev

## Cilj
Naučene napovedne modele iz prejšnjih nalog uporabiti v obliki **REST API** spletne
storitve (Flask), zapakirane v **Docker** sliko.

## Končne točke
| Metoda | Pot | Opis | Model |
|--------|-----|------|-------|
| POST | `/predict/naloga4` | en primerek → št. izposojenih koles | najboljši regresijski model iz naloge 4 |
| POST | `/predict/naloga6` | 186 primerkov (časovna vrsta) → naslednja vrednost | najboljši RNN iz naloge 6 |
| POST | `/predict/naloga5` | slika (base64) → razred oblike | najboljši CNN iz naloge 5 (dodatni del) |

> Opomba: dodatni del naloge 7 predvideva zbirko *rock-paper-scissors*; pri nas je
> uporabljena zbirka **shapes** (naloga 5), zato `/predict/naloga5` vrne razred
> `circles` / `squares` / `triangles`.

## Struktura
```
naloga7/
├── app.py              # Flask storitev (naloži vse modele ob zagonu)
├── train_naloga4.py    # zgradi in serializira regresijski model naloge 4 (NN vs XGBoost → izbere boljšega)
├── test_api.py         # testiranje vseh treh končnih točk
├── requirements.txt
├── Dockerfile
└── models/             # serializirani modeli + scalerji
    ├── prep_naloga4.pkl      (scaler, kodirne preslikave, najboljši model XGBoost)
    ├── model_naloga6.keras   + scaler_naloga6.pkl
    └── model_naloga5.keras   + razredi_naloga5.pkl
```

## Priprava modelov (serializacija)
- **naloga4:** `python train_naloga4.py` — zgradi NN in XGBoost na Seoul bike zbirki
  (`naloga1/bike_data.csv`), izbere model z najvišjim EVS (zmaga **XGBoost**,
  EVS ≈ 0.90, MAE ≈ 130) ter serializira model + `StandardScaler` + kodirne preslikave.
- **naloga6 / naloga5:** modele shranita notebooka teh nalog; v `models/` jih prenese
  skripta `_tools/gather_models_naloga7.py`.

## Zagon lokalno
```bash
# 1) priprava modelov
.venv/Scripts/python naloga7/train_naloga4.py
.venv/Scripts/python _tools/gather_models_naloga7.py   # prekopira modele nalog 5 in 6
# 2) zagon storitve
.venv/Scripts/python naloga7/app.py
# 3) test (v drugem terminalu)
.venv/Scripts/python naloga7/test_api.py
```

## Zagon prek Dockerja
```bash
cd naloga7
docker build -t naloga7 .
docker run -p 5000:5000 naloga7
```

## Primeri zahtevkov
```jsonc
// POST /predict/naloga4
{"day":1,"month":12,"year":2017,"hour":18,"temperature":-3.5,"humidity":40,
 "wind_speed":1.5,"visibility":2000,"dew_point_temperature":-15.0,
 "solar_radiation":0.0,"rainfall":0.0,"snowfall":0.0,
 "seasons":"Winter","holiday":"No Holiday","work_hours":"Yes"}
// odgovor: {"prediction": 95}

// POST /predict/naloga6
{"data":[13,12,11, ... 186 vrednosti available_bike_stands ...]}
// odgovor: {"prediction": 14}

// POST /predict/naloga5
{"image":"<base64 kodirana slika>"}
// odgovor: {"prediction":"triangles"}
```

## Implementacijske opombe za zagovor
- Modeli in scalerji se **deserializirajo enkrat ob zagonu** (globalne spremenljivke),
  ne ob vsakem zahtevku → hitrejši odziv.
- Predprocesiranje v storitvi je **identično** kot pri učenju (isti scaler, ista
  standardizacija, isto preoblikovanje oblik `(1,1,186)` itd.), kar zagotavlja pravilne napovedi.
- `/predict/naloga4` izbere najboljši model glede na EVS; ker zmaga XGBoost, se v `app.py`
  uporabi `xgboost`-ova `predict`, sicer Kerasov.
