import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, callback
from navbar import Navbar

import plotly.express as px
import pandas as pd
import geopandas as gpd
from dash.dependencies import Input, Output

dash.register_page(
    __name__,
    name = "Home", 
    title = "Home | Dashboard",
    path="/")

layout = html.Div([
    # Navbar(),
    html.H1('This is our Home page'),
    html.Div('This is our Home page content.'),
])
