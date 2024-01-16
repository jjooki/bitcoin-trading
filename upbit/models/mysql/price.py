from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Index, Column, Integer, CHAR, VARCHAR, String, DateTime, Float, Date

class RealtimePrice(Base):
    __tablename__ = "realtime_price"
    idx = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(VARCHAR(10), comment="시장 코드, ex) 'KRW-BTC'")
    trade_price = Column(Float, comment="종가")
    updated_at = Column(DateTime, nullable=False, comment="업데이트 시각")