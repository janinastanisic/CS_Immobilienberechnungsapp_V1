# Fairestate - Wohnungspreisschätzer der Stadt Zürich
Ein interaktives Tool zur Schätzung von Immobilienpreisen in Zürich basierend auf Lage, Grösse, Zustand und Ausstattung.

---

Dies ist die Gruppenarbeit der Gruppe 05.07.
Abgabedatum: 14.05.2026
Entwickelt als Gruppenprojekt im Rahmen des Kurses FCS-BWL an der Universität St. Gallen (HSG).

Team: Ainhoa Eggenberger, Ella Querner, Janina Stanisic, Philippe Bloch, Marc Scolaro


---

## Projektbeschreibung

Business Case: 
Der Immobilienmarkt ist geprägt von Informationsasymmetrien: Verkäufer und
Makler verfügen über deutlich mehr Marktwissen als Käufer, was zu Fehlbewertungen 
und finanziellen Verlusten führt. Fairestate begegnet diesem Problem mit einem datengetriebenen Ansatz.

App: 
**Fairestate** ist eine interaktive Streamlit-Webanwendung zur Schätzung von Immobilienpreisen in der Stadt Zürich. 
Nutzer geben Eigenschaften ihrer Immobilie ein und erhalten eine datenbasierte Preisschätzung. 
Ein Machine-Learning-Modell berechnet den Basispreis, Korrekturfaktoren passen ihn an die spezifischen Eigenschaften
an. Die Ergebnisse werden in drei visuellen Charts dargestellt.


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
├── feature_heatmap_chart.py      # Heatmap-Karte, Quartiere werden farbig eingefärbt (günstig = grün, mittel = orange etc.)
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
- Ergebnis: Geschätzter Kaufpreis (CHF) und Preis pro m²

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

### Literaturverzeichnis:

Chau, K. W., Wong, S. K., & Yiu, C. Y. (2004). The value of the provision of a balcony in apartments in Hong Kong. Property     Management, 22(3), 250–264. https://doi.org/10.1108/02637470410545020 
Conroy, S., Narwold, A., & Sandy, J. (2013). The value of a floor: valuing floor level in high‐rise condominiums in San Diego. International Journal of Housing Markets and Analysis, 6(2), 197–208. https://doi.org/10.1108/ijhma-01-2012-0003 
Dai, X., Yu, X., Ma, L., & Zheng, P. (2026). The Economic Benefit Evaluation of Elevator Retrofitting: An Empirical Analysis of Second-Hand Housing Price Premiums in Hangzhou’s Older Residential Compounds. Buildings, 16(1), 220. https://doi.org/10.3390/buildings16010220 
Deschermeier, P., Henger, R., Oberst, C., & Institut der deutschen Wirtschaft Köln e. V. (2023). Bedarfe und Preise. In BPD Immobilienentwicklung GmbH, Institut Der Deutschen Wirtschaft Köln E. V. 
Frey, S. (2026, February 4). The impact of property condition on sale price and time on market - Seb Frey, Silicon Valley + Bay Area REALTOR. Seb Frey, Silicon Valley + Bay Area REALTOR. https://sebfrey.com/the-impact-of-property-condition-on-sale-price-and-time-on-market/ 
Kempf, C., & Syz, J. (2022). Why pay for sustainable housing? Decomposing the green premium of the residential property market in the Canton of Zurich, Switzerland. SN Business & Economics, 2(11). https://doi.org/10.1007/s43546-022-00346-8 
Liegenschaftenbewertung 2026. (2026). Kanton Zürich. https://www.zh.ch/de/steuern-finanzen/steuern/steuern-natuerliche-personen/liegenschaftenneubewertung-2026.html 
LV95 in WGS84-Koordinaten umrechnen für Google Maps, OpenStreetMap etc. (2026). zurzach.ag. https://zurzach.ag/liegenschaften/lv95-in-wgs84-koordinaten-fuer-google-maps-oder-openstreetmap-umrechnen-und-konvertieren/ 
Niklowitz, M. (2026, April 18). Seesicht bei Immobilien: Wieviel zahlt man drauf? cash.ch. Retrieved May 7, 2026, from https://www.cash.ch/news/top-news/seesicht-bei-immobilien-wieviel-zahlt-man-drauf-927267 
Open Data Zürich - Stadt Zürich. (n.d.). https://data.stadt-zuerich.ch/dataset/bau_hae_preis_stockwerkeigentum_zimmerzahl_stadtquartier_od5155/resource/72ed5051-4552-4c2e-b761-78ce1d99d094
Statistische Quartiere - Stadt Zürich. (2026, May 8). Stadt Zürich. Retrieved May 9, 2026, from https://www.stadt-zuerich.ch/geodaten/download/Statistische_Quartiere?format=10008


