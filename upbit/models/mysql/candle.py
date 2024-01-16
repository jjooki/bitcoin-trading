from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Index, Column, Integer, CHAR, VARCHAR, String, DateTime, Float, Date

class MinuteCandle(Base):
    __tablename__ = "minute_candle_5min"
    idx = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(VARCHAR(10), comment="시장 코드, ex) 'KRW-BTC'")
    trade_date_time = Column(DateTime, comment="캔들 기준 시각(KST 기준)")
    open_price = Column(Float, comment="시가")
    high_price = Column(Float, comment="고가")
    low_price = Column(Float, comment="저가")
    trade_price = Column(Float, comment="종가")
    candle_trade_value = Column(Float, comment="해당 캔들의 누적 거래 금액")
    candle_trade_volume = Column(Float, comment="해당 캔들의 누적 거래량"),
    IDX_CODE_TRADE_DATE = Index("IDX_CODE_TRADE_DATE", "code", "trade_date_time")
    
    def __init__(self, code, trade_date_time,
                 open_price, high_price,
                 low_price, trade_price,
                 candle_trade_value, 
                 candle_trade_volume):
        self.code = code
        self.trade_date_time = trade_date_time
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.trade_price = trade_price
        self.candle_trade_value = candle_trade_value
        self.candle_trade_volume = candle_trade_volume
    
    def __repr__(self):
        return f"<MinuteCandle(code={self.code}, trade_date_time={self.trade_date_time}, open_price={self.open_price}, high_price={self.high_price}, low_price={self.low_price}, trade_price={self.trade_price}, candle_trade_value={self.candle_trade_value}, candle_trade_volume={self.candle_trade_volume})>"
    
    def columns(self) -> list:
        return [c.name for c in self.__table__.columns]
    

class DayCandel(Base):
    __tablename__ = "day_candle"
    idx = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(VARCHAR(10), nullable=False, comment="시장 코드, ex) 'KRW-BTC'")
    trade_date = Column(Date, nullable=False, comment="캔들 기준 날짜(KST 기준)")
    open_price = Column(Float, comment="시가")
    high_price = Column(Float, comment="고가")
    low_price = Column(Float, comment="저가")
    trade_price = Column(Float, comment="종가")
    candle_trade_value = Column(Float, comment="해당 캔들의 누적 거래 금액")
    candle_trade_volume = Column(Float, comment="해당 캔들의 누적 거래량"),
    prev_closing_price = Column(Float, comment="전일 종가(UTC 0시 기준)")
    change_rate = Column(Float, comment="전일 종가 대비 등락률")
    
    def __init__(self, code, trade_date,
                 open_price, high_price,
                 low_price, trade_price,
                 candle_trade_value,
                 candle_trade_volume,
                 prev_closing_price,
                 change_rate):
        self.code = code
        self.trade_date = trade_date
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.trade_price = trade_price
        self.candle_trade_value = candle_trade_value
        self.candle_trade_volume = candle_trade_volume
        self.prev_closing_price = prev_closing_price
        self.change_rate = change_rate
        
    def __repr__(self):
        return f"<DayCandel(code={self.code}, trade_date={self.trade_date}, open_price={self.open_price}, high_price={self.high_price}, low_price={self.low_price}, trade_price={self.trade_price}, candle_acc_trade_value={self.candle_acc_trade_value}, candle_acc_trade_volume={self.candle_acc_trade_volume}, prev_closing_price={self.prev_closing_price}, change_rate={self.change_rate})>"
    
    def columns(self) -> list:
        return [c.name for c in self.__table__.columns]