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
    df = pd.read_sql('SELECT * FROM data ORDER BY time DESC LIMIT %s' % settings["settings"]["limit"], con=db)
    count = int(pd.read_sql('SELECT COUNT(time) FROM data', con=db)['COUNT(time)'][0])
    dfl = pd.read_sql('SELECT * FROM superlicht LIMIT 7', con=db)
    licht = 0
    totaal = 0
    for i in range(7):
        licht = licht + dfl['zonnig'].iloc[i]
        totaal = totaal + dfl['total_licht'].iloc[i]
    shouldUpdate = False
    auto = False
    def updateAuto():
        nonlocal auto
        if settings['settings']['manual'] == False:
            auto = False
            print("aardapple")
        elif settings['settings']['manual'] == True:
            auto = True
            print("tomaata")
    updateAuto()

    app = dash.Dash()
    colors = {
        'background': '#0a0908',
        'text': '#BBBBBB',
        'graphbg': '#201E1C'
    }
    app.css.append_css({
        "external_url": "https://rawgit.com/verluci/public_stuff/master/plotly_webapp_style.css"
    })
    app.title = "Smart zonnescherm"
    app.layout = html.Div(style={}, children=[
        html.Div([
            html.Div(className='container', children=[
                #header, titel
                html.Section(className='header', style={'padding-bottom': 50}, children=[
                    html.H1(children='Smart zonnescherm'),
                ]),
                #body
                html.Div(className='row', style={'margin': 5}, children=[
                    #blok 1
                    html.Div(className='eight columns', style={'padding': 15, 'background-color': '#0a0908', 'color': '#BBBBBB'}, children=[
                        html.Div(children=[
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
                                    'layout': {
                                        'plot_bgcolor': colors['graphbg'],
                                        'paper_bgcolor': colors['background'],
                                        'font': {
                                            'color': colors['text']},
                                        'margin': {
                                            't': 30,
                                            'l': 25,
                                            'r': 15
                                        }
                                    },
                                },

                            ),
                            dcc.Interval(
                                id='temp-interval',
                                interval=3000),
                        ]),
                        html.Div(style={}, children=[
                            dcc.Slider(

                                id='temp-slider',
                                min=-30,
                                max=60,
                                step=1,
                                value=settings["settings"]["temp"],
                                marks={((i*10)-30): '{}'.format((i * 10)-30) for i in range(10)
                                },
                            ),
                            html.Br(),
                            html.Div(id='temp-output-container')
                        ]),
                    ]),
                    #blok 2
                    html.Div(className='four columns', style={'padding': 15, 'background-color': '#0a0908', 'color': '#BBBBBB'}, children=[
                        html.Div(className='manualButton', children=[
                            #manual knop
                            dcc.RadioItems(
                                id='manualMode',
                                options=[
                                    {'label': 'Handmatige modus', 'value': True},
                                    {'label': 'Automatische modus', 'value': False},
                                ],
                                value=auto
                            ),
                            html.Div(id='manual-output-container'),
                            html.Div(id='huidig'),

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

                ]),
                html.Div(className='row', style={'margin': 5}, children=[
                    #blok 4
                    html.Div(className='eight columns', style={'padding': 15, 'background-color': '#0a0908', 'color': '#BBBBBB'}, children=[
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
                                    'layout': {
                                        'plot_bgcolor': colors['graphbg'],
                                        'paper_bgcolor': colors['background'],
                                        'font': {
                                            'color': colors['text']
                                        },
                                        'margin': {
                                            't': 30,
                                            'l': 25,
                                            'r': 15
                                        }
                                    }
                                }
                            ),
                            dcc.Interval(
                                id='licht-interval',
                                interval=3000),
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
                    ]),
                    html.Div(classname='four columns', style={}, children=[
                        html.Div([dcc.Graph(id='vp_port')])
                    ]),
                ])
            ])
        ])
    ])

    #@app.callback(
    #    dash.dependencies.Output('changeToButton', 'children'),
    #    [dash.dependencies.Input('changeToButton', 'children')]
    #)



    @app.callback(Output('temp-graph', 'figure'),
                  events=[Event('temp-interval', 'interval')])
    def update_graph_live():
        nonlocal count
        nonlocal df
        nonlocal shouldUpdate
        dbn = dbs.connect(host="localhost", user="root", db="project21")
        newcount = pd.read_sql('SELECT COUNT(time) FROM data', con=dbn)['COUNT(time)'][0]
        toreadout = newcount - count
        if (toreadout > 0):
            shouldUpdate = True
            df2 = pd.read_sql('SELECT * FROM data ORDER BY time DESC LIMIT %s' % toreadout, con=dbn)
            count = newcount
            df = df.append(df2, ignore_index=True)
            if len(df) >= 10080:
                df = df.pop(0, ignore_index=True)

        figure = {
            'data': [
                go.Scatter(
                    x=df['time'],
                    y=df['temperatuur'],
                    mode='lines'
                ),
            #go.Layout(margin=dict(t=0))
            ],
        }
        return figure

    @app.callback(
        dash.dependencies.Output('vp_port', 'figure'))
    def update_pie():
        return {go.Pie(labels=['a', 'b'], values=[5, 6])}

    @app.callback(
        dash.dependencies.Output('temp-output-container', 'children'),
        [dash.dependencies.Input('temp-slider', 'value')])
    def update_output(value):
        settings["settings"]["temp"] = value
        with open("settings.json", "w") as jsonFile:
            json.dump(settings, jsonFile)
            jsonFile.truncate()
        return 'De temperatuurtreshold is {}°C'.format(value)

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
        return 'Momenteel staat het doek in {} modus'.format(hand)

    @app.callback(
        dash.dependencies.Output('pos-output-container', 'children'),
        [dash.dependencies.Input('pos-slider', 'value')])
    def update_output(value):
        settings["settings"]["pos"] = value
        with open("settings.json", "w") as jsonFile:
            json.dump(settings, jsonFile)
            jsonFile.truncate()
        return 'Zet het doek op {}cm van de grond'.format(value)


    @app.callback(Output('licht-graph', 'figure'),
                  events=[Event('licht-interval', 'interval')])
    def update_graph_live():
        figure = {
            'data': [
                go.Scatter(
                    x=df['time'],
                    y=df['licht'],
                    mode='lines'
                ),
            #go.Layout(margin=dict(t=50))
            ],
        }
        return figure

    @app.callback(
        dash.dependencies.Output('licht-output-container', 'children'),
        [dash.dependencies.Input('licht-slider', 'value')])
    def update_output(value):
        settings["settings"]["licht"] = value
        with open("settings.json", "w") as jsonFile:
            json.dump(settings, jsonFile)
            jsonFile.truncate()
        return 'Het doek gaat omlaag bij een lichtpercetage van {}%'.format(value)

    app.run_server()

test()
