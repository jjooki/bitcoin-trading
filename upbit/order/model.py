from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Index, Column, Integer, CHAR, VARCHAR, String, DateTime, Float, Date

class OrderHistory(Base):
    __tablename__ = "order_history"
    idx = Column(Integer, primary_key=True, autoincrement=True)
    market_code = Column(VARCHAR(10), nullable=False, comment="시장 코드, ex) 'KRW-BTC'")
    side = Column(CHAR(3), nullable=False, comment="주문 종류, ['bid', 'ask'] 중 하나")
    state = Column(CHAR(10), nullable=False, comment="주문 상태, ['wait', 'done', 'cancel'] 중 하나")
    ord_type = Column(CHAR(10), nullable=False, comment="주문 타입, ['limit', 'price', 'market'] 중 하나")
    volume = Column(Float, nullable=False, comment="주문량")
    remaining_volume = Column(Float, nullable=False, comment="남은 주문량")
    value = Column(Float, nullable=False, comment="주문 대금(KRW)")
    trade_fee = Column(Float, nullable=False, comment="수수료")
    
    def __init__(self, market_code,
                 side, state, ord_type,
                 volume, remaining_volume,
                 value, trade_fee):
        self.market_code = market_code
        self.side = side
        self.state = state
        self.ord_type = ord_type
        self.volume = volume
        self.remaining_volume = remaining_volume
        self.value = value
        self.trade_fee = trade_fee
        
    def columns(self) -> list:
        return [c.name for c in self.__table__.columns]