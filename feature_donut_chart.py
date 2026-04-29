# 
# CHART 1: DONUT  Zusammensetzung des Preises
# feature_donut_chart
# Zeigt wie stark jeder Faktor den geschätzten Preis beeinflusst.
# Jeder Faktor ist ein Multiplikator: 1.0 = kein Einfluss,
# z.B. 1.05 = +5% auf den Preis, 0.95 = -5% auf den Preis


def erstelle_donut_chart(faktoren):
    """
    Zeigt den relativen Einfluss jedes Faktors
    als Anteil am Gesamtpreis (in Prozent).
    """
    # Nur Faktoren ohne Basispreis und nur wenn sie vom Standard (1.0) abweichen
    labels = []
    anteile = []

    faktor_map = {
        "Zimmerzahl":  faktoren["Zimmerzahl"],
        "Zustand":     faktoren["Zustand"],
        "Stockwerk":   faktoren["Stockwerk"],
        "Baujahr":     faktoren["Baujahr"],
        "Ausstattung": faktoren["Ausstattung"],
    }

    # Basispreis als grössten Anteil setzen
    gesamt = faktoren["Basispreis (Quartier)"]
    basis_anteil = 100.0

    # Anteil jedes Faktors berechnen (Abweichung von 1.0 in Prozent)
    faktor_anteile = {}
    for name, wert in faktor_map.items():
        abweichung = abs((wert - 1.0) * 100)
        if abweichung > 0.1:  # nur relevante Faktoren anzeigen
            faktor_anteile[name] = round(abweichung, 1)
            basis_anteil -= abweichung


    labels = ["Lage (Quartier)"] + list(faktor_anteile.keys())
    werte  = [round(max(basis_anteil, 50), 1)] + list(faktor_anteile.values())
    farben = ["#378ADD", "#1D9E75", "#EF9F27", "#D85A30", "#7F77DD", "#5DCAA5"]


    fig = go.Figure(go.Pie(
        labels    = labels,
        values    = werte,
        hole      = 0.6,
        marker    = dict(colors=farben[:len(labels)]),
        textinfo  = "label+percent",
        hovertemplate = "<b>%{label}</b><br>Einfluss: %{value:.1f}%<extra></extra>",
    ))


    fig.update_layout(
        title       = "Zusammensetzung des Preises --> Einfluss der Faktoren", # Titel über dem Chart
        showlegend  = False, # keine Legende, da die Labels direkt im Chart angezeigt werden
        plot_bgcolor  = "white", # Hintergrundfarbe des Chart-Bereichs 
        paper_bgcolor = "white", # Hintergrundfarbe der gesamten Grafik / Figure
        margin = dict(t=60, b=20, l=20, r=20), # etwas mehr Platz oben für den Titel (Abstände in Pixeln, top bottom left right)
        annotations = [dict( 
            text      = "Einfluss", # Text in der Mitte des Donuts
            x=0.5, y=0.5, # Text in der Mitte des Donuts
            font_size = 14, # etwas kleinerer Text in der Mitte
            showarrow = False, # kein Pfeil in der Mitte, nur text
            font_color= "#6c757d" # grau für den Text in der Mitte
        )]
    )
    # Figure zurückgeben → wird in Streamlit mit st.plotly_chart(fig) angezeigt
    return fig
