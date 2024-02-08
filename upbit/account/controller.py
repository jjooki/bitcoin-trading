import pyupbit

from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from typing import Literal

from upbit.models.mysql.price import RealtimePrice
from upbit.modules import session_scope
from config import UpbitConfig

config = UpbitConfig()
upbit = pyupbit.Upbit(config.access_key, config.secret_key)

def get_realtime_price(market_type: Literal['KRW', 'BTC', 'USDT']):
    # 현재가정보조회
    with session_scope() as session:
        pass