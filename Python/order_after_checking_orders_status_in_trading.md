# Order After Checking Order Status 

### 요구사항
   1. 미체결된 주문을 확인하고 취소하고 다시 주문해야한다.   
      ex) 지정가 매도, 30분동안 안팔릴 경우 취소하고 시장가 매도

### 고려사항
   1. 이 기능은 개별 전략에 넣어야한다.  
      => 전략 각자마다 동작하는 방식을 다르게 설정할 수 있도록 해야하기 때문에
   2. 주문을 확인하는 기능은 portfolio_manager 에서 담당한다.
   
### 제한사항
   1. 개별전략은 들어간 주문에 대해 접근할 수 없다.
   2. 개별전략은 portfolio_manager에 접근할 수 없다.
      1. 접근하게 하는 경우  
         1. order을 cancle하면 balance에 있는 order_list를 삭제해야한다.
         2. 업비트에 취소주문을 넣어야한다.  
            => 객체별로 독립된 기능수행을 저해할 수 있음. 
   3. portfoio_manager 를 전략별로 만들경우
      1. 거의 동일한 일을 하는 객체를 여러개 만들게되어 공간, 시간적 낭비

### 해결방안 후보군
   1. 개별전략을 portfolio_manager에 접근하게 하는 경우  
       1. order을 cancle하면 balance에 있는 order_list를 삭제해야한다.
       2. 업비트에 취소주문을 넣어야한다.  
          => 객체별로 독립된 기능수행을 저해할 수 있음. 
   
   2. portfoio_manager 를 전략별로 만들경우  
      => 거의 동일한 일을 하는 객체를 여러개 만들게되어 공간, 시간적 낭비
   
   3. portfolio_manager가 미체결 주문 관련 모든 일을 전담하게 하는 경우 (채택)
       - 단점 
         1. 개별 전략이 미체결 주문전략까지 컨트롤 할 수 없다.  
            => 어떤 개별 전략에만 특화된 주문 방법이 있기보다는 대부분 모든 전략에 두루두루 통용될 것이라고 생각됨.
         2. 주문 접수라는 전략의 고유 영역을 침범함
            => 
       - 장점
         1. 쉬움.
         2. 독립성을 해치지 않음. 
  
### 기본 로직
   - main.py 
     - trader.run() #메인루프
       - for strategy in strategies:   
         trader.portfolio_manager.check_order_status(strategy.name)  
         = 전략 실행 전 접수된 order 확인하고 처리

```python      
"""매도주문 조회시 json form"""
{'uuid': '48d6d451-3db5-4357-9d5a-bfb8f417c943',
  'side': 'ask',
  'ord_type': 'limit',
  'price': '230000.0',
  'state': 'done',
  'market': 'KRW-LTC',
  'created_at': '2021-03-17T01:06:55+09:00',
  'volume': '0.5',
  'remaining_volume': '0.0',
  'reserved_fee': '0.0',
  'remaining_fee': '0.0',
  'paid_fee': '58.775',
  'locked': '0.0',
  'executed_volume': '0.5',
  'trades_count': 2}
```

### 코드
```python
"""30분 넘으면 시장가로 처리"""
def check_order_status(self, st_name):
   """주문이 체결되었는지 확인하고 처리""" 
   for order in self.record[st_name]['orders_list']:
      order_resp = self.upbit.get_the_order(order['uuid'])[0]
      if order_resp['state'] == "done":
         print(f"[{st_name}]{order_resp['market']} {math.ceil(float(order_resp['trades'][0]['funds']))}원 어치가 체결되었습니다.")
         if order_resp['side'] == 'bid':
            self.record_buy(st_name, order)    
         elif order_resp['side'] == 'ask':
            self.record_sell(st_name, order)    
         self.notifier.send_message_to_all(f"[{st_name}]{order_resp['market']} {math.ceil(float(order_resp['trades'][0]['funds']))}원 어치가 체결되었습니다.")
         self.record[st_name]['orders_list'].remove(order)
      if order_resp['state'] == "wait": #체결 되지 않고

         if order_resp['side'] == 'ask': #매도 주문일 때
            if (datetime.now() - pd.to_datetime(order_resp['created_at'][:-6])).total_seconds() > 0.5 * 3600: #접수한지 30분이 넘으면
               ticker = order_resp['market'] #종목과 남은갯수 확인
               size = order_resp['remaining_volume']
               self.upbit.cancel_order(order['uuid']) #기존 주문 cancle
               self.record[st_name]['orders_list'].remove(order) #주문 리스트에서 제거
               order = self.upbit.sell_market_order(ticker, size) #시장가로 접수
               self.notifier.send_message_to_all(f"{ticker} 를 {size}개 시장가 매도를 접수했습니다.")
               self.record[st_name]['orders_list'].append(order) #order list 에 추가
               self.update_last_order(st_name, order) # 마지막 주문시간 업데이트

         if (datetime.now() - pd.to_datetime(order_resp['created_at'][:-6])).total_seconds() > 3 * 3600: #매수주문이 3시간이 지나면
            self.upbit.cancel_order(order['uuid'])
            print(f"[{st_name}] {order_resp['market']} 주문이 만료되어 취소했습니다.")
            self.notifier.send_message_to_all((f"[{st_name}] {order_resp['market']} 주문이 만료되어 취소했습니다."))
            self.record[st_name]['orders_list'].remove(order)
         else:
            continue
```
