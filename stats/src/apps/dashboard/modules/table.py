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
    return df[country]

def layout():
    return html.Div([
        dcc.Dropdown(
            id="dropdown_country",
            options=[{"label":x,"value":x} for x in brain['df_covid'].T.index],
            value=['Germany/', 'Italy/'],
            multi=True),
        dash_table.DataTable(
            id='table',
            columns=[{"name": 'Country', "id": 'Country'},
                    {"name": 'Cases', "id": 'Cases'}]
        ),
        html.Div(id='graph_div', children=[dcc.Graph(id='graph')], hidden=True),
        ])


@app.callback(Output('table', 'data'),
              [Input('dropdown_country', 'value')])
def display_table(country):
    return [{'Country': k, 'Cases': v[0]} for k, v in get_country_df(country).iterrows()]


@app.callback([Output('graph', 'figure'),
               Output('graph_div', 'hidden')],
              [Input('dropdown_country', 'value')])
def display_table(country):
    if not country:
        return px.line([0]), True
    if len(country) > 10:
        return px.line([0]), True
    return px.line(get_data(country), y=country), False
