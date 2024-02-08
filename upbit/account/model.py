from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Index, Column, Integer, CHAR, VARCHAR, String, DateTime, Float, Date
from typing import List
class AccountInfo(Base):
    __tablename__ = "account_info"
    idx = Column(Integer, primary_key=True, autoincrement=True)
    market_code = Column(VARCHAR(10), nullable=False, comment="시장 코드, ex) 'KRW-BTC'")
    quantity = Column(Float, nullable=False, comment="보유 수량")
    value = Column(Float, nullable=False, comment="보유 원화 환산 가치")
    
    def __init__(self, market_code, quantity, value):
        self.market_code = market_code
        self.quantity = quantity
        self.value = value
    
    def columns(self) -> List[str]:
        return [c.name for c in self.__table__.columns]
    
    def update_column(self) -> List[str]:
        return ["quantity", "value"]