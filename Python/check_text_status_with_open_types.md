# Check Text Status With Open Type

### 'w'
```python
f = open("test.txt", 'w') #test.txt 새로 생김, 기존 내용 삭제
f.write('abc') # => 3 , 엔터 없음,, str 갯수 return
f.close # 파일에 써진다.
```

### 'a'
```python
f = open("test.txt", 'a') # test.txt 새로 생김, 기존내용 삭제x
f.write('abc') # => 3 , 엔터 없음, str 갯수 return
f.close # 파일에 써진다.
```