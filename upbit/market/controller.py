import pyupbit

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from typing import Literal

from config import UpbitConfig
from ..models.mysql.market import MarketInfo
from ..models.request.market import MarketRequest
from ..modules.my_upbit import Myupbit
from ..modules import session_scope, upsert

def get_market_info():
    # 현재가정보조회
    upbit = Myupbit()
    market_info = upbit.quotation_request('/market/all', MarketRequest().to_dict())
    
    with session_scope() as session:
        for coin_info in market_info:
            market_code = coin_info['market']
            market_type = market_code.split('-')[0]
            code = market_code.split('-')[1]
            
            market_info = MarketInfo(
                market_code, code, market_type,
                coin_info['korean_name'], coin_info['english_name'],
                is_use='Y', market_warning=coin_info['market_warning']
            )
            
            upsert(session=session,
                   model=MarketInfo,
                   instance=market_info,
                   filter_columns=['market_code'],
                   update_columns=market_info.update_column())
        
        existing_table = session.query(MarketInfo).all()
        market_list = [coin_info['market'] for coin_info in market_info]
        for table in existing_table:
            if table.market_code not in market_list:
                table.is_use = 'N'
                table.updated_at = datetime.now()