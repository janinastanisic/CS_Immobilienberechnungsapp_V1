# =============================================================
# feature_Koordinaten.py – GPS-Koordinaten der Zürcher Quartiere
# =============================================================

# ZUSAMMENFASSUNG
# Dieses Feature stellt die Mittelpunkt-Koordinaten (Latitude/Longitude)
# aller 24 Zürcher Stadtquartiere als Dictionary bereit.
# Die Koordinaten werden von der Heatmap-Karte benötigt, um die
# farbigen Kreise an der richtigen Stelle zu platzieren.

# Ablauf:
# 1. get_koordinaten() definieren
# 2. Dictionary mit Quartiernamen als Schlüssel und
#    (Latitude, Longitude)-Tupel als Wert wird zurückgegeben

# Hinweis: Koordinaten sind hardcodiert, da der offizielle der CSV link nicht funktioniert da die Stadt Zürich 
# #höchstwahrscheinlich den Zugriff blockiert hat. Wir haben probiert die Daten herunterzuladen und manuell abzuspeichern, 
# aber die Daten haben keine Lat/Lon Spalten sondern nur geometry mit POLYGON Koordinaten.
# Quelle: https://www.stadt-zuerich.ch/geodaten/download/Statistische_Quartiere?format=10008
# LV59 in WGS84-Koordinaten-Umrechner: https://zurzach.ag/liegenschaften/lv95-in-wgs84-koordinaten-fuer-google-maps-oder-openstreetmap-umrechnen-und-konvertieren/

# Bei der Entwicklung dieses Codes wurde Claude AI (Anthropic, 2026) als Hilfsmittel eingesetzt, um Lösungsansätze zu erarbeiten und Fehler zu korrigieren. 
# =============================================================

def get_koordinaten(): #Funktion get_koordinaten wird definiert
    return { #Die Funktion gibt ein Dictionary zurück mit Quartiername als Schlüssel (string), Latitude und Longitude (Tupel).
        "Affoltern":            (47.42318535463998, 8.50649991576755),
        "Albisrieden":          (47.37104029612350, 8.48484913751854),
        "Altstetten":           (47.38873152342202, 8.47940156739079),
        "City":                 (47.37138258712049, 8.53495017435000),
        "Enge":                 (47.36037645429785, 8.53272762685208),
        "Escher Wyss":          (47.38971927358194, 8.51484575510926),
        "Fluntern":             (47.38212345159577, 8.56213514753654),
        "Gewerbeschule":        (47.38388463813886, 8.53061421052996),
        "Hard":                 (47.38186639358355, 8.51254179635553),
        "Hirslanden":           (47.36276014977589, 8.56805810527094),
        "Hirzenbach":           (47.39839308309126, 8.58330624567168),
        "Hochschulen":          (47.36547968924089, 8.54460224375193),
        "Höngg":                (47.40812106396411, 8.49567358046803),
        "Hottingen":            (47.37755083630196, 8.58243239891855),
        "Langstrasse":          (47.37763850677041, 8.52812648007782),
        "Leimbach":             (47.33147426064787, 8.51072727278173),
        "Lindenhof":            (47.37305924026484, 8.53987336628224),
        "Oerlikon":             (47.40838124870649, 8.54572050197929),
        "Rathaus":              (47.37192975529810, 8.54445530400766),
        "Schwamendingen-Mitte": (47.40263884635722, 8.56664825075389),
        "Seebach":              (47.42389591762455, 8.53959877753388),
        "Wollishofen":          (47.33991307303191, 8.53207644593323),
        "Wipkingen":            (47.39722151402933, 8.52337352770674),
        "Witikon":              (47.35928810284236, 8.59639087269490),
    }