import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Import layouts
from layouts.summary import summary_layout
from layouts.throughput import throughput_layout
from layouts.parcel_journey import parcel_journey_layout
from layouts.volume import volume_layout
from layouts.identification import identification_layout
from layouts.recirculation import recirculation_layout
from layouts.chatbot import chatbot_layout, register_chatbot_callbacks

# Import navbar
from components.navbar import navbar  

# Import callbacks
import callbacks.volume_callbacks
import callbacks.summary_callbacks
import callbacks.throughput_callbacks
from callbacks.parcel_journey_callbacks import register_parcel_journey_callbacks

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "📦 Parcel Dashboard"

# App layout
app.layout = html.Div([
    dcc.Location(id='url'),
    navbar,
    html.Div(id='page-content', className='p-4')
])

# Register callbacks
register_parcel_journey_callbacks(app)
register_chatbot_callbacks(app)

# Routing
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/throughput':
        return throughput_layout
    elif pathname == '/identification':
        return identification_layout
    elif pathname == '/parcel-journey':
        return parcel_journey_layout
    elif pathname == '/volume':
        return volume_layout
    elif pathname == '/recirculation':
        return recirculation_layout
    elif pathname == '/chatbot':
        return chatbot_layout
    elif pathname == '/login':
        return html.H3("Login Page Placeholder", className="text-muted text-center mt-5")
    else:
        return summary_layout  # Default to summary

if __name__ == '__main__':
    app.run(debug=True)
