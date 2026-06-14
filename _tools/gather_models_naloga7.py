"""Zbere serializirane modele iz nalog 5 in 6 v mapo naloga7/models/,
da je spletna storitev (in Docker slika) samozadostna."""
import shutil, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
DST = os.path.join(ROOT, 'naloga7', 'models')
os.makedirs(DST, exist_ok=True)
pari = [
    ('naloga6/model_naloga6.keras', 'model_naloga6.keras'),
    ('naloga6/scaler_naloga6.pkl',  'scaler_naloga6.pkl'),
    ('naloga5/model_naloga5.keras', 'model_naloga5.keras'),
    ('naloga5/razredi_naloga5.pkl', 'razredi_naloga5.pkl'),
]
for src, name in pari:
    s = os.path.join(ROOT, src)
    if os.path.exists(s):
        shutil.copy(s, os.path.join(DST, name))
        print('kopirano:', name)
    else:
        print('MANJKA:', src)
