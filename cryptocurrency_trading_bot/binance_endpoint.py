import os
import time
import socket
import requests
import datetime
import pandas as pd
from binance import Client

class BinanceEndpoint:
    price_getter_flag = True

    def get_historical_price_data(self, ticker, binance_client):
        try:
            candle_sticks = binance_client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "9 minute ago UTC")
            for i in range(len(candle_sticks)):
                candle_sticks[i] = candle_sticks[i][:6]
                candle_sticks[i][0] = datetime.datetime.fromtimestamp(candle_sticks[i][0]/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
        
            self.data_frame = pd.DataFrame(candle_sticks)
            self.data_frame.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
            self.data_frame.Date = pd.to_datetime(self.data_frame.Date)
            print("history price data: ")
            print(self.data_frame)
            os.system("mkdir pricedatafiles 2>>/dev/null")
            self.data_frame.to_csv("pricedatafiles/price_data.csv")

        except socket.timeout:
            print("[x] "+ticker+" socket timed out")
            os.system("rm -r pricedatafiles")
            exit()
        except requests.exceptions.Timeout:
            print("[x] "+ticker+" socket timed out")
            os.system("rm -r pricedatafiles")
            exit()
        except requests.exceptions.ConnectionError:
            print("[x] "+ticker+" socket timed out")
            os.system("rm -r pricedatafiles")
            exit()

    def get_recent_price_data(self):
        klines = config.binance_client.get_historical_klines(ticker_string, Client.KLINE_INTERVAL_1MINUTE, "4 minute ago UTC")
        i = -1
        while (ticker_price_data[i][0] != klines[0][:5]):
            i = i -1
        ticker_closes = ticker_closes[:i]
        for candle in klines:
            ticker_closes.append(float(candle[4]))
        return ticker_closes
    
    def start_price_getter_thread(self, ticker, binance_client):
        while(self.price_getter_flag):

            candle_sticks = binance_client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "4 minute ago UTC")
            for i in range(len(candle_sticks)):
                candle_sticks[i] = candle_sticks[i][:6]
                candle_sticks[i][0] = datetime.datetime.fromtimestamp(candle_sticks[i][0]/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
            
            print("\n\nnew data found")
            print(candle_sticks)
            i = -1
            while(self.data_frame.values.tolist()[i][1:] != candle_sticks[0][1:]):
                i = i - 1
            print("found element",i,"where",self.data_frame.values.tolist()[i][1:],"is equal to",candle_sticks[0][1:])
            print("iloc output: \n",self.data_frame.iloc[:i])
            self.data_frame = self.data_frame.iloc[:i]
            for i in candle_sticks:
                self.data_frame.loc[len(self.data_frame)] = i
            self.data_frame.Date = pd.to_datetime(self.data_frame.Date)

            print(self.data_frame)
            print("sleeping 58 seconds")
            time.sleep(58)
        