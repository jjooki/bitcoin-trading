from models import MarketRequest, MarketResponse
from models.mysql.market import MarketInfo

def get_market_info(market_request: MarketRequest) -> MarketResponse: