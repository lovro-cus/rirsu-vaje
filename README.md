# RISU — naloge 5, 6, 7 in projektna naloga

Implementacije: konvolucijske (CNN) in rekurentne (RNN/GRU/LSTM) nevronske mreže,
REST API spletni storitvi (Flask + Docker) ter napovedovanje PM10.

## Struktura
```
naloga5/   CNN — razvrščanje slik (zbirka shapes)        -> naloga5.ipynb, povzetek.md
naloga6/   RNN/GRU/LSTM — časovne vrste (mbajk)           -> naloga6.ipynb, povzetek.md
naloga7/   REST API (modeli iz nalog 4, 5, 6) + Docker    -> app.py, povzetek.md
projekt/   Napoved PM10 (LSTM) + REST API + Docker         -> projekt.ipynb, service/, povzetek.md
_tools/    Pomožne skripte za generiranje notebookov (ni del oddaje)
naloga1..4 Podatki in notebooki prejšnjih nalog
```

## Postavitev okolja na NOVEM računalniku

Potrebuješ **Python 3.12** in (za spletne storitve) po želji **Docker**.

```bash
# 1) kloniraj repozitorij
git clone <URL> rirsu
cd rirsu

# 2) ustvari virtualno okolje (.venv se NE prenaša prek gita - ustvari se na novo)
python -m venv .venv

# 3) aktiviraj okolje
#   Windows (PowerShell):
.venv\Scripts\Activate.ps1
#   Windows (Git Bash):
source .venv/Scripts/activate
#   Linux/macOS:
source .venv/bin/activate

# 4) namesti odvisnosti
pip install --upgrade pip
pip install -r requirements.txt

# 5) registriraj Jupyter kernel (potreben za izvajanje notebookov prek nbconvert)
python -m ipykernel install --user --name rirsu --display-name "rirsu"
```

> **Opomba (Windows):** TensorFlow 2.18 na Windows teče v načinu CPU (GPU zahteva WSL2) —
> kar je za te naloge povsem dovolj.

## Izvajanje notebookov
```bash
# v brskalniku
jupyter notebook        # ali jupyter lab, izberi kernel "rirsu"

# ali samodejno izvedi notebook (z izhodi)
python -m nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.kernel_name=rirsu naloga6/naloga6.ipynb
```

## Spletni storitvi

### Naloga 7 (port 5000) — 3 končne točke
```bash
# priprava modelov (če manjkajo v naloga7/models/)
python naloga7/train_naloga4.py        # zgradi regresijski model naloge 4
python _tools/gather_models_naloga7.py # prekopira modele nalog 5 in 6
# zagon
python naloga7/app.py
python naloga7/test_api.py             # test (v drugem terminalu)
```
Docker:
```bash
cd naloga7 && docker build -t naloga7 . && docker run -p 5000:5000 naloga7
```

### Projekt (port 5001) — napoved PM10
```bash
cd projekt/service && python app.py
python test_api.py                     # test (v drugem terminalu)
```
Docker:
```bash
cd projekt/service && docker build -t projekt-pm10 . && docker run -p 5001:5001 projekt-pm10
```

## Pomembno
- **Serializirani modeli** (`*.keras`, `*.pkl`) so vključeni v repozitorij, zato storitvi
  delujeta takoj po kloniranju. Po želji jih je mogoče **ponovno zgenerirati** z izvajanjem
  pripadajočih notebookov / trening skript.
- Če Docker ne najde modelov, najprej zaženi korake "priprava modelov" zgoraj — `*.keras`
  in `*.pkl` morajo biti v `naloga7/models/` oz. `projekt/service/models/`.
