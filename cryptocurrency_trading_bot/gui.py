import time
import datetime
import threading
import pandas as pd
import tkinter as tk
import mplfinance as mpf
import matplotlib.pyplot as plt
import cryptocurrency_trading_bot as ctb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Gui:
    def __init__(self, enable_gui):
        self.continue_canvas_flag = True
        self.continue_trading_flag = True
        
        self.user = ctb.User()
        self.binance_end_point = ctb.BinanceEndpoint()

        trader_thread = threading.Thread(target = self.start_trading)
        trader_thread.start()

        if(enable_gui):
           self.create_gui()
    
    def create_gui(self):
        self.window = tk.Tk()
        self.window.title("Cryptocurrency trading bot") 
        self.window.geometry('1270x720')
        self.window.configure(bg="#02082b")

        self.graphFrame = tk.Frame(self.window, width=790, height= 600, bg='#34568B')
        self.graphFrame.grid(row=0, column=0, padx=10)
        self.graphFrame.pack_propagate(False)

        self.recentTradesFrame = tk.Frame(self.window, width=390, height=600, bg='#340d69' )
        self.recentTradesFrame.grid(row=0, column=1, padx=10)
        self.recentTradesFrame.grid_propagate(False)

        tk.Label(self.recentTradesFrame, text="Recently Executed Trades", bg="#340d69", fg="#ffffff", font=("Verdana",15)).grid(row=0, column=0, padx=8, pady=5)
        
        canvas_updater_thread = threading.Thread(target = self.create_canvas)
        canvas_updater_thread.start()

        self.window.protocol("WM_DELETE_WINDOW",self.on_closing)
        self.window.mainloop()
    
    def update_recent_trades():
        self.binance_client.get_order_book(self.user.get_client, "BTCUSDT", 10)
        dummy_data = """[{'symbol': 'BTCUSDT', 'orderId': 8125606451, 'orderListId': -1, 'clientOrderId': 'aVPpKqHVv6aGzjucuN5sBQ', 'price': '0.00000000', 'origQty': '0.00019000', 'executedQty': '0.00019000', 'cummulativeQuoteQty': '11.67528910', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'SELL', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635782957004, 'updateTime': 1635782957004, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8143249167, 'orderListId': -1, 'clientOrderId': '9wu939GhI1i7Dnk54ImsSr', 'price': '0.00000000', 'origQty': '0.00022000', 'executedQty': '0.00022000', 'cummulativeQuoteQty': '13.86112640', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635921983181, 'updateTime': 1635921983181, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8143457694, 'orderListId': -1, 'clientOrderId': 'and_02ce21cd0192465390a0e62402081a65', 'price': '62971.48000000', 'origQty': '0.00022000', 'executedQty': '0.00022000', 'cummulativeQuoteQty': '13.85508520', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'SELL', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635923918001, 'updateTime': 1635923918001, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8144005634, 'orderListId': -1, 'clientOrderId': 'QFKAXVzvWXmUtNWjNwOXXL', 'price': '0.00000000', 'origQty': '0.00021000', 'executedQty': '0.00021000', 'cummulativeQuoteQty': '13.21517820', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635928277108, 'updateTime': 1635928277108, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8144019925, 'orderListId': -1, 'clientOrderId': 'and_faa911d6ca3f4a1f9800b40526e28a19', 'price': '62983.34000000', 'origQty': '0.00021000', 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'CANCELED', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'SELL', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635928377003, 'updateTime': 1635928417273, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8144024961, 'orderListId': -1, 'clientOrderId': 'and_a8f0160a2c1f4ea693b79640b46164b3', 'price': '0.00000000', 'origQty': '0.00021000', 'executedQty': '0.00021000', 'cummulativeQuoteQty': '13.22180790', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'SELL', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635928419905, 'updateTime': 1635928419905, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8144033821, 'orderListId': -1, 'clientOrderId': '0YkvXvqtLzCnxTeNgoOh9e', 'price': '0.00000000', 'origQty': '0.00021000', 'executedQty': '0.00021000', 'cummulativeQuoteQty': '13.21737900', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635928484750, 'updateTime': 1635928484750, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8148493013, 'orderListId': -1, 'clientOrderId': 'and_187114c0e65c4b188ba3c645ece88bb4', 'price': '62518.99000000', 'origQty': '0.00021000', 'executedQty': '0.00021000', 'cummulativeQuoteQty': '13.12993080', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'SELL', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635961063125, 'updateTime': 1635961063125, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8148501940, 'orderListId': -1, 'clientOrderId': 'iUQAGajZz5to3OFLlApuvE', 'price': '0.00000000', 'origQty': '0.00021000', 'executedQty': '0.00021000', 'cummulativeQuoteQty': '13.11979200', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635961142578, 'updateTime': 1635961142578, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8148533881, 'orderListId': -1, 'clientOrderId': '71rRHSGmsCPhaeCKoJi2qV', 'price': '0.00000000', 'origQty': '0.00021000', 'executedQty': '0.00021000', 'cummulativeQuoteQty': '13.12551660', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'SELL', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635961489804, 'updateTime': 1635961489804, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}]"""
        #TODO: implement updating trades

    def start_trading(self):
        trader_text = tk.StringVar()
        trader_text.set("Start trading")
        label = tk.Label(self.window, textvariable=trader_text, bg="#340d69", fg="#ffffff", font=("Verdana",15)).grid(row=1, column=0, padx=8, pady=5)
        while(self.continue_trading_flag):
            data_frame = self.binance_end_point.get_historical_price_data("BTCUSDT", "50 minute ago UTC", self.user.get_client().KLINE_INTERVAL_1MINUTE, self.user.get_client())
            trading_strategy = ctb.Trading_Strategies()
            data = trading_strategy.rsi(data_frame, 12)
            trader_text.set(data)
            i = 0
            while(i<12 and self.continue_trading_flag):
                time.sleep(4.85)
                i = i + 1

    def create_canvas(self):
            market_colours = mpf.make_marketcolors(up='#23e851',down='#e04212',inherit=True)
            mpf_style  = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors=market_colours)
            
            while(self.continue_canvas_flag):
                data_frame = self.binance_end_point.get_historical_price_data("BTCUSDT", "30 minute ago UTC", self.user.get_client().KLINE_INTERVAL_1MINUTE, self.user.get_client())
                fig, _ = mpf.plot(data_frame, type="candle", mav=(20), volume=True, tight_layout=True, style=mpf_style, returnfig=True)

                canvas = FigureCanvasTkAgg(fig, self.graphFrame)
                canvas.draw()
                canvas.get_tk_widget().grid(row=0, column=0, padx=15, pady=15)
                i = 0
                while(i<12 and self.binance_end_point.price_getter_flag):
                    time.sleep(5)
                    i = i + 1

    def on_closing(self):
        plt.close('all')
        self.window.destroy()
        self.continue_trading_flag = False
        self.continue_canvas_flag = False
