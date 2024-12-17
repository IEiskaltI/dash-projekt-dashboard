import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# CSV-Datei laden
df = pd.read_csv("entwicklungsprozesse.csv")

# Nur bestimmte Projekt_IDs auswählen
projekt_ids = [
    111, 114, 115, 141, 124, 117, 108, 135, 2, 32, 59, 26, 122, 98, 46, 92, 93, 64, 72, 83,
    121, 90, 13, 104, 119, 99, 137, 143, 132, 102, 68, 94, 89, 14, 116, 130, 131, 136, 118,
    63, 129, 103, 120, 126, 134, 142, 128, 127, 16, 70, 140, 17
]

# Stelle sicher, dass Projekt_ID als Integer interpretiert wird
df['Projekt_ID'] = pd.to_numeric(df['Projekt_ID'], errors='coerce').astype('Int64')

# Ersetze NaN-Werte durch "Weitere"
df = df.fillna("Weitere")

# Filtere nur die gewünschten IDs
df = df[df['Projekt_ID'].isin(projekt_ids)]

# Kürze lange Texte in allen Spalten mit Strings
def shorten_text(value, max_length=20):
    if isinstance(value, str) and len(value) > max_length:
        return value[:max_length] + '...'
    return value

# Wende die Kürzung auf alle String-Spalten an
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].apply(lambda x: shorten_text(x, max_length=20))

# Dash App initialisieren
app = dash.Dash(__name__)

# Layout der App
app.layout = html.Div([
    html.Div([
        dcc.Graph(id='sunburst-chart', style={'width': '100vw', 'height': '100vh'})
    ], style={'margin': '0', 'padding': '0', 'width': '100%', 'height': '100vh'})
])

# Callback-Funktion für Sunburst
@app.callback(
    Output('sunburst-chart', 'figure'),
    [Input('sunburst-chart', 'id')]  # Dummy-Input
)
def update_sunburst(dummy_input):
    sunburst_chart = px.sunburst(
        df,
        path=['Baugruppe', 'Projekttitel'],
        title=None,
        color='Baugruppe'
    )
    return sunburst_chart

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=False, host='0.0.0.0', port=port)
