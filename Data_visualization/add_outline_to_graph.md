# Add outline to graph

모든 plotly 그래프에 응용가능하다.

```python

line_template = dict(
            color="black",
            width=1,
        )

for n in range(5):
    fig.add_shape(type="rect",
        x0=n-.5, y0=-.5, x1=n+1.5, y1=6.5,
        line=line_template)
    fig.add_shape(type="rect",
        x0=-.5, y0=n-.5, x1=6.5, y1=n+1.5,
        line=line_template)
```