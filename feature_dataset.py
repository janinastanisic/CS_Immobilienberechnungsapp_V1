# =============================================================
# feature_dataset.py – Datenladen und Datenbankanbindung
# =============================================================

# ZUSAMMENFASSUNG
# Dieses Feature lädt die Immobilienpreisdaten der Stadt Zürich
# und speichert sie lokal in einer SQLite-Datenbank, damit das
# CSV nicht bei jedem Start neu geladen werden muss.

# Ablauf:
# 1. Beim ersten Start: Datenset wird geladen, Spalten umbenannt,
#    irrelevante und Quartiere (kreise, "Ganze Stadt") gefiltert --> wollen uns nicht auf Kreise fokusieren sondern nur auf Bezirk, weil die bezirke innerhalb der Kreise sich preislich unterscheiden --> wäre weniger präzise
#    und in immobilien.db gespeichert
# 2. Ab dem zweiten Start: Daten werden direkt aus der lokalen
#    Datenbank gelesen nicht mehr von bau515od5155.csv
# 3. Rückgabe: DataFrame mit Spalten Jahr, Quartier,
#    Zimmer, Preis_pro_m2

# Bei der Entwicklung dieses Codes wurde Claude AI (Anthropic, 2026) als Hilfsmittel eingesetzt, um Lösungsansätze zu erarbeiten und Fehler zu korrigieren. 
# =============================================================

# Lädt das CSV Format des Datensets, umbennen der Spalten des Datensets --> erleichtert die Arbeit mit dem Set
import pandas as pd #Werkzeugpaket für Tabellen-Daten
import sqlite3 #Dadurch kann man eine lokale Datenbank-Datei erstellen
import os #Um zu prüfen, ob eine Datei bereits existiert


CSV_URL = "bau515od5155.csv"
#Diese Variable speichert den Link zu unserem Datenset
DB_PATH = "immobilien.db" #Erster Durchlauf: bau515od5155.csv laden und in immobilien.db speichern
#Zweiter Durchlauf: immobilien.db wird direkt gelesen
#immobilien.db = Dateiname unserer lokalen Datenbank
#Erstellt beim ersten Durchlauf des Codes die Datei automatisch --> speichert Daten aus dem CSV
# --> so wird es gespeichert



#Funktion 1#:
def daten_laden(): #Definition der Funktion daten_laden
    df=pd.read_csv(CSV_URL) 
    #Unser Datenset wird eingelesen und in einen Dataframe (Tabelle) verwandelt. 
    #Diese Tabelle wird in df (für Dataframe) gespeichert

    print(list(df.columns))  # zeigt die spaltennamen im Log 

    df = df.rename(columns={        # NEU: Umbenennen der Spaltennamen, damit sie einfacher zu handhaben sind
        "Stichtagdatjahr":     "Jahr",      
        "RaumLang":            "Quartier",
        "AnzZimmerLevel2Lang_noDM":  "Zimmer",
        "HAPreisWohnflaeche":  "Preis_pro_m2",   
    })
    #Benennt die Spaltennamen von unserem Datenset um --> einfacher für uns, um unseren Code zu lesen und verstehen

    spalten= ["Jahr", "Quartier", "Zimmer", "Preis_pro_m2"]
    df=df[spalten]
    #Fokus nur auf für uns relevante Spalten, die anderen von unserem Datenset werden so aussortiert
    #So werden nur diese Spalten in unserem DataFrame übernommen
  
    df = df[~df["Quartier"].str.contains("Kreis|Ganze Stadt", na=False)]
    # Kreise und "Ganze Stadt" herausfiltern, nur Bezirke behalten --> Nur Bezirke ist präziser als Kreise weil z.B. Kreis 2 aus Leimbach, Wollishofen und Enge bestehen, welche sich alle preislich unterscheiden

    df["Jahr"]=df["Jahr"].astype(int)
    df["Preis_pro_m2"] = df["Preis_pro_m2"].astype(float)

    #Anpassung gewisser Datentypen, weil CSV oft alles als String laden
    #Anpassung nötig für die Rechnungen 

    speichere_in_datenbank(df)
    return(df)
   
    #Ruft Funktion 2 auf und speichert so die Daten, return gibt den fertigen df zurück
    #So müsste man eine saubere Tabelle zurück bekommen


 #Funktion 2: 
def speichere_in_datenbank(df): #Defintion der neuen Funktion, df als Parameter
    conn = sqlite3.connect(DB_PATH)
    #conn = connection --> öffnet eine Verbindung zur Datenbankdatei immobilien.db
    df.to_sql("immobilienpreise", conn, if_exists="replace", index=False)
    #Schreibt kompletten DataFrame als Tabelle in die Datenbank
    #"immobilienpreise" ist der name dieser Tabelle
    #if_exits="replace" bedeutet: Falls die Tabelle schon existiert, überschrieben
    #index=false verhindert dass panda eine unnötige Nummerierungsspalte mitspeichert
    conn.close()
    #Schliesst die Verbindung zur Datenbank --> wichtig falls mehrere Teile darauf zugreifen wollen

#Funktion 3: 
def lade_aus_datenbank(): #Liest die Daten aus der lokalen Datenbank --> so muss CVS nicht immer neu vob bau515od5155.csv eingelesen werden
    conn = sqlite3.connect(DB_PATH)
    #Öffnet Verbindung zur Datenbank
    df = pd.read_sql("SELECT * FROM immobilienpreise", conn)
    #SQL-Abfrage --> verwandelt das Ergebnis direkt in einen DataFrame
    conn.close()
    #Verbindung schliessen
    return df


#Funktion 4: #Hauptfunktion --> muss in app.py integriert werden
def get_daten():
    if os.path.exists(DB_PATH):
        return lade_aus_datenbank()
    else:
        return daten_laden()
    # os.path.exists(DB_PATH) gibt True zurück wenn die Datei immobilien.db bereits existiert, 
    #Sonst False. Die Logik: beim allerersten Start existiert die Datenbank noch nicht
    #wir laden das CSV und speichern es. Ab dem zweiten Start existiert die Datei 
    #wir lesen einfach lokal. So wird bau515od5155.csv nur einmal verwendet