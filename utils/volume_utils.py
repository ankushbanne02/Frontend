import numpy as np
import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc

def generate_bar_chart(data_dict, title, xaxis_title):
    """Generates a bar chart from distribution data."""
    if not data_dict:
        return html.Div("No data available", className="text-muted")

    x = list(map(float, data_dict.keys()))
    y = list(data_dict.values())

    fig = go.Figure(data=[go.Bar(x=x, y=y, marker_color="#4e79a7")])
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title="Count",
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )
    return html.Div(dcc_graph_wrapper(fig))


def generate_normal_chart(stats_dict, title, xaxis_title):
    """Generates a Gaussian curve from mean and std deviation."""
    mean = stats_dict.get("mean", 0)
    std_dev = stats_dict.get("std_dev", 0)

    if std_dev <= 0:
        return html.Div("No data for normal distribution", className="text-muted")

    x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 200)
    y = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)

    fig = go.Figure(data=[go.Scatter(x=x, y=y, mode="lines", line=dict(color="#59a14f"))])
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title="Probability Density",
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )
    return html.Div(dcc_graph_wrapper(fig))


def generate_stats_table(h_data, w_data, l_data):
    """Generates table with min, max, avg for each dimension."""
    def calc_stats(data_dict):
        if not data_dict:
            return "-", "-", "-"
        values = list(map(float, data_dict.keys()))
        counts = list(data_dict.values())
        avg = np.average(values, weights=counts)
        return min(values), max(values), round(avg, 2)

    h_min, h_max, h_avg = calc_stats(h_data)
    w_min, w_max, w_avg = calc_stats(w_data)
    l_min, l_max, l_avg = calc_stats(l_data)

    table_header = [
        html.Thead(html.Tr([html.Th("Dimension"), html.Th("Min"), html.Th("Max"), html.Th("Average")]))
    ]
    table_body = [
        html.Tbody([
            html.Tr([html.Td("Height (mm)"), html.Td(h_min), html.Td(h_max), html.Td(h_avg)]),
            html.Tr([html.Td("Width (mm)"), html.Td(w_min), html.Td(w_max), html.Td(w_avg)]),
            html.Tr([html.Td("Length (mm)"), html.Td(l_min), html.Td(l_max), html.Td(l_avg)])
        ])
    ]

    return dbc.Table(table_header + table_body, bordered=True, striped=True, hover=True, responsive=True)

def generate_kpi_card(title, count, pct, color="#17a2b8"):
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, className="mb-2", style={"fontWeight": "600"}),
            html.H3(f"{count}", className="mb-1", style={"fontWeight": "bold", "fontSize": "2rem"}),
            html.Div(f"{pct:.2f} %", className="small")
        ]),
        style={
            "backgroundColor": color,
            "color": "white",
            "textAlign": "center",
            "height": "140px",
            "borderRadius": "12px",
            "boxShadow": "0 4px 10px rgba(0,0,0,0.15)"
        },
        className="mb-3"
    )

def dcc_graph_wrapper(fig):
    """Wrap Plotly figure in a responsive Div."""
    return dcc.Graph(figure=fig, config={"displayModeBar": False}, style={"height": "300px"})
