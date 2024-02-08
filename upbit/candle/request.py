from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class CandleRequest:
    market: str # KRW-BTC
    to: str = datetime.now().isoformat(sep='T', timespec='seconds') # 2023-01-01T00:00:00+09:00
    count: int = 200 # up to 200
    
    def to_dict(self):
        return {
            "market": self.market,
            "to": self.to,
            "count": self.count
        }