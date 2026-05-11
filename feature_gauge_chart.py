# =============================================================
# feature_gauge_chart.py – Chart 2: Gauge-Diagramm Marktvergleich
# =============================================================

# ZUSAMMENFASSUNG
# Dieses Feature erstellt einen interaktiven Gauge-Chart mit Plotly,
# der zeigt ob der geschätzte Preis für das gewählte Quartier
# günstig, durchschnittlich oder teuer ist.

# Ablauf:
# 1. ML-Basispreis des gewählten Quartiers als Referenzlinie setzen
# 2. Preisskala aus günstigstem und teuerstem Quartier berechnen
# 3. Drei Zonen einfärben: grün (günstig), gelb (mittel), rot (teuer)
# 4. Berechneten Preis als Zeiger und Delta zum Basispreis anzeigen
# 5. Fertigen Chart zurückgeben für Streamlit

# Bei der Entwicklung dieses Codes wurde Claude AI (Anthropic, 2026) als Hilfsmittel eingesetzt, um Lösungsansätze zu erarbeiten und Fehler zu korrigieren. 
# =============================================================

import plotly.graph_objects as go


# Die Funktion nimmt zwei Parameter entgegen:
# preis_pro_m2: der berechnete Preis aus unserem ML-Modell
# quartier: der vom Nutzer gewählte Stadtquartier-Name
# Sie gibt am Ende eine Plotly-Figur zurück (als Gauge Chart)
def erstelle_gauge_chart(preis_pro_m2, quartier, ml_basispreis, BASISPREIS_PRO_QUARTIER):
    """
    Zeigt ob der geschätzte Preis für das gewählte
    Quartier günstig, durchschnittlich oder teuer ist.
    """
    basispreis  = ml_basispreis                           # ML-Basispreis als Referenzlinie verwenden
    min_preis   = min(BASISPREIS_PRO_QUARTIER.values())   # Günstigstes Quartier im Dictionary suchen
    max_preis   = max(BASISPREIS_PRO_QUARTIER.values())   # Teuerstes Quartier im dictionary suchen

    # Range dynamisch anpassen falls Endpreis die Range überschreitet
    gauge_min = float(min_preis * 0.8)
    gauge_max = float(max(max_preis * 1.1, preis_pro_m2 * 1.1))  # Endpreis wird berücksichtigt

    fig = go.Figure(go.Indicator( #Erstellt einen Plotly-Chart vom Typ Indicator
        mode  = "gauge+number+delta", #Zeigt drei Elemente: Den Halbkreis, die grosse Zahl in der Mitte und die Differenz zum Basispreis
        value = float(preis_pro_m2), #Der berechnete Endpreis der Wohnung, explizit als float
        delta = {
            "reference": float(basispreis), #Vergleichswert: ML-Basispreis
            "increasing": {"color": "#666666"}, #grau wenn teurer als Basispreis
            "decreasing": {"color": "#666666"}, #grau wenn günstiger als Basispreis
            "suffix": " CHF/m2"
        },
        number = {"suffix": " CHF/m²", "font": {"size": 28}}, #Formatiert Zahl mit Einheit und Schriftgrösse
        title = {"text": f"{quartier}: Preis im Vergleich zum Zürcher Markt", #Definiert den Titel mit dynamischem Quartiernamen
                  "font": {"size": 14}},
        gauge  = {
            "axis": {
                "range":     [gauge_min, gauge_max], #Definiert die Range des Gauge Chart: dynamisch angepasst
                "ticksuffix": " CHF", #Einheiten auf der Skala
                "tickfont":   {"size": 11}, #Schriftgrösse der Skala
            },
            "bar":       {"color": "#2563eb"}, #Definiert den blauen Balken
            "steps": [ #Definiert die ranges der Färbung
                {"range": [gauge_min, float(min_preis * 1.1)], "color": "#dcfce7"}, #grün = günstig
                {"range": [float(min_preis * 1.1), float(max_preis * 0.9)], "color": "#fef9c3"}, #gelb = mittel
                {"range": [float(max_preis * 0.9), gauge_max], "color": "#fee2e2"}, #rot = teuer
            ],
            "threshold": {
                "line":  {"color": "#1D9E75", "width": 3}, #Definiert die grüne Linie, 3px breit
                "value": float(basispreis), #Die grüne Linie zeigt den Basispreis
            },
        }
    ))

    fig.update_layout(
        plot_bgcolor  = "white", #Weisser Hintergrund des Charts
        paper_bgcolor = "white", #Weisser Hintergrund der ganzen Figur
        height        = 300, #Pixel
        margin        = dict(t=80, b=20, l=40, r=40), #Abstände zu den Seiten
    )
    return fig