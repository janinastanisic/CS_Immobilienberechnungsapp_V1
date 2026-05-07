#Berechnung_feature
from feature_machine_learning import ml_basispreis_schaetzen

# ─────────────────────────────────────────────
# KORREKTURFAKTOREN:Der Faktor wird mit dem Basispreis mulitpliziert und passt den Preis prozentual an. Bsp. Faktor 0.92 = Preis wird um 8% reduziert. Die Faktoren basieren auf Schätzwerten.
# ─────────────────────────────────────────────

FAKTOR_ZUSTAND = {
    "Neuwertig / Neubau":    1.10,
    "Gut gepflegt":          1.00,
    "Renovationsbeduerftig": 0.85,
}

FAKTOR_STOCKWERK = {
    "Erdgeschoss":       0.95,
    "1. Obergeschoss":   0.98,
    "2. Obergeschoss":   1.00,
    "3. Obergeschoss":   1.02,
    "4. Obergeschoss":   1.04,
    "5. OG oder hoeher": 1.06,
    "Dachgeschoss":      1.08,
}

AUSSTATTUNG_FAKTOREN = {
    "hat_balkon":    0.03,
    "hat_parkplatz": 0.04,
    "hat_lift":      0.02,
    "hat_keller":    0.01,
    "hat_seesicht":  0.08,
    "hat_minergie":  0.03,
} #Jede zusätzliche Ausstattung addiert einen Prozentsatz zum Preis: Bsp. Faktor 0.03 = +3%. Der Prozentsatz basiert auf Schätzwerten.

AUSSTATTUNG_LABELS = {
    "hat_balkon":    "Balkon / Terrasse",
    "hat_parkplatz": "Parkplatz / Garage",
    "hat_lift":      "Lift",
    "hat_keller":    "Keller / Estrich",
    "hat_seesicht":  "Seesicht",
    "hat_minergie":  "Minergie",
} #Übersetzung von Bezeichnungen in Texte, welche in der App ersichtlich sind
#überprüfe, ob diese in anderen features verwendet werden, sonst kann mann Austattung_labels löschen

# ─────────────────────────────────────────────
# BAUJAHR-FAKTOR: 
# ─────────────────────────────────────────────
def faktor_baujahr(baujahr):
    alter = 2026 - baujahr #Alter der Immobilie wird berechnet. Das Alter wird in Kategorien eingeteil. Bsp. wenn Immobilie jünger als 5 Jahre ist, wird der Preis um 10% erhöht.
    if alter <= 5:    return 1.10
    elif alter <= 15: return 1.05
    elif alter <= 30: return 1.00
    elif alter <= 50: return 0.95
    else:             return 0.90


# ─────────────────────────────────────────────
# BERECHNUNGSFUNKTION: Die Funktion berechne_preis wird definiert
# ─────────────────────────────────────────────
def berechne_preis(quartier, zimmerzahl, wohnflaeche, baujahr,
                   stockwerk, zustand, ausstattung,knn_modell, knn_le, BASISPREIS_PRO_QUARTIER): #Definition einer Funktion mit Eingabewerten
    ml_preis = ml_basispreis_schaetzen(knn_modell, knn_le, quartier, zimmerzahl, jahr=2026) #berechnet den Basispreis: Jahr wird als 2026 gesetzt, da die Schätzung für den heutigen Preis ist
    basispreis = ml_preis if ml_preis is not None else BASISPREIS_PRO_QUARTIER.get(quartier, 11000) #zb. 11k/m^2 und sonst den berechneten durchschnitt unserer Daten als Basispreis
    f_zustand   = FAKTOR_ZUSTAND.get(zustand, 1.00) #holt den Wert, der bei zustand als Input angegeben wurde und nimmt den Korrekturfaktor. Falls der Wert nicht gefunden wurde, wird 1.00 als Standardwert verwendet.
    f_stockwerk = FAKTOR_STOCKWERK.get(stockwerk, 1.00) #holt den Wert, der bei stockwerk als Input angegeben wurde und nimmt den Korrekturfaktor. Falls der Wert nicht gefunden wurde, wird 1.00 als Standardwert verwendet.
    f_baujahr   = faktor_baujahr(baujahr) #holt den Wert, der bei baujahr als Input angegeben wurde und nimmt den Korrekturfaktor.

    f_ausstattung = 1.00 #Startet bei 1.00. 
    for merkmal, wert in ausstattung.items(): #Iteriert mit einer for Schleife durch alle Ausstattungsmerkmale durch
        if wert: #Nur wenn eine Checkbox aktiviert ist (deren Wert = True) wird der nächste Schritt durchgeführt
            f_ausstattung += AUSSTATTUNG_FAKTOREN.get(merkmal, 0) #Holt den Faktor für das Ausstattungsmerkmal aus dem obigen Dictionary und addiert ihn zu 1.00

    preis_pro_m2 = (basispreis * f_zustand
                    * f_stockwerk * f_baujahr * f_ausstattung) #Berechnet den Preis pro Quadratmeter, indem es unser durch das ML-modell kalulierter Basispreis mit allen Korrekturfaktoren multipliziert
    gesamtpreis  = preis_pro_m2 * wohnflaeche #Berechnet den Gesamtpreis indem der Preis pro Quadratmeter mit der wohnflaeche als Input Multipliziert wird

    faktoren = { #speichert die berechneten Faktoren als Dictionary ab
        "Basispreis (Quartier)": basispreis,
        "Zustand":               f_zustand,
        "Stockwerk":             f_stockwerk,
        "Baujahr":               f_baujahr,
        "Ausstattung":           f_ausstattung,
    }

    return round(preis_pro_m2), round(gesamtpreis), faktoren #gibt den gerundeten Preis pro m2, den gerundeten Gesamtpreis und das Dictionary der Faktoren zurück
