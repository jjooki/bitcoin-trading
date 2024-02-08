import pyupbit

from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from typing import Literal

from ..models.mysql.price import RealtimePrice
from ..modules import session_scope

def get_realtime_price(market_type: Literal['KRW', 'BTC', 'USDT']):
    # 현재가정보조회
    with session_scope() as session:
        for market_code, price \
            in pyupbit.get_current_price(pyupbit.get_tickers(market_type)).items():
                price = RealtimePrice(market_code, price, datetime.now())
                try:
                    q = session.query(RealtimePrice).filter_by(code=market_code)
                    existing_default = q.one()
                    
                except NoResultFound:
                    session.add(price)
                    
                else:
                    assert isinstance(existing_default, RealtimePrice)
                    existing_default.trade_price = price.trade_price
                    existing_default.updated_at = price.updated_at
                    
        session.flush()