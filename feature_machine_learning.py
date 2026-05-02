#feature_machine learning

# feature_machine_learning.py – KNN-Modell für Basispreisschätzung
# Ersetzt die einfache Durchschnittsberechnung pro Quartier durch ein
# datengetriebenes Modell, das Quartier, Zimmerzahl und Jahr berücksichtigt.

import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline


def _zimmer_zu_zahl(zimmer_str):
    """Wandelt einen Zimmerzahl-String in einen Float-Wert um."""
    s = str(zimmer_str).strip().replace(",", ".").replace(" Zimmer", "")
    if "+" in s:
        return 5.0
    try:
        return float(s)
    except ValueError:
        return 3.0


def trainiere_knn_modell(df):
    
    # Trainiert einen KNN-Regressor auf den Zürich-Immobiliendaten.

    #Eingabe-Features: Quartier (kodiert), Zimmerzahl (numerisch), Jahr
    #Zielgrösse: Preis_pro_m2

    #Ablauf:
    #1. Datenvorbereitung (fehlende Werte entfernen, Encoding)
    #2. Cross-Validation (5-fach) für k = 2 bis 10 → optimales k ermitteln
    #3. Finales Modell mit optimalem k trainieren

    #Rückgabe:
    #   modell        – trainiertes sklearn-Pipeline-Objekt
    #  le            – LabelEncoder für Quartiernamen
     #   bestes_k      – optimales k aus Cross-Validation
     #   mae_chf       – mittlerer absoluter Fehler in CHF/m²
     #   cv_ergebnisse – dict {k: mae} aller getesteten k-Werte
    
    daten = df.copy().dropna(subset=["Preis_pro_m2", "Jahr", "Quartier", "Zimmer"])

    le = LabelEncoder()
    daten["Quartier_enc"] = le.fit_transform(daten["Quartier"])
    daten["Zimmer_num"] = daten["Zimmer"].apply(_zimmer_zu_zahl)

    X = daten[["Quartier_enc", "Zimmer_num", "Jahr"]].values
    y = daten["Preis_pro_m2"].values

    bestes_k = 3
    bester_mae = float("inf")
    cv_ergebnisse = {}

    # k von 2 bis 10 testen (aber nie mehr als Datenpunkte / 5 erlauben)
    k_max = min(11, len(daten) // 5)
    for k in range(2, k_max):
        modell = Pipeline([
            ("scaler", StandardScaler()),
            ("knn", KNeighborsRegressor(n_neighbors=k)),
        ])
        scores = cross_val_score(
            modell, X, y, cv=5, scoring="neg_mean_absolute_error"
        )
        mae = -scores.mean()
        cv_ergebnisse[k] = round(mae)
        if mae < bester_mae:
            bester_mae = mae
            bestes_k = k

    # Finales Modell mit optimalem k auf allen Daten trainieren
    final = Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsRegressor(n_neighbors=bestes_k)),
    ])
    final.fit(X, y)

    return final, le, bestes_k, round(bester_mae), cv_ergebnisse


def ml_basispreis_schaetzen(modell, le, quartier, zimmerzahl_str, jahr=2024):
    """
    Schätzt den Basispreis pro m² für ein gegebenes Quartier und eine Zimmerzahl.

    Rückgabe: geschätzter Preis als int (CHF/m²), oder None falls Quartier unbekannt
    """
    try:
        q_enc = le.transform([quartier])[0]
    except ValueError:
        return None
    zimmer = _zimmer_zu_zahl(zimmerzahl_str)
    X = np.array([[q_enc, zimmer, jahr]])
    return int(round(float(modell.predict(X)[0])))