import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote

class Myupbit:
    def __init__(self):
        self.access_key = os.getenv('UPBIT_OPEN_API_ACCESS_KEY')
        self.secret_key = os.getenv('UPBIT_OPEN_API_SECRET_KEY')
        self.server_url = os.getenv('UPBIT_OPEN_API_SERVER_URL')

        self.payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
        }
        
        self.endpoint = {}
        
    def set_payload(self, params: dict) -> dict:
        query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()
        
        _payload = self.payload
        _payload['query_hash'] = query_hash
        _payload['query_hash_alg'] = 'SHA512'
        return _payload
        
    def exchange_request(self, method: str, endpoint: str, params: dict):
        self.set_payload(params)
        self.jwt_token = jwt.encode(self.payload, self.secret_key)
        self.authorization = 'Bearer {}'.format(self.jwt_token)
        headers = {
            'Authorization': self.authorization,
        }
        url = self.server_url + endpoint
        
        response = requests.request(method, self.server_url, params=params, headers=headers)
        assert response.status_code == 200, "Error: {}".format(response.json())
        return response
    
    def quotation_request(self, endpoint: str, params: dict=None):
        headers = {"accept": "application/json"}
        url = self.server_url + endpoint
        
        if params:
            response = requests.get(url, headers=headers, params=params)
        else:
            response = requests.get(url, headers=headers)
            
        assert response.status_code == 200, "Error: {}".format(response.json())
        
        return response
        