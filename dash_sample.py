# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import math
from dash.dependencies import Input, Output, State

app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#FFFFFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
o1 = 0.1
o2 = 0.15
k1 = 0.05
k2 = 0.056


df = pd.DataFrame({
    "t": [],
    "x": [],
    "y": [],
    "wav": []
})


def wave(o, k, t, x):
    return math.sin(k*x-o*t)


for t in range(200):
    for x in range(100):
        df_add = pd.DataFrame(
            {"t": [t], "x": [x], "y": [wave(o1, k1, t, x)], "wav": "wave1"})
        df = pd.concat([df, df_add], ignore_index=True)
        df_add = pd.DataFrame(
            {"t": [t], "x": [x], "y": [wave(o2, k2, t, x)], "wav": "wave2"})
        df = pd.concat([df, df_add], ignore_index=True)

fig = px.line(df, x="x", y="y", animation_frame="t",
              color="wav", range_x=[0, 100], range_y=[-2.2, 2.2])

fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 60
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 10

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    html.Br(),
    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(['item1', 'item2', 'item3'], multi=True),
    html.Br(),
    html.Label('Slider'),
    dcc.Slider(
        id="thisSlider",
        min=0,
        max=99,
    ),
    html.P(
        id="test-output", style={"marginTop": "5%", "fontSize": 30}
    )
])


@app.callback(
    Output("test-output", "children"),
    Input("thisSlider", "value")
)
def display_value(value):
    return f"num: {value} | 10: {10*value: .3f}"


if __name__ == '__main__':
    app.run_server(debug=True)
