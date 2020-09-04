import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
from dash.exceptions import PreventUpdate
from .modules import table
from app import app

layout = html.Div(id='dashboard-layout')

@app.callback(
    Output('dashboard-layout', 'children'),
    [Input('memory-store', 'data')])
def update(parameter_list):
    return html.Div([
        table.layout()
        ])
