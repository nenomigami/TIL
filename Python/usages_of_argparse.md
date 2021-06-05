# How to Use Argparse
### 1. Basic Usage
```python
import argparse
# Create the parser and add arguments
parser = argparse.ArgumentParser()
parser.add_argument(dest='argument1', help="This is the first argument") # -h 하면 argument1 : 설명 이런식으로 들어감

# Parse and print the results
args = parser.parse_args()
print(args.argument1)
```

### 2. 타입지정
```python
parser.add_argument(dest='argument1', type=str, help="A string argument")
parser.add_argument(dest='argument2', choices=['red', 'green', 'blue'])
args = parser.parse_args()
print(args.argument1)
print(args.argument2)
```

### 3. arg 여러개
```python
parser.add_argument(dest='argument1', nargs=2, type=int)
args = parser.parse_args()
print(args.argument1) #=> list 리턴

#input 방법
#$ python main.py 1 2 3 4 5
```

### 4. optional 한 사용
```python
parser.add_argument('-a3', '--argument3', action = 'store_true')#a3 flag가 발견되면 args.argument3 = true 를 할당한다. 
parser.add_argument('-a3', '--argument3', type=int, default=0) #default 값 설정하기
args = parser.parse_args()
print(args.argument1) #=> list 리턴
```