# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash

app = DjangoDash('Gender')
genders = ["Male", "Female"]

app.layout = html.Div(children=[

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [go.Pie(labels=genders, values=[156, 76], scalegroup='one')],
            'layout': go.Layout( margin={"l": 300, "r": 300, }, legend={"x": 1, "y": 0.7})
        }
    )
])