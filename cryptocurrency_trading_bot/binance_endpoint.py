import os
import time
import socket
import requests
import datetime
import pandas as pd
from binance import Client

class BinanceEndpoint:
    price_getter_flag = True
    updating_data_frame_mutex = True
    data_frame = pd.DataFrame()
    
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
            print("[x] "+ticker+" socket timed out")
            exit()
        except requests.exceptions.Timeout:
            print("[x] "+ticker+" socket timed out")
            exit()
        except requests.exceptions.ConnectionError:
            print("[x] "+ticker+" socket timed out")
            exit()


    def get_order_book(self, binance_client, ticker, limit):
        orders = binance_client.get_all_orders(symbol=ticker, limit=10)
        print(orders)

    def buy():
        pass
    # def get_price_data_frame(self):
    #     return self.data_frame
    
    # def start_price_getter_thread(self, ticker, binance_client):
    #     while(self.price_getter_flag):
    #         updating_data_frame_mutex = True
    #         candle_sticks = binance_client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "4 minute ago UTC")
    #         for i in range(len(candle_sticks)):
    #             candle_sticks[i] = candle_sticks[i][:6]
    #             candle_sticks[i][0] = datetime.datetime.fromtimestamp(candle_sticks[i][0]/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
            
    #         # print("\n\nnew data found")
    #         # print(candle_sticks)
    #         i = -1
    #         while(self.data_frame.values.tolist()[i][1:] != candle_sticks[0][1:]):
    #             i = i - 1
    #         # print("found element",i,"where",self.data_frame.values.tolist()[i][1:],"is equal to",candle_sticks[0][1:])
    #         # print("iloc output: \n",self.data_frame.iloc[:i])
    #         self.data_frame = self.data_frame.iloc[:i]
    #         for i in candle_sticks:
    #             self.data_frame.loc[len(self.data_frame)] = i
    #         self.data_frame.Date = pd.to_datetime(self.data_frame.Date)
    #         self.data_frame.set_index("Date", inplace=True)
    #         # print(self.data_frame)
    #         # print("sleeping 58 seconds")
    #         updating_data_frame_mutex = False
    #         i = 0
    #         while(i<12 and self.price_getter_flag):
    #             time.sleep(4.85)
    #             i = i + 1
# be = BinanceEndpoint()
# binance_client = Client(api_keys.API_KEY, api_keys.API_SECRET)
# be.get_order_book(binance_client, "BTCUSDT", 10)