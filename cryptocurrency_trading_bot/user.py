import socket
import requests
from binance import Client
from cryptocurrency_trading_bot import api_keys

class User():
    def __init__(self):
        #Creates a binance client object using api key and secret
        self._api_key = api_keys.API_KEY
        self._api_secret = api_keys.API_SECRET
        
        try:
            self._client = Client(self._api_key, self._api_secret)
        except socket.timeout:
            print("[x] socket timed out")
            exit()
        except requests.exceptions.Timeout:
            print("[x] socket timed out")
            exit()
        except requests.exceptions.ConnectionError:
            print("[x] socket timed out")
    
    def get_client(self):
        return self._client

if __name__=="__main__":
    user = User()
    