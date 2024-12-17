
import pandas as pd
import pyodbc
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# SQL-Abfrage und Verbindung zur Datenbank
connection_string = (
    "DRIVER={SQL Server};"
    "SERVER=DE1DS004\\SQLPROD_2,46512;"
    "DATABASE=Projekte_FolieEntwicklung;"
    "UID=FolieEntwicklung;"
    "PWD=-[HNkWusnAed{J98[RPm.bfh+Mf4ER;"
)
bedingung = "WHERE Gesamtstatus = 'Abgeschlossen'"
query = f"""
SELECT 
    Projekt_ID, Gesamtstatus, Prioritaet, Baugruppe, Projekttitel, Projektmanager, Kalenderwoche,
    KW_Uebersicht, Abteilung, BudgetFreigabe_akt_GJ, Prozesstyp, Projekttyp, Reserve1, Reserve2, Reserve3,
    CONVERT(VARCHAR, Stage0Start, 104) AS Stage0Start,
    CONVERT(VARCHAR, Stage0Ende, 104) AS Stage0Ende,
    CONVERT(VARCHAR, Stage1Start, 104) AS Stage1Start,
    CONVERT(VARCHAR, Stage1Ende, 104) AS Stage1Ende,
    CONVERT(VARCHAR, Stage2Start, 104) AS Stage2Start,
    CONVERT(VARCHAR, Stage2Ende, 104) AS Stage2Ende,
    DateiPfadundName
FROM Entwicklungsprozesse
{bedingung}
"""

# Daten aus der Datenbank holen
try:
    conn = pyodbc.connect(connection_string)
    df = pd.read_sql(query, conn)
    conn.close()
except Exception as e:
    print("Fehler beim Zugriff auf die Datenbank:", e)

# None-Werte entfernen
df = df.dropna(subset=['Baugruppe', 'Projekttitel'])

# Dash App initialisieren
app = dash.Dash(__name__)

# Layout der App
app.layout = html.Div([
    # Sunburst Diagramm ohne Titel
    html.Div([
        dcc.Graph(id='sunburst-chart', style={'width': '100vw', 'height': '100vh'})
    ], style={'margin': '0', 'padding': '0', 'width': '100%', 'height': '100vh'})
])

# Callback-Funktion für Sunburst
@app.callback(
    Output('sunburst-chart', 'figure'),
    [Input('sunburst-chart', 'id')]  # Dummy-Input, um die Figur zu erstellen
)
def update_sunburst(dummy_input):
    sunburst_chart = px.sunburst(
        df,
        path=['Baugruppe', 'Projekttitel'],
        title=None,  # Titel entfernen
        color='Baugruppe'
    )
    return sunburst_chart

# App starten
if __name__ == '__main__':
    app.run_server(debug=True)
