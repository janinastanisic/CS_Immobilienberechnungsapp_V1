# ─────────────────────────────────────────────────────────────
# CHART 1b: WATERFALL – Zusammensetzung des Preises
# erhöht (grün) oder senkt (rot) – mit korrektem Vorzeichen.
# ─────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# ZUSAMMENFASSUNG

# Diese Funktion erstellt einen interaktiven Waterfall-Chart mit Plotly.
# Sie zeigt wie sich der Immobilienpreis (CHF/m²) aus einzelnen Faktoren
# zusammensetzt – von der Lage als Startpunkt bis zum Endpreis.

# Ablauf:
# 1. Basispreis (Lage) als Startpunkt setzen
# 2. Jeden Faktor (Zimmerzahl, Zustand, etc.) einzeln durchgehen
# 3. CHF-Beitrag pro Faktor berechnen (vorher vs. nachher)
# 4. Balken grün = preiserhöhend, rot = preissenkend
# 5. Fertigen Chart zurückgeben für Streamlit

# Design und Visualisierung wurden mit Unterstützung von Claude AI (Anthropic)
# umgesetzt, da professionelles Chart-Design unsere aktuellen
# Fähigkeiten übersteigt.
# ─────────────────────────────────────────────────────────────


import plotly.graph_objects as go 
# import lädt eine externe Bibliothek (hier Plotly-Bibliothek) in den Code. Plotly is eine Bib die Erstellung von Diagrammen, insbesondere hier für das Wasserfall-Diagramm.
# Plotly ist eine leistungsstarke Bibliothek zur Erstellung interaktiver Diagramme in Python. Hier verwenden wir sie, um ein Wasserfall-Diagramm zu erstellen, das die Zusammensetzung des Preises zeigt.
# go ist der Spitzname für plotly.graph_objects, eine Unterbibliothek von Plotly, die es ermöglicht, komplexe Diagramme zu erstellen. Wir verwenden go.Waterfall, um das Wasserfall-Diagramm zu erstellen.

    # Funktion definieren mit def erstelle_waterfall_chart(faktoren, preis_pro_m2), die ein Wasserfall-Diagramm erstellt. Sie nimmt zwei Parameter:
    # Parameter 1. faktoren (dict), dictionary, eine Sammlung von Key Value Paaren und 
    # Parameter 2. preis_pro_m2 (int), eine ganze Zahl (kein Komma).

def erstelle_waterfall_chart(faktoren, preis_pro_m2):       
    
    # Docstring unten beschreibt die Funktion, ihre Parameter und was sie tut. 
    # Es ist eine gute Praxis, Funktionen mit einem Docstring zu dokumentieren, damit andere Coder verstehen, was die Funktion macht und wie man sie verwenden soll.
    """                                                                    
    Zeigt den Aufbau des Preises als Wasserfall-Diagramm.
    Jeder Balken zeigt den CHF-Beitrag eines Faktors.
    Grün = preiserhöhend, Rot = preissenkend.

    Parameter:
        faktoren    (dict): Multiplikatoren aus berechne_preis()
        preis_pro_m2 (int): Endpreis pro m² aus berechne_preis()
    """


    basispreis = faktoren["Basispreis (Quartier)"]  
    # Der Basispreis repräsentiert CHF/m2 des Quartiers
    # Es wird auf das dictionary "faktoren" zugegriffen und den Wert zum Key "Basispreis (Quartier)" rausgeholt. 
    # Dieser Wert hängt nur von der Lage ab – noch ohne Korrekturen wie Zimmerzahl oder Zustand.
    
    # 5 Faktoren, aus dem grossen dictionary rausgenommen und in ein kleineres dictionary namens faktor_map gepackt.
    # Kurz gesagt, faktoren = alles, und faktor_map = nur die 5 Multiplikatoren, die den Preis beeinflussen.
    faktor_map = {
        "Zimmerzahl":  faktoren["Zimmerzahl"],
        "Zustand":     faktoren["Zustand"],
        "Stockwerk":   faktoren["Stockwerk"],
        "Baujahr":     faktoren["Baujahr"],
        "Ausstattung": faktoren["Ausstattung"],
    }


    # --> CHF-Beitrag jedes Faktors berechnen
    # Logik: Wie viel CHF/m2 kommt durch diesen Faktor dazu oder weg?
    # Basispreis wird schrittweise mit jedem Faktor multipliziert.
    # Der Unterschied zum vorherigen Schritt = Beitrag dieses Faktors.

    # zum Beispiel:
    #   Basispreis:          12'000.-
    #   × Zimmer (1.02):     12'240.-  --> +240 CHF/m2
    #   × Zustand (1.10):    13'464.-  --> +1'224 CHF/m2
    #   × Baujahr (0.95):    12'791.-  --> -673 CHF/m2


    # leere Listen für die Daten des Diagramms vorbereiten bevor Loop beginnt
    namen  = []   # x-Achse: Bezeichnungen
    werte  = []   # y-Achse: CHF-Beitrag pro Faktor
    farben = []   # grün = positiv, rot = negativ


    laufender_preis = basispreis  # startet beim Basispreis
    # laufender_preis ändert sich durch alle Multiplikatoren


    for name, faktor in faktor_map.items():     # Loop-Header, dieser startet die Iteration
        # alles drinn wird wiederholt für jeden Faktor (Zimmerzahl, Zustand, Stockwerk,Baujahr, Ausstattung)
        
        neuer_preis = laufender_preis * faktor          # Preis nach diesem Faktor: laufender Preis x Multiplikator
        beitrag = round(neuer_preis - laufender_preis)  # Differenz zwischen vorher/nacher = Einfluss in CHF/m2

        if abs(beitrag) > 10:  
            # abs = Absolutwert, ignoriert Vorzeichen 
            # Faktoren unter CHF 10 Einfluss ignorieren

            namen.append(name)          # Fügt den Name des Faktors zur Liste hinzu (z.B. "Zimmerzahl" etc.)
            werte.append(beitrag)       # Fügt den CHF-Beitrag zur Liste hinzu (z.B. +240 oder -673)
            
            # Grün wenn Faktor Preis erhöht, Rot wenn er ihn senkt
            farben.append("#1D9E75" if beitrag >= 0 else "#D85A30")
        
        laufender_preis = neuer_preis  # nächster Faktor startet vom neuen Preis
            # Wichtig: ausserhalb des if --> wird immer aktualisiert, nicht nur wenn Beitrag > 10


    # Basispreis und Endpreis als Rahmen hinzufügen, damit der Chart von Anfang bis Ende die Preisveränderungen zeigt.
    # "inside" = Balken im Waterfall-Chart (relative Änderung)
    # "total"  = absoluter Wert (Basispreis und Endpreis)
    alle_namen  = ["Lage (Quartier)"] + namen           + ["Endpreis"]
    alle_werte  = [basispreis]        + werte           + [preis_pro_m2]
    alle_typen  = ["absolute"]        + ["relative"] * len(namen) + ["total"] # Claude AI hat uns hier geholfen: Plotly spezifische Strings, damit die Balken korrekt dargestellt werden. "absolute" für den Basispreis, "relative" für die Faktoren, "total" für den Endpreis.
    alle_farben = ["#6AAAE9"]         + farben          + ["#0e48c6"]

    # Waterfall-Chart erstellt mit Hilfe von Claude AI (Anthropic)
    # Professionelles Chart-Design, especially Plotly spezifische Strings übersteigen unsere aktuellen Fähigkeiten.
    fig = go.Figure(go.Waterfall(
        orientation = "v",                    # vertikale Balken
        measure     = alle_typen,             # "absolute", "relative" oder "total"
        x           = alle_namen,             # Beschriftung x-Achse
        y           = alle_werte,             # Werte in CHF/m²
        connector   = {"line": {"color": "#e2e8f0", "width": 1}},  # Verbindungslinien zwischen Balken
        text        = [
            f"+{v:,}".replace(",", "'") if v > 0
            else f"{v:,}".replace(",", "'")
            for v in alle_werte
        ],  # Wert direkt auf jedem Balken anzeigen, mit Vorzeichen
        textposition = "outside",             # Text oberhalb/unterhalb des Balkens
        increasing   = {"marker": {"color": "#1D9E75"}},  # grün für positive Balken
        decreasing   = {"marker": {"color": "#D85A30"}},  # rot für negative Balken
        totals       = {"marker": {"color": "#378ADD"}},  # blau für Lage und Endpreis
    ))

    fig.update_layout(
        title         = "Zusammensetzung des Preises – Einfluss der Faktoren (CHF/m²)",
        yaxis_title   = "CHF pro m²",
        plot_bgcolor  = "white",
        paper_bgcolor = "white",
        margin        = dict(t=60, b=20, l=20, r=20),
        showlegend    = False,
    )

    return fig
