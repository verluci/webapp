import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import datetime
import json
import MySQLdb as dbs
import pandas as pd

def test():
    with open("settings.json", "r") as jsonFile:
        settings = json.load(jsonFile)
    db = dbs.connect(host="localhost", user="root", db="project21")
    df = pd.read_sql('SELECT * FROM data ORDER BY time DESC LIMIT 10080', con=db)
    count = int(pd.read_sql('SELECT COUNT(time) FROM data', con=db)['COUNT(time)'][0])
    shouldUpdate = False
    app = dash.Dash()
    app.css.append_css({
        "external_url": "https://rawgit.com/verluci/public_stuff/master/plotly_webapp_style.css"
    })
    app.layout = html.Div(style={}, children=[
        html.Div([
            html.Div(className='container', children=[
                #header, titel
                html.Section(className='header', style={'padding-bottom': 50}, children=[
                    html.H1(children='Test'),
                ]),
                #body
                html.Div(className='row', children=[
                    #blok 1
                    html.Div(className='eight columns', style={'padding': 15, 'background-color': 'LightSlateGrey '}, children=[
                        html.Div(children=[
                            html.H3('Temperatuur'),
                            #grafiek temp
                            dcc.Graph(
                                animate='true',
                                id='temp-graph',
                                figure={
                                    'data': [
                                        go.Scatter(
                                            x=df['time'],
                                            y=df['temperatuur'],
                                            mode='lines'
                                        )
                                    ],
                                }
                            ),
                            dcc.Interval(
                                id='temp-interval',
                                interval=5000),
                        ]),
                        dcc.Slider(
                            id='temp-slider',
                            min=-30,
                            max=60,
                            step=1,
                            value=settings["settings"]["temp"],
                            marks={
                                -30: "-30c",
                                60: "60c"
                            }
                        ),
                        html.Br(),
                        html.Div(id='temp-output-container')
                    ]),
                    #blok 2
                    html.Div(className='four columns', style={'padding': 15, 'background-color': 'LightSlateGrey '}, children=[
                        html.Div(className='manualButton', children=[
                            #manual knop
                            dcc.RadioItems(
                                id='manualMode',
                                options=[
                                    {'label': 'Handmatige modus', 'value': 'True'},
                                    {'label': 'Automatische modus', 'value': 'False'},
                                ],
                                value=settings['settings']['manual']
                            ),
                            html.Div(id='manual-output-container'),
                            html.P('De huidige temperatuur is'),
                            html.P('De huidige lichtintensiteit is')
                        ]),
                        html.Div(children=[
                            dcc.Slider(
                                id='pos-slider',
                                min=0,
                                max=settings["settings"]["maxpos"],
                                step=1,
                                value=settings["settings"]["pos"],
                                marks={(i*5): '{}'.format(5 * i) for i in range(int(settings["settings"]["maxpos"]/5+1))},
                            ),
                            html.Br(),
                            html.Div(id='pos-output-container')
                        ]),
                    ]),
                    #blok 3
                    html.Div(className='eight columns', style={'padding': 15, 'background-color': 'LightSlateGrey '}, children=[
                        #grafiek licht
                        html.Div(children=[
                            dcc.Graph(
                                animate='true',
                                id='licht-graph',
                                figure={
                                    'data': [
                                        go.Scatter(
                                            x=df['time'],
                                            y=df['licht'],
                                            mode='lines'
                                        )
                                    ],
                                }
                            ),
                            dcc.Interval(
                                id='licht-interval',
                                interval=5000),
                        ]),
                        html.Div(children=[
                            dcc.Slider(
                                id='licht-slider',
                                min=0,
                                max=100,
                                step=1,
                                value=settings["settings"]["licht"],
                                marks={(i*10): '{}'.format(10 * i) for i in range(11)}
                            ),
                            html.Br(),
                            html.Div(id='licht-output-container')
                        ])
                    ])
                ])
            ])
        ])
    ])

    #@app.callback(
    #    dash.dependencies.Output('changeToButton', 'children'),
    #    [dash.dependencies.Input('changeToButton', 'children')]
    #)

    @app.callback(
        dash.dependencies.Output('manual-output-container', 'children'),
        [dash.dependencies.Input('manualMode', 'value')])
    def update_output(value):
        if(value == True):
            hand = "handmatige"
        else:
            hand = "automatische"
        settings["settings"]["manual"] = value
        with open("settings.json", "w") as jsonFile:
            json.dump(settings, jsonFile)
            jsonFile.truncate()
        return 'momenteel {} modus'.format(hand)

    @app.callback(
        dash.dependencies.Output('licht-output-container', 'children'),
        [dash.dependencies.Input('licht-slider', 'value')])
    def update_output(value):
        settings["settings"]["licht"] = value
        with open("settings.json", "w") as jsonFile:
            json.dump(settings, jsonFile)
            jsonFile.truncate()
        return 'Het doek gaat omlaag bij een lichtpercetage van {}%'.format(value)

    @app.callback(
        dash.dependencies.Output('temp-output-container', 'children'),
        [dash.dependencies.Input('temp-slider', 'value')])
    def update_output(value):
        settings["settings"]["temp"] = value
        with open("settings.json", "w") as jsonFile:
            json.dump(settings, jsonFile)
            jsonFile.truncate()
        return 'De temperatuurtreshold is {}c'.format(value)

    @app.callback(
        dash.dependencies.Output('pos-output-container', 'children'),
        [dash.dependencies.Input('pos-slider', 'value')])
    def update_output(value):
        settings["settings"]["pos"] = value
        with open("settings.json", "w") as jsonFile:
            json.dump(settings, jsonFile)
            jsonFile.truncate()
        return 'Zet het doek op {}cm van de grond'.format(value)

    @app.callback(Output('temp-graph', 'figure'),
                  events=[Event('temp-interval', 'interval')])
    def update_graph_live():
        nonlocal count
        nonlocal df
        nonlocal shouldUpdate
        dbn = dbs.connect(host="localhost", user="root", db="project21")
        newcount = pd.read_sql('SELECT COUNT(time) FROM data', con=dbn)['COUNT(time)'][0]
        toreadout = newcount-count
        if(toreadout > 0):
            shouldUpdate = True
            df2 = pd.read_sql('SELECT * FROM data ORDER BY time DESC LIMIT %s' % toreadout, con=dbn)
            count = newcount
            df = df.append(df2, ignore_index=True)
            figure = {
                'data': [
                    go.Scatter(
                        x=df['time'],
                        y=df['temperatuur'],
                        mode='lines'
                    )
                ],
            }
            return figure

    @app.callback(Output('licht-graph', 'figure'),
                  events=[Event('licht-interval', 'interval')])
    def update_graph_live():
        nonlocal shouldUpdate
        if(shouldUpdate == True):
            shouldUpdate = False
            figure = {
                'data': [
                    go.Scatter(
                        x=df['time'],
                        y=df['licht'],
                        mode='lines'
                    )
                ],
            }
            return figure


    app.run_server(debug=True)

test()
