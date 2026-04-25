import streamlit as st 

 

st.title("Immobilienpreisberechner 🏠") 

st.write("Hallo! Hier berechnen wir einen fairen Preis für deine Immobilie.") 

 

kantone = [ 

"Aargau", "Appenzell Ausserrhoden", "Appenzell Innerrhoden", 

"Basel-Landschaft", "Basel-Stadt", "Bern", "Freiburg", "Genf", 

"Glarus", "Graubünden", "Jura", "Luzern", "Neuenburg", "Nidwalden", 

"Obwalden", "Schaffhausen", "Schwyz", "Solothurn", "St. Gallen", 

"Thurgau", "Tessin", "Uri", "Waadt", "Wallis", 

"Zug", "Zürich" 

] 

 

kanton = st.selectbox("In welchem Kanton ist deine Immobilie?", kantone) 

adresse = st.text_input("Wie lautet die Adresse der Immobilie?") 

 

zimmer = st.slider("Wie viele Zimmer hat deine Immobilie?", 1, 20, 4) 

flaeche = st.slider("Wie gross ist die Fläche deiner Immobilie? (m²)", 10, 500, 100) 

stockwerke = st.slider("Wie viele Stockwerke hat deine Immobilie?", 1, 20, 2) 

alter = st.slider("Wie alt ist deine Immobilie? (Jahre)", 0, 200, 20) 

extras = st.multiselect("Was ist alles vorhanden?",  

["Parkplatz", "Keller", "Estrich", "Balkon", "Garten"]) 
print("Another thing")
print("This is a demo")
