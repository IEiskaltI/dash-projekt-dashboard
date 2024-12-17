import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# CSV-Datei laden
df = pd.read_csv("entwicklungsprozesse.csv")

# None-Werte entfernen
df = df.dropna(subset=['Baugruppe', 'Projekttitel'])

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
    app.run_server(debug=True)
