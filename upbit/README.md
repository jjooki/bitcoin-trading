# AutoTrading

## Module Architecture

### 1. main.py
: Autotrade 알고리즘이 계속 돌아가는 메인파일

### 2. slack.py
: Slack 채널에 거래

### 3. price.py
: upbit price 관련 메소드(거래단위, 거래금액 환산, 거래/출금수수료 계산) 

### 4. order.py
: upbit API request 관련 함수(ticker 전체조회, ticker별 info 조회, 주문하기)

### 5. predict.py
: prophet 시계열 모델을 활용한 가격예측

### 6. strategy.py
: 투자전략 구현(예정)
