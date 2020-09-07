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
    return dbc.Container(
            children=[
                dbc.Row(dbc.Col(dcc.Dropdown(
                    id="dropdown_country",
                    options=[{"label": x,"value": x} for x in brain['df_covid'].T.index],
                    value=['Germany', 'Italy'],
                    multi=True,
                    searchable=True,
                    ),
                )),
                dbc.Row(dbc.Col(
                    children=[
                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": 'Country', "id": 'Country'},
                                    {"name": 'Cases', "id": 'Cases'}],
                            sort_action='native',
                        )
                    ],
                    )
                ),
                dbc.Container(html.Div(children=[
                    dcc.Graph(id='graph1'),
                    dcc.Graph(id='graph2')
                    ],
                    hidden=True,
                    id='graph_div',
                    style={'border': '1px solid grey', 'margin-left': '-30px', 'margin-right': '-30px'}
                ))
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
    
    fig = px.line(get_data(country), y=country, x=get_data(country).index)
    fig.update_layout(
        title={'text': 'Cases', 'xanchor': 'center', 'x': 0.5},
        xaxis_title=None,
        yaxis_title=None,
        plot_bgcolor='rgba(0,0,0,0)',
        legend_title_text='',
        xaxis=dict(
            autorange=True,
            showgrid=True,
            ticks='',
            showticklabels=True
        ),
        yaxis=dict(
            autorange=True,
            showgrid=True,
            ticks='',
            showticklabels=True,
            gridcolor='lightgrey'
        ),
        legend=dict(
            orientation="v",
            bordercolor="Black",
            borderwidth=0.1,
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01),
    )
    return fig, False

def removeNegatives(df):
    df1 = df
    df1[df<0] = 0
    return df1

@app.callback(Output('graph2', 'figure'),
              [Input('dropdown_country', 'value')])
def display_graph(country):
    if not country:
        return px.line([0])
    if len(country) > 10:
        return px.line([0])

    fig = go.Figure(data=[
        go.Bar(
            name=c,
            x=get_data_frame().index,
            y=removeNegatives(get_data(c).diff())
        ) for c in country
    ])
    fig.update_layout(
        barmode='group',
        title={'text': 'Daily Cases', 'xanchor': 'center', 'x': 0.5},
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=None,
        yaxis_title=None,
        xaxis=dict(
            autorange=True,
            showgrid=True,
            ticks='',
            showticklabels=True
        ),
        yaxis=dict(
            autorange=True,
            showgrid=True,
            ticks='',
            showticklabels=True,
            gridcolor='lightgrey'
        ),
        legend=dict(
            orientation="v",
            bordercolor="Black",
            borderwidth=0.1,
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01),
    )
    return fig
