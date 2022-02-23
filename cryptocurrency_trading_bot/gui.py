import mplfinance as mpf
import matplotlib
import matplotlib.pyplot as plt
import cryptocurrency_trading_bot as ctb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import ttk


class Gui:
    canvas = None
    a = 2
    def __init__(self, enable_gui):
        self.continue_canvas_flag = True
        self.continue_trading_flag = True
        
        self.user = ctb.User()
        self.binance_end_point = ctb.BinanceEndpoint()

        self.trading_strategies = ctb.Trading_Strategies()

        if(enable_gui):
           self.create_gui()

    def create_canvas(self):
            # print("executed trade.............................")
            market_colours = mpf.make_marketcolors(up='#07d400',down='#d40000',inherit=True)
            mpf_style  = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors=market_colours)
            
           
            data_frame = self.binance_end_point.get_historical_price_data("BTCUSDT", "200 minute ago UTC", self.user.get_client().KLINE_INTERVAL_1MINUTE, self.user.get_client())
            fig, _ = mpf.plot(data_frame, type="candle", mav=(20), volume=True, tight_layout=True, style=mpf_style, returnfig=True)

            #deletes the previous canvas so that the next canvas can occupy the space
            if (isinstance(self.canvas, matplotlib.backends.backend_tkagg.FigureCanvasTkAgg)):
                self.canvas.get_tk_widget().destroy()
            self.canvas = FigureCanvasTkAgg(fig, self.graph_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=LEFT, fill="both", expand=True, padx=35, pady=15)

            self.window.after(30000, self.create_canvas)
                        


    def create_gui(self):
        self.window = Tk()
        self.window.title("Cryptocurrency trading bot") 
        self.window.resizable(True, True)
        self.window.config()
        self.app_icon = PhotoImage(file="images/icons.png")
        self.window.iconphoto(True, self.app_icon)

        #constructing frames to bind widgets wherever required

        #creating the menu frame which will consists of menubar
        self.menu_frame = Frame(self.window, bg="#0b1047", width=1200, height=50, relief=SUNKEN, pady=10, padx=50, bd=10, borderwidth=5)
        self.menu_frame.pack(side=TOP, fill="x", expand=False)

        self.setting_photo = PhotoImage(file="images/user_icons.png")
        self.user_icon = self.setting_photo.subsample(3, 3)

        self.user_photo = PhotoImage(file="images/setting_icon.png")
        self.setting_icon = self.user_photo.subsample(3, 3)

        Button(self.menu_frame, image=self.user_icon, bg="white", activebackground="#1f2769", cursor="hand2").pack(side=RIGHT, padx=15)
        Button(self.menu_frame, image=self.setting_icon, bg="white", activebackground="#1f2769", cursor="hand2").pack(side=RIGHT, padx=15)
        Button(self.menu_frame, text="Menu1", font=('Helvetica', 12), activebackground="#1f2769", activeforeground="white", cursor="hand2").pack(side=LEFT, padx=15, ipadx=5)
        Button(self.menu_frame, text="Menu2", font=('Helvetica', 12), activebackground="#1f2769", activeforeground="white", cursor="hand2").pack(side=LEFT, padx=15, ipadx=5)
        Button(self.menu_frame, text="Menu3", font=('Helvetica', 12), activebackground="#1f2769", activeforeground="white", cursor="hand2").pack(side=LEFT, padx=15, ipadx=5)
        Button(self.menu_frame, text="Menu4", font=('Helvetica', 12), activebackground="#1f2769", activeforeground="white", cursor="hand2").pack(side=LEFT, padx=15, ipadx=5)

        #creaing the portfolio frame to show open orders and funds
        self.portfolio_frame = Frame(self.window, width=1200, bg="#232a75", height=300, relief=GROOVE, bd=10, borderwidth=10)
        self.portfolio_frame.pack(side=BOTTOM, fill="x", expand=False)

        #creating multiple tabs in the portfolio frame
        self.s = ttk.Style()
        self.s.configure('.', font=('Arial', 12))
        self.notebook = ttk.Notebook(self.portfolio_frame)

        self.open_orders = Frame(self.notebook, width=1200, height=260, bg="#4656fa")
        self.order_history = Frame(self.notebook, width=1200, height=260, bg="#4656fa")
        self.trade_history = Frame(self.notebook, width=1200, height=260, bg="#4656fa")
        self.available_funds = Frame(self.notebook, width=1200, height=260, bg="#4656fa")

        self.notebook.add(self.open_orders, text="   Open Orders   ")
        self.notebook.add(self.order_history, text="   Order History   ")
        self.notebook.add(self.trade_history, tex="   Trade History   ")
        self.notebook.add(self.available_funds, text="   Funds   ")

        self.notebook.pack(side=LEFT, fill="both", expand=True)

        # Label(self.open_orders, text="This is the open orders section").pack(side=TOP)
        # Label(self.order_history, text="This is the order_history section").pack(side=TOP)
        # Label(self.trade_history, text="This is the trade history section").pack(side=TOP)
        # Label(self.available_funds, text="This is the funds section").pack(side=TOP)

        #creating a graph frame to plot the candle stick chart
        self.graph_frame = Frame(self.window, width=800, bg="#232a75", height=500, relief=GROOVE, borderwidth=1)
        self.graph_frame.pack(side=LEFT, fill="both", expand=True)

        #Call create_canvas to draw canvas on to the graph_frame
        self.create_canvas()

        #creating trade frame and putting recent trade actions into the frame
        self.trade_frame = Frame(self.window, bg="#5b64ba", width=400, height=500, relief=SUNKEN, bd=10)
        self.trade_frame.pack(side=RIGHT, fill="both", expand=False)

        self.green_bar_image = PhotoImage(file="images/green_bar.png")
        self.red_bar_image = PhotoImage(file="images/red_bar.png")

        Label(self.trade_frame, image=self.red_bar_image, bg="#c2c8ff", width=400).pack()
        Label(self.trade_frame, text="Recent Trades", font=('Arial', 20), bg="#c2c8ff").pack()
        Label(self.trade_frame, image=self.green_bar_image, bg="#c2c8ff", width=400).pack()



        self.window.protocol("WM_DELETE_WINDOW",self.on_closing)
        self.window.mainloop()

    

    def on_closing(self):
        plt.close('all')
        self.window.destroy()
        self.trading_strategies.continue_trading_flag = False



    # def update_recent_trades(self):
    #     self.binance_client.get_order_book(self.user.get_client, "BTCUSDT", 10)
    #     dummy_data = """[{'symbol': 'BTCUSDT', 'orderId': 8125606451, 'orderListId': -1, 'clientOrderId': 'aVPpKqHVv6aGzjucuN5sBQ', 'price': '0.00000000', 'origQty': '0.00019000', 'executedQty': '0.00019000', 'cummulativeQuoteQty': '11.67528910', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'SELL', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635782957004, 'updateTime': 1635782957004, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8143249167, 'orderListId': -1, 'clientOrderId': '9wu939GhI1i7Dnk54ImsSr', 'price': '0.00000000', 'origQty': '0.00022000', 'executedQty': '0.00022000', 'cummulativeQuoteQty': '13.86112640', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635921983181, 'updateTime': 1635921983181, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8143457694, 'orderListId': -1, 'clientOrderId': 'and_02ce21cd0192465390a0e62402081a65', 'price': '62971.48000000', 'origQty': '0.00022000', 'executedQty': '0.00022000', 'cummulativeQuoteQty': '13.85508520', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'SELL', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635923918001, 'updateTime': 1635923918001, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8144005634, 'orderListId': -1, 'clientOrderId': 'QFKAXVzvWXmUtNWjNwOXXL', 'price': '0.00000000', 'origQty': '0.00021000', 'executedQty': '0.00021000', 'cummulativeQuoteQty': '13.21517820', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635928277108, 'updateTime': 1635928277108, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8144019925, 'orderListId': -1, 'clientOrderId': 'and_faa911d6ca3f4a1f9800b40526e28a19', 'price': '62983.34000000', 'origQty': '0.00021000', 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'CANCELED', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'SELL', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635928377003, 'updateTime': 1635928417273, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8144024961, 'orderListId': -1, 'clientOrderId': 'and_a8f0160a2c1f4ea693b79640b46164b3', 'price': '0.00000000', 'origQty': '0.00021000', 'executedQty': '0.00021000', 'cummulativeQuoteQty': '13.22180790', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'SELL', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635928419905, 'updateTime': 1635928419905, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8144033821, 'orderListId': -1, 'clientOrderId': '0YkvXvqtLzCnxTeNgoOh9e', 'price': '0.00000000', 'origQty': '0.00021000', 'executedQty': '0.00021000', 'cummulativeQuoteQty': '13.21737900', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635928484750, 'updateTime': 1635928484750, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8148493013, 'orderListId': -1, 'clientOrderId': 'and_187114c0e65c4b188ba3c645ece88bb4', 'price': '62518.99000000', 'origQty': '0.00021000', 'executedQty': '0.00021000', 'cummulativeQuoteQty': '13.12993080', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'SELL', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635961063125, 'updateTime': 1635961063125, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8148501940, 'orderListId': -1, 'clientOrderId': 'iUQAGajZz5to3OFLlApuvE', 'price': '0.00000000', 'origQty': '0.00021000', 'executedQty': '0.00021000', 'cummulativeQuoteQty': '13.11979200', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635961142578, 'updateTime': 1635961142578, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}, {'symbol': 'BTCUSDT', 'orderId': 8148533881, 'orderListId': -1, 'clientOrderId': '71rRHSGmsCPhaeCKoJi2qV', 'price': '0.00000000', 'origQty': '0.00021000', 'executedQty': '0.00021000', 'cummulativeQuoteQty': '13.12551660', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'SELL', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1635961489804, 'updateTime': 1635961489804, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}]"""
    #     #TODO: implement updating trades



    # def start_trading(self):
    #     trader_text = StringVar()
    #     trader_text.set("Start trading")
    #     # label = Label(self.window, textvariable=trader_text, bg="#340d69", fg="#ffffff", font=("Verdana",15)).grid(row=1, column=0, padx=8, pady=5)
    #     while(self.continue_trading_flag):
    #         data_frame = self.binance_end_point.get_historical_price_data("BTCUSDT", "50 minute ago UTC", self.user.get_client().KLINE_INTERVAL_1MINUTE, self.user.get_client())
    #         trading_strategy = ctb.Trading_Strategies()
    #         data = trading_strategy.rsi(data_frame, 12)
    #         trader_text.set(data)
    #         i = 0
    #         while(i<12 and self.continue_trading_flag):
    #             time.sleep(4.85)
    #             i = i + 1



