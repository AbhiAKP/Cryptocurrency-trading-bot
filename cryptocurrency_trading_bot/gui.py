import threading
import pandas as pd
import tkinter as tk
import mplfinance as mpf
import matplotlib.pyplot as plt
import cryptocurrency_trading_bot as ctb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Gui:
    def __init__(self):
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
        
        user = ctb.User()
        binance_end_point = ctb.BinanceEndpoint()
        binance_end_point.get_historical_price_data("BTCUSDT", user.get_client())
        t1 = threading.Thread(target = self.get_client_data())
        t1.start()

        self.window.protocol("WM_DELETE_WINDOW",self.on_closing)
        self.window.mainloop()
    
    def get_client_data(self):
        self.user = ctb.User()
        self.binance_end_point = ctb.BinanceEndpoint()
        self.binance_end_point.get_historical_price_data("BTCUSDT", self.user.get_client())
        self.binance_end_point.start_price_getter_thread("BTCUSDT", self.user.get_client())

    def create_chart():
        pass

    def on_closing(self):
        plt.close('all')
        window.destroy()
        os.system("rm -r pricedatafiles")
        self.binance_end_point.price_getter_flag = False
