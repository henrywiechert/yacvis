from app import app
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
from brain_plasma import Brain
import plotly.express as px

brain = Brain()

def get_country_df(country):
    df = brain['df_covid'].tail(1).T
    if not country:
        return df
    else:
        return df.filter(country, axis=0)

def get_data(country):
    df = brain['df_covid']
    print(df[country])
    return df[country]

def layout():
    return html.Div(
        children=[
            dcc.Dropdown(
                id="dropdown_country",
                options=[{"label":x,"value":x} for x in brain['df_covid'].T.index],
                value=['Germany/', 'Italy/'],
                multi=True),
            html.Div(
                children=[
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": 'Country', "id": 'Country'},
                                 {"name": 'Cases', "id": 'Cases'}])
                ],
                style={'margin-top': 10, 'margin-bottom': 10, 'margin-left': 20, 'margin-right': 20},
            ),
            html.Div(id='graph_div1', children=[dcc.Graph(id='graph1')], hidden=True),
            html.Div(id='graph_div2', children=[dcc.Graph(id='graph2')], hidden=True),
        ],
    )


@app.callback(Output('table', 'data'),
              [Input('dropdown_country', 'value')])
def display_table(country):
    return [{'Country': k, 'Cases': v[0]} for k, v in get_country_df(country).iterrows()]


@app.callback([Output('graph1', 'figure'),
               Output('graph_div1', 'hidden')],
              [Input('dropdown_country', 'value')])
def display_graph(country):
    if not country:
        return px.line([0]), True
    if len(country) > 10:
        return px.line([0]), True
    return px.line(get_data(country), y=country, x=get_data(country).index), False


@app.callback([Output('graph2', 'figure'),
               Output('graph_div2', 'hidden')],
              [Input('dropdown_country', 'value')])
def display_graph(country):
    if not country:
        return px.line([0]), True
    if len(country) > 10:
        return px.line([0]), True
    return px.line(get_data(country).diff(), y=country, x=get_data(country).index), False
