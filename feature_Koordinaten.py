# Mittelpunkt-Koordinaten der Züricher Quartiere
# Quelle: https://www.stadt-zuerich.ch/geodaten/download/Statistische_Quartiere?format=10008
#LV59 in WGS84-Koordinaten Umrechner: https://zurzach.ag/liegenschaften/lv95-in-wgs84-koordinaten-fuer-google-maps-oder-openstreetmap-umrechnen-und-konvertieren/
#Wir benutzen hardcodierte Daten weil der CSV link nicht funktioniert da die Stadt Zuerich hoechstwahrscheinlich den Zugriff blockiert hat
#Wir haben probiert die Daten herunterzuladen und manuell abzuspeichern, aber die Daten haben keine Lat/Lon Spalten sondern nur geometry mit POLYGON Koordinaten 

def get_koordinaten():
    return {
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
        "Hoengg":               (47.40812106396411, 8.49567358046803),
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