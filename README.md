# Fairestate - Wohnungspreisschätzer der Stadt Zürich
Ein interaktives Tool zur Schätzung von Immobilienpreisen in Zürich basierend auf Lage, Grösse, Zustand und Ausstattung.

---

Dies ist die Gruppenarbeit der Gruppe 05.07.
Abgabedatum: 14.05.2026
Entwickelt als Gruppenprojekt im Rahmen des Kurses FCS-BWL an der Universität St. Gallen (HSG).

Team: Ainhoa Eggenberger, Ella Querner, Janina Stanisic, Philippe Bloch, Marc Scolaro


---

## Projektbeschreibung

**Fairestate** ist eine Streamlit-Webanwendung, die den geschätzten Marktwert von Wohnungen in der Stadt Zürich berechnet. 

Das Tool nutzt:
- Machine Learning (KNN-Modell) zur Basispreisschätzung pro Quartier
- Manuelle Faktoren für individuelle Immobilienmerkmale (Baujahr, Stockwerk, Ausstattung, etc.)
- Interaktive Visualisierungen (Wasserfalldiagramm, Gauge-Chart, Heatmap)

---

## Projektstruktur

CS_Immobilienberechnungsapp_V1/
│
├── app.py                        # Hauptdatei: Eingabeformular, sammelt User-Daten, ruft Features auf & zeigt Ergebnisse
├── bau5156d5155.csv              # Rohdaten von echten Wohnungsverkäufen in Zürich (Quartier, Preis, Grösse, Baujahr etc.)
│
├── feature_berechnung.py         # Preisberechnung  
├── feature_dataset.py            # Lädt & verarbeitet 
├── feature_gauge_chart.py        # Gauge-Chart (Tacho-Diagramm), zeigt visuell ob dein Quartier günstig/teuer ist
├── feature_heatmap_chart.py      # Heatmap-Karte, Quartiere werde farbig eingefärbt (günstig = grün, mittel = orange etc.)
├── feature_Koordinaten.py        # Speichert GPS-Koordinaten der Quartiere (latitude, longitude), damit Karte funktioniert
├── feature_layout.py             # Layout & Styling der App, macht sie schön mit Farben und Designs
├── feature_machine_learning.py   # KNN-Modell Training & Vorhersage, lernt aus alten Verkaufsdaten
├── feature_waterfall_chart.py    # Wasserfalldiagramm (Plotly)
│
├── Immobilienpreisberechner.py   # 
│
├── README.md                     # Diese Datei
└── requirements.txt              # Liste aller Python-Abhängigkeiten

---

### Eingabeformular

Der User gibt folgende Informationen ein:
- Lage: Stadtquartier (Dropdown)
- Grösse: Zimmerzahl, Wohnfläche in m²
- Gebäude: Baujahr, Stockwerk
- Zustand: Neuwertig / Gut gepflegt / Renovationsbedürftig
- Ausstattung: Balkon, Tiefgarage, Lift, Seesicht, Minergie

---

### Preisberechnung
- Basispreis: Machine Learning (KNN) schätzt den Durchschnittspreis pro m² im Quartier
- Faktoren: Anpassungen basierend auf Baujahr, Stockwerk, Zustand, Ausstattung
- Ergebnis: Geschätzter Kaufpreis (CHF) + Preis pro m²

---

### Visualisierungen
- Wasserfalldiagramm: Zeigt, wie sich der Endpreis aus Basispreis + Faktoren zusammensetzt
- Gauge-Chart: Vergleicht den Preis mit anderen Quartieren (günstig/mittel/teuer)
- Heatmap: Interaktive Karte von Zürich mit farblichen Preisunterschieden

---

## Technische Details

### Machine Learning
- Algorithmus: K-Nearest Neighbors (KNN)
- Training: Basierend auf historischen Wohnungsverkaufsdaten aus `bau5156d5155.csv`
- Output: Durchschnittlicher Basispreis pro m² im gewählten Quartier

---

Hochschule: Universität St. Gallen (HSG)  
Kurs: FCS-BWL  
Semester: Frühling 2026

Dieses Projekt ist für akademische Zwecke an der HSG entwickelt worden.

Literaturverzeichnis:

Statistische Quartiere - Stadt Zürich. (n.d.). https://www.stadt-zuerich.ch/geodaten/download/Statistische_Quartiere format=10008
