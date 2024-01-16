from dataclasses import dataclass
from datetime import datetime
from typing import List, Literal, Union

@dataclass
class BaseOrderResponse:
    uuid: str
    side: str
    ord_type: str
    price: Union[float, str]
    state: str
    market: str
    created_at: Union[datetime, str]
    volume: Union[float, str]
    remaining_volume: Union[float, str]
    reserved_fee: Union[float, str]
    remaining_fee: Union[float, str]
    paid_fee: Union[float, str]
    locked: Union[float, str]
    executed_volume: Union[float, str]
    trades_count: int

@dataclass
class OrderResponse(BaseOrderResponse):
    pass

@dataclass
class IndividualOrderResponse(BaseOrderResponse):
    trades: List[dict]

@dataclass
class OrderChanceResponse:
    bid_fee: Union[float, str]
    ask_fee: Union[float, str]
    market: dict
    bid_account: dict
    ask_account: dict

@dataclass
class OrderListResponse(BaseOrderResponse):
    pass

@dataclass
class CancelOrderResponse(BaseOrderResponse):
    pass