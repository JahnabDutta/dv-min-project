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

#murder victims
murder_victims = pd.read_csv('data-dir/murder_victims.csv')

#arrests by crimes and ethnicity
arrests_by_crime_ethnicity = pd.read_csv('data-dir/arrests_by_crime_ethnicity_T.csv')

#murder offenders
murder_offenders = pd.read_csv('data-dir/murder_offenders.csv')

#heatmap offenders victims
heatmap_offenders_victims_by_race = pd.read_csv('data-dir/heatmap_offenders_victims_by_race.csv')
heatmap_offenders_victims_by_sex = pd.read_csv('data/heatmap_offenders_victims_by_sex.csv')
heatmap_offenders_victims_by_race = heatmap_offenders_victims_by_race.drop(columns=['Total'])
heatmap_offenders_victims_by_sex = heatmap_offenders_victims_by_sex.drop(columns=['Total'])


def get_stacked_barplot():
    crimes = ["Violent Crime","Motor Vehicle Theft","Robbery","Aggravated Assult","Rape (Legacy Definition)"]
    fig = go.Figure()

    for crime in crimes:
        # Sort by crime and select top 5
        top_states = crimes_by_state.sort_values(by=crime, ascending=False).head(5)
        for state in top_states['State']:
            fig.add_trace(go.Bar(
                y=[crime],
                x=[top_states.loc[top_states['State'] == state, crime].values[0]],
                name=state,
                orientation='h',
                width=0.5,
            ))

    fig.update_layout(barmode='group',bargap=0.1)

    return fig

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
        ),
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


        ],width=4),
        dbc.Col([
            html.H1('Murder Victims Composition'),
            dcc.RadioItems(
            id='murder_victims_radiobox',
            options=[
                {'label': 'Ethnicity', 'value': 'ethnicity'},
                {'label': 'Sex', 'value': 'sex'}
            ],
            value='ethnicity'
            ),  
            dcc.Graph(id='murder_victims')
            
        ],width=4),
        dbc.Col([
            html.H1('Murder Offenders Composition'),
            dcc.RadioItems(
            id='murder_offenders_radiobox',
            options=[
                {'label': 'Ethnicity', 'value': 'ethnicity'},
                {'label': 'Sex', 'value': 'sex'},
                {'label':'Age','value':'age'}
            ],
            value='ethnicity'
            ),  
            dcc.Graph(id='murder_offenders')
            
        ],width=4),
    ]),
    dbc.Row([
        dbc.Col([
            html.H1("Heatmap of victims and offenders"),
            dcc.RadioItems(
            id='heatmap_victims_offenders_radiobox',
            options=[
                {'label': 'Ethnicity', 'value': 'ethnicity'},
                {'label': 'Sex', 'value': 'sex'},
            ],
            value='ethnicity'
            ), 
            dcc.Graph(id='heatmap_victims_offenders') 
        ],width=6),
        dbc.Col([
            html.H1("Stacked barplot of highest crimes"),
            dcc.Graph(figure=get_stacked_barplot())
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

@app.callback(
    Output('murder_victims','figure'),
    Input('murder_victims_radiobox','value')
)
def update_victims_piechart(feature):
    if feature == 'ethnicity':
        fig = px.pie(murder_victims, values='Total', names='Race', title='Murder Victims by Race')
    else:
        df_sex = pd.DataFrame({'sex': ['male', 'female','unknown'], 'total': [murder_victims['Male'].sum(), murder_victims['Female'].sum(),murder_victims['Unkown'].sum()]})
        fig = px.pie(df_sex, values='total', names='sex', title='Murder Victims by Sex')
    return fig 


@app.callback(
    Output('murder_offenders','figure'),
    Input('murder_offenders_radiobox','value')
)
def update_offenders_piechart(feature):

    races = ['White','Black','Other','Unknown','Hispanic or latino']
    sexes = ['Male','Female','Unknown Sex']
    if feature=='ethnicity':
        df_ethnicity= pd.DataFrame({
            'ethnicity':races,'total':[murder_offenders[i].sum() for i in races]
        })
        fig=px.pie(df_ethnicity,values='total',names='ethnicity',title='Murder Offenders by Ethnicity')
    elif feature=="sex":
        df_sex = pd.DataFrame({
            'sex':sexes, 'total':[murder_offenders[i].sum() for i in sexes]
        })
        fig=px.pie(df_sex,values='total',names='sex',title='Murder Offenders by Sex')
    
    else:
        fig = px.pie(murder_offenders,values='Total',names='Age',title="Murder Offenders by Age")
    return fig

@app.callback(
    Output('heatmap_victims_offenders', 'figure'),
    Input('heatmap_victims_offenders_radiobox', 'value')
)

def update_heatmap(feature):
    if feature == 'sex':

        grouped = heatmap_offenders_victims_by_sex.groupby('Sex of victim').sum()
        grouped = grouped.drop(columns=['Unnamed: 0'])
        fig = go.Figure(data=go.Heatmap(
        z=grouped.values,
        x=grouped.columns,
        y=grouped.index,
        hoverongaps = False))
                
        # Add labels
        fig.update_layout(
            title='Sex of Victims vs. Sex of Offenders',
            xaxis=dict(title='Sex of Offenders'),
            yaxis=dict(title='Sex of Victims')
        )
    else:
        
        grouped = heatmap_offenders_victims_by_race.groupby('Race of victim').sum()
        grouped = grouped.drop(columns=['Unnamed: 0'])
        fig = go.Figure(data=go.Heatmap(
        z=grouped.values,
        x=grouped.columns,
        y=grouped.index,
        hoverongaps = False))
                
        # Add labels
        fig.update_layout(
            title='Ethnicity of Victims vs. Ethnicity of Offenders',
            xaxis=dict(title='Ethnicity of Offenders'),
            yaxis=dict(title='Ethnicity of Victims')
        )

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
    


