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
#wandelt die Zimmerzahl in einen float um, weil das Modell nur mit Zahlen arbeiten kann

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
    
    daten = df.copy().dropna(subset=["Preis_pro_m2", "Jahr", "Quartier", "Zimmer"]) #kopiert die Daten von df und entfernt alle Zeilen mit fehlenden Werten

    le = LabelEncoder()
    daten["Quartier_enc"] = le.fit_transform(daten["Quartier"]) #Wandelt die verschiedenen Quartiernamen in Zahlen um
    daten["Zimmer_num"] = daten["Zimmer"].apply(_zimmer_zu_zahl) #wandelt die zimmerzahl-Spalte in Zahlen um mit der Hilffunktion _zimmer_zu_zahl von oben

    X = daten[["Quartier_enc", "Zimmer_num", "Jahr"]].values #Das sind die Eingabe Merkmale --> Quartier, Zimmer und Jahr
    y = daten["Preis_pro_m2"].values #Das ist der Preis, den das Modell lernen soll 

    bestes_k = 3 #als Startwert, wird überschrieben wenn ein besseres k gefunden wird, k ist die Anzahl an Nachbarn, bei k=2 nimmt es die 2 ähnlichsten Einträge, bei 3 nimmt es 3 und so weiter
    bester_mae = float("inf") #unendlich weil so der erste Fehler kleiner sein muss und somit auch gespeichert wird
    cv_ergebnisse = {} #Leeres Dictionary, wird später mit allen k-Werten und ihren Fehlern gefüllt 

    # k von 2 bis 10 testen (aber nie mehr als Datenpunkte / 5 erlauben)
    k_max = min(11, len(daten) // 5) #berechnet das maximale k. Es darf nie mehr als 11 sein oder mehr als die Anzahl Datenpunkte geteilt durch 5, so bleiben genügen Daten zur Überprüfung übrig
    for k in range(2, k_max): #diese for clause testet k=2, k=3 etc. bis k_max
        modell = Pipeline([
            ("scaler", StandardScaler()),
            ("knn", KNeighborsRegressor(n_neighbors=k)),
        ])
        #ertsellt ein Nodell mit zwei Schritten: StandartScaler skaliert zuerst alle Zahlen auf gleiche Grössenordnung, dann KNN mit dem aktuellen k.
        scores = cross_val_score(
            modell, X, y, cv=5, scoring="neg_mean_absolute_error"
        )#testet das Modell 5 mal. Jedes Mal wird mit anderen Daten getestet fürs Lernen und Testen
        #neg_mean_absolut_error ist der negative Fehler und wird deshalb unten umgekehrt
        mae = -scores.mean() #macht den negativen Fehler positiv und berechnet dann den Durchschnitt dieser 5 Tests von oben
        cv_ergebnisse[k] = round(mae) #Fehler dieses k's wird in unserern Dictionary cv_ergebnisse gespeichert

        if mae < bester_mae:
            bester_mae = mae
            bestes_k = k
        #diese if clause untersucht ob der aktuelle k-Wert einen kleineren Fehler hatte als der vorherige und wenn ja wird er als bestes k gespeichert

    #Die Formle test k bis zu k_max. Für jedes K wird das Modell 5 mal getestet (Cross-Validation) und der durchschnittliche Fehler (mae) berechnet. 
    # Das beste k (also das k mit dem kleinsten Fehler) wird dann gespeichert

    # Finales Modell mit optimalem k auf allen Daten trainieren:
    final = Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsRegressor(n_neighbors=bestes_k)), #Hier wird das finale Modell mit dem oben gefundenen besten Ks
    ])
    final.fit(X, y) #trainiert das Modell auf alle Daten und mehr aufgeteteilt wie bei der Cross-Validation
    return final, le, bestes_k, round(bester_mae), cv_ergebnisse #das fertige Modell wird zurückgegeben mit dem LabelEncounter, dem besten k, dem besten fehler, und allen Ergebnissen in unserem Dictionary
#Trainiert das Modell einmal mit dem besten k auf alle Daten

#Die Quartier- und Zimmereingabe in der App werden in mit dieser Funktion in Zahlen umgewandelt und gibt den geschätzten Preis als Rückgabe:
def ml_basispreis_schaetzen(modell, le, quartier, zimmerzahl_str, jahr=2024):
    """
    Schätzt den Basispreis pro m² für ein gegebenes Quartier und eine Zimmerzahl.

    Rückgabe: geschätzter Preis als int (CHF/m²), oder None falls Quartier unbekannt
    """
    try:
        q_enc = le.transform([quartier])[0] #wandelt Quartiername in Zahl um
    except ValueError:
        return None #falls das Quartier unbekannt ist --> Fallback auf Durchschnitt
    zimmer = _zimmer_zu_zahl(zimmerzahl_str)
    X = np.array([[q_enc, zimmer, jahr]]) #steckt unsere drei Werte die wir benutzen in einen Array, welches das Format ist, welches das Modell erwartet
    return int(round(float(modell.predict(X)[0]))) #berechnet den Preis und gibt ihn als integer zurück

#Verständnis notiz zur Cross-validation: Die Daten werden aufgeteilt: ein Teil zum Lernen und einen Teil zum Testen. 
#es vergleicht dann den echten Preis aus der Datenbank mit dem vorhergesagten Wert und berechnet den Fehler
#dann wird der Durchschnitt der Fehler aller Tests berechnet und das k mit dem kleinsten Fehlerdurchschnitt für die Preisberechnung verwendet