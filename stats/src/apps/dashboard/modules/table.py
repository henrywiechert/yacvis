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

def get_country_df_cases(country):
    df = brain['df_covid_cases'].tail(1).T
    if not country:
        return df
    else:
        return df.filter(country, axis=0)

def get_data_cases(country):
    df = brain['df_covid_cases']
    return df[country]

def get_data_frame_cases():
    df = brain['df_covid_cases']
    return df

def get_country_df_deaths(country):
    df = brain['df_covid_deaths'].tail(1).T
    if not country:
        return df
    else:
        return df.filter(country, axis=0)

def get_data_deaths(country):
    df = brain['df_covid_deaths']
    return df[country]

def get_data_frame_deaths():
    df = brain['df_covid_deaths']
    return df

def layout():
    return dbc.Container(
            children=[
                dbc.Row(dbc.Col(dcc.Dropdown(
                    id="dropdown_country",
                    options=[{"label": x,"value": x} for x in brain['df_covid_cases'].T.index],
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
                dbc.Tabs([
                    dbc.Tab(
                        dbc.Container(html.Div(children=[
                            dcc.Graph(id='graph1'),
                            dcc.Graph(id='graph2')
                            ],
                            hidden=True,
                            id='graph_div',
                        )),
                        label='Cases'
                    ),
                    dbc.Tab(
                        dbc.Container(html.Div(children=[
                            dcc.Graph(id='graph3'),
                            dcc.Graph(id='graph4')
                            ],
                            hidden=True,
                            id='graph_div2',
                        )),
                        label='Deaths'
                    )]
                )
            ],
    )


@app.callback(Output('table', 'data'),
              [Input('dropdown_country', 'value')])
def display_table(country):
    return [{'Country': k, 'Cases': v[0]} for k, v in get_country_df_cases(country).iterrows()]


@app.callback([Output('graph1', 'figure'),
               Output('graph_div', 'hidden')],
              [Input('dropdown_country', 'value')])
def display_graph(country):
    if not country:
        return px.line([0]), True
    if len(country) > 10:
        return px.line([0]), True
    
    fig = px.line(get_data_cases(country), y=country, x=get_data_cases(country).index)
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
            x=get_data_frame_cases().index,
            y=removeNegatives(get_data_cases(c).diff())
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

@app.callback([Output('graph3', 'figure'),
               Output('graph_div2', 'hidden')],
              [Input('dropdown_country', 'value')])
def display_graph_deaths(country):
    if not country:
        return px.line([0]), True
    if len(country) > 10:
        return px.line([0]), True
    
    fig = px.line(get_data_deaths(country), y=country, x=get_data_deaths(country).index)
    fig.update_layout(
        title={'text': 'Deaths', 'xanchor': 'center', 'x': 0.5},
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

@app.callback(Output('graph4', 'figure'),
              [Input('dropdown_country', 'value')])
def display_graph(country):
    if not country:
        return px.line([0])
    if len(country) > 10:
        return px.line([0])

    fig = go.Figure(data=[
        go.Bar(
            name=c,
            x=get_data_frame_deaths().index,
            y=removeNegatives(get_data_deaths(c).diff())
        ) for c in country
    ])
    fig.update_layout(
        barmode='group',
        title={'text': 'Daily Deaths', 'xanchor': 'center', 'x': 0.5},
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
