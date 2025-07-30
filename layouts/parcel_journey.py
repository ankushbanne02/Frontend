from dash import html, dcc
import dash_bootstrap_components as dbc
import datetime

parcel_journey_layout = html.Div([

    html.H4("Parcel journey", className="mb-3"),

    dbc.Row([
        dbc.Col([
            html.Small("Time window"),
            dcc.DatePickerSingle(
                id='date-picker',
                date=datetime.date.today(),
                display_format='YYYY-MM-DD',
                className="w-100"
            )
        ], width=2),

        dbc.Col([
            html.Small("Search for parcel based on:"),
            dcc.Dropdown(
                id='search-based-on',
                options=[
                    {'label': 'HOST ID', 'value': 'host_id'},
                    {'label': 'Barcode', 'value': 'barcode'},
                    {'label': 'ALIBI ID', 'value': 'alibi_id'}
                ],
                value='BARCODE',
                clearable=False,
                className="w-100"
            )
        ], width=2),

        dbc.Col([
            html.Small(id='input-label', children="Enter Barcode"),
            dbc.Input(
                id='search-input',
                placeholder="*",
                type="text",
                className="w-100"
            )
        ], width=2),

        dbc.Col([
            html.Small("Sorter"),
            dcc.Dropdown(
                id='sorter-dropdown',
                options=[
                    {'label': 'All', 'value': 'All'},
                ],
                value='All',
                className="w-100"
            )
        ], width=2),

        dbc.Col([
            html.Small("Output location"),
            dcc.Dropdown(
                id='output-location-dropdown',
                options=[
                    {'label': 'All', 'value': 'All'},
                ],
                value='All',
                className="w-100"
            )
        ], width=2),

        dbc.Col([
            html.Small("Preferred location naming"),
            dcc.Dropdown(
                id='location-naming-dropdown',
                options=[
                    {'label': 'Descriptive name', 'value': 'descriptive'},
                    {'label': 'Raw ID', 'value': 'raw'}
                ],
                value='descriptive',
                className="w-100"
            )
        ], width=2),

        dbc.Col([
            html.Small(" "),
            dbc.Button("Get Details", id="get-details-btn", color="primary", className="mt-2 w-100")
        ], width=2)
    ], className="gy-2"),

    # 🔽 Table Output Appears Here
    html.Div(id='parcel-journey-output', className="mt-4")

], className="parcel-journey-tab")
