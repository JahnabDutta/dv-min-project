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
            )
        ], width=6, style={'border': '2px solid black', 'padding': '10px'}),
        
        dbc.Col([
            # html.H1('Crime Trends in the US'),
            dcc.Dropdown(
                options=['Violent Crime', 'Murder and Manslaughter', 'Rape', 'Aggravated Assault', 'Robbery', 'Property Crime', 'Burglary', 'Larceny and Theft', 'Motor Vehicle Theft'],
                value=['Violent Crime', 'Robbery', 'Property Crime'],
                id='crime_trends_dd',
                multi=True,
                searchable=False,
                placeholder="Choose Crime Type"
            ),
            dcc.Checklist(
                id='per_capita_cb',
                options=[{'label': html.Span('View incidents per capita', style={'paddingLeft': 5, 'fontSize': 'smaller'}), 'value': 'check'}],
                value=[],  # Not selected by default
            ),
            dcc.Graph(id='crime_trends')
        ], width=6, style={'border': '2px solid black'})
    ], style={'--bs-gutter-x': '0px', 'height': '100%', 'justifyContent': 'space-around', 'alignItems': 'center', 'border': '2px solid black'})
], style={'height': '100%'})

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
    fig = px.line(df, x='Year', y=crime_types)
    fig.update_layout(title='Crime Trends in the US')

    # temp = pd.DataFrame({
    #     'Year': crime_trends['Year'],
    #     incidents
    # })

    # Update y-axis label
    fig.update_yaxes(title_text=y_label)
    fig.update_xaxes(title_text='Year')

    # Update layout
    fig.update_layout(title='Crime Trends in the US', legend_title_text='Crime Type')

    return fig
