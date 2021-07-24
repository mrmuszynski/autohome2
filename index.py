import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from datetime import date, timedelta, datetime
import requests
import json
import dash_table
from collections import OrderedDict
from glob import glob
# def weather():
#     api_request = requests.get('https://api.weather.gov/gridpoints/LOX/158,50/forecast') 
#     weather_json = json.loads(api_request.text)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
'control_panel.css'
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# def write_heartbeat():
#     open('heartbeat/' + str((datetime.now()-datetime(1970,1,1)).total_seconds()), "a").close()
#     return

# def check_stale_heartbeats():
#     heartbeat_messages = glob('heartbeat/*')
#     return heartbeat_messages

@app.callback(Output('live-update', 'children'),
              Input('interval-component', 'n_intervals'))
def update_control_panel(n):
    now = datetime.now()
    children = [
        html.H1(children='192 W Terrace. Welcome Home.'),
        html.H2(children=datetime.now()),
        # house.control_panel(),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
            )
        ]
    return children



if __name__ == '__main__':

    print('Loading Current States')
    # house.load_states()

    print('Building App Layout')
    app.layout = html.Div(id="live-update", children=[
            html.H1(children='192 W Terrace. Welcome Home.'),
            html.H2(children=datetime.now()),
            # house.control_panel(),
            dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
                )
            ])
    # print('Adding Callbacks')
    # house.add_callbacks(app)

    
    app.run_server(host='0.0.0.0', debug=True)
