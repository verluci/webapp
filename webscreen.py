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


with open("settings.json", "r") as jsonFile:
    settings = json.load(jsonFile)
db = dbs.connect(host="localhost", user="root", db="project21")
df = pd.read_sql('SELECT * FROM data LIMIT 7200', con=db)
x = True
changeto = "test"
N = 500
random_x = np.linspace(0, 1, N)
random_y = np.random.randn(N)
count = pd.read_sql('SELECT COUNT(time) FROM data', con=db)
print(count)

app = dash.Dash()

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})
app.layout = html.Div(style={'background-color': 'grey'}, children=[
    html.Div([
        html.Div(className='container', style={'background-color': 'white'}, children=[
            #header, titel
            html.Section(className='header', style={'padding-bottom': 50}, children=[
                html.H1(children='Test'),
            ]),
            #body
            html.Div(className='row', children=[
                #blok 1
                html.Div(className='eight columns', style={'border-width': 4, 'border-style': 'solid', 'padding': 20}, children=[
                    html.H3('Temperatuur'),
                    #grafiek temp
                    dcc.Graph(
                        id='temp-graph'
                    ),
                    dcc.Interval(
                        id='temp-interval',
                        interval=60000),

                    """dcc.Graph(
                        id='temp-graph',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=df['time'],
                                    y=df['temperatuur'],
                                    mode='lines'
                                )
                            ]

                        }
                    ),""",
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
                html.Div(className='four columns', style={'border-width': 4, 'border-style': 'solid', 'padding': 20}, children=[
                    html.Div(className='manualButton', children=[
                        #manual knop
                        html.Button(changeto, id='changeToButton'),
                        html.P('De huidige temperatuur is'),
                        html.P('De huidige lichtintensiteit is')
                    ]),
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
                #blok 3
                html.Div(className='eight columns', style={'border-width': 4, 'border-style': 'solid', 'padding': 20}, children=[
                    #grafiek licht
                    dcc.Graph(
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
                    dcc.Slider(
                        id='light-slider',
                        min=0,
                        max=100,
                        step=1,
                        value=settings["settings"]["licht"],
                        marks={(i*10): '{}'.format(10 * i) for i in range(11)}
                    ),
                    html.Br(),
                        html.Div(id='light-output-container')


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
    dash.dependencies.Output('light-output-container', 'children'),
    [dash.dependencies.Input('light-slider', 'value')])
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
    print("echo")


def callback_a(self):
    print("te")

app.run_server(debug=True)


