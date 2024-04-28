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
        brand="US Crime Data Dashboard",
        color="#000435",
        dark=True,
        style={
            'fontFamily': 'Roboto',
            'fontWeight': '400',
        },
        brand_style={
            'fontFamily': 'Roboto',
            'fontWeight': '600',
            'fontSize': '1.5em'
        }
    )
    return navbar