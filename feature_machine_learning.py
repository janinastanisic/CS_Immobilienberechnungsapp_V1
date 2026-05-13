# =============================================================
# feature_machine_learning.py – KNN-Modell für Basispreisschätzung
# =============================================================

# ZUSAMMENFASSUNG
# Dieses Feature trainiert ein K-Nearest-Neighbors-Modell (KNN),
# das den Basispreis pro m² für ein Quartier, eine Zimmerzahl
# und ein Jahr (wir definieren immer 2026) schätzt. Es ersetzt die einfache Durchschnitts-
# berechnung durch ein datengetriebenes Modell.

# Ablauf:
# 1. Daten vorbereiten: Quartiernamen in Zahlen umwandeln (LabelEncoder),
#    Zimmerzahl bereinigen und in Float umwandeln
# 2. Optimales k ermitteln: k=2 bis k=10 mit 5-facher Cross-Validation
#    testen und k mit kleinstem mittleren Fehler (MAE) wählen
# 3. Finales Modell mit bestem k auf allen Daten trainieren
# 4. ml_basispreis_schaetzen() schätzt für neue Eingaben den Preis
#    indem Quartier, Zimmer und Jahr ins Modell eingespeist werden

# Bei der Entwicklung dieses Codes wurde Claude AI (Anthropic, 2026) als Hilfsmittel eingesetzt, um Lösungsansätze zu erarbeiten und Fehler zu korrigieren. 
# =============================================================

import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline

def _zimmer_zu_zahl(zimmer_str): #Definition einer Funktion. Input ist ein Zimmer-Wert als String. Die Idee der Funktion ist es, eine Zahl zurückzubekommen
    s = str(zimmer_str).strip() #Wandelt den Iinput in einen String um und entfernt alle Leerzeichen vorher und nacher " 3-Zimmer " --> "3-Zimmer"
    if "6" in s:        #In unserem Datenset haben wir manchmal als Zimmeranzahl "6-Zimmer und mehr". Wegen dem "und mehr" können wir diesen Wert nicht normal umwandeln:
        return 6.0      #Deshalb wird diese Eingabe als errstes abgefangen und direkt in ein 6.0 umgewandelt --> aufgrund des "und mehr" müssen wir hier einen Sonderfall machen
    s = s.replace("-Zimmer", "").replace(" Zimmer", "") #Entfernt -Zimmer und Zimmer aus dem Text des Datensets. "3-Zimmer", "3 Zimmer" --> "3"
    if "+" in s: #Falls ein plus vorkommt, wie z.B: 5+ aus der Auswahl in unserer App, wird 5.0 zurückgegeben
        return 5.0
    try:
        return float(s) #Der oben "gereinigte" Text wird in einen float umgewandelt
    except ValueError:
        return 3.0 #Standardwert falls die Zimmerzahl unbekannt ist. Wir nehmen 3 weil es der häufigste Wohnungstyp im Datenset ist
    

def trainiere_knn_modell(df):
    
    # Trainiert einen KNN-Regressor auf den Zürich-Immobiliendaten

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
    
    daten = df.copy().dropna(subset=["Preis_pro_m2", "Jahr", "Quartier", "Zimmer"]) #Kopiert die Daten von df und entfernt alle Zeilen mit fehlenden Werten

    le = LabelEncoder()
    daten["Quartier_enc"] = le.fit_transform(daten["Quartier"]) #Wandelt die verschiedenen Quartiernamen in Zahlen um
    daten["Zimmer_num"] = daten["Zimmer"].apply(_zimmer_zu_zahl) #Wandelt die zimmerzahl-Spalte in Zahlen um mit der Hilffunktion _zimmer_zu_zahl von oben

    X = daten[["Quartier_enc", "Zimmer_num", "Jahr"]].values #Das sind die Eingabe Merkmale --> Quartier, Zimmer und Jahr
    y = daten["Preis_pro_m2"].values #Das ist der Preis, den das Modell lernen soll 

    bestes_k = 3 #Als Startwert, wird überschrieben wenn ein besseres k gefunden wird, k ist die Anzahl an Nachbarn, bei k=2 nimmt es die 2 ähnlichsten Einträge, bei 3 nimmt es 3 und so weiter
    bester_mae = float("inf") #Unendlich weil so der erste Fehler kleiner sein muss und somit auch gespeichert wird
    cv_ergebnisse = {} #Leeres Dictionary, wird später mit allen k-Werten und ihren Fehlern gefüllt 

    # k von 2 bis 10 testen (aber nie mehr als Datenpunkte / 5 erlauben)
    k_max = min(11, len(daten) // 5) #Berechnet das maximale k. Es darf nie mehr als 10 sein oder mehr als die Anzahl Datenpunkte geteilt durch 5, weil wir ja CV=5 gesetzt haben (würde sonst nicht aufgehen)
    for k in range(2, k_max): #diese for clause testet k=2, k=3 etc. bis k_max
        modell = Pipeline([
            ("scaler", StandardScaler()),
            ("knn", KNeighborsRegressor(n_neighbors=k)),
        ])
        #Erstellt ein Modell mit zwei Schritten: StandartScaler skaliert zuerst alle Zahlen auf gleiche Grössenordnung (also alle inputs sind gleich gewichtet), dann KNN mit dem aktuellen k
        
        
        scores = cross_val_score(
            modell, X, y, cv=5, scoring="neg_mean_absolute_error"
        )#Testet das Modell 5 mal. Jedes Mal wird mit anderen Daten getestet fürs lernen und Testen
        #neg_mean_absolut_error ist der negative Fehler und wird deshalb unten umgekehrt
        mae = -scores.mean() #Macht den negativen Fehler positiv und berechnet dann den Durchschnitt dieser 5 Tests von oben
        cv_ergebnisse[k] = round(mae) #Fehler dieses k's wird in unserern Dictionary cv_ergebnisse gespeichert

        if mae < bester_mae:
            bester_mae = mae
            bestes_k = k
        #Diese if clause untersucht ob der aktuelle k-Wert einen kleineren Fehler hatte als der vorherige und wenn ja wird er als bestes k gespeichert


    #Finales Modell mit optimalem k auf allen Daten trainieren:
    final = Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsRegressor(n_neighbors=bestes_k)), #Hier wird das finale Modell mit dem oben gefundenen besten k erstellt
    ])
    final.fit(X, y) #Trainiert das Modell auf alle Daten und mehr aufgeteilt wie bei der Cross-Validation
    return final, le, bestes_k, round(bester_mae), cv_ergebnisse #Das fertige Modell wird zurückgegeben mit dem LabelEncounter, dem besten k, dem besten Fehler, und allen Ergebnissen in unserem Dictionary
#Trainiert das Modell einmal mit dem besten k auf alle Daten

#Diese Funktion nimmt Quartier, Zimmerzahl und Jahr als Eingabe und gibt den geschätzten Basispreis pro m2 als Rückgabe:
def ml_basispreis_schaetzen(modell, le, quartier, zimmerzahl_str, jahr=2026):
    
    #Schätzt den Basispreis pro m² für ein gegebenes Quartier und eine Zimmerzahl.

    #Rückgabe: geschätzter Preis als int (CHF/m²), oder None falls Quartier unbekannt
    
    try:
        q_enc = le.transform([quartier])[0] #Wandelt Quartiername in Zahl um
    except ValueError:
        return None #Falls das Quartier unbekannt ist --> Fallback auf Durchschnitt
    zimmer = _zimmer_zu_zahl(zimmerzahl_str)
    X = np.array([[q_enc, zimmer, jahr]]) #Steckt unsere drei Werte die wir benutzen in einen Array, welches das Format ist, welches das Modell erwartet
    return int(round(float(modell.predict(X)[0]))) #Berechnet den Preis und gibt ihn als integer zurück

#Verständnis notiz zur Cross-validation: Die Daten werden aufgeteilt: ein Teil zum Lernen und einen Teil zum Testen
#Es vergleicht dann den echten Preis aus der Datenbank mit dem vorhergesagten Wert und berechnet den Fehler
#Dann wird der Durchschnitt der Fehler aller Tests berechnet und das k mit dem kleinsten Fehlerdurchschnitt für die Preisberechnung verwendet