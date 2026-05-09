# 🏘️ Fairestate - Wohnungspreisschätzer der Stadt Zürich
Ein interaktives Tool zur Schätzung von Immobilienpreisen in Zürich basierend auf Lage, Grösse, Zustand und Ausstattung.

---

Dies ist die Gruppenarbeit der Gruppe 05.07.
Abgabedatum: 14.05.2026
Entwickelt als Gruppenprojekt im Rahmen des Kurses **FCS-BWL** an der **Universität St. Gallen (HSG)**.

Team: Ainhoa Eggenberger, Ella Querner, Janina Stanisic, Philippe Bloch, Marc Scolaro


---

## 📋 Projektbeschreibung

**Fairestate** ist eine Streamlit-Webanwendung, die den geschätzten Marktwert von Wohnungen in der Stadt Zürich berechnet. Das Tool nutzt:
- **Machine Learning (KNN-Modell)** zur Basispreisschätzung pro Quartier
- **Manuelle Faktoren** für individuelle Immobilienmerkmale (Baujahr, Stockwerk, Ausstattung, etc.)
- **Interaktive Visualisierungen** (Wasserfalldiagramm, Gauge-Chart, Heatmap)

---

## Projektstruktur

CS_Immobilienberechnungsapp_V1/
│
├── app.py                           # Hauptdatei (UI & Logik der Streamlit-App)
├── bau5156d5155.csv                 # Rohdaten (Immobilienpreise Zürich)
│
├── feature_berechnung.py            # Preisberechnung mit Faktoren
├── feature_dataset.py               # Lädt & verarbeitet Immobiliendaten
├── feature_gauge_chart.py           # Gauge-Chart (Tacho-Diagramm)
├── feature_heatmap_chart.py         # Heatmap-Karte (Folium)
├── feature_Koordinaten.py           # GPS-Koordinaten der Quartiere
├── feature_layout.py                # Layout & Styling der App
├── feature_machine_learning.py      # KNN-Modell Training & Vorhersage
├── feature_waterfall_chart.py       # Wasserfalldiagramm (Plotly)
│
├── Immobilienpreisberechner.py      # [Optional: Legacy/Alternative Version?]
│
├── README.md                        # Diese Datei
└── requirements.txt                 # Liste aller Python-Abhängigkeiten

---

### 1️⃣ Eingabeformular

Der User gibt folgende Informationen ein:
- **Lage:** Stadtquartier (Dropdown)
- **Grösse:** Zimmerzahl, Wohnfläche in m²
- **Gebäude:** Baujahr, Stockwerk
- **Zustand:** Neuwertig / Gut gepflegt / Renovationsbedürftig
- **Ausstattung:** Balkon, Tiefgarage, Lift, Seesicht, Minergie

---

### 2️⃣ Preisberechnung
- **Basispreis:** Machine Learning (KNN) schätzt den Durchschnittspreis pro m² im Quartier
- **Faktoren:** Anpassungen basierend auf Baujahr, Stockwerk, Zustand, Ausstattung
- **Ergebnis:** Geschätzter Kaufpreis (CHF) + Preis pro m²

---

### 3️⃣ Visualisierungen
- **Wasserfalldiagramm:** Zeigt, wie sich der Endpreis aus Basispreis + Faktoren zusammensetzt
- **Gauge-Chart:** Vergleicht den Preis mit anderen Quartieren (günstig/mittel/teuer)
- **Heatmap:** Interaktive Karte von Zürich mit farblichen Preisunterschieden

---

## 🧠 Technische Details

### Machine Learning
- **Algorithmus:** K-Nearest Neighbors (KNN)
- **Training:** Basierend auf historischen Immobiliendaten aus `bau5156d5155.csv`
- **Output:** Durchschnittlicher Basispreis pro m² im gewählten Quartier

---

**Hochschule:** Universität St. Gallen (HSG)  
**Kurs:** FCS-BWL  
**Semester:** Frühling 2026

Dieses Projekt ist für akademische Zwecke an der HSG entwickelt worden.