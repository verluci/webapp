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

    donker  = totaal - licht
    licht = licht/totaal*24
    donker = donker/totaal*24

    shouldUpdate = False
    auto = False
    def updateAuto():
        nonlocal auto
        if settings['settings']['manual'] == False:
            auto = False
        elif settings['settings']['manual'] == True:
            auto = True
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
    app.layout = html.Div(style={'background-color': '#BBBBBB'}, children=[
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
                                animate=settings["settings"]["animate"],
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
                    #blok 4
                    html.Div(className='four columns', style={'padding': 15, 'margin-top': 15, 'background-color': '#0a0908', 'color': '#BBBBBB'}, children=[
                            html.Div(className='buttons', children=[
                                html.Div(id='animate-output-container'),
                                dcc.RadioItems(
                                    id='animateTF',
                                    options=[
                                        {'label': 'Aan', 'value': False},
                                        {'label': 'Uit', 'value': True},
                                    ],
                                    value=settings["settings"]["animate"],
                                ),
                            ]),
                    ])
                ]),
                html.Div(className='row', style={'margin': 5}, children=[
                    #blok 5
                    html.Div(className='eight columns', style={'padding': 15, 'background-color': '#0a0908', 'color': '#BBBBBB'}, children=[
                        #grafiek licht
                        html.Div(children=[
                            dcc.Graph(
                                animate=settings["settings"]["animate"],
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
                    #blok 6
                    html.Div(className='four columns', style={'padding': 15, 'background-color': '#0a0908', 'color': '#BBBBBB'}, children=[
                        html.H5('Verdeling zonuren'),
                        dcc.Graph(
                            id='zon-per-dag',
                            figure={
                                'data': [
                                    {'x': [1], 'y': [licht], 'type': 'bar', 'name': 'zonuren per dag'},
                                    {'x': [1], 'y': [donker], 'type': 'bar', 'name': 'uren donker per dag'}
                                ],
                                'layout': {
                                    'barmode': 'stack',
                                    'plot_bgcolor': colors['graphbg'],
                                    'paper_bgcolor': colors['background'],
                                    'font': {
                                        'color': colors['text']},
                                    'margin': {
                                        't': 30,
                                        'l': 25,
                                        'r': 15
                                    }
                                }
                            }
                        )
                    ])
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
        return figure

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
        dash.dependencies.Output('animate-output-container', 'children'),
        [dash.dependencies.Input('animateTF', 'value')])
    def update_output(value):
        settings["settings"]["animate"] = value
        with open("settings.json", "w") as jsonFile:
            json.dump(settings, jsonFile)
            jsonFile.truncate()
        return 'Zet live grafieken (na verversing):'

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
