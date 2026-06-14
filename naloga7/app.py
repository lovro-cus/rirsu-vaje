"""NALOGA 7 - REST API spletna storitev za napovedovanje.

Konecne tocke:
  POST /predict/naloga4 - regresija: stevilo izposojenih koles (model iz naloge 4)
  POST /predict/naloga6 - casovna vrsta: naslednja vrednost iz 186 primerkov (model iz naloge 6)
  POST /predict/naloga5 - klasifikacija slike (base64) v razred oblike (model iz naloge 5)

Vsi modeli in scalerji se nalozijo ENKRAT ob zagonu storitve.
"""
import os, io, base64, pickle
import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
from tensorflow.keras.models import load_model

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, 'models')

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Nalaganje (deserializacija) vseh modelov in pripadajocih objektov ob zagonu
# ---------------------------------------------------------------------------
# -- Naloga 4: regresijski model (XGBoost ali Keras) + scaler + kodirne preslikave
with open(os.path.join(MODELS, 'prep_naloga4.pkl'), 'rb') as f:
    PREP4 = pickle.load(f)
if PREP4['model_type'] == 'keras':
    MODEL4 = load_model(os.path.join(MODELS, 'model_naloga4.keras'))
    PREDICT4 = lambda X: MODEL4.predict(X, verbose=0).flatten()
else:  # xgboost model je shranjen kar v pkl slovarju
    MODEL4 = PREP4['model']
    PREDICT4 = lambda X: MODEL4.predict(X)

# -- Naloga 6: rekurentni model + scaler ciljne casovne vrste
MODEL6 = load_model(os.path.join(MODELS, 'model_naloga6.keras'))
with open(os.path.join(MODELS, 'scaler_naloga6.pkl'), 'rb') as f:
    SCALER6 = pickle.load(f)
WINDOW6 = 186

# -- Naloga 5: konvolucijski klasifikator slik + seznam razredov
MODEL5 = load_model(os.path.join(MODELS, 'model_naloga5.keras'))
with open(os.path.join(MODELS, 'razredi_naloga5.pkl'), 'rb') as f:
    RAZREDI5 = pickle.load(f)


# ---------------------------------------------------------------------------
@app.route('/predict/naloga4', methods=['POST'])
def predict_naloga4():
    """Prejme en primerek (JSON) in napove stevilo izposojenih koles."""
    data = request.get_json(force=True)
    # zgradimo vektor znacilnic v pravem vrstnem redu; kategoricne kodiramo
    vrstica = []
    for f in PREP4['features']:
        v = data.get(f)
        if f == 'seasons':
            v = PREP4['seasons'].get(v, v)
        elif f == 'holiday':
            v = PREP4['holiday'].get(v, v)
        elif f == 'work_hours':
            v = PREP4['work'].get(v, v)
        vrstica.append(float(v))
    X = PREP4['scaler'].transform(np.array(vrstica, dtype='float32').reshape(1, -1))
    napoved = float(PREDICT4(X)[0])
    return jsonify({'prediction': round(napoved)})


@app.route('/predict/naloga6', methods=['POST'])
def predict_naloga6():
    """Prejme 186 primerkov (casovno vrsto) in napove naslednjo vrednost."""
    data = request.get_json(force=True)
    # dovolimo bodisi cist seznam stevil bodisi {"data": [...]} bodisi seznam objektov
    if isinstance(data, dict):
        data = data.get('data', data.get('available_bike_stands'))
    vrednosti = [float(x['available_bike_stands']) if isinstance(x, dict) else float(x)
                 for x in data]
    if len(vrednosti) != WINDOW6:
        return jsonify({'error': f'pricakovanih {WINDOW6} vrednosti, prejetih {len(vrednosti)}'}), 400
    # standardizacija z istim scalerjem kot pri ucenju + preoblikovanje v (1, 1, 186)
    arr = SCALER6.transform(np.array(vrednosti, dtype='float32').reshape(-1, 1)).flatten()
    arr = arr.reshape(1, 1, WINDOW6)
    napoved_s = MODEL6.predict(arr, verbose=0).flatten()[0]
    # inverzna standardizacija napovedi
    napoved = float(SCALER6.inverse_transform([[napoved_s]])[0, 0])
    return jsonify({'prediction': round(napoved)})


@app.route('/predict/naloga5', methods=['POST'])
def predict_naloga5():
    """Prejme sliko v base64 in vrne razred oblike (circles/squares/triangles)."""
    data = request.get_json(force=True)
    b64 = data['image'] if isinstance(data, dict) else data
    # odstranimo morebitno predpono "data:image/...;base64,"
    if ',' in b64:
        b64 = b64.split(',', 1)[1]
    slika = Image.open(io.BytesIO(base64.b64decode(b64))).convert('L')  # sivinska
    slika = slika.resize((100, 100))
    x = np.array(slika, dtype='float32') / 255.0      # normalizacija
    x = x.reshape(1, 100, 100, 1)
    razred = RAZREDI5[int(np.argmax(MODEL5.predict(x, verbose=0)[0]))]
    return jsonify({'prediction': razred})


@app.route('/', methods=['GET'])
def index():
    return jsonify({'storitev': 'naloga7', 'koncne_tocke':
                    ['/predict/naloga4', '/predict/naloga6', '/predict/naloga5']})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
