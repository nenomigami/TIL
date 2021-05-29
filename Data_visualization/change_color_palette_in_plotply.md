# Change color palette in plotly

### 기초지식
   1. Color scale
      0~1 로 표현되며, 보색이 되는 color domain이다. Color scale의 기본값은 활성중인 templete의 layout.colorscales attributes에 의존하며, color_continuous_scale argument 를 활용해 외부에서 변경할 수 있다. 예를 들어 [(0,"blue"), (1,"red")] 는 간단한 color scale 이며 blue 에서 purple을 거쳐 red 로 변경된다. 암시적으로 ["blue", "red"] 로 사용해도된다.

   2. Color ranges 
      Color range는 color scale에서 0 ~ 1에 mapping 될 데이터의 최소 최대를 나타낸다. 기본값은 input data의 range이며 range_color 나 color_continuous_midpoint arguments 를 통해 변경할 수 있다. 설정한 최소, 최대 값을 넘으면 color scale 0과 1값이 적용된다.

   3. Color Bar
      color range 와 color scale을 보여주는 범례같은 막대그래프
   
   4. Color Axis
      color scales, color ranges, color bars를 데이터와 연결하는 객체. 기본적으로 한 데이터 trace는 고유의 color axis를 가진다. 그러나 글로벌하게 공유될 수도있다. by setting e.g. marker.coloraxis in go.Scatter traces or coloraxis in go.Heatmap traces. 지역적인 color axis attributes 는 trace에서 바로 설정된다. e.g. marker.showscale whereas shared color axis attributes are configured within the Layout e.g. layout.coloraxis.showscale

### 요구사항
   1. plotly heatmap 에서 android app "습관"의 contribution chart와 동일한 color scale을 사용하고 싶음.
      => [discrete color scale 설정](https://plotly.com/python/colorscales/)

### 코드
```python
fig.add_trace(go.Heatmap(
    z=[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]],
    colorscale=[
        
        [0, "rgb(0, 0, 0)"], #원하는 값과 컬러값 매치
        [0.1, "rgb(0, 0, 0)"],

        [0.1, "rgb(20, 20, 20)"],
        [0.2, "rgb(20, 20, 20)"],

        [0.2, "rgb(40, 40, 40)"],
        [0.3, "rgb(40, 40, 40)"],

        [0.3, "rgb(60, 60, 60)"],
        [0.4, "rgb(60, 60, 60)"],

        [0.4, "rgb(80, 80, 80)"],
        [0.5, "rgb(80, 80, 80)"],

        [0.5, "rgb(100, 100, 100)"],
        [0.6, "rgb(100, 100, 100)"],

        [0.6, "rgb(120, 120, 120)"],
        [0.7, "rgb(120, 120, 120)"],

        [0.7, "rgb(140, 140, 140)"],
        [0.8, "rgb(140, 140, 140)"],

        [0.8, "rgb(160, 160, 160)"],
        [0.9, "rgb(160, 160, 160)"],

        [0.9, "rgb(180, 180, 180)"],
        [1.0, "rgb(180, 180, 180)"]
    ],
    colorbar=dict(
        tick0=0,
        dtick=1
    )
))

fig.show()
```
