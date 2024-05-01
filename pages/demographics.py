import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, callback
import plotly.graph_objects as go


import plotly.express as px
import pandas as pd
import geopandas as gpd
from dash.dependencies import Input, Output

dash.register_page(
    __name__,
    name = "Crime Demographics", 
    title = "Crime Demographics | Dashboard",
    path="/demographics")

# state data
us_states = gpd.read_file('data-dir/States_shapefile.shp')
crimes_by_state = pd.read_csv('data-dir/crime_data_by_state.csv')
officers_by_state = pd.read_csv('data-dir/officers_data_by_state.csv')

merged_crime_data = us_states.merge(crimes_by_state, how='left', left_on='State_Name', right_on='State')
merged_officer_data = us_states.merge(officers_by_state, how='left', left_on='State_Name', right_on='State')

merged_crime_data['Crime_Rate_Per_Capita'] = merged_crime_data['Violent Crime'] / merged_crime_data['Population']
merged_officer_data['Officers_Per_Capita'] = merged_officer_data['Total Officers'] / merged_officer_data['Population']

# crime trends
crime_trends = pd.read_csv('data-dir/crime_trends.csv')


layout = html.Div([
    # Navbar(),
    dbc.Row([
        dbc.Col([
            html.P('This figure shows crime data by state in the US.'),
            html.P('Hover over the map to see the crime rate per capita for each state.'),
            # html.P('Hover over the map to see the crime rate per capita.'),
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
                style={'width': '40%', 'margin-bottom': '20px'}
            ),
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='crime-map')
                ])
            ], style={'box-shadow': '5px 5px 5px 0px rgba(255,255,255,0.25)'})
        ], width=6, style={'padding': '30px'}),

        dbc.Col([
            dbc.Col([
                html.P('Different types of crimes in the US along with their trends:'),
                dcc.Dropdown(
                    options=['Violent Crime', 'Murder and Manslaughter', 'Rape', 'Aggravated Assault', 'Robbery', 'Property Crime', 'Burglary', 'Larceny and Theft', 'Motor Vehicle Theft'],
                    value=['Violent Crime', 'Robbery', 'Property Crime'],
                    id='crime_trends_dd',
                    multi=True,
                    searchable=False,
                    placeholder="Choose Crime Type"
                ),
                
            ], style={'display': 'flex', 'flex-direction': 'column'}),
            dbc.Col([
                dbc.Card([
                    dcc.Checklist(
                        id='per_capita_cb',
                        options=[{'label': html.Span('View incidents per capita', style={'paddingLeft': 5, 'fontSize': 'smaller'}), 'value': 'check'}],
                        value=[],  # Not selected by default
                    ),
                    dbc.CardBody([
                        
                        dcc.Graph(id='crime_trends', style={'height': '100%'})
                    ])
                ], style={'box-shadow': '5px 5px 5px 0px rgba(255,255,255,0.25)', 'height': '50%', 'margin-bottom':'10px', 'padding-left':'10px'}),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='crime_distribution', style={'height': '100%'})
                    ])
                ], style={'box-shadow': '5px 5px 5px 0px rgba(255,255,255,0.25)', 'height': '50%'})
                # html.Div([
                #     dcc.Graph(id='crime_trends', style={'height': '100%'})
                # ], style={'height': '50%'}),
                # html.Div([
                #     dcc.Graph(id='crime_distribution', style={'height': '100%'})
                # ], style={'height': '50%'})
            ], style={'height': '85%', 'padding': '10px 40px'})
        ], width = 6, style={'padding': '0 20px'})
        
        # dbc.Col([
        #     # html.H1('Crime Trends in the US'),
        #     dcc.Dropdown(
        #         options=['Violent Crime', 'Murder and Manslaughter', 'Rape', 'Aggravated Assault', 'Robbery', 'Property Crime', 'Burglary', 'Larceny and Theft', 'Motor Vehicle Theft'],
        #         value=['Violent Crime', 'Robbery', 'Property Crime'],
        #         id='crime_trends_dd',
        #         multi=True,
        #         searchable=False,
        #         placeholder="Choose Crime Type"
        #     ),
        #     dcc.Checklist(
        #         id='per_capita_cb',
        #         options=[{'label': html.Span('View incidents per capita', style={'paddingLeft': 5, 'fontSize': 'smaller'}), 'value': 'check'}],
        #         value=[],  # Not selected by default
        #     ),
        #     dcc.Graph(id='crime_trends', style={'maxHeight': '35%'}),
        #     dcc.Graph(id='crime_distribution', style={'maxHeight': '35%'})
        #     # html.Div([
        #     #     html.Div([
        #     #         dcc.Graph(id='crime_trends', style={'height': '50%', 'width': '100%'}),
        #     #     ], style={'width': '100%', 'overflow': 'hidden', 'border': '2px solid red'}),  # Container for the first graph
        #     #     html.Div([
        #     #         dcc.Graph(id='crime_distribution', style={'height': '50%', 'width': '100%'}),
        #     #     ], style={'width': '100%', 'overflow': 'hidden', 'border': '2px solid red'})   # Container for the second graph
        #     # ])
        # ], width=6, style={'display': 'flex', 'flex-direction': 'column', 'maxHeight': '80vh'})
    ], style={'--bs-gutter-x': '0px', 'height': '100%', 'padding': '20px'})
], style={'height': '92vh', 'backgroundImage': 'url(\'assets/bg/w15.jpg\')', 'backgroundPosition': "50% 50%", 'backgroundSize': 'cover'})

@callback(
    Output('crime-map', 'figure'),
    Input('state-dropdown', 'value')
)

def update_map(dataset):
    # make a heatmap of the crime data by state using plotly express
    if dataset == 'officers':
        fig = px.choropleth(merged_officer_data, geojson=merged_officer_data.geometry, locations=merged_officer_data.index,
                            color='Officers_Per_Capita', hover_name='State_Name',
                            color_continuous_scale='OrRd', projection='mercator').update_layout(title="Officers per Capita by State", title_x=0.5, title_y=0.95)
    else:
        fig = px.choropleth(merged_crime_data, geojson=merged_crime_data.geometry, locations=merged_crime_data.index,
                            color='Crime_Rate_Per_Capita', hover_name='State_Name',
                            color_continuous_scale='OrRd', projection='mercator').update_layout(title="Crime Rate per Capita by State", title_x=0.5, title_y=0.95)
    
    # Update geos layout to show only specific countries
    fig.update_geos(
        showcountries=True,
        showcoastlines=False,
        showland=True,
        fitbounds='locations',
        visible=True,
        projection_type="equirectangular",
        # projection_rotation={"lat": 37.0902, "lon": -95.7129},  # Centered around North America
        # scope="north america"  # Scope parameter to restrict to North America
    )

    # Update the layout
    fig.update_layout(
        coloraxis_colorbar=dict(title="Value", thickness=10),
        # coloraxis_showscale=False,
        # margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(
            showcountries=True,
            countrycolor="Black",
            showocean=True,
            oceancolor="LightBlue",
            landcolor="LightGrey"
        ),
        dragmode='pan',  # Restrict panning
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    return fig

@callback(
    Output('crime_trends', 'figure'),
    [Input('crime_trends_dd', 'value'),
     Input('per_capita_cb', 'value')]
)

def update_trends(crime_types, per_capita_checked):
    df = crime_trends.copy()
    y_label = 'Incidents'
    
    # Divide the selected crime types' values by the 'Population' column
    if per_capita_checked:
        for crime_type in crime_types:
            df[crime_type] /= df['Population']
        y_label = 'Incidents per Capita'
    
    # Make a line chart of the crime trends over time
    fig = px.line(df, x='Year', y=crime_types, markers=True)
    # fig.update_layout(title='Crime Trends in the US')

    # temp = pd.DataFrame({
    #     'Year': crime_trends['Year'],
    #     incidents
    # })

    # Update y-axis label
    fig.update_yaxes(title_text=y_label)
    fig.update_xaxes(title_text='Year')

    # Update layout
    fig.update_layout(title='Crime Trends in the US', legend_title_text='Crime Type')
    fig.update_layout(margin=dict(t=40, b=0))
    fig.update_traces(marker=dict(size=4))

    return fig

@callback(
    Output('crime_distribution', 'figure'),
    Input('crime_trends_dd', 'value')
)

def update_crime_distribution(crime_types):
    fig = go.Figure()
    for crime in crime_types:
        fig.add_trace(go.Box(y=crime_trends[crime], name=crime))
        # add the value of crime for 2016 on the boxplot
        fig.add_trace(go.Scatter(x=[crime], y=[crime_trends.loc[crime_trends['Year'] == 2016, crime].values[0]],
                                 mode='markers', name=f'{crime} in 2016', marker=dict(size=5)))
    fig.update_layout(title='Boxplot of Crimes over Time')
    fig.update_yaxes(title_text='Incidents')
    fig.update_layout(margin=dict(t=40, b=0))
    return fig