from dash import html, Input, Output, State, callback
import dash_bootstrap_components as dbc

from utils.volume_utils import (
    fetch_volume_data,
    generate_bar_chart,
    compute_stats,
    generate_stats_table,
    calculate_length_allocation_kpis,
    generate_kpi_card
)

@callback(
    Output("volume-graphs-output", "children"),
    Input("volume-submit", "n_clicks"),
    State("volume-date-picker", "date"),
    prevent_initial_call=True
)
def update_volume_charts(n_clicks, selected_date):
    if not selected_date:
        return html.Div("Please select a date.", className="text-warning")

    try:
        data = fetch_volume_data(selected_date)

        if not any(data.get(key) for key in ["height_distribution", "width_distribution", "length_distribution"]):
            return html.Div("No data available for the selected date.", className="text-danger fw-bold text-center mt-4")

        height_chart = generate_bar_chart(data.get("height_distribution", {}), "Parcel Height Distribution [mm]", "Parcel Height (mm)")
        width_chart = generate_bar_chart(data.get("width_distribution", {}), "Parcel Width Distribution [mm]", "Parcel Width (mm)")
        length_chart = generate_bar_chart(data.get("length_distribution", {}), "Parcel Length Distribution [mm]", "Parcel Length (mm)")

        raw_length_dist = data.get("length_distribution", {})
        filtered_length_dist = {
            k: v for k, v in raw_length_dist.items()
            if float(k) > 0 and v is not None
        }

        allocated_length_chart = generate_bar_chart(
            filtered_length_dist,
            "Parcel Allocated Length Distribution [mm]",
            "Parcel Length (mm)"
        )

        pct_400, pct_600 = calculate_length_allocation_kpis(data.get("length_distribution", {}))

        return html.Div([
            dbc.Row([
                dbc.Col(height_chart, width=4),
                dbc.Col(width_chart, width=4),
                dbc.Col(length_chart, width=4),
            ]),

            html.Br(),

            html.H5("Dimension Summary Table", className="mt-4 mb-2 text-center"),
            generate_stats_table(
                data.get("height_distribution", {}),
                data.get("width_distribution", {}),
                data.get("length_distribution", {})
            ),

            html.Br(),

            html.H5("Parcel Allocation KPIs (Length-Based)", className="mt-4 mb-2 text-center"),
            dbc.Row([
                dbc.Col(allocated_length_chart, width=6),
                dbc.Col([
                    generate_kpi_card("Parcels allocated under 400 mm", pct_400),
                    generate_kpi_card("Parcels allocated under 600 mm", pct_600)
                ], width=6)
            ])
        ])
    
    except Exception as e:
        print(f"Callback error: {e}")
        return html.Div("An error occurred while updating the graphs.", className="text-danger")
