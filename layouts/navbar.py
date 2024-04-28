import dash_bootstrap_components as dbc
def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/index")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("State", href="/crime-by-state", style={'font-size': 'smaller'}),
                    dbc.DropdownMenuItem("Time", href="#", style={'font-size': 'smaller'}),
                    dbc.DropdownMenuItem("Division", href="#", style={'font-size': 'smaller'}),
                ],
                nav=True,
                in_navbar=True,
                label="Crime by...",
                menu_variant="dark"
            ),
            dbc.NavItem(dbc.NavLink("About", href="/about")),
        ],
        brand="US Crime Data Dashboard",
        color="#000435",
        dark=True,
        style={
            'font-family': 'Roboto',
            'font-weight': '400',
        },
        brand_style={
            'font-family': 'Roboto',
            'font-weight': '600',
        }
    )
    return navbar