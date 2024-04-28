import dash_bootstrap_components as dbc
from dash import dcc, html

def crime_by_state_layout():
    layout = html.Div([
        dbc.Row([
            # Left half - Filters
            dbc.Col([
                html.H1('US Crime Data by State'),
                html.P('This app shows crime data by state in the US.'),
                html.P('Hover over the map to see the crime rate per capita.'),
                html.P('The table below shows the crime data by state.'),
                dcc.Dropdown(
                    id='state-dropdown',
                    options=[
                        {'label': 'Crimes', 'value': 'crimes'},
                        {'label': 'Officers', 'value': 'officers'}
                    ],
                    value='crimes'
                ),
            ], width=6),
            
            # Right half - Chloropleth map
            dbc.Col([
                html.H3("US Crime Data by State"),
                dcc.Graph(
                    id='crime-map',
                    # Add chloropleth map here
                    # Set the figure property to your chloropleth map figure
                    # Example: figure=your_chloropleth_map_figure
                )
            ], width=6)
        ])
    ])

    return layout

