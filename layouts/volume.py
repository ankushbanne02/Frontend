import dash
from dash import dcc, html, dash_table
import plotly.express as px
import requests
import pandas as pd
import dash_bootstrap_components as dbc

volume_layout = html.Div([
    html.H2("📈 Volume Tab"),
    html.P("This is the Volume tab content.")
])


# ---------- Fetch data from FastAPI endpoint ---------- #
def fetch_volume_data():
    try:
        response = requests.get("https://backend-vanderlande-1.onrender.com/volume")
        response.raise_for_status()  # Raise error for bad responses
        data = response.json()
        return pd.DataFrame(data)
    except Exception as e:
        print("API Error:", e)
        return pd.DataFrame()

df = fetch_volume_data()

# ---------- Stats table function ---------- #
def generate_stats_table(df, dimension):
    return dash_table.DataTable(
        columns=[
            {"name": "Minimum [mm]", "id": "min"},
            {"name": "Average [mm]", "id": "avg"},
            {"name": "Maximum [mm]", "id": "max"},
        ],
        data=[{
            "min": round(df[dimension].min(), 2),
            "avg": round(df[dimension].mean(), 2),
            "max": round(df[dimension].max(), 2),
        }] if not df.empty else [],
        style_cell={'textAlign': 'center'},
        style_header={'fontWeight': 'bold'},
        style_table={'marginTop': '10px'}
    )

# ---------- Dash App Layout ---------- #
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H3("📦 Parcel Volume Statistics", className="mt-4 mb-4 text-center"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(
                figure=px.histogram(df, x="height", nbins=20,
                                    title="Parcel Height Distribution [mm]",
                                    color_discrete_sequence=["#ff4c8b"]) if not df.empty else {}
            ),
            generate_stats_table(df, "height")
        ]),
        dbc.Col([
            dcc.Graph(
                figure=px.histogram(df, x="width", nbins=20,
                                    title="Parcel Width Distribution [mm]",
                                    color_discrete_sequence=["#4c8bff"]) if not df.empty else {}
            ),
            generate_stats_table(df, "width")
        ]),
        dbc.Col([
            dcc.Graph(
                figure=px.histogram(df, x="length", nbins=20,
                                    title="Parcel Length Distribution [mm]",
                                    color_discrete_sequence=["#50fa7b"]) if not df.empty else {}
            ),
            generate_stats_table(df, "length")
        ]),
    ])
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)
