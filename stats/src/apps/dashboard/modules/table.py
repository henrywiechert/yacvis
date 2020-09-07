from app import app
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
from brain_plasma import Brain
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


brain = Brain()

def get_country_df(country):
    df = brain['df_covid'].tail(1).T
    if not country:
        return df
    else:
        return df.filter(country, axis=0)

def get_data(country):
    df = brain['df_covid']
    return df[country]

def get_data_frame():
    df = brain['df_covid']
    return df

def layout():
    return html.Div(
            children=[
                dbc.Row(dbc.Col(dcc.Dropdown(
                    id="dropdown_country",
                    options=[{"label":x,"value":x} for x in brain['df_covid'].T.index],
                    value=['Germany', 'Italy'],
                    multi=True), width={'size': 10, 'offset': 1})
                ),
                dbc.Row(dbc.Col(
                    children=[
                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": 'Country', "id": 'Country'},
                                    {"name": 'Cases', "id": 'Cases'}],
                            sort_action='native')
                    ], width={'size': 10, 'offset': 1})
                    #style={'margin-top': 10, 'margin-bottom': 10, 'margin-left': 20, 'margin-right': 20},
                ),
                html.Div(
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(id='graph1')),
                            dbc.Col(dcc.Graph(id='graph2'))
                        ]
                    ),
                    hidden=True,
                    id='graph_div',
                )
            ],
    )


@app.callback(Output('table', 'data'),
              [Input('dropdown_country', 'value')])
def display_table(country):
    return [{'Country': k, 'Cases': v[0]} for k, v in get_country_df(country).iterrows()]


@app.callback([Output('graph1', 'figure'),
               Output('graph_div', 'hidden')],
              [Input('dropdown_country', 'value')])
def display_graph(country):
    if not country:
        return px.line([0]), True
    if len(country) > 10:
        return px.line([0]), True
    return px.line(get_data(country), y=country, x=get_data(country).index), False


@app.callback(Output('graph2', 'figure'),
              [Input('dropdown_country', 'value')])
def display_graph(country):
    if not country:
        return px.line([0])
    if len(country) > 10:
        return px.line([0])

    fig = go.Figure(data=[
        go.Bar(name=c, x=get_data_frame().index, y=get_data(c).diff()) for c in country
    ])
    fig.update_layout(barmode='group')
    return fig
