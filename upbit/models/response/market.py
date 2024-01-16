from dataclasses import dataclass
from typing import Literal, Optional

@dataclass
class MarketResponse:
    market: str
    korean_name: str
    english_name: str
    market_warning: Optional[Literal['NONE', 'CAUTION']]