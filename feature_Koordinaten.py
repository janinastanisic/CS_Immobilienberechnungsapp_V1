#in diesem feature laden wir die Koordinaten fuer die Quartiere der Stadt Zuerich und laden sie wie bei feature_dataset in eine lokale datenbank 
import pandas as pd
import sqlite3 
import os
import requests #brauchen wir neu hier wil es um GeoJSON Daten geht !!!hinzufuegen zu requirements.txt!!!

GEO_URL = "https://www.ogd.stadt-zuerich.ch/wfs/geoportal/Statistische_Quartiere?service=WFS&version=1.1.0&request=GetFeature&outputFormat=GeoJSON&typename=adm_statistische_quartiere_map"
#link zum Datensatz der Stadt Zuerich

DB_PATH = "immobilien.db" 
#speichern es in der gleichen Datenbank wie beim feature_dataset --> nur eine Datenbank aber sozusagen jetzt mit 2 getrennten Tabellen
#eine Datenbank macht unserer code uebersichtlicher und vereinfachert hoffentlich unser coding


#/Funktion 1: 
#gleich wie beim feature_dataset --> daten/Koordinaten werden hier vom Internet geladen
#die Funktion berechnet den Mittelpunkt (Centroid) von jedem Quartier
def lade_koordinaten():
    antwort = requests.get(GEO_URL) #besser fragen
    daten = antwort.json() # besser fragen
    zeilen = [] #Leere Liste definiert

#Mit der for clause koennen wir den Mittelpunkt berechnen. 
#Wir berechnen den Durchschnitt alles Laengen- und Breitengraden
#Dieser Mittelpunkt wird auch "Centroid" genannt (geographischer Mittelpunkt eines Quartiers)
    for feature in daten["features"]:
        name = feature["properties"]["qname"]
        koordinaten = feature["geometry"]["coordinates"][0]
        alle_lon = [punkt[0] for punkt in koordinaten] #Laengengrade
        alle_lat = [punkt[1] for punkt in koordinaten] #Breitengrade
        mittelpunkt_lat = sum(alle_lat) / len(alle_lat)
        mittelpunkt_lon = sum(alle_lon) / len(alle_lon)
        zeilen.append({
            "Quartier": name,
            "Lat":      round(mittelpunkt_lat, 4),
            "Lon":      round(mittelpunkt_lon, 4)
        })

    df_geo = pd.DataFrame(zeilen) #verwandlung in ein dataframe
    speichere_koordinaten_in_datenbank(df_geo) #siehe naechste Funktion 
    return df_geo


#/Funktion 2: #gehoert sozusagen zu Funktion 1 (siehe Zeile 40) macht es meiner Meinung nach ein wenig uebersichtlicher

def speichere_koordinaten_in_datenbank(df_geo):
    conn = sqlite3.connect(DB_PATH) 
    df_geo.to_sql("quartier_koordinaten", conn, if_exists="replace", index=False)
    conn.close()
  #Schreibt kompletten DataFrame als Tabelle in die Datenbank. 
    #"quartier_koordinaten" ist der name dieser Tabelle
    #if_exits="replace" bedeutt: Falls die tabelle schon existiert, ueberschrieben
    #index=false verhindert dass panda eine unnoetige Nummerierungsspalte mitspeichert

#/Funktion 3: 

def lade_koordinaten_aus_datenbank():
    conn = sqlite3.connect(DB_PATH)
    df_geo = pd.read_sql("""
        SELECT Quartier, Lat, Lon
        FROM quartier_koordinaten
        ORDER BY Quartier ASC
    """, conn)
    conn.close()
    return df_geo


#/Funktion 4: Hauptfunktion: benutzt lokale DB falls vorhanden, sonst wird sie vom Internet geladen
def get_koordinaten():
    conn = sqlite3.connect(DB_PATH)
    tabelle_existiert = pd.read_sql("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name='quartier_koordinaten'
    """, conn)
    conn.close()
    #prueft ob die Tabelle schon existiert

    if len(tabelle_existiert) > 0:
        return lade_koordinaten_aus_datenbank()
    else:
        return lade_koordinaten()