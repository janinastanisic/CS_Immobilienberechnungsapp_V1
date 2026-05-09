# =============================================================
# feature_berechnung.py – Preisberechnung mit Korrekturfaktoren
# =============================================================

# ZUSAMMENFASSUNG
# Dieses Feature berechnet den geschätzten Immobilienpreis (CHF/m²
# und Gesamtpreis) basierend auf dem ML-Basispreis und mehreren
# Korrekturfaktoren.

# Ablauf:
# 1. ML-Modell schätzt den Basispreis pro m² (nach Quartier,
#    Zimmerzahl und Jahr)
# 2. Korrekturfaktoren werden multipliziert:
#    - Zustand      
#    - Stockwerk    
#    - Baujahr      
#    - Ausstattung  
# 3. Gesamtpreis = Preis pro m² × Wohnfläche
# 4. Rückgabe: Preis/m², Gesamtpreis, Faktoren-Dictionary

# Bei der Entwicklung dieses Codes wurde Claude AI (Anthropic, 2026) als Hilfsmittel eingesetzt, um Lösungsansätze zu erarbeiten und Fehler zu korrigieren. 
# =============================================================

from feature_machine_learning import ml_basispreis_schaetzen

# ─────────────────────────────────────────────
# KORREKTURFAKTOREN:Der Faktor wird mit dem Basispreis mulitpliziert und passt den Preis prozentual an. Bsp. Faktor 0.92 = Preis wird um 8% reduziert.
# ─────────────────────────────────────────────

FAKTOR_ZUSTAND = { 
    "Neuwertig / Neubau":    1.125, 
    "Gut gepflegt":          1.075,
    "Renovationsbedürftig": 1.00,
}
#Gemäss Frey (2026) führt ein neuwertiger Zustand zu einer Wertsteigerung von 10 bis 15 %, während für einen guten Zustand 
#eine Wertsteigerung von 5 bis 10 % angegeben wird. Für die vorliegende Bewertung wurde jeweils der Mittelwert der in der 
#Quelle genannten Spannbreiten als Korrekturfaktor verwendet, sodass 12,5 % für den neuwertigen sowie 7,5 % für den guten Zustand gewält wurden.

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
    "10. Obergeschoss oder höher":  1.22,
}
#Gemäss Conroy et al. (1013, S.201) geht ein höheres Stockwerk mit einem Anstieg des Immobilienpreises von 2.2 Prozent einher. 

AUSSTATTUNG_FAKTOREN = {
    "hat_balkon":    0.1385,
    "hat_tiefgarage": 0.10,
    "hat_lift":      0.00,#wird nicht direkt verwendet, Faktor_Lift wird stockwerkabhängig in berechne_preis() berechnet
    "hat_seesicht":  0.11,
    "hat_minergie":  0.491,
} #Jede zusätzliche Ausstattung addiert einen Prozentsatz zum Preis: Bsp. Faktor 0.10 = +10%.
#Gemäss Chau et al. (2004, S. 256) führt ein grosser Balkon mit guter Aussicht zu 24 Prozent höherem Kaufpreis und ein kleiner Balkon ohne Aussicht 
#zu 3.7% höherem Kaufpreis. Für den gewählten Korrekturfaktor hat_balkon von 13.85 Prozent haben wir daraus den Mittelwert berechnet. 
#Gemäss Deschermeier et al. (2023, S. 46) steigert eine Tiefgarage den Immobilienwert um durchschnittlich 10 Prozent.
#Gemäss Niklowitz (2026) erhöht eine Seesicht den Immobilienpreis um 11 Prozent.
#Gemäss Kempf & Syz (2022, S. 170) hat die Stadt Zürich eine Minergie Preisprämie von 4.91 Prozent.

# ─────────────────────────────────────────────
# BAUJAHR-FAKTOR: 
# ─────────────────────────────────────────────

def faktor_baujahr(baujahr):
    alter = 2026 - baujahr  # Alter der Immobilie in Jahren
    abschreibung = min(alter * 0.01, 0.40)  # 1% pro Jahr, max. 40% wird abgeschrieben
    faktor = 1.0 - abschreibung
    return faktor
    # Quelle: Weisung Liegenschaftenneubewertung 2026, Kanton Zürich.
    # Altersentwertung = 1% des Neubauwerts pro Jahr, höchstens 40%.
    # (Kanton Zürich, 2026)

def lift_faktor_berechnen(stockwerk):
    #Berechnet den Lift-Faktor abhängig vom Stockwerk.
    #Erdgeschoss: kein Effekt (Faktor 0)
    #1.-2. OG: +1.59% 
    #3.-5. OG: +4.58% 
    #6.-10. OG: +8.10% Gemäss Dai et al. (2026, S. 21) erhöht ein Lift im Gebäude den Wohnungspreis bei unteren Stockwerken um 1.59 Prozent, bei mittleren um 4.58% und bei höheren um 8.10 Prozent.
    if stockwerk == "Erdgeschoss":
        return 0.00
    elif stockwerk in ["1. Obergeschoss", "2. Obergeschoss"]:
        return 0.0159
    elif stockwerk in ["3. Obergeschoss", "4. Obergeschoss", "5. Obergeschoss"]:
        return 0.0458
    elif stockwerk in ["6. Obergeschoss", "7. Obergeschoss", "8. Obergeschoss",
                       "9. Obergeschoss", "10. Obergeschoss oder höher"]:
        return 0.0810
    else:
        return 0.00 #Fallback falls unbekanntes Stockwerk

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
            if merkmal == "hat_lift": #Lift-Faktor ist abhängig vom Stockwerk
                f_ausstattung += lift_faktor_berechnen(stockwerk) #Ruft die Hilfsfunktion auf und addiert den stockwerkabhängigen Lift-Faktor
            else:
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
