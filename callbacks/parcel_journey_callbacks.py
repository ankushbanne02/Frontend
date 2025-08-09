from dash import Input, Output, State, no_update, html, dash_table
import pandas as pd
import requests
import json

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
            payload = {
                "date": date,
                "search_by": search_by,
                "search_value": input_value,
            }

            API_URL = "http://127.0.0.1:8000/parcel-journey"
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()

            if not data:
                return html.Div("No parcel journey data found.", className="text-warning")

            # Convert barcode list to string
            for entry in data:
                if isinstance(entry.get("barcode"), list):
                    entry["barcode"] = ", ".join(entry["barcode"])

            df = pd.DataFrame(data)

            # Rename columns for display
            df.rename(columns={
                "host_id": "HOST ID",
                "status": "Status",
                "barcodes": "Barcode(s)",
                "alibi_id": "Alibi ID",
                "register_on_and_at": "Register Time & Location",
                "identification_on_and_at":"identification Time & Location",
                "exit_on_and_at":"exit Time & Location",
                "destination": "Destination",
                "volume Data": "Volume",  # This is the only change you need for column name
            }, inplace=True)

            # Extract and display RAW logs
            raw_logs = []
            for idx, entry in enumerate(data):
                raw_content = entry.get("RAW", {})
                if isinstance(raw_content, dict):
                    raw_text = "\n".join([f"{k}: {v}" for k, v in raw_content.items()])
                elif isinstance(raw_content, str):
                    try:
                        parsed = json.loads(raw_content)
                        raw_text = "\n".join([f"{k}: {v}" for k, v in parsed.items()])
                    except json.JSONDecodeError:
                        raw_text = raw_content
                else:
                    raw_text = str(raw_content)

                raw_logs.append(html.Details([
                    html.Summary(f"RAW Logs for Parcel #{idx + 1}"),
                    html.Pre(raw_text, style={"whiteSpace": "pre-wrap"})
                ]))

            if "RAW" in df.columns:
                df = df.drop(columns=["RAW"])

            return html.Div([
                dash_table.DataTable(
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
                    style_data={"backgroundColor": "#ffffff"}
                ),
                html.Hr(),
                html.Div(raw_logs)
            ])

        except requests.exceptions.RequestException as e:
            return html.Div(f"Error connecting to the API: {str(e)}", className="text-danger")
        except Exception as e:
            return html.Div(f"Error fetching data: {str(e)}", className="text-danger")
