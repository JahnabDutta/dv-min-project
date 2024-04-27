from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import geopandas as gpd

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

us_states = gpd.read_file('data-dir/States_shapefile.shp')
crimes_by_state = pd.read_csv('data-dir/crime_data_by_state.csv')
officers_by_state = pd.read_csv('data-dir/officers_data_by_state.csv')

merged_crime_data = us_states.merge(crimes_by_state, how='left', left_on='State_Name', right_on='State')
merged_officer_data = us_states.merge(officers_by_state, how='left', left_on='State_Name', right_on='State')

merged_crime_data['Crime_Rate_Per_Capita'] = merged_crime_data['Violent Crime'] / merged_crime_data['Population']
merged_officer_data['Officers_Per_Capita'] = merged_officer_data['Total Officers'] / merged_officer_data['Population']



# fig, ax = plt.subplots(1, 1, figsize=(10, 8))
# merged_data.plot(column='Crime_Rate_Per_Capita', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
# plt.title('Violent Crime Rate per Capita')
# plt.axis('off')
# us_states.boundary.plot(ax=ax, linewidth=1, color='black')
# plt.show()


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('US Crime Data by State'),
            html.P('This app shows crime data by state in the US.'),
            html.P('Hover over the map to see the crime rate per capita.'),
            html.P('The table below shows the crime data by state.'),
            dcc.Dropdown(
                id='dataset-dropdown',
                options=[
                    {'label': 'Crimes', 'value': 'crimes'},
                    {'label': 'Officers', 'value': 'officers'}
                ],
        value='crimes'
    ),
            dcc.Graph(id='crime_map')
        ], width=6),
    ])
])

@app.callback(
    Output('crime_map', 'figure'),
    Input('dataset-dropdown', 'value')

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
    fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds='locations')
    # remove the legend
    fig.update_layout(coloraxis_colorbar=dict(title='Crime Rate per Capita'))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)

