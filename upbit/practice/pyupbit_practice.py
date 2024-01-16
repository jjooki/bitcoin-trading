import pyupbit
import os

# pyubit installing check
# <class 'pyupbit.exchange_api.Upbit'>
print(pyupbit.Upbit)

# import 'KRW' market information
print(pyupbit.get_tickers('KRW'))

# get current price of coin
print(pyupbit.get_current_price('KRW-BTC'))

# get current price of coins
print(pyupbit.get_current_price(['KRW-BTC','KRW-ETH','KRW-SAND']))

# get current price of all coins
print(pyupbit.get_current_price(pyupbit.get_tickers('KRW')))

# get open-high-low-close-volume-value DataFrame
# interval - month, week, day, minute 120/60/30/15/10/5/3/1
# count - default 200
# period - count under 200 -> X
print(pyupbit.get_ohlcv(ticker='KRW-BTC', interval='minute60', count=200, to=None, period=0.1))

# bid-ask price
# Output : market = ticker, timestamps(ms)
print(pyupbit.get_orderbook(ticker="KRW-BTC"))

access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

upbit = pyupbit.Upbit(access_key, secret_key)
print(upbit.get_balances())
print(upbit.get_balance('KRW'))

# limit order bid/ask
# buy_limit_order(ticker, price, volume, contain_req=False)
# sell_limit_order(ticker, price, volume, contain_req=False)
ret = upbit.buy_limit_order("KRW-BTC", 33000000, 1)
print(ret)

# market price order
# buy_market_order(ticker, price, contain_req=False) 
# sell_market_order(ticker, price, contain_req=False)
sell = upbit.sell_market_order("KRW-BTC", 1)
print(sell)

# order view/cancel
# view : get_order(ticker_or_uuid, state='wait', kind='normal', contain_req=False)
# cancel : cancel_order(uuid, contain_req=False)
ongoing_order = upbit.get_order("KRW-BTC") # 미체결 주문
finished_order = upbit.get_order("KRW-BTC", state="done") # 완료된 주문
uuid_order = upbit.get_order("UUID") # 특정 주문 상세 조회