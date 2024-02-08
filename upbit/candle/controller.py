import pyupbit

from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from typing import Literal

from ..models.mysql.price import RealtimePrice
from ..modules import session_scope

def get_5min_candle(market_type: Literal['KRW', 'BTC', 'USDT']):
    # 현재가정보조회
    with session_scope() as session:
        for ticker in pyupbit.get_tickers(market_type):
            candle = pyupbit.get_ohlcv(ticker, interval="minute5", count=1)
            candle = candle.iloc[0]
            candle = RealtimePrice(ticker, candle['close'], datetime.now())
            try:
                q = session.query(RealtimePrice).filter_by(code=ticker)
                existing_default = q.one()
                
            except NoResultFound:
                session.add(candle)
                
            else:
                assert isinstance(existing_default, RealtimePrice)
                existing_default.trade_price = candle.trade_price
                existing_default.updated_at = candle.updated_at