import socket
import requests
from binance import Client
from cryptocurrency_trading_bot import api_keys

class User:
    def __init__(self):
        self._api_key = api_keys.API_KEY
        self._api_secret = api_keys.API_SECRET
        
        try:
            self._client = Client(self._api_key, self._api_secret)
        except socket.timeout:
            print("[x] "+ticker+" socket timed out")
            print("[x] Terminating trading with "+ticker)
            exit()
        except requests.exceptions.Timeout:
            print("[x] "+ticker+" socket timed out")
            print("[x] Terminating trading with "+ticker)
            exit()
        except requests.exceptions.ConnectionError:
            print("[x] "+ticker+" socket timed out")
            print("[x] Terminating trading with "+ticker)
            exit()
    
    def get_client(self):
        return self._client

if __name__=="__main__":
    user = User()
    