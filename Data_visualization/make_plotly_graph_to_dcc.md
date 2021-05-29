# Make plotly Graph into dcc

### 요구사항
   1. plotly.express 또는 go 로 표현되는 그래프를 dash로 래핑하여 html에 삽입해야한다.

### 기본지식
   1. dcc.Graph 의 대표적인 argument
   2. go.figure의 대표적인 argument
### 코드

1. figure를 딕셔너리로서 사용하는 방법 
```python
fig = dict({
    "data": [{"type": "bar",
              "x": [1, 2, 3],
              "y": [1, 3, 2]}],
    "layout": {"title": {"text": "A Figure Specified By Python Dictionary"}}
})

# To display the figure defined by this dict, use the low-level plotly.io.show function
import plotly.io as pio

pio.show(fig)
```

2. dcc graph에서 figure를 dictionary로 받는 방법
```python
dcc.Graph(
        id="piechart",
        figure={
            "data": [
                {
                    "labels": labels,
                    "values": values,
                    "type": "pie",
                    "marker": {"line": {"color": "white", "width": 1}},
                    "hoverinfo": "label",
                    "textinfo": "label",
                }
            ],
            "layout": {
                "margin": dict(l=20, r=20, t=20, b=20),
                "showlegend": True,
                "paper_bgcolor": "rgba(255,255,255,150)",
                "plot_bgcolor": "rgba(0,0,0,255)",
                "font": {"color": "white"},
                "autosize": True,
            },
        },
        style={'width': '100%', 'height': '100%'}
    )
```

```python
import plotly.graph_objects as go # or plotly.express as px
fig = go.Figure(data=go.Heatmap(
        z = [[1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1]]
))
# fig.add_trace( ... )
# fig.update_layout( ... )


import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False) 
```
