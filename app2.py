from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import geopandas as gpd
from layouts.navbar import Navbar
from layouts.state import crime_by_state_layout

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

us_states = gpd.read_file('data-dir/States_shapefile.shp')
crimes_by_state = pd.read_csv('data-dir/crime_data_by_state.csv')
officers_by_state = pd.read_csv('data-dir/officers_data_by_state.csv')

merged_crime_data = us_states.merge(crimes_by_state, how='left', left_on='State_Name', right_on='State')
merged_officer_data = us_states.merge(officers_by_state, how='left', left_on='State_Name', right_on='State')

merged_crime_data['Crime_Rate_Per_Capita'] = merged_crime_data['Violent Crime'] / merged_crime_data['Population']
merged_officer_data['Officers_Per_Capita'] = merged_officer_data['Total Officers'] / merged_officer_data['Population']

content_div = html.Div(id='content', className='container mt-4')

# custom_css = '''
# .navbar-dd .dropdown-menu a.dropdown-item:hover {
#     background-color: #151C62 !important;
#     color: #fff !important;     
# }
# '''

app.layout = html.Div([
    html.Link(rel='stylesheet', href='https://fonts.googleapis.com/css2?family=Roboto:wght@400;600;700&display=swap'),  # Link to Google Fonts
    dcc.Location(id='url', refresh=False),  # No refresh on URL change
    Navbar(),
    html.Div(id='page-content')
])

# Callback to update the page content based on the URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/crime-by-state':
        return crime_by_state_layout()
    # Add more conditions for other screens/pages if needed
    else:
        return html.Div([
            html.H2('404 - Page Not Found'),
            html.P('The requested page was not found.')
        ])
    
@app.callback(
    Output('crime-map', 'figure'),
    Input('state-dropdown', 'value')
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