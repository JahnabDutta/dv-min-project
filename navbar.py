import dash
import dash_bootstrap_components as dbc
def Navbar():
    navbar = dbc.NavbarSimple(
        # children=[
        #     dbc.NavItem(dbc.NavLink("Home", href="/")),
        #     dbc.NavItem(dbc.NavLink("Crime Demographics", href="/demographics")),
        #     dbc.NavItem(dbc.NavLink("Crime Statistics", href="/statistics")),
        #     dbc.NavItem(dbc.NavLink("About", href="/about")),
        # ],
        children=[
            dbc.NavItem(dbc.NavLink(page["name"], href=page["relative_path"])) for page in dash.page_registry.values()
        ],
        brand="CSL4050 Mini Project",
        color="#034694",
        dark=True,
        style={
            'fontFamily': 'Roboto',
            'fontWeight': '400',
            'height': '8vh'
        },
        brand_style={
            'fontFamily': 'Roboto',
            'fontWeight': '600',
            'fontSize': '1.5em'
        }
    )
    return navbar