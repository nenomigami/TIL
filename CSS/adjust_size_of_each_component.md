

### 제일 큰 화면
```css
#big-app-container {
  width: 75vw; 
  height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 6.0vh 12.5vw;
}

vw, vh : 유동단위, 뷰포트(보여지는 영역)에서 몇 %를 차지할 것인지
         %와의 차이점 - %는 부모영역을 기준으로 한다.

em : 부모의 폰트크기, 대부분 디폴트 값 16px
rem : 최상위 루트의 폰트크기, 대부분 디폴트 값 12px, </html> 에서 선언된 그 크기임
```