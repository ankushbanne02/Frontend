# navbar.py
import dash_bootstrap_components as dbc
from dash import html

# Top Navbar: Title, Chatbot, Login
navbar_top = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand(
            html.A("📦 Parcel Monitoring", href="/", className="text-dark text-decoration-none"),
            className="fw-bold display-6 me-auto"
        ),
        dbc.Nav([
            dbc.NavItem(dbc.NavLink("Chatbot", href="/chatbot", className="text-dark me-3")),
            dbc.Button("Login", href="/login", color="primary", className="me-2"),
        ], className="d-flex", navbar=True)
    ]),
    color="light",
    sticky="top",
    className="custom-navbar py-3 shadow-sm"
)

# Tabs Navbar: Summary, Throughput, etc.
navbar_tabs = dbc.Navbar(
    dbc.Container([
        dbc.Nav([
            dbc.NavItem(dbc.NavLink("Summary", href="/")),
            dbc.NavItem(dbc.NavLink("Throughput", href="/throughput")),
            dbc.NavItem(dbc.NavLink("Identification", href="/identification")),
            dbc.NavItem(dbc.NavLink("Parcel Journey", href="/parcel-journey")),
            dbc.NavItem(dbc.NavLink("Volume", href="/volume")),
            dbc.NavItem(dbc.NavLink("Recirculation", href="/recirculation")),
        ], className="me-auto", navbar=True)
    ]),
    sticky="top",
    className="custom-navbar tab-navbar py-2 border-top"
)

# Combined layout to be used in your app
navbar = html.Div([navbar_top, navbar_tabs])
