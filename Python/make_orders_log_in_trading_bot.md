# Order log

### 요구사항
   1. analyzer를 통해 날짜, 일별 자산, 일별 자산비율, 일별 수익률, 일별 손익, 일별 승패, 승률, 손익비 등을 만들 수 있는   
      기초 자료를 수립해야한다.
   
### 고려사항
   1. 자료는 체결된 주문을 기초로 한다.   
      => 접수주문은 의미가 없음. 
   2. 이 기능은 포트폴리오 매니저에 넣어야한다.   
      => 주문은 포트폴리오 매니저가 관리한다.
   3. 포트폴리오의 check_order_status 단에서 동작해야한다.  
      => 주문이 체결될 때 마다 쓰면 편리.
   4. json 형식을 정제해서 넣을 것인지, 그냥 raw data로 넣을 것인지  
      => 나중에 어떻게 다른 데이터가 필요할지 모르며, 처리 속도를 높이기 위해 그냥 넣기
   5. 어느전략에서 체결된 order 인지 식별할 수 있게 json stream에 추가해야한다.
   6. 프로그램이 중간에 꺼져도 동작해야 한다.  
      => open 'a' 로 열어서 close를 안해도 내용이 보존되게 
   
### 제한사항
   1. class 를 초기화할때 open 한 파일을 을 객체에 멤버로 할당하는 경우
      open 'a' 로 열고 추가한 내용은 close 를 해야 써진다.
      1. 매 실행마다 file을 열고 한 줄 쓰고 닫는 경우
         - 장점 : 안정적이다.
         - 단점 : 매번 열고 닫으므로 속도가 느리다.
            => 별로 느리지 않음
   
### 해결방안 후보군
   1. 파일 이름만 class 멤버로 할당하고 함수로 열고 닫자

### 기본 로직
   - main.py 
     - trader.run() #메인루프
       - for strategy in strategies:   
         trader.portfolio_manager.check_order_status(strategy.name)  
         = 전략 실행 전 접수된 order 확인하고 처리
         - write_log(order)
### 코드
```python
    def write_order_log(self, st_name, order):
        order_added = order.copy()
        order_added['st_name'] = st_name
        with open(self.order_log_file_path, 'a') as f:
            f.write(str(order) + '\n')
```
