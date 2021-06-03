table - 표처럼 레이아웃(없어짐)
position - absolute하게 혹은 relative하게 element를 정렬
float - 삽화 옆 글씨처럼

1. 부모 컨테이너의 display 값에 flex를 줘야한다
2. flex-direction 으로 정렬방법을 선택할 수 있다.  
    ex) row, row-reverse, column 등
3. 아이템에 크기를 설정하려면 grow, shink를 사용해야한다.
4. 아이템에서 flex-basis: npx;을 주면 픽셀대로 들어간다(플렉스의 방향대로 폭 또는 높이 지정)
5. flex-grow:1을 하면 플렉스방향대로 나누어가짐
6. 경계는 border값 주면됨.
7. 플렉스 element의 속성을쓸때는 display:flex를 쓰면안됨
8. %로 넣으면 안들어감, px지정필요
9. 마진은 layout={"margin": dict(l=20, r=20, t=20, b=20),}