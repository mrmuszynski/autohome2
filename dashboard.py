import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from datetime import date, timedelta, datetime
import requests
import json
import sqlite3
import dash_table
from collections import OrderedDict
from glob import glob
from random import randint
import time
# def weather():
#     api_request = requests.get('https://api.weather.gov/gridpoints/LOX/158,50/forecast') 
#     weather_json = json.loads(api_request.text)


external_stylesheets = []

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


@app.callback(Output('dashboard_status', 'children'),
              Input('interval-component', 'n_intervals'))
def update_control_panel(n):
    files = glob('heartbeat/*')

    if len(files) > 1:
        return "LCARS • ERROR"
    elif len(files) == 0:
        return "LCARS • ONLINE"
    elif time.time() - float(files[0].split('/')[1]) > 3:
        return "LCARS • OFFLINE"
    else:
        return "LCARS • ONLINE"


@app.callback(Output('main_content', 'children'),
    [
    Input('top-left', 'n_clicks'),
    Input('bottom-left', 'n_clicks'),
    Input('top-right', 'n_clicks'),
    Input('bottom-right', 'n_clicks'),
    ])
def update_main_content(a,b,c,d):
    if a is None and b is None and c is None and d is None: raise PreventUpdate
    page = "Hello"
    if dash.callback_context.triggered[0]['prop_id'] == "top-left.n_clicks": page = "Lights"
    if dash.callback_context.triggered[0]['prop_id'] == "bottom-left.n_clicks": page = "Thermostat"
    if dash.callback_context.triggered[0]['prop_id'] == "top-right.n_clicks": page = "03"
    if dash.callback_context.triggered[0]['prop_id'] == "bottom-right.n_clicks": page = "04"
    return main_content_children(page)

# @app.callback(Output('thermostat_layer', 'children'),Input('bottom-left', 'n_clicks'))
# def update_main_content(n):
#     if n is None: raise PreventUpdate
#     return thermostat_layer("thermostat")



app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="format-detection" content="telephone=no">
        <meta name="format-detection" content="date=no">
        <link rel="stylesheet" type="text/css" href="static/lcars-classic.min.css">
        <link rel="preconnect" href="https://fonts.gstatic.com">
        <link href="https://fonts.googleapis.com/css2?family=Antonio:wght@100..700&display=swap" rel="stylesheet">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <script type="text/javascript" src="static/lcars.js"></script>
    </body>
</html>
'''

def data_cascade_row(row_no):
    return html.Div(className="row-"+str(row_no), children=[
        html.Div(className="grid", children=[str(randint(0,9999))]),
        html.Div(className="grid-2", children=[str(randint(0,9999))]),
        html.Div(className="grid", children=[str(randint(0,9999))]),
        html.Div(className="grid", children=[str(randint(0,9999))]),
        html.Div(className="grid", children=[str(randint(0,9999))]),
        html.Div(className="grid-4", children=[str(randint(0,9999))]),
        html.Div(className="grid-2", children=[str(randint(0,9999))]),
        html.Div(className="grid-2", children=[str(randint(0,9999))]),
        html.Div(className="grid-2", children=[str(randint(0,9999))]),
        html.Div(className="grid-1", children=[str(randint(0,9999))]),
        html.Div(className="grid-1", children=[str(randint(0,9999))]),
        html.Div(className="grid-1", children=[str(randint(0,9999))]),
        html.Div(className="grid-3", children=[str(randint(0,9999))]),
        html.Div(className="grid-3", children=[str(randint(0,9999))])
        ])

def data_cascade():
    return html.Div(className="data-cascade", id="default", children=[
        data_cascade_row(1),
        data_cascade_row(2),
        data_cascade_row(3),
        data_cascade_row(4),
        data_cascade_row(5),
        data_cascade_row(6)
        ])

def cascade_button_group():
    return html.Div(className="data-cascade-button-group", children=[
            html.Div(className="cascade-wrapper", children=[
                html.Div(className="data-cascade", children=[data_cascade()])
                ]),
            buttons_column_1(),
            buttons_column_2()
            ])

def buttons_column_1():
    return html.Div(className="button-col-1", children=[
            html.Div(className="button", id="top-left", children=[html.A(href="#", children=["Lights"])]),
            html.Div(className="button", id="bottom-left", children=[html.A(href="#", children=["Thermostat"])])
        ])

def buttons_column_2():
    return html.Div(className="button-col-2", children=[
            html.Div(className="button", id="top-right", children=[html.A(href="#", children=["03"])]),
            html.Div(className="button", id="bottom-right", children=[html.A(href="#", children=["04"])])
        ])

def left_frame_children():
    return html.Div(children=[
        html.Div(className="panel-3", children=['03', html.Span(className="hop", children="-"+str(randint(100000,999999)))]),
        html.Div(className="panel-4", children=['04', html.Span(className="hop", children="-"+str(randint(100000,999999)))]),
        html.Div(className="panel-5", children=['05', html.Span(className="hop", children="-"+str(randint(100000,999999)))]),
        html.Div(className="panel-6", children=['06', html.Span(className="hop", children="-"+str(randint(100000,999999)))]),
        html.Div(className="panel-7", children=['07', html.Span(className="hop", children="-"+str(randint(100000,999999)))]),
        html.Div(className="panel-8", children=['08', html.Span(className="hop", children="-"+str(randint(100000,999999)))]),
        html.Div(className="panel-9", children=['09', html.Span(className="hop", children="-"+str(randint(100000,999999)))]),
        html.Div(className="panel-10", children=['10', html.Span(className="hop", children="-"+str(randint(100000,999999)))])
        ])



def main_content_children(page):
    return [
            html.H1(page),
            html.P('Welcome to LCARS 8 Classic Theme.'),
            html.P('Live long and prosper.')
            ]


if __name__ == '__main__':

    # print('Loading Current States')
    # house.load_states()

    # print('Building App Layout')
    app.layout = html.Div(children=[
                    dcc.Interval(
                        id='interval-component',
                        interval=1*1000, # in milliseconds
                        n_intervals=0
                        ),
                    html.Div(className="wrap", children=[
                        html.Div(className="scroll-top", children=[html.A(id="scroll-top", href="", children=[html.Span(className="hop", children="screen"), "top"])]),
                        html.Div(className="left-frame-top", children=[
                            html.Div(className="panel-1", children=[html.A("LCARS", href="#")]),
                            html.Div(className="panel-2", children=["02", html.Span(className="hop", children="-26200")]),
                            ]),
                        html.Div(className="right-frame-top", children=[
                            html.Div(id="dashboard_status", className="banner", children=["LCARS • Online"]), 
                            cascade_button_group(),
                            html.Div(className="top-corner-bg", children=[
                                html.Div(className="top-corner")
                            ]),
                            html.Div(className="bar-panel", children=[
                                html.Div(className="bar-1"),
                                html.Div(className="bar-2"),
                                html.Div(className="bar-3"),
                                html.Div(className="bar-4"),
                                html.Div(className="bar-5"),
                                ])
                            ]),
                    ]),
                    html.Div(className="wrap", id="gap", children=[
                        html.Div(className="left-frame", children=[left_frame_children()]),
                        html.Div(className="right-frame", children=[
                            html.Div(className="bar-panel", children=[
                                html.Div(className="bar-6"),
                                html.Div(className="bar-7"),
                                html.Div(className="bar-8"),
                                html.Div(className="bar-9"),
                                html.Div(className="bar-10"),
                                ]),
                            html.Div(className="corner-bg", children=[
                                html.Div(className="corner")
                                ]),
                            html.Div(id="main_content", className="content", children=
                                main_content_children("Hello")
                                ),
                            html.Div(className="lcars-bar-slice-top"),
                            html.Div(className="lcars-bar", children=[
                                html.Div(className="lcars-bar-inner", children=[
                                    html.Div(className="lcars-bar-cutout")
                                    ])
                                ]),
                            html.Div(className='lcars-bar-slice-bottom')

                        ]),
                    ])
            ])
    
    # print('Adding Callbacks')
    # house.add_callbacks(app)

    
    app.run_server(host='0.0.0.0', debug=True)
