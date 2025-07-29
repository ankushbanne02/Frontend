import dash_bootstrap_components as dbc
from dash import html

navbar = dbc.Navbar(
    dbc.Container([
        # Navbar Brand/Title on the left
        dbc.NavbarBrand(
            "Parcel Monitoring",
            href="/",
            className="fw-bold text-white me-3"
        ),

        # Navigation links with custom left margin
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Summary", href="/", className="text-white")),
                dbc.NavItem(dbc.NavLink("Throughput", href="/throughput", className="ms-3 text-white")),
                dbc.NavItem(dbc.NavLink("Parcel Journey", href="/parcel-journey", className="ms-3 text-white")),
                dbc.NavItem(dbc.NavLink("Volume", href="/volume", className="ms-3 text-white")),
            ],
            style={"marginLeft": "10px"},
            navbar=True
        )
    ]),
    color="dark",
    dark=True,
    sticky="top",
    className="py-2"
)
