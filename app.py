"""
data_loader.py
==============
Lädt die Immobiliendaten von der Open Data Zürich API
und speichert sie in einer lokalen SQLite-Datenbank.

Datenquelle:
    Stadt Zürich – Verkaufspreise Stockwerkeigentum nach Zimmerzahl & Stadtquartier
    URL: https://data.stadt-zuerich.ch/dataset/bau_hae_preis_stockwerkeigentum_zimmerzahl_stadtquartier_od5155
"""

import requests
import pandas as pd
import sqlite3
import os

# ─────────────────────────────────────────────
# KONFIGURATION
# ─────────────────────────────────────────────

# Direkte Download-URL des CSV-Datensatzes (Open Data Zürich)
CSV_URL = (
    "https://data.stadt-zuerich.ch/dataset/"
    "bau_hae_preis_stockwerkeigentum_zimmerzahl_stadtquartier_od5155/"
    "download/BAU515OD5155.csv"
)

# Pfad zur lokalen SQLite-Datenbank
DB_PATH = "database.db"

# Name der Tabelle in der Datenbank
TABLE_NAME = "immobilienpreise"


# ─────────────────────────────────────────────
# SCHRITT 1: DATEN VON DER API LADEN
# ─────────────────────────────────────────────

def load_data_from_api() -> pd.DataFrame:
    """
    Lädt die CSV-Daten direkt von der Open Data Zürich API.

    Returns:
        pd.DataFrame: Rohdaten als DataFrame
    
    Raises:
        Exception: Wenn der API-Aufruf fehlschlägt
    """
    print("📡 Lade Daten von Open Data Zürich API...")

    try:
        # HTTP GET-Request zur API
        response = requests.get(CSV_URL, timeout=30)
        response.raise_for_status()  # Fehler werfen, falls Status != 200

        # CSV-Inhalt in einen Pandas DataFrame einlesen
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))

        print(f"✅ Daten erfolgreich geladen: {len(df)} Zeilen, {len(df.columns)} Spalten")
        return df

    except requests.exceptions.RequestException as e:
        print(f"❌ Fehler beim Laden der Daten: {e}")
        raise


# ─────────────────────────────────────────────
# SCHRITT 2: DATEN BEREINIGEN & AUFBEREITEN
# ─────────────────────────────────────────────

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bereinigt und transformiert den Rohdatensatz für die weitere Verarbeitung.

    Spalten im Original-Dataset:
        - Stichtagdatjahr       → Jahr der Erhebung
        - HAArtLevel1Lang       → Art des Handänderung (z.B. "Kauf")
        - HASTWELang            → Typ: Stockwerkeigentum
        - RaumLang              → Stadtquartier / Raum
        - AnzZimmerLevel2Lang   → Zimmerkategorie (z.B. "3 Zimmer")
        - AnzHA                 → Anzahl Handänderungen (Transaktionen)
        - HAPreisWohnflaeche    → Preis pro m² Wohnfläche
        - HAMedianPreis         → Median-Kaufpreis
        - HASumPreis            → Gesamtvolumen aller Käufe

    Returns:
        pd.DataFrame: Bereinigter DataFrame
    """
    print("🔧 Bereinige und transformiere Daten...")

    # Kopie erstellen, um Originaldaten nicht zu verändern
    df = df.copy()

    # ── Spalten umbenennen (deutsch, leserlich) ──
    df = df.rename(columns={
        "Stichtagdatjahr":              "Jahr",
        "HAArtLevel1Lang":              "Handaenderungsart",
        "HASTWELang":                   "Eigentumstyp",
        "RaumLang":                     "Quartier",
        "AnzZimmerLevel2Lang_noDM":     "Zimmerkategorie",
        "AnzHA":                        "Anzahl_Transaktionen",
        "HAPreisWohnflaeche":           "Preis_pro_m2",
        "HAMedianPreis":                "Median_Preis",
        "HASumPreis":                   "Gesamtvolumen",
    })

    # ── Nur relevante Spalten behalten ──
    relevante_spalten = [
        "Jahr", "Handaenderungsart", "Eigentumstyp",
        "Quartier", "Zimmerkategorie",
        "Anzahl_Transaktionen", "Preis_pro_m2",
        "Median_Preis", "Gesamtvolumen"
    ]
    # Nur Spalten nehmen, die auch wirklich im Datensatz existieren
    df = df[[col for col in relevante_spalten if col in df.columns]]

    # ── Numerische Spalten bereinigen ──
    # Manchmal kommen Zahlen als Text mit Leerzeichen oder Hochkomma (z.B. "1'200'000")
    for col in ["Anzahl_Transaktionen", "Preis_pro_m2", "Median_Preis", "Gesamtvolumen"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("'", "", regex=False)   # Tausender-Trennzeichen entfernen
                .str.replace(" ", "", regex=False)   # Leerzeichen entfernen
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")  # In Zahl umwandeln

    # ── Jahr als Integer ──
    if "Jahr" in df.columns:
        df["Jahr"] = pd.to_numeric(df["Jahr"], errors="coerce").astype("Int64")

    # ── Zimmerzahl als numerischen Wert extrahieren ──
    # Beispiel: "3 Zimmer" → 3.0
    if "Zimmerkategorie" in df.columns:
        df["Zimmer_Anzahl"] = (
            df["Zimmerkategorie"]
            .astype(str)
            .str.extract(r"(\d+(?:\.\d+)?)")  # erste Zahl extrahieren
            .astype(float)
        )

    # ── Zeilen ohne Preis entfernen (nicht verwendbar für ML) ──
    df = df.dropna(subset=["Median_Preis"])

    # ── Nur echte Käufe behalten (falls Spalte vorhanden) ──
    if "Handaenderungsart" in df.columns:
        df = df[df["Handaenderungsart"].str.contains("Kauf", na=False, case=False)]

    # ── Index zurücksetzen ──
    df = df.reset_index(drop=True)

    print(f"✅ Bereinigung abgeschlossen: {len(df)} Zeilen nach Filterung")
    return df


# ─────────────────────────────────────────────
# SCHRITT 3: DATEN IN SQLITE-DATENBANK SPEICHERN
# ─────────────────────────────────────────────

def save_to_database(df: pd.DataFrame, db_path: str = DB_PATH) -> None:
    """
    Speichert den bereinigten DataFrame in einer SQLite-Datenbank.
    Falls die Tabelle bereits existiert, wird sie ersetzt (aktualisiert).

    Args:
        df (pd.DataFrame): Bereinigter Datensatz
        db_path (str): Pfad zur SQLite-Datenbankdatei
    """
    print(f"💾 Speichere Daten in Datenbank: {db_path}")

    # Verbindung zur SQLite-Datenbank öffnen (wird neu erstellt, falls nicht vorhanden)
    conn = sqlite3.connect(db_path)

    try:
        # DataFrame direkt in SQLite-Tabelle schreiben
        # if_exists="replace" → Tabelle wird bei jedem Aufruf aktualisiert
        df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
        print(f"✅ {len(df)} Datensätze in Tabelle '{TABLE_NAME}' gespeichert")

    finally:
        # Verbindung immer schliessen, auch bei Fehlern
        conn.close()


# ─────────────────────────────────────────────
# SCHRITT 4: DATEN AUS DATENBANK LADEN
# ─────────────────────────────────────────────

def load_from_database(db_path: str = DB_PATH) -> pd.DataFrame:
    """
    Liest alle Immobiliendaten aus der SQLite-Datenbank.

    Args:
        db_path (str): Pfad zur SQLite-Datenbankdatei

    Returns:
        pd.DataFrame: Alle gespeicherten Immobiliendaten
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(
            f"Datenbank nicht gefunden: {db_path}. "
            "Bitte zuerst initialize_database() aufrufen."
        )

    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", conn)
        return df
    finally:
        conn.close()


def load_filtered(
    db_path: str = DB_PATH,
    quartier: str = None,
    min_zimmer: float = None,
    max_zimmer: float = None,
    min_jahr: int = None,
    max_jahr: int = None,
) -> pd.DataFrame:
    """
    Lädt gefilterte Daten aus der Datenbank.
    Ermöglicht Benutzerinteraktion (Anforderung 4).

    Args:
        quartier (str):     Nur Daten für dieses Quartier
        min_zimmer (float): Minimale Zimmerzahl
        max_zimmer (float): Maximale Zimmerzahl
        min_jahr (int):     Frühestes Jahr
        max_jahr (int):     Spätestes Jahr

    Returns:
        pd.DataFrame: Gefilterter Datensatz
    """
    # Basis-Query
    query = f"SELECT * FROM {TABLE_NAME} WHERE 1=1"
    params = []

    # Filter dynamisch hinzufügen
    if quartier:
        query += " AND Quartier = ?"
        params.append(quartier)
    if min_zimmer is not None:
        query += " AND Zimmer_Anzahl >= ?"
        params.append(min_zimmer)
    if max_zimmer is not None:
        query += " AND Zimmer_Anzahl <= ?"
        params.append(max_zimmer)
    if min_jahr is not None:
        query += " AND Jahr >= ?"
        params.append(min_jahr)
    if max_jahr is not None:
        query += " AND Jahr <= ?"
        params.append(max_jahr)

    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    finally:
        conn.close()


# ─────────────────────────────────────────────
# HAUPTFUNKTION: Alles in einem Schritt
# ─────────────────────────────────────────────

def initialize_database(force_reload: bool = False) -> pd.DataFrame:
    """
    Vollständiger Setup-Prozess:
    1. Prüft ob Datenbank bereits existiert
    2. Falls nicht (oder force_reload=True): lädt von API und speichert
    3. Gibt den bereinigten DataFrame zurück

    Args:
        force_reload (bool): Erzwingt Neuladen von der API

    Returns:
        pd.DataFrame: Bereinigte und gespeicherte Daten
    """
    db_exists = os.path.exists(DB_PATH)

    if db_exists and not force_reload:
        # Datenbank existiert → direkt aus DB laden (schneller)
        print("📂 Datenbank gefunden – lade aus lokaler DB...")
        df = load_from_database()
        print(f"✅ {len(df)} Datensätze aus Datenbank geladen")
        return df
    else:
        # Neu laden von API
        raw_df = load_data_from_api()
        clean_df = clean_data(raw_df)
        save_to_database(clean_df)
        return clean_df


# ─────────────────────────────────────────────
# TEST: Direkt ausführen zum Testen
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Datenbank initialisieren und Daten laden
    df = initialize_database(force_reload=True)

    # Überblick ausgeben
    print("\n📊 Datenübersicht:")
    print(df.head(10).to_string())
    print(f"\nSpalten: {list(df.columns)}")
    print(f"\nQuartiere ({df['Quartier'].nunique()}): {sorted(df['Quartier'].unique())[:10]}")
    print(f"\nJahre: {sorted(df['Jahr'].dropna().unique())}")
    print(f"\nZimmerkategorien: {sorted(df['Zimmerkategorie'].unique())}")
    print(f"\nPreis-Statistik (Median):\n{df['Median_Preis'].describe()}")