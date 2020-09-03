from app import app
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from brain_plasma import Brain
import pandas as pd
import dash_table

layout = html.Div(id='app1-module1-layout')

brain = Brain()

def createDataset(colStr, colName, matchValue):
    if 'df' in Brain.object_map(brain):
        df = brain['df']
        d = df.filter(regex=colStr).dropna(how='all').head(1000)
        if colName and matchValue:
            d = d[d[colName] == int(matchValue)]
        return d
    else:
        return pd.DataFrame()


@app.callback(
    Output('app1-module1-layout', 'children'),
    [Input('memory-store', 'data')])
def update(parameter_list):
    return html.Div([
        html.H5('App 1 - Module 1'),
        dcc.Input(  placeholder='Enter column regex ...',
                    type='text',
                    id='app1-module1-input1'),
        dcc.Input(  placeholder='Enter column name ...',
                    type='text',
                    id='app1-module1-input2'),
        dcc.Input(  placeholder='Enter match value ...',
                    type='text',
                    id='app1-module1-input3'),
        dcc.Loading(
        id="loading-2",
        children=[html.Div(dash_table.DataTable(
            id='table',
            style_data={'whiteSpace': 'normal'},
            style_header= {
                "whiteSpace": "normal",
                "overflow": "hidden",
                "textOverflow": "ellipsis",
                'height': 'auto',
                'fontSize':10,
                'font-family':'sans-serif',
                'font-weight': 'bold',
                'align': 'left'
            },
            style_table={
                'overflowX': 'scroll',
                'overflowY': 'scroll',
                'border': 'thin lightgrey solid',
                'height': 'auto'},
            style_cell={
                'fontSize':14,
                'font-family':'courier',
                'height': 'auto',
                'minWidth': '100px',
                'maxWidth': '200px',
            },
            fixed_rows={ 'headers': True, 'data': 0 },
            style_data_conditional=[
            {
               'if': {'row_index': 'odd'},
               'backgroundColor': 'rgb(248, 248, 230)'
            }],
            
            fixed_columns={'headers': True, 'data':0},
            merge_duplicate_headers=True,
            )
            ),
            ],
            type='circle'
            ),
        ])


@app.callback(
    [Output('table', 'columns'), Output('table', 'data')],
    [Input('app1-module1-input1', 'value')],
    [State('app1-module1-input2', 'value'),
     State('app1-module1-input3', 'value')]
)
def onType(regex, colName, matchValue):
    df = createDataset(regex, colName, matchValue)
    columns=(
            [{'id': p, 'name': [p.split('.', 1)[0], p.split('.', 1)[1].replace('.', '-')]} for p in df.to_dict().keys()])
    return columns, df.to_dict('records')
