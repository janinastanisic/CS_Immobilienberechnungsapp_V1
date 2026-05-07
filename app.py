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
    "hat_lift":      0.00,#wird nicht direkt verwendet, Faktor_Lift wird stockwerkabhaengig in berechne_preis() berechnet
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
    alter = 2026 - baujahr #Alter der Immobilie wird berechnet
    faktor = 1 - ((80 - alter) / 80) #Berechnet den Multiplikator direkt: Bsp. Alter 0 = Faktor 0.0, Alter 40 = Faktor 0.50, Alter 80 = Faktor 1.0
    faktor = max(0.01, min(faktor, 1.0)) #Begrenzt den Faktor auf 0.01 bis 1.0, damit keine negativen oder über 1.0 liegenden Werte entstehen
    return faktor
#Die gewaehlte Formel basiert auf der Berechnung der Alterswertminderung gemaess Gutknecht (n.d.). Dabei wird eine Gesamtnutzungsdauer von 80 Jahren angenommen. 

def lift_faktor_berechnen(stockwerk):
    #Berechnet den Lift-Faktor abhängig vom Stockwerk.
    #Erdgeschoss: kein Effekt (Faktor 0)
    #1.-2. OG: +1.59% 
    #3.-5. OG: +4.58% 
    #6.-10. OG: +8.10% Gemaess Dai et al. (2026, S. 21) erhoeht ein Lift im Gebaede den Wohnungspreis bei unteren Stockwerken um 1.59 Prozent, bei mittleren um 4.58% und bei hoehern um 8.10 Prozent.
    if stockwerk == "Erdgeschoss": #Wenn das Stockwerk Erdgeschoss angegeben wurde, wird kein Faktor dazugerechnet.
        return 0.00
    elif stockwerk in ["1. Obergeschoss", "2. Obergeschoss"]:#Prüft, ob der eingegebene Wert in der Liste 1. Obergeschoss, 2. Obergeschoss vorkommt. Wenn das True ist, nimmt es den Faktor 0.0159
        return 0.0159
    elif stockwerk in ["3. Obergeschoss", "4. Obergeschoss", "5. Obergeschoss"]: #Prüft, ob der eingegebene Wert in der List 3. Obergeschoss, 4. Obergeschoss, 5. Obergeschoss vorkommt. Wenn das True ist, nimmt es den Faktor 0.0458
        return 0.0458
    elif stockwerk in ["6. Obergeschoss", "7. Obergeschoss", "8. Obergeschoss", #Prüft, ob der eingegebene Wert in der List 6. Obergeschoss, 7. Obergeschoss, 8. Obergeschoss, 9. Obergeschoss, 10. Obergeschoss oder hoeher vorkommt. Wenn das True ist, nimmt es den Faktor 0.0810
                       "9. Obergeschoss", "10. Obergeschoss oder hoeher"]:
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

#=========================
# Literaturverzeichnis
#=========================
#Niklowitz, M. (2026, April 18). Seesicht bei Immobilien: Wieviel zahlt man drauf? cash.ch. Retrieved May 7, 2026, from https://www.cash.ch/news/top-news/seesicht-bei-immobilien-wieviel-zahlt-man-drauf-927267
#Chau, K. W., Wong, S. K., & Yiu, C. Y. (2004). The value of the provision of a balcony in apartments in Hong Kong. Property Management, 22(3), 250–264. https://doi.org/10.1108/02637470410545020
#Conroy, S., Narwold, A., & Sandy, J. (2013). The value of a floor: valuing floor level in high‐rise condominiums in San Diego. International Journal of Housing Markets and Analysis, 6(2), 197–208. https://doi.org/10.1108/ijhma-01-2012-0003
#Dai, X., Yu, X., Ma, L., & Zheng, P. (2026). The Economic Benefit Evaluation of Elevator Retrofitting: An Empirical Analysis of Second-Hand Housing Price Premiums in Hangzhou’s Older Residential Compounds. Buildings, 16(1), 220. https://doi.org/10.3390/buildings16010220
#Deschermeier, P., Henger, R., Oberst, C., & Institut der deutschen Wirtschaft Köln e. V. (2023). Bedarfe und Preise. In BPD Immobilienentwicklung GmbH, Institut Der Deutschen Wirtschaft Köln E. V.
#Frey, S. (2026, February 4). The impact of property condition on sale price and time on market - Seb Frey, Silicon Valley + Bay Area REALTOR. Seb Frey, Silicon Valley + Bay Area REALTOR. https://sebfrey.com/the-impact-of-property-condition-on-sale-price-and-time-on-market/
#Gutknecht, L. (n.d.). Altersabschlag beim Haus: Alterswertminderung von Immobilien berechnen. Wohnglück.de. https://wohnglueck.de/artikel/altersabschlag
#Kempf, C., & Syz, J. (2022). Why pay for sustainable housing? Decomposing the green premium of the residential property market in the Canton of Zurich, Switzerland. SN Business & Economics, 2(11). https://doi.org/10.1007/s43546-022-00346-8
