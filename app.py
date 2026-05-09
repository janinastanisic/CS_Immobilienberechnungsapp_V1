# =============================================================
# app.py – Fairestate: Wohnungspreisschätzer der Stadt Zürich
# Ausführen im Terminal: streamlit run app.py
# =============================================================

# ZUSAMMENFASSUNG
# Dies ist die Hauptdatei der Streamlit-App. Sie verbindet alle
# Features und steuert die Benutzeroberfläche.

# Ablauf:
# 1. Daten und ML-Modell werden einmalig beim Start geladen
# 2. User gibt Eigenschaften der Immobilie ein (Lage, Grösse,
#    Gebäude, Zustand, Ausstattung)
# 3. Auf Knopfdruck wird berechne_preis() aufgerufen
# 4. Ergebnis wird als Kennzahlen und drei Charts angezeigt:
#    Waterfall (Preiszusammensetzung), Gauge (Marktvergleich),
#    Heatmap (Preisübersicht Zürich)
# 5. Ergebnisse bleiben via Session State sichtbar

# Bei der Entwicklung dieses Codes wurde Claude AI (Anthropic, 2026) als Hilfsmittel eingesetzt, um Lösungsansätze zu erarbeiten und Fehler zu korrigieren. 
# =============================================================

import streamlit as st #importiert das Framework Streamlit, mit der Abkürzung st
import plotly.graph_objects as go #importiert eine Bibliothek für interaktive Diagramme mit der low-level Variante go
import folium #importiert interaktive Landkarten
from streamlit_folium import st_folium #Bindeglied, damit die Karte in Streamlit angezeigt werden kann
from feature_dataset import get_daten #importiert get_daten vom Dataset Feature
from feature_Koordinaten import get_koordinaten #importiert get_koordinaten von Koordinaten Feature
from feature_heatmap_chart import erstelle_heatmap_karte #importiert die Funktion erstelle_heatmap_karte von feature_heatmap_chart, welche die Heatmap Karte erstellt
from feature_machine_learning import trainiere_knn_modell, ml_basispreis_schaetzen #importiert die Funktion trainiere_knn_modell vom feature_achine_learning
from feature_waterfall_chart import erstelle_waterfall_chart #importiert die Funktion erstelle_waterfall_chart von feature_waterfall_chart, welche das Wasserfalldiagramm erstellt
from feature_gauge_chart import erstelle_gauge_chart #importiert die Funktion erstelle_gauge_chart von feature_gauge_chart, welche das Gauge Diagramm erstellt
from feature_berechnung import berechne_preis, FAKTOR_ZUSTAND, FAKTOR_STOCKWERK, AUSSTATTUNG_FAKTOREN #Importiert die Funktion berechne_preis mit verschiedenen Faktoren von dem feature_berechnung

st.set_page_config(
    page_title="Fairestate - Wohnungspreisschätzer der Stadt Zürich", #Setzt den Titel im Browser
    layout="centered" #zentriert das layout auf streamlit mittig
)

# =============================================
# BASISPREISE PRO QUARTIER (CHF pro m²)
# =============================================
df= get_daten()
#Daten werden einmalig geladen (aus Feature Dataset.py)
BASISPREIS_PRO_QUARTIER = (
    df.groupby("Quartier")["Preis_pro_m2"]
    .mean()
    .round()
    .astype(int)
    .to_dict()
)

#ML-Modell wird beim start einmalig trainiert
knn_modell, knn_le, _, _, _ = trainiere_knn_modell(df)

# =============================================
# KOORDINATEN DER QUARTIERE (Mittelpunkte)
# =============================================

QUARTIER_KOORDINATEN = get_koordinaten() #Die Funktion get_Koordinaten wird aufgerufen (welche die Koordinaten aller Zürcher Quartiere enthält) und in der Variabel QUARTIER_KOORDINATEN abgespeichert.


# =============================================================
# STREAMLIT APP
# =============================================================

st.title("Fairestate - Wohnungspreisschätzer der Stadt Zürich") #Erstellt den Titel in Streamlit
st.write("Gib die Eigenschaften deiner Immobilie ein - wir berechnen den geschätzten Marktwert.") #Erstellt den Beschreibungstext in Streamlit
st.markdown("---") #Erstellt eine horizontale Trennlinie in Streamlit

# ── 1. LAGE ──
st.subheader("Lage") #Erstellt einen Untertitel in Streamlit
QUARTIERE = ["— Bitte wählen —"] + sorted(BASISPREIS_PRO_QUARTIER.keys()) #Zwei Listen werden erstellt und miteinander verbunden. Die erste besteht aus dem Platzhalter: Bitte wählen. Die zweite Liste besteht aus allen Schlüsseln (Quartiernamen) des Dictionaries, welche alphabetisch sortiert werden.
quartier  = st.selectbox("In welchem Stadtquartier liegt die Immobilie?", options=QUARTIERE) #Ein Dropdown Menü wird in Streamlit erstellt mit einem Beschriftungstext. Das Dropdown Menu beinhaltet eine Liste aller Optionen, die in der vorherigen Zeile definiert wurde. 

# ── 2. GRÖSSE ──
st.subheader("Grösse") #Erstellt einen Untertitel in Streamlit
col1, col2 = st.columns(2) #Die Seite wird in zwei gleich breite Spalten aufgeteilt. col1 links und col2 rechts.
with col1: #Definiert, was in der linken Spalte angezeigt wird
    zimmerzahl = st.selectbox( #Erstellt ein Dropdown Menü und speichert den Eingabewert unter zimmerzahl ab
        "Anzahl Zimmer", #Definiert den Text über dem Dropdown Menu
        options=["1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5+"], #Beschreibt die Liste aller auswählbaren Optionen
        index=0 #Definiert den Standardwert bei Index 0 --> 1 Zimmer
    )
with col2: #Definiert, was in der rechten Spalte angezeigt wird
    wohnflaeche = st.number_input( #Erstellt ein Eingabefeld und speichert den Eingabewert unter wohnflaeche
        "Wohnfläche (m2)", min_value=10, max_value=500, value=10, step=5 #Definiert die kleinste erlaubte Zahl, die grösste erlaubte Zahl, den Standardwert und die Steps (wenn man auf + klickt, springt die Zahl um diesen Wert)
    )

# ── 3. GEBÄUDE ──
st.subheader("Gebäude") #Erstellt einen Untertitel in Streamlit
col3, col4 = st.columns(2) #Die Seite wird in zwei gleich breite Spalten aufgeteilt. col3 links und col4 rechts.
with col3: #Definiert die linke Seite
    baujahr = st.slider("Baujahr", min_value=1900, max_value=2026, value=2026) #Erstellt einen Schieberegler in Streamlit mit dem Beschriftungstext, dem Mindestwert, dem Maximalwert und dem Standardwert und speichert den Eingabewert unter baujahr ab
with col4: #Definiert die rechte Seite
    stockwerk = st.selectbox( #Erstellt ein Dropdown Menu und speichert den Eingabewert unter stockwerk ab
        "Stockwerk", #Definiert den Text über dem Dropdown Menü
        options=[ #Beschreibt die Liste aller auswählbaren Optionen, Erdgeschoss wird mit index 0 als Stadardwert gezeigt
            "Erdgeschoss", "1. Obergeschoss", "2. Obergeschoss",
            "3. Obergeschoss", "4. Obergeschoss",
            "5. Obergeschoss", "6. Obergeschoss",
            "7. Obergeschoss", "8. Obergeschoss",
            "9. Obergeschoss", "10. Obergeschoss oder höher"
        ]
    )

# ── 4. ZUSTAND ──
st.subheader("Zustand") #Erstellt einen Untertitel in Streamlit
zustand = st.radio( #Erstellt buttons, von denen der User eine Option wählen kann
    "Wie ist der aktuelle Renovationsstand?", #Definiert den Text über den Buttons
    options=["Neuwertig / Neubau", "Gut gepflegt", "Renovationsbedürftig"], #Definiert die Liste aller auswählbaren Optionen
    index=1, #Setzt Gut gepflegt als Standardwert
    horizontal=True #Formatiert die Buttons horizontal, also nebeneinander
)

# ── 5. AUSSTATTUNG ──
st.subheader("Ausstattung") #Erstellt einen Untertitel in Streamlit
col5, col6 = st.columns(2) #Die Seite wird in zwei gleich breite Spalten aufgeteilt. col5 links und col6 rechts
with col5: #Definiert die linke Seite
    hat_balkon    = st.checkbox("Balkon / Terrasse") #Erstellt Checkboxen, welche den Wert als True speichert, wenn die Checkbox aktiviert wurde und als False, wenn sie nicht aktiviert wurde. Die Standardwerte sind False
    hat_tiefgarage = st.checkbox("Tiefgarage")
    hat_lift      = st.checkbox("Lift im Gebäude")
with col6:
    hat_seesicht = st.checkbox("Seesicht / Aussicht")
    hat_minergie = st.checkbox("Minergie-Standard") #Erstellt Checkboxen, welche den Wert als True speichert, wenn die Checkbox aktiviert wurde und als False, wenn sie nicht aktiviert wurde. Die Standardwerte sind False

# ── 6. BERECHNUNG & ERGEBNIS ──
st.markdown("---") #Erstellt eine horizontale Trennlinie in Streamlit
berechnen = st.button("Marktwert berechnen") #Erstellt einen Button mit dem Text Marktwert berechnen, wenn der Button angeglickt wird, wird der Wert True in der variable berechnen gespeichert. Ansonsten False

# Session State initialisieren – speichert Ergebnisse über Neuladen hinweg. Erstellt leeren Platz für Ergebnis beim Start der App. Wird päter mit dem berechneten Preis überschrieben, sobald User auf Marktwert berechnen klickt.
if "ergebnis" not in st.session_state:
    st.session_state.ergebnis = None

if berechnen: #Sofern der Button Marktwert berechnen geklickt wurde, ist diese if-Bedingung true
    if quartier == "— Bitte wählen —":
        st.error("Bitte wähle ein Stadtquartier aus.") #Erstellt eine Fehlermeldung mit dem Text Bitte wähle ein Stadtquartier aus, wenn bei quartier nichts angewählt wurde
    else:
        ausstattung = {
            "hat_balkon":    hat_balkon,
            "hat_tiefgarage": hat_tiefgarage,
            "hat_lift":      hat_lift,
            "hat_seesicht":  hat_seesicht,
            "hat_minergie":  hat_minergie, #Wenn die obige if Bedingung nicht erfüllt ist, werden alle Ausstattungswerte, welche angegeben wurden, in einem Dictionary zusammengefasst
        }

        preis_pro_m2, gesamtpreis, faktoren = berechne_preis( #Ruft die Funktion berechne_preis aus dem feature_berechnung auf und bekommt alle Inputs des Users mitgegeben. Die Funktion gibt die Werte preis_pro_m2, gesamtpreis und faktoren zürich. Diese Werte werden später für die Anzeige und die Charts verwendet.
            quartier, zimmerzahl, wohnflaeche,
            baujahr, stockwerk, zustand, ausstattung, 
            knn_modell,knn_le, BASISPREIS_PRO_QUARTIER
        )

        # Ergebnis im Session State speichern
        st.session_state.ergebnis = { #überschreibt das none im session state mit den berechneten und eingegebenen Werten
            "preis_pro_m2": preis_pro_m2,
            "gesamtpreis":  gesamtpreis,
            "faktoren":     faktoren,
            "quartier":     quartier,
            "ml_basispreis": faktoren["Basispreis (Quartier)"],
        }

# Ergebnis anzeigen – bleibt sichtbar solange session_state gefüllt ist: Sofern Ergebnisse im Session state abgespeichert wurden, wird eine Kurzform für session state definiert (e)
if st.session_state.ergebnis:
    e = st.session_state.ergebnis

    st.markdown("### Geschätzter Marktwert") #Erstellt einen mittelgrossen Titel in Streamlit
    col_r1, col_r2 = st.columns(2) #Die Seite wird in zwei gleich breite Spalten aufgeteilt. col_r1 links und col_r2 rechts
    with col_r1: #Definiert die linke Seite
        st.metric( #Formatiert die nächsten Zeilen als Kennzahlen (Kleiner Text + Grosse Zahl)
            label="Geschätzter Kaufpreis", #Kleiner Text
            value=f"CHF {e['gesamtpreis']:,.0f}".replace(",", "'") #Grosse Zahl, die berechnet wurde. e['gesamtpreis'] holt den Gesamtpreis aus dem Session State Dictionary. ,.0f: Zahl wird mit Tausendertrennzeichen und ohne Nachkommastellen dargestellt. ",", "'": Tausendertrennzeichen , werden durch ' ersetzt
        )
    with col_r2: #Definiert die rechte Seite
        st.metric(#Formatiert die nächsten Zeilen als Kennzahlen (Kleiner Text + Grosse Zahl)
            label="Preis pro m2", #Kleiner Text
            value=f"CHF {e['preis_pro_m2']:,.0f}".replace(",", "'") #Grosse Zahl, die berechnet wurde. e['preis_pro_m2'] holt den preis pro m2 aus dem Session State Dictionary. ,.0f: Zahl wird mit Tausendertrennzeichen und ohne Nachkommastellen dargestellt. ",", "'": Tausendertrennzeichen , werden durch ' ersetzt
        )

    st.markdown("---") #Erstellt eine horizontale Trennlinie in Streamlit

 

    # Chart 1: Waterfall
    st.markdown("### Preiszusammensetzung – Schritt für Schritt") # Streamlit Funktion, zeigt formatierten Text an, ### definiert die größe der Überschrift
    st.caption("Wie sich der Endpreis aus dem Basispreis und den einzelnen Faktoren aufbaut.") #Streamlit Funktion, zeigt formatierten Text an, hier als Erklärungstext zum Chart
    fig_waterfall = erstelle_waterfall_chart(e["faktoren"], e["preis_pro_m2"]) # Python Funktionsaufruf
    st.plotly_chart(fig_waterfall, width="stretch") # Streamlit Funktion, zeigt das Diagramm an, welches in der vorherigen Zeile erstellt wurde.

    # Chart 2: Gauge
    st.markdown("### Preis im Marktvergleich") # Streamlit Funktion, zeigt formatierten Text an, ### definiert die größe der Überschrift
    st.caption(
        f"Der grüne Strich zeigt den Basispreis für {e['quartier']}. "
        "Die farbigen Zonen zeigen günstig (grün), mittel (gelb) und teuer (rot) im Vergleich zu allen Zürcher Quartieren."
    )
    fig_gauge = erstelle_gauge_chart(e["preis_pro_m2"], e["quartier"], e["ml_basispreis"], BASISPREIS_PRO_QUARTIER) # Python Dictionary Zugriff
    st.plotly_chart(fig_gauge, width="stretch") #width = stretch sorgt dafür, dass das Diagramm die gesamte Breite der Seite einnimmt.

    # Chart 3: Heatmap
    st.markdown("### Preisübersicht Zürich – Heatmap") # Streamlit Funktion, zeigt formatierten Text an, ### definiert die größe der Überschrift
    st.caption(                                        # Zeigt formatierten Text an, hier als Erklärungstext zum Chart
        "Grün = günstigere Quartiere, Rot = teurere Quartiere. "
        "Ihr Quartier ist dunkel umrandet."
    )

    karte = erstelle_heatmap_karte(ausgewaehltes_quartier=e["quartier"], quartier_koordinaten=QUARTIER_KOORDINATEN, basispreis_pro_quartier=BASISPREIS_PRO_QUARTIER)
        # Erstelle eine Heatmap-Karte, die alle Quartiere in Zürich farblich darstellt
        # Parameter:
        # - ausgewaehltes_quartier=e["quartier"]: Das aktuell gewählte Quartier wird hervorgehoben
        # - quartier_koordinaten=QUARTIER_KOORDINATEN: Die GPS-Koordinaten aller Quartiere
    st_folium(karte, use_container_width=True, height=450)
        # Zeige die Karte in der Streamlit-App an
        # Parameter:
        # - use_container_width=True: Die Karte nutzt die volle Breite des Containers
        # - height=450: Die Karte wird 450 Pixel hoch dargestellt