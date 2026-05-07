#Berechnung_feature
from feature_machine_learning import ml_basispreis_schaetzen

# ─────────────────────────────────────────────
# KORREKTURFAKTOREN:Der Faktor wird mit dem Basispreis mulitpliziert und passt den Preis prozentual an. Bsp. Faktor 0.92 = Preis wird um 8% reduziert.
# ─────────────────────────────────────────────

FAKTOR_ZUSTAND = { 
    "Neuwertig / Neubau":    1.125, 
    "Gut gepflegt":          1.075,
    "Renovationsbeduerftig": 1.00,
}
#Gemaess Frey (2026) fuehrt ein neuwertiger Zustand zu einer Wertsteigerung von 10 bis 15 %, waehrend fuer einen guten Zustand 
#eine Wertsteigerung von 5 bis 10 % angegeben wird. Fuer die vorliegende Bewertung wurde jeweils der Mittelwert der in der 
#Quelle genannten Spannbreiten als Korrekturfaktor verwendet, sodass 12,5 % fuer den neuwertigen sowie 7,5 % fuer den guten Zustand gewaelt wurden.

FAKTOR_STOCKWERK = {
    "Erdgeschoss":                   1.00,
    "1. Obergeschoss":               1.022,
    "2. Obergeschoss":               1.044,
    "3. Obergeschoss":               1.066,
    "4. Obergeschoss":               1.088,
    "5. Obergeschoss":               1.11,
    "6. Obergeschoss":               1.132,
    "7. Obergeschoss":               1.154,
    "8. Obergeschoss":               1.176,
    "9. Obergeschoss":               1.198,
    "10. Obergeschoss oder hoeher":  1.22,
}
#Gemaess Conroy et al. (1013, S.201) geht ein hoeheres Stockwerk mit einem Anstieg des Immobilienpreises von 2.2 Prozent einher. 

AUSSTATTUNG_FAKTOREN = {
    "hat_balkon":    0.1385,
    "hat_tiefgarage": 0.10,
    "hat_lift":      0.022,
    "hat_seesicht":  0.11,
    "hat_minergie":  0.491,
} #Jede zusätzliche Ausstattung addiert einen Prozentsatz zum Preis: Bsp. Faktor 0.03 = +3%.
#Gemaess Chau et al. (2004, S. 256) fuehrt ein grosser Balkon mit guter Aussicht zu 24 Prozent hoeherem Kaufpreis und ein kleiner Balkon ohne Aussicht 
#zu 3.7% hoeherem Kaufpreis. Fuer den gewaehlten Korrekturfaktor hat_balkon von 13.85 Prozent haben wir daraus den Mittelwert berechnet. 
#Gemaess Deschermeier et al. (2023, S. 46) steigert eine Tiefgarage den Immobilienwert um durchschnittlich 10 Prozent.
#Gemaess Niklowitz (2026) erhoeht eine Seesicht den Immobilienpreis um 11 Prozent.
#Gemaess Kempf & Syz (2022, S. 170) hat die Stadt Zuerich eine Minergie Preispraemie von 4.91 Prozent.

AUSSTATTUNG_LABELS = {
    "hat_balkon":    "Balkon / Terrasse",
    "hat_tiefgarage": "Tiefgarage",
    "hat_lift":      "Lift",
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
