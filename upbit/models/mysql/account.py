from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Index, Column, Integer, CHAR, VARCHAR, String, DateTime, Float, Date

class AccountInfo(Base):
    __tablename__ = "account_info"
    idx = Column(Integer, primary_key=True, autoincrement=True)
    market_code = Column(VARCHAR(10), nullable=False, comment="시장 코드, ex) 'KRW-BTC'")
    quantity = Column(Float, nullable=False, comment="보유 수량")