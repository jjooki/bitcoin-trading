import jwt
import hashlib
import os
import requests
import uuid
import json
from urllib.parse import urlencode, unquote

access_key = os.getenv('UPBIT_OPEN_API_ACCESS_KEY')
secret_key = os.getenv('UPBIT_OPEN_API_SECRET_KEY')
server_url = os.getenv('UPBIT_OPEN_API_SERVER_URL')

# parameter를 입력하여 queryhash를 만드는 함수
def make_queryhash(params):
    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")
    m = hashlib.sha512()
    m.update(query_string)
    return m.hexdigest()

# queryhash를 입력하여 payload를 만드는 함수
def make_payload(query_hash = "a"):
    if query_hash == "a":
        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }
    else:
        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
    return payload

# parameter를 입력하여 queryhash를 만드는 함수
def make_header(payload):
    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    return {'Authorization': authorization,}

def account():
    payload = make_payload()
    
    jwt_token = jwt.encode(payload, secret_key).decode('utf8')
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
        'Authorization': authorization,
    }
    
    res = requests.get(server_url + '/v1/accounts', headers=headers)
    return res.json()

def ticker_list(market = 'KRW'):
    url = server_url + "/v1/market/all?isDetails=true"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    return [ticker['market'] for ticker in json.loads(response.text) if ticker['market'][:3] == market]

def ticker_info(ticker):
    if isinstance(ticker, str):
        params = {
            'market': ticker
        }
    else:
        return "Input string only!"

    query_hash = make_queryhash(params=params)
    payload = make_payload(query_hash=query_hash)
    headers = make_header(payload=payload)

    res = requests.get(server_url + '/v1/orders/chance', params=params, headers=headers)
    return res.json()

def current_price(ticker):
    url = server_url + "/v1/ticker?markets=KRW-" + ticker
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers) 
    json_data = json.loads(response.text)[0]
    return float(json_data['trade_price'])

def limit_order(ticker, side, price, volume):
    if isinstance(ticker, str):
        params = {
            'market': ticker,
            'side': side,
            'ord_type': 'limit',
            'price': str(price),
            'volume': str(volume),
        }
    else:
        return "Input string only!"

    query_hash = make_queryhash(params=params)
    payload = make_payload(query_hash=query_hash)
    headers = make_header(payload=payload)

    res = requests.post(server_url + '/v1/orders', params=params, headers=headers)
    return res.json()

# side : bid(매수), ask(매도)
def market_order(ticker, side, ord_type, volume):
    if isinstance(ticker, str):
        params = {
            'market': ticker,
            'side': side,
            'ord_type': 'market',
            'price': str(current_price(ticker)),
            'volume': str(volume),
        }
    else:
        return "Input string only!"

    query_hash = make_queryhash(params=params)
    payload = make_payload(query_hash=query_hash)
    headers = make_header(payload=payload)

    res = requests.post(server_url + '/v1/orders', params=params, headers=headers)
    return res.json()

def cancel_order():
    pass

if __name__ == "__main__":
    url = "https://api.upbit.com/v1/market/all?isDetails=true"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    ticker_list = [ticker['market'] for ticker in json.loads(response.text) if ticker['market'][:3] == 'KRW']
    print(ticker_list)
    market_order('KRW-XRP', 'bid', '')
