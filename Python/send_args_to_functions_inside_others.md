# send_args_to_functions_inside_others

### 요구사항
   1. function 내부에 있는 function까지 인수를 전달한다.
   2. 전달은 인수를 지정해서 하지않고 있으면 하는 식으로 전달한다.
   
### 코드
```python
def temp(a, **kwargs):
    a += add(kwargs.pop('b'), kwargs.pop('c')) # kwargs.get() 으로 넣으면, kwargs에 없을경우 None을 전달하는 식으로 할 수있다.
    print(a)
    temp2(kwargs.pop('d'))

def add(b,c):
    return b + c

def temp2(d):
    print(d)

temp(1,b = 2, c = 3, d = 6)
```
