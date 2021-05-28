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

### 해결방안 후보군
   1. child process 알아서 중단하고, 다시 시작하는 방법
      - 단점 
        1. 안정적이지 못함(생각치 못한 오류가 생겨 다시시작하는 것으로 해결안될 수 있음)
      - 장점
        1. 쉬움.
        2. 프로그램 구조상 이렇게 해도 오류는 없음
   
   2. mp.pipe를 만들어서 부모 프로세스로 에러를 전송하는 방법(채택)
      - 장점
        1. 안정적임
        2. 다양한 상황에 적용할 수 있음. 


### 고려사항
   1. subprocess와 parent process 를 pipe로 연결, subprocess에서는 오류 발생시 pipe로 오류내용을 전송하는 로직을,
      부모 프로세스에서는 pipe에 읽을 내용이 있으면 확인에서 오류를 발생시키고 내용을 출력하는 로직을 설계 
   2. 자식 프로세스에서의 try except를 넣는 구간 : run?, Loop?
      1. 자식 프로세스의 오류를 총괄해야하니 run이 맞다.
   3. 부모 프로세스에서 오류 확인하는 구간:
      1. 루프문에 있어야하므로 trader.run()
         => 코드가 지저분해지는 경향이 있는 것같으나 loop문이 하나라 어쩔 수 없음.

### 기본 로직
   - main.py 
     - trader.run() #메인루프
       - while True:
         for strategy in strategies:   
            trader.portfolio_manager.check_order_status(strategy.name)  
         check_subprocess_error()

### 참조
```python      
import multiprocessing
import traceback

from time import sleep
import os

class Process(multiprocessing.Process):
    """
    Class which returns child Exceptions to Parent.
    https://stackoverflow.com/a/33599967/4992248
    """

    def __init__(self, *args, **kwargs):
        multiprocessing.Process.__init__(self, *args, **kwargs)
        self._parent_conn, self._child_conn = multiprocessing.Pipe() #데이터를 공유할 pipe
        self._exception = None

    def run(self): #프로세스가시작되면 _parent_conn 으로 None 신호를 보낸다.
        try:
            multiprocessing.Process.run(self)
            self._child_conn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._child_conn.send((e, tb))
            # raise e  # You can still rise this exception if you need to

    @property #property decorator를 사용하면 함수로 호출하지 않아도 불러올 수 있다.
    def exception(self):
        if self._parent_conn.poll(): #부모 프로세스에서 읽어올거리가 있으면
            self._exception = self._parent_conn.recv() #읽어온다
        return self._exception


class Task_1:
    def do_something(self, queue):
        queue.put(dict(users=2))
        print("task1 : ", os.getpid()) #프로세스 번호를 호출할 수있다.

class Task_2:
    def do_something(self, queue):
        print("task2 : ", os.getpid())
        queue.put(dict(users=5))


def main():
    try:
        task_1 = Task_1() 
        task_2 = Task_2()

        task_1_queue = multiprocessing.Queue()
        task_2_queue = multiprocessing.Queue()

        task_1_process = Process(
            target=task_1.do_something,
            kwargs=dict(queue=task_1_queue)) #메모리를 공유할 Queue설정

        task_2_process = Process(
            target=task_2.do_something,
            kwargs=dict(queue=task_2_queue))

        task_1_process.start()
        task_2_process.start()

        while task_1_process.is_alive() or task_2_process.is_alive():
            sleep(5)

            if task_1_process.exception: #process.exception()을 호출한다. 오류가 났을경우
                error, task_1_traceback = task_1_process.exception #process._exception을 할당하고
                task_2_process.terminate() #다른 프로세스를 종료한다.
                
                raise ChildProcessError(task_1_traceback) #에러를 raise한다.(부모프로세스)

            if task_2_process.exception:
                error, task_2_traceback = task_2_process.exception
                task_1_process.terminate()

                raise ChildProcessError(task_2_traceback)

        task_1_process.join() #프로세스가 끝날 때 까지 기다린다.
        task_2_process.join()

        task_1_results = task_1_queue.get()
        task_2_results = task_2_queue.get()

        task_1_users = task_1_results['users']
        task_2_users = task_2_results['users']

    except Exception:
        # Here usually I send email notification with error.
        print('traceback:', traceback.format_exc())


if __name__ == "__main__":
    print("main : " , os.getpid())
    main()
```

### 코드
```python
#웹소켓 api(subprocess)
def run(self): 
   try:
      self._child_conn.send(None)
      self.alive = True
      self.__aloop = asyncio.get_event_loop()
      self.__aloop.run_until_complete(self.__connect_socket())
   except Exception as e:
      tb = traceback.format_exc()
      self._child_conn.send((e, tb))

#실시간 데이터 수신객체(parent process)
def check_subprocess_error(self):
   """웹소켓 프로세스에서 에러가 일어나면 부모프로세스에서 raise"""
   if self.wm.exception:
      error, traceback = self.wm.exception
      raise ChildProcessError(traceback)

#trader 함수
def run(self):
   #시작시간과같으면 init_strategy 하기 이건 전략에 넣어야 while문이 안끊길듯
   self.notifier.send_message_to_all("자동 매매 시스템이 시작됩니다.")
   while True:
      for strategy in self.strategies:
            if strategy.restart_condition():
               strategy.init_strategy()#시가가 되면 자동으로 다시 price_df 구축
               self.init_data_collector()
            self.portfolio_manager.check_order_status(strategy.name)#접수한 order 들 체결, 만료, 취소 상태를 확인하고 대처 
            strategy.run()
      self.realtime_data_collector.check_subprocess_error()
      time.sleep(7)
```
