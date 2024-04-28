from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.graph_objects as go

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

#crimes and officers by state
us_states = gpd.read_file('data-dir/States_shapefile.shp')
crimes_by_state = pd.read_csv('data-dir/crime_data_by_state.csv')
officers_by_state = pd.read_csv('data-dir/officers_data_by_state.csv')

merged_crime_data = us_states.merge(crimes_by_state, how='left', left_on='State_Name', right_on='State')
merged_officer_data = us_states.merge(officers_by_state, how='left', left_on='State_Name', right_on='State')

merged_crime_data['Crime_Rate_Per_Capita'] = merged_crime_data['Violent Crime'] / merged_crime_data['Population']
merged_officer_data['Officers_Per_Capita'] = merged_officer_data['Total Officers'] / merged_officer_data['Population']

#crime trends
crime_trends = pd.read_csv('data-dir/crime_trends.csv')


#arrests by crimes and ethnicity
arrests_by_crime_ethnicity = pd.read_csv('data-dir/arrests_by_crime_ethnicity_T.csv')

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('US Crime Data by State'),
            dcc.Dropdown(
                id='crime_officers_map_dropdown',
                options=[
                    {'label': 'Crimes', 'value': 'crimes'},
                    {'label': 'Officers', 'value': 'officers'}
                ],
                value='crimes'
    ),
            dcc.Graph(id='crime_officers_map')
        ],
        width=6
        ),
        dbc.Col([
            html.H1('Crime Trends in the US'),
            # make a checkbox for each crime type
            dcc.Checklist(
                id='crime_trends_checklist',
                options=[
                    {'label': 'All Crime', 'value': 'Violent Crime'},
                    {'label': 'Murder and Manslaughter', 'value':'Murder and Manslaughter'},
                    {'label':'Rape','value':'Rape'},
                    {'label':'Aggrevated Assault','value':'Aggrevated Assult'},
                    {'label':'Robbery','value':'Robbery'},
                    {'label':'Property Crimes','value':'Property Crime'}
                ],
                value=['Violent Crime']

            ),
            dcc.Graph(id='crime_trends')
        ],
        width=6
        )
    ]),
    dbc.Row([
        dbc.Col([
            html.H1('Arrests by Crime and Ethnicity'),
            dcc.Checklist(
                id='arrests_by_crime_ethnicity_checklist',
                options=[
                    {'label': 'White', 'value': 'White'},
                    {'label': 'Black', 'value':'Black'},
                    {'label':'American or Alaskan Native','value':'American or Alaskan Native'},
                    {'label':'Asian','value':'Asian'},
                    {'label':'Hawaiian or North Pacific Ilander','value':'Hawaiian or North Pacific Ilander'}
                ],
                value=['White']
            ),
            dcc.Graph(id='arrests_by_crime_ethnicity')


        ])
    ])
])

@app.callback(
    Output('crime_officers_map', 'figure'),
    Input('crime_officers_map_dropdown', 'value')

)
def update_map(dataset):
    # make a heatmap of the crime data by state using plotly express
    if dataset == 'crimes':
        fig = px.choropleth(merged_crime_data, geojson=merged_crime_data.geometry, locations=merged_crime_data.index,
                            color='Crime_Rate_Per_Capita', hover_name='State_Name',
                            color_continuous_scale='OrRd', projection='mercator')

    else:
        fig = px.choropleth(merged_officer_data, geojson=merged_officer_data.geometry, locations=merged_officer_data.index,
                            color='Officers_Per_Capita', hover_name='State_Name',
                            color_continuous_scale='OrRd', projection='mercator')
    
    # add state boundaries in black colour to the map
    fig.update_geos(showcountries=True, showcoastlines=False, showland=True, fitbounds='locations')
    # remove the legend
    fig.update_layout(coloraxis_colorbar=dict(title='Crime Rate per Capita'))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig


@app.callback(
    Output('crime_trends', 'figure'),
    Input('crime_trends_checklist', 'value')
)
def update_trends(crime_types):
    # make a line chart of the crime trends over time
    fig = px.line(crime_trends, x='Year', y=crime_types)
    fig.update_layout(title='Crime Trends in the US')
    return fig


@app.callback(
    Output('arrests_by_crime_ethnicity', 'figure'),
    Input('arrests_by_crime_ethnicity_checklist', 'value')
)
def update_radarplot(races):
    cols = ['Murder and Manslaughter','Rape','Robbery','Aggravated Assault','Burglary','Larceny-theft']
    fig = go.Figure()
    arrests_by_crime_ethnicity[cols] = (arrests_by_crime_ethnicity[cols] - arrests_by_crime_ethnicity[cols].min()) / (arrests_by_crime_ethnicity[cols].max() - arrests_by_crime_ethnicity[cols].min())
    for i in range(len(races)):
        df_temp = arrests_by_crime_ethnicity[arrests_by_crime_ethnicity['Type of crime']==races[i]]
        df_temp = df_temp[cols]
        fig.add_trace(go.Scatterpolar(
            r= df_temp.values.reshape(1,-1)[0],
            theta= cols,
            fill='toself',
            name=races[i]
        ))
    fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]
        )),
    showlegend=False,
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

