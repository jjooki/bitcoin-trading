from dataclasses import dataclass
from typing import List, Literal, Optional

@dataclass
class OrderRequest:
    market: str
    side: Literal['ask', 'bid']
    volume: str
    price: str
    ord_type: Literal['limit', 'price', 'market']
    identifier: Optional[str]

@dataclass
class IndividualOrderRequest:
    uuid: str
    identifier: Optional[str]
    
@dataclass
class OrderChanceRequest:
    market: str
    
@dataclass
class OrderListRequest:
    market: str
    uuids: List[str]
    identifiers: List[str]
    state: Literal['wait', 'watch', 'done', 'cancel']
    states: List[str]
    page: int
    limit: int
    order_by: Literal['desc', 'asc']

@dataclass
class CancelOrderRequest:
    uuid: str
    identifier: Optional[str]