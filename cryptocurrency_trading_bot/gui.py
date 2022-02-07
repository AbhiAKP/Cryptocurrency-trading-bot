import time
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
        
        self.user = ctb.User()
        self.binance_end_point = ctb.BinanceEndpoint()

        price_getter_thread = threading.Thread(target = self.get_client_data)
        canvas_updater_thread = threading.Thread(target = self.create_canvas)
        price_getter_thread.start()
        canvas_updater_thread.start()
        if(enable_gui):
            self.window.protocol("WM_DELETE_WINDOW",self.on_closing)
            self.window.mainloop()
    
    def get_client_data(self):
        self.prices = self.binance_end_point.get_historical_price_data("BTCUSDT", "8 day ago UTC", self.user.get_client())
        # self.binance_end_point.start_price_getter_thread("BTCUSDT", self.user.get_client())

    def create_canvas(self):
            market_colours = mpf.make_marketcolors(up='#23e851',down='#e04212',inherit=True)
            mpf_style  = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors=market_colours)
            
            while(self.continue_canvas_flag):
                data_frame = self.binance_end_point.get_historical_price_data("BTCUSDT", "30 minute ago UTC", self.user.get_client())
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
        self.binance_end_point.price_getter_flag = False
        self.continue_canvas_flag = False
