from dataclasses import dataclass, field
from typing import Literal

@dataclass
class CandleResponse:
    market: str # KRW-BTC
    candle_date_time_utc: str # 2021-01-01T00:00:00
    candle_date_time_kst: str # 2021-01-01T09:00:00
    opening_price: float
    high_price: float
    low_price: float
    trade_price: float
    timestamp: int
    candle_acc_trade_price: float
    candle_acc_trade_volume: float
    unit: int = None
    
    def to_dict(self):
        return {
            "market": self.market,
            "candle_date_time_utc": self.candle_date_time_utc,
            "candle_date_time_kst": self.candle_date_time_kst,
            "opening_price": self.opening_price,
            "high_price": self.high_price,
            "low_price": self.low_price,
            "trade_price": self.trade_price,
            "timestamp": self.timestamp,
            "candle_acc_trade_price": self.candle_acc_trade_price,
            "candle_acc_trade_volume": self.candle_acc_trade_volume,
            "unit": self.unit
        }
        
    def minute_candle_5min(self):
        return {
            "code": self.market,
            "trade_date_time": self.candle_date_time_kst,
            "open_price": self.opening_price,
            "high_price": self.high_price,
            "low_price": self.low_price,
            "trade_price": self.trade_price,
            "candle_trade_value": self.candle_acc_trade_price,
            "candle_trade_volume": self.candle_acc_trade_volume,
        }
        
    def day_candle(self):
        return {
            "code": self.market,
            "trade_date": self.candle_date_time_kst,
            "open_price": self.opening_price,
            "high_price": self.high_price,
            "low_price": self.low_price,
            "trade_price": self.trade_price,
            "candle_trade_value": self.candle_acc_trade_price,
            "candle_trade_volume": self.candle_acc_trade_volume,
            "prev_closing_price": None,
            "change_rate": None
        }