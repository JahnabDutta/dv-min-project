import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from navbar import Navbar

dash.register_page(
    __name__,
    name = "Crime Statistics", 
    title = "Crime Statistics | Dashboard",
    path="/statistics")


layout = html.Div([
    # Navbar(),
    dbc.Row([
        # Left half - choropleth
        dbc.Col([
            # html.H1('US Crime Data by State'),
            html.P('This app shows crime data by state in the US.'),
            html.P('Hover over the map to see the crime rate per capita.'),
            html.P('The table below shows the crime data by state.'),
            html.Div(
                [dcc.Dropdown(
                    id='state-dropdown',
                    options=[
                        {
                            'label': html.Span(
                                [
                                    html.Img(src="/assets/icons/crimes.png", height=20),
                                    html.Span("Crime Rate", style={'paddingLeft': 10}),
                                ], style={'alignItems': 'center', 'justifyContent': 'center', 'width': '50%'}
                            ), 
                            'value': 'crimes'},
                        {
                            'label': html.Span(
                                [
                                    html.Img(src="/assets/icons/police.png", height=20),
                                    html.Span("Officers", style={'paddingLeft': 10}),
                                ], style={'alignItems': 'center', 'justifyContent': 'center', 'width': '50%'}
                            ), 
                            'value': 'officers'},
                    ],
                    value='crimes',
                    # style={'width': '50%'},
                    searchable=False,
                    clearable=False,
                    placeholder="Select...",
                    # option_style={'fontSize': 'smaller'}
                )], 
                style={'width': '30%'}
            ),
            dcc.Graph(
                id='crime-map',
                # Add chloropleth map here
                # Set the figure property to your chloropleth map figure
                # Example: figure=your_chloropleth_map_figure
            )
        ], width=6, style={'border': '2px solid black', 'padding': '10px'}),
        
        # Right half - Chloropleth map
        dbc.Col([
            html.H3("Top 5 states for different crimes"),
            
        ], width=6, style={'border': '2px solid black'})
    ], style={'--bs-gutter-x': '0px', 'height': '100%', 'justifyContent': 'space-around', 'alignItems': 'center', 'border': '2px solid black'})
], style={'height': '100%'})

