import os

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
from apps.app1 import app1
from apps.dashboard import dashboard
from apps.sysinfo import sysinfo

from config import config

GIT_SHA = os.environ.get('GIT_SHA') or 'unknown'
GIT_STATUS = os.environ.get('GIT_STATUS') or 'unknown'

navbar = dbc.Row(dbc.Col(
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Dashboard", href="/apps/dashboard")),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="More",
                children=[
                    dbc.DropdownMenuItem("Dashboard", href='/apps/dashboard'),
                    dbc.DropdownMenuItem("SysInfo", href='/apps/sysinfo'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("App 1", href='/apps/app1'),
                ],
            ),
        ],
        brand="Yet Another Covid19 Visualization - YACVIS",
        sticky="left",
        color="primary",
    ),
    #width=12,
))


app.layout = dbc.Container(html.Div(
    children=[
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='memory-store', storage_type='session'),
        navbar,
        html.Div(id='page-content'),
        html.Div(
            'GIT revision: ' + GIT_SHA + ' (' + GIT_STATUS + ')' + ' ' + dcc.__version__,
            style={ 'color': 'white',
                    'fontSize': 14,
                    'text-align': 'center',
                    'margin-top': 50,
                    'background-color': 'lightgray' }) ])
)

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/dashboard':
        return dashboard.layout
    elif pathname == '/apps/sysinfo':
        return sysinfo.layout
    else:
        return dashboard.layout

if __name__ == '__main__':
    app.run_server(debug=config.debug, host=config.host, port=config.port)
