import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
def generate_table(dataframe, max_rows=10):
    return html.Div(

    )

N = 500
random_x = np.linspace(0, 1, N)
random_y = np.random.randn(N)

app = dash.Dash()

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})
app.layout = html.Div(style={'background-color': 'grey'}, children=[
    html.Div([
        html.Div(className='container', style={'background-color': 'white'}, children=[
            html.Section(className='header', style={'padding-bottom': 50}, children=[
                html.H1(children='Test'),
            ]),
            html.Div(className='row', children=[
                html.Div(className='eight columns', style={'border-width': 4, 'border-style': 'solid'}, children=[
                    html.H3('Temperatuur'),
                    dcc.Graph(
                        id='example-graph',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=random_x,
                                    y=random_y,
                                    mode='lines'
                                )
                            ]

                        }
                    )
                ]),
                html.Div(className='four columns', style={'border-width': 4, 'border-style': 'solid'}, children=[
                    html.Button('Change to manual', id='button'),
                    html.P('De huidige temperatuur is'),
                    html.P('De huidige lichtintensiteit is')
                ]),
                html.Div(className='eight columns', style={'border-width': 4, 'border-style': 'solid'}, children=[
                    dcc.Graph(
                        id='example-graph2',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=random_x,
                                    y=random_y,
                                    mode='lines'
                                )
                            ]

                        }
                    )

                ])
            ])
        ])
    ])
])

#@app.callback(

 #   )

if __name__ == '__main__':
    app.run_server(debug=True)