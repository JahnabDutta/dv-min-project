import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
# from layouts.demographics import crime_demographics_layout
# from layouts.demographics_cb import update_map
from navbar import Navbar

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True)
server = app.server
app.config.suppress_callback_exceptions = True



content_div = html.Div(id='content', className='container mt-4')

# custom_css = '''
# .navbar-dd .dropdown-menu a.dropdown-item:hover {
#     background-color: #151C62 !important;
#     color: #fff !important;     
# }
# '''

app.layout = html.Div([
    html.Link(rel='stylesheet', href='https://fonts.googleapis.com/css2?family=Roboto:wght@400;600;700&display=swap'),  # Link to Google Fonts
    # dcc.Location(id='url', refresh=False),  # No refresh on URL change
    Navbar(),
    dash.page_container
])

# # Callback to update the page content based on the URL
# @app.callback(
#     Output('page-content', 'children'),
#     [Input('url', 'pathname')]
# )
# def display_page(pathname):
#     if pathname == '/demographics':
#         return crime_demographics_layout()
#     # Add more conditions for other screens/pages if needed
#     else:
#         return html.Div([
#             html.H2('404 - Page Not Found'),
#             html.P('The requested page was not found.')
#         ])
    


if __name__ == '__main__':
    app.run_server(debug=False)