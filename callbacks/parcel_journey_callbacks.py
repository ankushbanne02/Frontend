from dash import Input, Output, State, no_update, html, dash_table
import pandas as pd
import requests

def register_parcel_journey_callbacks(app):
    @app.callback(
        Output('parcel-journey-output', 'children'),
        Input('get-details-btn', 'n_clicks'),
        State('date-picker', 'date'),
        State('search-based-on', 'value'),
        State('search-input', 'value'),
        prevent_initial_call=True
    )
    def get_details(n_clicks, date, search_by, input_value):
        if not input_value:
            return html.Div("Please enter a value to search.", className="text-danger")

        try:
            # Prepare request payload
            payload = {
                "date": date,
                "search_by": search_by,
                "search_value": input_value,
            }

            # Replace with your actual backend URL
            API_URL = "https://backend-vanderlande-1.onrender.com/parcel-journey"

            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()

            if not data:
                return html.Div("No parcel journey data found.", className="text-warning")

            # Convert response to DataFrame
            df = pd.DataFrame(data)

            # Rename for display (optional)
            column_rename = {
                "host_id": "HOST ID",
                "status": "Status",
                "barcode": "Barcode",
                "alibi_id": "Alibi ID",
                "register_at": "Register At",
                "destination": "Destination",
                "volume": "Volume",
                "location": "Location"
            }
            df.rename(columns=column_rename, inplace=True)

            return dash_table.DataTable(
                columns=[{"name": col, "id": col} for col in df.columns],
                data=df.to_dict("records"),
                page_size=10,
                style_table={"overflowX": "auto", "border": "1px solid #dee2e6", "borderRadius": "6px"},
                style_cell={
                    "textAlign": "left",
                    "padding": "6px",
                    "borderBottom": "1px solid #dee2e6",
                },
                style_header={
                    "backgroundColor": "#f8f9fa",
                    "fontWeight": "bold",
                    "borderBottom": "2px solid #dee2e6",
                },
                style_data={
                    "backgroundColor": "#ffffff"
                }
            )

        except Exception as e:
            return html.Div(f"Error fetching data: {str(e)}", className="text-danger")
