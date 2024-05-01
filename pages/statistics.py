import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State

dash.register_page(
    __name__,
    name = "Crime Statistics", 
    title = "Crime Statistics | Dashboard",
    path="/statistics")

crimes_by_state = pd.read_csv('data-dir/crime_data_by_state.csv')

#murder victims
murder_victims = pd.read_csv('data-dir/murder_victims.csv')

#arrests by crimes and ethnicity
arrests_by_crime_ethnicity = pd.read_csv('data-dir/arrests_by_crime_ethnicity_T.csv')

#murder offenders
murder_offenders = pd.read_csv('data-dir/murder_offenders.csv')

#heatmap offenders victims
heatmap_offenders_victims_by_race = pd.read_csv('data-dir/heatmap_offenders_victims_by_race.csv')
heatmap_offenders_victims_by_sex = pd.read_csv('data-dir/heatmap_offenders_victims_by_sex.csv')
heatmap_offenders_victims_by_race = heatmap_offenders_victims_by_race.drop(columns=['Total'])
heatmap_offenders_victims_by_sex = heatmap_offenders_victims_by_sex.drop(columns=['Total'])

def get_stacked_barplot():
    crimes = ["Violent Crime","Rape (Legacy Definition)","Robbery","Aggravated Assult","Motor Vehicle Theft"]
    fig = go.Figure()

    # Define a color map for the states
    states_names = crimes_by_state['State'].unique()
    # remove nan from states_names
    states_names = states_names[~pd.isna(states_names)]
    # make colour map for all the states
    color_map = {}
    for i in range(len(states_names)):
        # make px color map
        color_map[states_names[i]] = px.colors.qualitative.Plotly[i%len(px.colors.qualitative.Plotly)]

    # Keep track of states that have already been added to the legend
    added_states = set()

    for crime in crimes:
        # Sort by crime and select top 5
        top_states = crimes_by_state.sort_values(by=crime, ascending=False).head(5)
        for state in top_states['State']:
            fig.add_trace(go.Bar(
                y=[crime],
                x=[top_states.loc[top_states['State'] == state, crime].values[0]],
                name=state[0] + state[1:].lower(),
                orientation='h',
                width=0.4,
                marker_color=color_map[state] if state !="TEXAS" else "red",
                showlegend=state not in added_states  # Only show in legend if state has not been added yet
            ))
            added_states.add(state)  # Add state to added_states set

    #Change legend such that each state is only shown once
    fig.update_layout(barmode='group',legend_title_text='States',legend_traceorder='reversed',bargroupgap=0.5, title='<b>Stacked barplot of highest crimes</b>')
    fig.update_layout(margin=dict(l=30, r=40, t=50, b=30))
    return fig

layout = html.Div([
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='arrests_by_crime_ethnicity', style={'width': '100%', 'height': '100%', 'margin-bottom': '20px'}),
                            dcc.Dropdown(
                                options=['White', 'Black', 'American or Alaskan Native', 'Asian', 'Hawaiian or North Pacific Ilander'],
                                value=['White'],
                                id='crime_ethnicity_dd',
                                multi=True,
                                searchable=False,
                                placeholder="Choose Ethnicity"
                            ),
                        ], style={'display': 'flex', 'flexDirection': 'column', 'height': '100%'})
                    ], style={'height': '100%', 'box-shadow': '5px 5px 5px 0px rgba(255,255,255,0.25)'}),
                ], style={'width': '80%', 'height': '50%'}),

                dbc.Row([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                dcc.Graph(id='heatmap_victims_offenders', style={'width': '100%', 'height': '100%', 'padding-right': '20px'}),
                            ], style={'width': '75%'}),
                            html.Div([
                                html.Div(style={'borderLeft': '1px solid grey', 'height': '100%'}),
                                html.Div([
                                    html.Label(['Choose type:'], style={'fontSize': 'smaller', "text-align": "center", }),
                                    dcc.RadioItems(
                                        id='heatmap_victims_offenders_radiobox',
                                        options=[
                                            {'label': html.Span('Ethnicity', style={'margin-right': '20px', 'margin-bottom': '10px', 'margin-left': '10px'}), 'value': 'ethnicity'},
                                            {'label': html.Span('Sex', style={'margin-left': '10px'}), 'value': 'sex'},
                                        ],
                                        value='ethnicity',
                                    ),
                                ], style={'margin-left': '20px'}),
                            ], style={'width': '25%', 'display': 'flex'})
                        ], style={'display': 'flex', 'justifyContent': 'space-between', 'height': '100%'}),
                    ], style={'height': '100%', 'box-shadow': '5px 5px 5px 0px rgba(255,255,255,0.25)'})
                ], style={'width': '80%', 'height': '50%'}),
                
            ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '30px', 'justifyContent': 'center', 'alignItems': 'end', 'width': '40%', 'height': '80vh'}),
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='murder_pie', style={'width': '80%', 'height': '100%', 'margin-right': '20px'}),
                            html.Div(style={'borderLeft': '1px solid grey', 'height': '100%'}),
                            html.Div([
                                html.Div([
                                    html.Label(['Choose type:'], style={'fontSize': 'smaller', "text-align": "center", }),
                                    dcc.RadioItems(
                                        id='murder_pie_radiobox',
                                        options=[
                                            {'label': html.Span('Victims', style={'margin-right': '20px', 'margin-bottom': '10px', 'margin-left': '10px'}), 'value': 'victims'},
                                            {'label': html.Span('Offenders', style={'margin-left': '10px'}), 'value': 'offenders'},
                                        ],
                                        value='victims',
                                    ),
                                ], style={'width': '100%'}),
                                html.Div([
                                    html.Label(['Group by:'], style={'fontSize': 'smaller', "text-align": "center", }),
                                    dcc.Dropdown(
                                        id='murder_pie_dd',
                                        options=[
                                            {'label': 'Ethnicity', 'value': 'ethnicity'},
                                            {'label': 'Sex', 'value': 'sex'},
                                            {'label':'Age', 'value':'age', 'disabled': True}
                                        ],
                                        value='ethnicity'
                                    )
                                ], style={'width': '100%'})
                            ], style={'display': 'flex', 'flexDirection': 'column', 'width':'30%', 'justifyContent': 'start', 'alignItems': 'start', 'gap': '20px', 'padding-left': '20px', 'padding-right': '10px'})
                        ], style={'display': 'flex', 'height': '100%'})
                    ], style={'height': '100%', 'box-shadow': '5px 5px 5px 0px rgba(255,255,255,0.25)'}),
                ], style={'width': '80%', 'height': '50%'}),
                
                dbc.Row([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(figure=get_stacked_barplot(), style={'width': '100%', 'height': '100%'})
                        ])
                    ], style={'height': '100%', 'box-shadow': '5px 5px 5px 0px rgba(255,255,255,0.25)'})
                ], style={'width': '80%', 'height': '50%'}),
            ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '30px', 'justifyContent': 'center', 'alignItems': 'start', 'width': '40%', 'height': '80vh'})
        ], style={'display': 'flex', 'padding': '30px', 'gap': '50px', 'width': '100%', 'height': '92vh', 'backgroundImage': 'url(\'assets/bg/w15.jpg\')', 'backgroundPosition': "50% 50%", 'backgroundSize': 'cover'})

@callback(
    Output('arrests_by_crime_ethnicity', 'figure'),
    Input('crime_ethnicity_dd', 'value')
)
def update_radarplot(races):
    cols = ['Murder and Manslaughter','Rape','Robbery','Aggravated Assault','Burglary','Larceny-theft']
    fig = go.Figure()
    arrests_by_crime_ethnicity[cols] = (arrests_by_crime_ethnicity[cols] - arrests_by_crime_ethnicity[cols].min()) / (arrests_by_crime_ethnicity[cols].max() - arrests_by_crime_ethnicity[cols].min())
    for i in range(len(races)):
        df_temp = arrests_by_crime_ethnicity[arrests_by_crime_ethnicity['Type of crime']==races[i]]
        df_temp = df_temp[cols]
        l_name = races[i]
        if races[i] == 'Hawaiian or North Pacific Ilander':
            l_name = 'Hawaiian/NPI'
        elif races[i] == 'American or Alaskan Native':
            l_name = 'American/Alaskan'
        fig.add_trace(go.Scatterpolar(
            r= df_temp.values.reshape(1,-1)[0],
            theta= cols,
            fill='toself',
            name=l_name
        ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title='<b>Arrests by Crime and Ethnicity</b>'
    )
    fig.update_layout(margin=dict(l=0, r=50, t=45, b=30))

    return fig

@callback(
    Output('murder_pie','figure'),
    [Input('murder_pie_radiobox','value'),
     Input('murder_pie_dd','value')]
)
def update_victims_piechart(type, grouped_by):
    if type == 'victims':
        if grouped_by == 'ethnicity':
            fig = px.pie(murder_victims, values='Total', names='Race', title='<b>Murder Victims by Race</b>')
        else:
            df_sex = pd.DataFrame({'sex': ['male', 'female','unknown'], 'total': [murder_victims['Male'].sum(), murder_victims['Female'].sum(),murder_victims['Unkown'].sum()]})
            fig = px.pie(df_sex, values='total', names='sex', title='<b>Murder Victims by Sex</b>')
        fig.update_layout(margin=dict(l=20, r=0, t=40, b=10))
        return fig 
    else:
        races = ['White','Black','Other','Unknown','Hispanic or latino']
        sexes = ['Male','Female','Unknown Sex']
        if grouped_by=='ethnicity':
            df_ethnicity= pd.DataFrame({
                'ethnicity':races,'total':[murder_offenders[i].sum() for i in races]
            })
            fig=px.pie(df_ethnicity,values='total',names='ethnicity',title='<b>Murder Offenders by Ethnicity</b>')
        elif grouped_by=="sex":
            df_sex = pd.DataFrame({
                'sex':sexes, 'total':[murder_offenders[i].sum() for i in sexes]
            })
            fig=px.pie(df_sex,values='total',names='sex',title='<b>Murder Offenders by Sex</b>')
        
        else:
            fig = px.pie(murder_offenders,values='Total',names='Age',title="<b>Murder Offenders by Age</b>")
        fig.update_layout(margin=dict(l=20, r=0, t=40, b=10))
        return fig

@callback(
    Output('murder_pie_dd', 'options'),
    Input('murder_pie_radiobox', 'value'),
    State('murder_pie_dd', 'options')
)
def update_dropdown_options(type, existing_options):
    if type == 'victims':
        # Initial call, disable one option
        return [{'label': 'Ethnicity', 'value': 'ethnicity'},
                {'label': 'Sex', 'value': 'sex'},
                {'label':'Age', 'value':'age', 'disabled': True}]
    else:
        # Enable all options after button click
        return [{'label': 'Ethnicity', 'value': 'ethnicity'},
                {'label': 'Sex', 'value': 'sex'},
                {'label':'Age', 'value':'age', 'disabled': False}]

@callback(
    Output('murder_pie_dd', 'value'),
    Input('murder_pie_radiobox', 'value'),
    State('murder_pie_dd', 'value')
)
def update_radio_items(type, grouped_by):
    if type == 'victims' and grouped_by == 'age':
        return 'ethnicity'
    return grouped_by

@callback(
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
            title='<b>Victims\' vs. Offenders\' Sex</b>',
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
        hoverongaps = False,
        colorbar=dict(thickness=10)))
                
        # Add labels
        fig.update_layout(
            title='<b>Victims\' vs. Offenders\' Ethnicity</b>',
            xaxis=dict(title='Ethnicity of Offenders'),
            yaxis=dict(title='Ethnicity of Victims')
        )

        
    fig.update_layout(margin=dict(l=0, r=40, t=50, b=0))
    return fig