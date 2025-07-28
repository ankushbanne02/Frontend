import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

from layouts.summary import summary_layout
from layouts.throughput import throughput_layout

from layouts.parcel_journey import parcel_journey_layout
from layouts.volume import volume_layout

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "📦 Parcel Dashboard"

# Custom Navbar with tabs aligned right
navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("Parcel Monitoring", href="/", className="fw-bold text-white"),

        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Summary", href="/", className="ms-3 text-white")),
                dbc.NavItem(dbc.NavLink("Throughput", href="/throughput", className="ms-3 text-white")),
                dbc.NavItem(dbc.NavLink("Parcel Journey", href="/parcel-journey", className="ms-3 text-white")),
                dbc.NavItem(dbc.NavLink("Volume", href="/volume", className="ms-3 text-white")),
            ],
            className="ms-auto",
            navbar=True
        )
    ]),
    color="primary",
    dark=True,
    sticky="top"
)

# App layout
app.layout = html.Div([
    dcc.Location(id='url'),
    navbar,
    html.Div(id='page-content', className='p-4')
])

# Routing callback
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/throughput':
        return throughput_layout
    elif pathname == '/parcel-journey':
        return parcel_journey_layout
    elif pathname == '/volume':
        return volume_layout
    else:
        return summary_layout  # Default to summary

if __name__ == '__main__':
    app.run(debug=True)
