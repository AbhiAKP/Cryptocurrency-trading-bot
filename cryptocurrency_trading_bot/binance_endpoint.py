import os
import time
import socket
import requests
import datetime
import pandas as pd
from binance import Client

class BinanceEndpoint:
    
    #Gets a dataframe with the pricedata of any crypto in any time period and interval
    def get_historical_price_data(self, ticker, time_interval, time_period, binance_client):
        try:
            candle_sticks = binance_client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, time_interval)
            for i in range(len(candle_sticks)):
                candle_sticks[i] = candle_sticks[i][:6]
                candle_sticks[i][0] = datetime.datetime.fromtimestamp(candle_sticks[i][0]/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
        
            data_frame = pd.DataFrame(candle_sticks)
            data_frame.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
            data_frame.Date = pd.to_datetime(data_frame.Date)
            data_frame.Open = pd.to_numeric(data_frame.Open, downcast="float")
            data_frame.High = pd.to_numeric(data_frame.High, downcast="float")
            data_frame.Low = pd.to_numeric(data_frame.Low, downcast="float")
            data_frame.Close = pd.to_numeric(data_frame.Close, downcast="float")
            data_frame.Volume = pd.to_numeric(data_frame.Volume, downcast="float")
            data_frame.set_index("Date", inplace=True)
    
            return data_frame

        except socket.timeout:
            print("[x]  socket timed out")
            exit()
        except requests.exceptions.Timeout:
            print("[x] request timed out")
            exit()
        except requests.exceptions.ConnectionError:
            print("[x] connection error timed out")
            exit()


    #gets the past orders placed on a specific cryptocurrency
    def get_order_book(self, binance_client, ticker, limit):
        try:
            orders = binance_client.get_all_orders(symbol=ticker, limit=10)
            return orders
        except socket.timeout:
            print("[x]  socket timed out")
            exit()
        except requests.exceptions.Timeout:
            print("[x] request timed out")
            exit()
        except requests.exceptions.ConnectionError:
            print("[x] connection error timed out")
            exit()

    #Get the current price of a particular ticker
    def get_current_price(self, ticker, client):
        try:
            print(ticker)
            candle_sticks = client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "3 minute ago UTC")
            return candle_sticks[-1][0], candle_sticks[-1][4]
        except socket.timeout:
            print("[x]  socket timed out")
            exit()
        except requests.exceptions.Timeout:
            print("[x] request timed out")
            exit()
        except requests.exceptions.ConnectionError:
            print("[x] connection error timed out")
            exit()

    def buy():
        pass
