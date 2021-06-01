# Customize plotly Graph 

### 요구사항
   1. plotly 그래프를 자유자재로 편집해야한다.

### 기본지식
   1. [plotly 튜토리얼](https://plotly.com/python/creating-and-updating-figures/#updating-figures)
   2. [plotly 파이썬 api 문서](https://plotly.com/python-api-reference/index.html)
   
   3. plotly 의 figure 오브젝트 인수에는 data와 layout이있다.
      data : 그래프 오브젝트가 들어가며, 그래프 오브젝트 내에서 개별 그래프에 맞게 axis, marker 등을 커스터마이징 할 수있다. 
      layout : annotations, ticks, subplot 등을 control 할 수있다.

### 코드
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
