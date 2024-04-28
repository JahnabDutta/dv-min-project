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

most_used_weapon = "Handgun"

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(  
                        dbc.Card(
                            [
                                dbc.CardHeader("Most Used Weapon"),
                                dbc.CardBody(
                                    [
                                        html.H3(f"{most_used_weapon}", className="card-title"),
                                        html.Img(src="assets/handgun.svg", style={"width": "50px", "height": "50px"}),
                                    ],
                                    className="d-flex justify-content-between"

                                ),
                                dbc.CardFooter("7,105 homicides in 2016")
                            ],
                        ),
                        # add padding
                        className="py-2",
                        width=3,
                ),
                dbc.Col(
                     dbc.Card(
                            [
                                dbc.CardHeader("State with Highest Crime Rate"),
                                dbc.CardBody(
                                    [
                                        html.H3(f"California", className="card-title"),
                                        html.Img(src="assets/california.svg", style={"width": "50px", "height": "50px"}),
                                    ],
                                    className="d-flex justify-content-between"

                                ),
                                dbc.CardFooter("1,861,269 crimes in 2016")
                            ],
                            
                        ),className="py-2",
                        width=3,
                ),
                dbc.Col(
                     dbc.Card(
                            [
                                dbc.CardHeader("Crime with Highest Rate"),
                                dbc.CardBody(
                                    [
                                        html.H3(f"Property Crime", className="card-title"),
                                        html.Img(src="assets/theft.svg", style={"width": "50px", "height": "50px"}),
                                    ],
                                    className="d-flex justify-content-between"

                                ),
                                dbc.CardFooter("7,993,631 incidents in 2016")
                            ],
                            
                        ),className="py-2",
                        width=3,
                ),
                dbc.Col(
                     dbc.Card(
                            [
                                dbc.CardHeader("State with Highest Law Enforcement"),
                                dbc.CardBody(
                                    [
                                        html.H3(f"California ", className="card-title"),
                                        html.Img(src="assets/california.svg", style={"width": "50px", "height": "50px"}),
                                    ],
                                    className="d-flex justify-content-between"

                                ),
                                dbc.CardFooter("78,062 officers")
                            ],
                            
                        ),className="py-2",
                        width=3,
                )
            ],
            # add style such that the height of the card is 100% of the container
            style={"height": "100%"}
        )
    ],
    fluid=True
)