from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, CHAR, VARCHAR, String, DateTime, Float
from typing import List

class MarketInfo(Base):
    __tablename__ = 'market_info'
    idx = Column(Integer, primary_key=True)
    market_code = Column(VARCHAR(10), nullable=False, unique=True, comment="시장 코드, ex) 'KRW-BTC'")
    code = Column(CHAR(4), nullable=False, unique=True, comment="시장 코드, ex) 'KRW-BTC'")
    market_type = Column(CHAR(3), nullable=False, comment="시장 종류, ['KRW', 'BTC', 'USDT'] 중 하나")
    korean_name = Column(VARCHAR(100), comment="한글 이름")
    english_name = Column(VARCHAR(100), comment="영어 이름")
    market_warning = Column(VARCHAR(10), comment="시장 경고, ['NONE', 'CAUTION'] 중 하나", server_default="NONE")
    is_use = Column(CHAR(1), nullable=False, comment="사용 여부, ['Y', 'N'] 중 하나", server_default="Y")
    updated_at = Column(DateTime, nullable=False, comment="업데이트 시각", server_default=func.now)
    
    def __init__(self, market_code,
                 code, market_type,
                 korean_name,
                 english_name,
                 is_use,
                 market_warning=None,):
        self.market_code = market_code
        self.code = code
        self.market_type = market_type
        self.korean_name = korean_name
        self.english_name = english_name
        self.is_use = is_use
        if market_warning:
            self.market_warning = market_warning
            
    def __repr__(self):
        return f"<MarketInfo(code={self.code}, korean_name={self.korean_name}, english_name={self.english_name}, market_warning={self.market_warning})>"
    
    def columns(self) -> List[str]:
        return [c.name for c in self.__table__.columns]
    
    def update_column(self) -> List[str]:
        return ["is_use", "market_warning", "updated_at"]
        