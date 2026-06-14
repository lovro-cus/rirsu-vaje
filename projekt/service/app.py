"""Spletna storitev projektne naloge - napoved PM10.

Konecna tocka:
  POST /predict - v telesu prejme zaporedje (okno) urnih meritev v JSON obliki,
                  vrne napovedano naslednjo vrednost PM10: {"prediction": 3.14}
"""
import os, pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model

# uvozimo skupni modul za predprocesiranje (kopiran poleg storitve)
import prep_projekt as pp

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, 'models')

app = Flask(__name__)

# nalaganje modela in scalerjev ob zagonu
MODEL = load_model(os.path.join(MODELS, 'model_pm10.keras'))
with open(os.path.join(MODELS, 'scalers_pm10.pkl'), 'rb') as f:
    CFG = pickle.load(f)
WINDOW = CFG['window']


@app.route('/predict', methods=['POST'])
def predict():
    """Prejme okno meritev (seznam vrstic) in napove naslednjo vrednost PM10."""
    data = request.get_json(force=True)
    # dovolimo {"data": [...]} ali cist seznam vrstic
    vrstice = data['data'] if isinstance(data, dict) and 'data' in data else data
    df = pd.DataFrame(vrstice)

    # enako predprocesiranje kot pri ucenju
    X_df, _ = pp.build_features(df)
    if len(X_df) < WINDOW:
        return jsonify({'error': f'pricakovano vsaj {WINDOW} meritev, prejetih {len(X_df)}'}), 400

    # vzamemo zadnjih WINDOW vrstic, standardiziramo in preoblikujemo v (1, WINDOW, n_feat)
    Xwin = CFG['feat_scaler'].transform(X_df.values[-WINDOW:])
    Xwin = Xwin.reshape(1, WINDOW, len(CFG['features']))

    napoved_s = MODEL.predict(Xwin, verbose=0).flatten()[0]
    # inverzna standardizacija v izvirno skalo PM10
    napoved = float(CFG['targ_scaler'].inverse_transform([[napoved_s]])[0, 0])
    return jsonify({'prediction': round(napoved, 2)})


@app.route('/', methods=['GET'])
def index():
    return jsonify({'storitev': 'projekt PM10', 'koncna_tocka': '/predict',
                    'velikost_okna': WINDOW})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
