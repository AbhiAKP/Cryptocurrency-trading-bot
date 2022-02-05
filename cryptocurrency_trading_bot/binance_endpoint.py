import os
import socket
import requests
import datetime
import pandas as pd
from binance import Client

class BinanceEndpoint:
    def get_historical_price_data(self, ticker, binance_client):
        try:
            candle_sticks = binance_client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "20 minute ago UTC")
            for i in range(len(candle_sticks)):
                candle_sticks[i] = candle_sticks[i][:6]
                candle_sticks[i][0] = datetime.datetime.fromtimestamp(candle_sticks[i][0]/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
        
            data_frame = pd.DataFrame(candle_sticks)
            data_frame.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
            data_frame.Date = pd.to_datetime(data_frame.Date)
            os.mkdir("pricedatafiles")
            data_frame.to_csv("pricedatafiles/price_data.csv")

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

    def get_recent_price_data(self, ):
        klines = config.binance_client.get_historical_klines(ticker_string, Client.KLINE_INTERVAL_1MINUTE, "4 minute ago UTC")
        i = -1
        while (ticker_price_data[i][0] != klines[0][:5]):
            i = i -1
        ticker_closes = ticker_closes[:i]
        for candle in klines:
            ticker_closes.append(float(candle[4]))
        return ticker_closes

