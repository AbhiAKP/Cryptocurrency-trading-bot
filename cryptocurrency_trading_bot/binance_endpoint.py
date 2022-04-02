import os
import time
import socket
import requests
import datetime
import pandas as pd
from binance import Client

class BinanceEndpoint:

    def __init__(self, binance_client, user):
        self.binance_client = binance_client
        self.candle_sticks = []
        self.user = user

    #converts the latest prices into a pandas data frame and returns it
    def get_historical_prices_dataframe(self, time_period):
        data_frame = pd.DataFrame(self.candle_sticks[-time_period:])
        data_frame.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        data_frame.Date = pd.to_datetime(data_frame.Date)
        data_frame.Open = pd.to_numeric(data_frame.Open, downcast="float")
        data_frame.High = pd.to_numeric(data_frame.High, downcast="float")
        data_frame.Low = pd.to_numeric(data_frame.Low, downcast="float")
        data_frame.Close = pd.to_numeric(data_frame.Close, downcast="float")
        data_frame.Volume = pd.to_numeric(data_frame.Volume, downcast="float")
        data_frame.set_index("Date", inplace=True)
        return data_frame
    
    #Gets a dataframe with the pricedata of any crypto in any time period and interval
    def get_historical_price_data(self, ticker, time_interval, time_period):
        try:
            self.candle_sticks = self.binance_client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, time_interval)
            for i in range(len(self.candle_sticks)):
                self.candle_sticks[i] = self.candle_sticks[i][:6]
                self.candle_sticks[i][0] = datetime.datetime.fromtimestamp(self.candle_sticks[i][0]/1000).strftime('%Y-%m-%d %H:%M')
            
            self.user.buffer_period = True
            while(self.user.continue_trading_flag):
                klines = self.binance_client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "6 minute ago UTC")
                for i in range(len(klines)):
                    klines[i] = klines[i][:6]
                    klines[i][0] = datetime.datetime.fromtimestamp(klines[i][0]/1000).strftime('%Y-%m-%d %H:%M')
                i = -1
                while self.candle_sticks[i][0]!=klines[0][0]:
                    i = i -1
                self.candle_sticks = self.candle_sticks[:i]
                for candle in klines:
                    self.candle_sticks.append(candle)
                i = 0
                while(self.user.continue_trading_flag and i < 115):
                    time.sleep(0.45)
                    i += 1 
        except Exception as e:
            print("[*] Exception occurred while trying to get historical prices: ",e)

    #gets the past orders placed on a specific cryptocurrency
    def get_order_book(self, ticker, limit):
        # print("get order book, limit:", limit)
        try:
            orders = self.binance_client.get_all_orders(symbol=ticker, limit=limit)
            for order in orders:
                ts = int(order["time"])
                order["time"] = datetime.datetime.utcfromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M') + " GTC"
                order["type"] = "LIMT" if order["type"].lower() == "limit" else "MKT"
                order.pop("clientOrderId")
                order.pop("orderListId")
                order.pop("timeInForce")
                order.pop("icebergQty")
                order.pop("isWorking")
                order.pop("price")
                order.pop("origQuoteOrderQty")
            orders.reverse()
            return orders
        except socket.timeout:
            print("[*] Socket timed out while trying to get order book, try again")
            return None, None
        except requests.exceptions.Timeout:
            print("[*] Request timed out while trying to get order book, try again")
            return None, None
        except requests.exceptions.ConnectionError:
            print("[*] Connection error occurred while trying to get oder book, try again")
            return None, None

    #Get the current price of a particular ticker
    def get_last_close(self):
        return self.candle_sticks[-1][4],self.candle_sticks[-1][0]
    
    #Get the current live price
    def get_current_live_price(self):
        try:
            candle_sticks = self.binance_client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "3 minute ago UTC")
            return candle_sticks[-1][4]
        except socket.timeout:
            return None
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.ConnectionError:
            return None