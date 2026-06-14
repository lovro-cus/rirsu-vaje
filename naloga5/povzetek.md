# Naloga 5 — Konvolucijske nevronske mreže (CNN)

## Cilj
Razvrščanje slik zbirke **shapes** v 3 razrede (`circles`, `squares`, `triangles`) z
uporabo konvolucijskih nevronskih mrež, ovrednoteno s **5-kratno prečno validacijo**.

## Zagon
```bash
.venv/Scripts/python -m nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.kernel_name=rirsu naloga5/naloga5.ipynb
```
Notebook ob koncu shrani najboljši model `model_naloga5.keras` in `razredi_naloga5.pkl`
(uporabljena v nalogi 7, končna točka `/predict/naloga5`).

## Obdelava podatkov
1. **DataFrame** s stolpcema `filepath` in `label` (300 slik, po 100 na razred).
2. **ImageDataGenerator**:
   - `train_datagen`: `rescale=1/255` + `validation_split=0.2` (razmerje 80:20) → Model 1.
   - `train_datagen_aug`: dodatno **augmentira** (rotacija ±20°, zamik, povečava) → Model 2 in finalni model.
   - `test_datagen`: samo `rescale=1/255`.
3. Znotraj zanke 5-kratne CV iteratorji prek `flow_from_dataframe`:
   - vhodne slike `100×100×1` (sivinske), `class_mode='categorical'`,
   - učni/validacijski: `shuffle=True, seed=1234`; testni: `batch_size=1, shuffle=False, seed=1234`.

## Arhitekture
**Model 1 (predpisana arhitektura):**
`Conv2D(16,3×3,relu) → MaxPool → Conv2D(16,3×3,relu) → MaxPool → Flatten → Dense(128,relu) → Dense(3,softmax)`,
optimizator `adam`, batch 32.

**Model 2 (lastna arhitektura):** globlja mreža
`Conv(32)→BN→Pool → Conv(64)→BN→Pool → Conv(64)→Pool → Flatten → Dense(128)→Dropout(0.3) → Dense(3,softmax)`,
optimizator `Adam(lr=5e-4)`, **batch 16 + augmentacija** (spremenjeni hiperparametri).

Oba modela učena do **50 epoh**; zgodovina vsakega modela v vsakem rezu shranjena in izrisana
(točnost + izguba, učna in validacijska).

## Ovrednotenje (metrike kot pri nalogi 3)
Točnost, utežen F1, utežena preciznost, utežen priklic — za vsak rez; nato povprečja,
**boxploti** (4, po en na metriko) in **stolpčni diagrami** povprečij.

### Doseženi rezultati (povprečje 5 rezov)
| Model | točnost | F1 | preciznost | priklic |
|-------|---------|----|-----------|---------|
| Model 1 (osnovni)          | ~0.52 | ~0.52 | ~0.53 | ~0.52 |
| Model 2 (augmentacija)     | **~0.63** | ~0.60 | ~0.82 | ~0.63 |

## Ugotovitve za zagovor
- Zbirka je majhna (100 ročno risanih slik/razred), zato je generalizacija zahtevna:
  brez augmentacije model **preprileže** (učna točnost ~1.0, testna ~0.5–0.6).
- **Augmentacija** (Model 2) bistveno izboljša rezultate (~0.63 proti ~0.52); en rez doseže celo 0.83.
- Točnost po rezih precej **niha** (0.42–0.83), ker ima vsak testni rez le 60 slik — to je
  pričakovano pri tako majhni zbirki.
- CNN sicer presega klasične algoritme strojnega učenja (naloge 3/4), ker samodejno učijo
  prostorske značilnice; tu jih omejuje predvsem velikost zbirke.
- Najboljši model (Model 2) je ponovno naučen na vseh podatkih in serializiran za nalogo 7.

## Dodatni del (Kaggle)
Koda za izbiro in shranjevanje najboljše arhitekture je vključena (`model_naloga5.keras`).
Za dejansko oddajo na Kaggle bi z istim modelom napovedali razrede slik iz mape `test`
in zgradili `submission.csv`; v tej zbirki testna mapa ni priložena, zato je korak oddaje
le opisan (model je pripravljen za napovedovanje nad poljubnimi novimi slikami).
