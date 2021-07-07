# Make calendar for last 50 days

### 요구사항
   1. 최근 (최대) 50일의 달력을 만든다.
   2. 요일, 달이 써있어야한다.
   3. 일자가 칸 안에 써있어야한다.

### 고려사항
   1. subprocess와 parent process 를 pipe로 연결, subprocess에서는 오류 발생시 pipe로 오류내용을 전송하는 로직을,
      부모 프로세스에서는 pipe에 읽을 내용이 있으면 확인에서 오류를 발생시키고 내용을 출력하는 로직을 설계 
   2. 자식 프로세스에서의 try except를 넣는 구간 : run?, Loop?
      1. 자식 프로세스의 오류를 총괄해야하니 run이 맞다.
   3. 부모 프로세스에서 오류 확인하는 구간:
      1. 루프문에 있어야하므로 trader.run()
         => 코드가 지저분해지는 경향이 있는 것같으나 loop문이 하나라 어쩔 수 없음.

### 코드
```python
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
%matplotlib inline

def main():
    dates, data = generate_data()
    fig, ax = plt.subplots(figsize=(8, 8))
    calendar_heatmap(ax, dates, data)

def generate_data():
    start = dt.datetime.today() #오늘 날짜를 로드
    num = start.isocalendar()[2] + 7*6 # year, week, weekday 중 weekday만 뽑아서 42더함
    data = np.arange(num)
    dates = [start - dt.timedelta(days=i) for i in reversed(range(num))] # 하루씩 감소시킴
    return dates, data #연월일 datetime, 일자 갯수 return

def calendar_array(dates, data):
    i, j = zip(*[d.isocalendar()[1:] for d in dates]) #(연간으로 셋을 때 몇 번째 주인지), (몇 번째 일자인지) 튜플을 뽑은 일자 갯수만큼 만들기
    i = np.array(i) - min(i) # 15주차에서 시작했으면 15를 기준으로 1번째로
    j = np.array(j) - 1 #인덱싱 위해 -1
    ni = max(i) + 1 # 최대 몇 번째 주인지, +1은 i가 0부터 시작하므로 첨가

    calendar = np.nan * np.zeros((7, ni))
    calendar[j, i] = data #1 ~ 일자 갯수 할당
    return i, j, calendar

def calendar_heatmap(ax, dates, data):
    i, j, calendar = calendar_array(dates, data)
    im = ax.imshow(calendar, interpolation='none', cmap='summer')
    label_days(ax, dates, i, j, calendar)
    label_months(ax, dates, i, j, calendar)

def label_days(ax, dates, i, j, calendar):
    nj, ni = calendar.shape # 캘린더 행, 열
    day_of_month = np.nan * np.zeros((7, ni)) # 7xni 개의 nan 만들기
    day_of_month[j, i] = [d.day for d in dates] # 일자 할당

    for (i, j), day in np.ndenumerate(day_of_month):
        if np.isfinite(day): #무한이 아니면
            ax.text(j, i, int(day), ha='center', va='center') #일자 annotation

    ax.set(yticks=np.arange(7),  #7일치 yticks
           yticklabels=['M', 'T', 'W', 'R', 'F', 'S', 'S'])

def label_months(ax, dates, i, j, calendar):
    month_labels = np.array(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                             'Aug', 'Sep', 'Oct', 'Nov', 'Dec']) 
    months = np.array([d.month for d in dates]) #몇 월인지
    uniq_months = sorted(set(months)) # month 종류만 
    xticks = [i[months == m].mean() for m in uniq_months] #특정 month인 일자들의 주차의 평균
    labels = [month_labels[m - 1] for m in uniq_months] #그 달의 이름이 뭔지
    ax.set(xticks=xticks,
           xticklabels = labels)
    ax.xaxis.tick_top() #위에서 세기

main()
```
