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