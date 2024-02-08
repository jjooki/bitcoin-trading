from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
Base = declarative_base()

from sqlalchemy import Index, Column, Integer, CHAR, VARCHAR, String, DateTime, Float, Date

class RealtimePrice(Base):
    __tablename__ = "realtime_price"
    idx = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(VARCHAR(10), comment="시장 코드, ex) 'KRW-BTC'")
    trade_price = Column(Float, comment="종가")
    updated_at = Column(DateTime, nullable=False, comment="업데이트 시각", server_default=func.now)
    
    def __init__(self, code, trade_price, updated_at=None):
        self.code = code
        self.trade_price = trade_price
        if updated_at:
            self.updated_at = updated_at
        
    def columns(self) -> list:
        return [c.name for c in self.__table__.columns]