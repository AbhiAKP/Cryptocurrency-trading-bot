import os
import threading
import matplotlib
from tkinter import *
from tkinter import ttk
from pathlib import Path
import mplfinance as mpf
import matplotlib.pyplot as plt
import cryptocurrency_trading_bot as ctb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


class Gui:
    canvas = None
    single_trade_button = None

    def __init__(self, enable_gui):
        self.enable_gui = enable_gui
        #Checks if the config directory exists
        if(os.path.isdir("config") and os.path.isfile("config/api_keys.py")):
            print("test")
            self.initiate_trading()
        else:
            #If the config directory doesn't exist, create an initial window to prompt the user to enter api_key and api_secret
            self.create_initial_window()

    #Create necessary variables for starting trading and initiate trading
    def initiate_trading(self):
        self.continue_canvas_flag = True
        self.continue_trading_flag = True
        
        self.user = ctb.User()
        self.binance_end_point = ctb.BinanceEndpoint(self.user.get_client())
        self.user.set_trading_details(1000, 12, 0, self.binance_end_point.get_order_book("BTCUSDT", 50))

        self.trading_strategies = ctb.Trading_Strategies(ticker="BTCUSDT", binance_end_point=self.binance_end_point, user=self.user, paper_trading=True)
        trading_thread = threading.Thread(target = self.trading_strategies.rsi, args = (14,))
        # trading_thread.start()
        
        self.portfolio_dummy_data = [{'symbol': 'BTC', 'balance': '0.00000006', 'symbol_name': 'Bitcoin', 'usd_value': '43923.49000000'}, {'symbol': 'SOL', 'balance': '0.37000000', 'symbol_name': 'Solana', 'usd_value': '101.47000000'}, {'symbol': 'HNT', 'balance': '0.41000000', 'symbol_name': 'Helium', 'usd_value': '27.18000000'}, {'symbol': 'USDT', 'balance': '0.07441810', 'symbol_name': 'Tether', 'usd_value': 0.0}, {'symbol': 'VET', 'balance': '95.20000000', 'symbol_name': 'Vechain', 'usd_value': '0.05902000'}, {'symbol': 'DOT', 'balance': '0.20000000', 'symbol_name': 'Polkadot', 'usd_value': '19.63000000'}, {'symbol': 'ICX', 'balance': '4.70000000', 'symbol_name': 'Icon', 'usd_value': '0.77500000'}, {'symbol': 'BNB', 'balance': '0.00032104', 'symbol_name': 'Binance coin', 'usd_value': '426.20000000'}]
        
        if(self.enable_gui):
           self.create_gui()


    def create_canvas(self):
            market_colours = mpf.make_marketcolors(up='#07d400',down='#d40000',inherit=True)
            mpf_style  = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors=market_colours)
            
           
            data_frame = self.binance_end_point.get_historical_price_data("BTCUSDT", "100 minute ago UTC", self.user.get_client().KLINE_INTERVAL_1MINUTE)
            fig, _ = mpf.plot(data_frame, type="candle", mav=(20), volume=True, tight_layout=True, style=mpf_style, returnfig=True)

            #deletes the previous canvas so that the next canvas can occupy the space
            if (isinstance(self.canvas, matplotlib.backends.backend_tkagg.FigureCanvasTkAgg)):
                self.canvas.get_tk_widget().destroy()
            self.canvas = FigureCanvasTkAgg(fig, self.graph_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=LEFT, fill="both", expand=True, padx=35, pady=15)

            self.window.after(30000, self.create_canvas)
                        


    def update_recent_trades(self, call_num = None):
        # self.binance_client.get_order_book(self.user.get_client, "BTCUSDT", 10)

        #This is to create the label once and not every time during recursion
        if (call_num == 0):
            heading_text = " Coin Name\tAmount(BTC)\tPrice(USDT)\tType\tSide "
            self.heading_label = Label(self.trade_frame, text=heading_text, font=('Arial', 9, "bold"), bg="#b8d2ff").pack(pady=15, padx=5)
        
        #destroy all existing widgets so that new widgets can occupy the space
        if isinstance(self.single_trade_button, list):
            for x in range(11):
                self.single_trade_button[x].destroy()

        #displaying latest trades one by one, using looping
        self.single_trade_button = list()
        for x in range(len(self.user.trades) - 11, len(self.user.trades)):
            symbol = self.user.trades[x]['symbol']
            executed_qty = self.user.trades[x]['executedQty']
            cummulative_qty = self.user.trades[x]['cummulativeQuoteQty']
            trade_type = self.user.trades[x]['type']
            trade_side = self.user.trades[x]['side']

            if (trade_side == 'SELL'):
                btn_bg = "#ffabab"
            else:
                btn_bg = "#bbffb3"

            display_text = " {}\t{}\t{}\t{}\t{} ".format(symbol, executed_qty, cummulative_qty, trade_type, trade_side)
            self.single_trade_button.append( Button(self.trade_frame, text=display_text, bg=btn_bg, command=lambda y=x: self.trade_window(y), width=58))
            self.single_trade_button[-1].pack(padx=10, pady=11)


    def trade_window(self, trade_num):
        self.new_window = Toplevel(self.window)
        self.new_window.title("Trade Details")
        self.new_window.resizable(False, False)
        self.new_window.iconphoto(True, self.app_icon)
        self.new_window.config(background="#84a6d1")

        counter = 0
        for x in range(3):
            for y in range(3):
                key = list(self.user.trades[trade_num])[counter]
                value = self.user.trades[trade_num][key]
                Label(self.new_window, text= key + ":  " + str(value), font=('Arial', 11, "bold"), bg="#002c73", fg="#ffffff", relief=GROOVE, bd=5).grid(row=x, column=y, padx=20, pady=15, sticky='ew', ipadx=3, ipady=3)
                counter += 1


    def create_gui(self):
        self.window = Tk()
        self.window.title("Cryptocurrency trading bot")
        width= self.window.winfo_screenwidth()
        height= self.window.winfo_screenheight()               
        self.window.geometry("%dx%d" % (width, height))
        self.window.resizable(True, True)
        self.window.config()

        self.app_icon = PhotoImage(file="assets/icons.png")
        self.window.iconphoto(True, self.app_icon)

        #constructing frames to bind widgets wherever required

        #creating the menu frame which will consists of menubar
        self.menu_frame = Frame(self.window, bg="#0b1047", width=1200, height=50, relief=SUNKEN, pady=10, padx=50, bd=10, borderwidth=5)
        self.menu_frame.pack(side=TOP, fill="x", expand=False)

        self.setting_photo = PhotoImage(file="assets/user_icons.png")
        self.user_icon = self.setting_photo.subsample(3, 3)

        self.user_photo = PhotoImage(file="assets/setting_icon.png")
        self.setting_icon = self.user_photo.subsample(3, 3)

        Button(self.menu_frame, image=self.user_icon, bg="white", activebackground="#1f2769", cursor="hand2").pack(side=RIGHT, padx=15)
        Button(self.menu_frame, image=self.setting_icon, bg="white", activebackground="#1f2769", cursor="hand2", command=self.create_settings_window).pack(side=RIGHT, padx=15)
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
        self.notebook = ttk.Notebook(self.portfolio_frame, width=1200, height=300)

        self.open_orders = Frame(self.notebook, width=1200, height=260, bg="#4656fa")
        self.order_history = Frame(self.notebook, width=1200, height=260, bg="#4656fa")
        self.portfolio = Frame(self.notebook, width=1200, height=260, bg="#4656fa")
        self.available_funds = Frame(self.notebook, width=1200, height=260, bg="#4656fa")

        self.notebook.add(self.open_orders, text="   Open Orders   ")
        self.notebook.add(self.order_history, text="   Order History   ")
        self.notebook.add(self.portfolio, tex="   Portfolio   ")
        self.notebook.add(self.available_funds, text="   Funds   ")

        self.notebook.pack(side=LEFT, fill="both", expand=True)

        # Label(self.open_orders, text="This is the open orders section").pack(side=TOP)
        # Label(self.order_history, text="This is the order_history section").pack(side=TOP)
        # Label(self.portfolio, text="This is the trade history section").pack(side=TOP)
        # Label(self.available_funds, text="This is the funds section").pack(side=TOP)


        #displaying open_orders data
        for x in range(11):
            temp_string = ""
            for key,value in self.portfolio_dummy_data[0].items():
                temp_string += key + ": " + str(value) + "      "
            Label(self.open_orders, text=temp_string, bg="#fae19d", font=('Arial', 10)).pack(ipady=2, ipadx=10, pady=4, fill="x")

        #displaying order_history data
        for x in range(11):
            temp_string = ""
            for key,value in self.user.trades[0].items():
                temp_string += key + ": " + str(value) + "      "
            Label(self.order_history, text=temp_string, bg="#fae19d", font=('Arial', 10)).pack(ipady=2, ipadx=10, pady=4)

    

        #creating a graph frame to plot the candle stick chart
        self.graph_frame = Frame(self.window, width=800, bg="#232a75", height=500, relief=GROOVE, borderwidth=1)
        self.graph_frame.pack(side=LEFT, fill="both", expand=True)

        #Call create_canvas to draw canvas on to the graph_frame
        self.create_canvas()

        #creating trade frame and putting recent trade actions into the frame
        self.trade_frame = Frame(self.window, bg="#5b64ba", width=400, height=500, relief=SUNKEN, bd=10)
        self.trade_frame.pack(side=RIGHT, fill="both", expand=False)

        self.green_bar_image = PhotoImage(file="assets/green_bar.png")
        self.red_bar_image = PhotoImage(file="assets/red_bar.png")

        Label(self.trade_frame, image=self.red_bar_image, bg="#c2c8ff", width=400).pack()
        Label(self.trade_frame, text="Recent Trades", font=('Arial', 20, "bold"), bg="#b8d2ff").pack()
        Label(self.trade_frame, image=self.green_bar_image, bg="#c2c8ff", width=400).pack()
    
        # call update_recent_trades to update the data in trade frame
        self.update_recent_trades(call_num=0)

        self.window.protocol("WM_DELETE_WINDOW",self.on_closing)
        self.window.mainloop()

    #Initial window to prompt user to enter api_key and api_secret
    def create_initial_window(self):
        self.initial_window = Tk()

        self.initial_window.geometry("862x519")
        self.initial_window.configure(bg = "#3A7FF6")

        self.api_key_var = StringVar()
        self.api_secret_var = StringVar()

        canvas = Canvas(
            self.initial_window,
            bg = "#3A7FF6",
            height = 519,
            width = 862,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        canvas.create_rectangle(
            430.9999999999999,
            0.0,
            861.9999999999999,
            519.0,
            fill="#FCFCFC",
            outline="")

        button_image_1 = PhotoImage(
            file=Path("assets/button_1.png"))
        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.initial_window_get_keys,
            relief="flat"
        )
        button_1.place(
            x=556.9999999999999,
            y=401.0,
            width=180.0,
            height=55.0
        )

        canvas.create_text(
            39.999999999999886,
            127.0,
            anchor="nw",
            text="Cryptocurrency Trading bot",
            fill="#FCFCFC",
            font=("Roboto Bold", 24 * -1)
        )

        canvas.create_text(
            481.9999999999999,
            74.0,
            anchor="nw",
            text="Enter your keys",
            fill="#505485",
            font=("Roboto Bold", 24 * -1)
        )

        canvas.create_text(
            482.9999999999999,
            131.0,
            anchor="nw",
            text="Api key",
            fill="#505485",
            font=("Roboto Bold", 18 * -1)
        )

        canvas.create_text(
            483.9999999999999,
            239.0,
            anchor="nw",
            text="Api secret",
            fill="#505485",
            font=("Roboto Bold", 18 * -1)
        )

        canvas.create_rectangle(
            39.999999999999886,
            160.0,
            99.99999999999989,
            165.0,
            fill="#FCFCFC",
            outline="")

        entry_image_1 = PhotoImage(
            file=Path("assets/entry_1.png"))
        entry_bg_1 = canvas.create_image(
            654.4999999999999,
            190.5,
            image=entry_image_1
        )
        api_key_entry = Entry(
            bd=0,
            bg="#F1F5FF",
            highlightthickness=0,
            textvariable=self.api_key_var
        )
        api_key_entry.place(
            x=493.9999999999999,
            y=160.0,
            width=321.0,
            height=59.0
        )

        entry_image_2 = PhotoImage(
            file=Path("assets/entry_2.png"))
        entry_bg_2 = canvas.create_image(
            654.4999999999999,
            299.5,
            image=entry_image_2
        )
        api_secret_entry = Entry(
            bd=0,
            bg="#F1F5FF",
            highlightthickness=0,
            textvariable=self.api_secret_var
        )
        api_secret_entry.place(
            x=493.9999999999999,
            y=269.0,
            width=321.0,
            height=59.0
        )

        canvas.create_text(
            39.999999999999886,
            203.0,
            anchor="nw",
            text="Automate your cryptocurrency",
            fill="#FCFCFC",
            font=("Armata Regular", 24 * -1)
        )

        canvas.create_text(
            39.999999999999886,
            239.0,
            anchor="nw",
            text="trading with ease\n",
            fill="#FCFCFC",
            font=("Armata Regular", 24 * -1)
        )

        canvas.create_text(
            39.999999999999886,
            325.0,
            anchor="nw",
            text="Minor project by -\nAbhishek Pradhan\nDaksh Mishra\nDevakrishna C Nair\nRaj Kamal",
            fill="#FCFCFC",
            font=("Armata Regular", 18 * -1)
        )
        self.initial_window.mainloop()
    
    #Save api keys entered in initial window
    def initial_window_get_keys(self):
        self.api_key = self.api_key_var.get()
        self.api_secret = self.api_secret_var.get()
        os.mkdir("config")
        # print(self.api_key, self.api_secret)
        #Create config directory and save the user entered api_key and api_secret to "config/api_keys.py"
        api_file = open("config/api_keys.py", "w")
        api_file.write(self.api_key)
        api_file.write("\n"+self.api_secret)
        api_file.close()
        self.initial_window.destroy()
        self.initiate_trading()

    #Create a new settings window
    def create_settings_window(self):
        self.settings_window=Tk()
        self.settings_window.geometry("400x300")
        self.settings_window.title('Ctb Settings')
        
        pane=Frame(self.settings_window)
        API_KEY=Label(text="API KEY : ")
        API_KEY.place(x=5,y=5)
        text_box1=Text(height=1,width=20)
        text_box1.place(x=150,y=5)
        API_SECRET=Label(text="API SECRET :")
        API_SECRET.place(x=5,y=50)
        text_box2=Text(height=1,width=20)
        text_box2.place(x=150,y=50)
        x_cordinate=5
        y_cordinate=80
        self.settings_string_var=StringVar(self.settings_window,"0")
        frame=Frame(self.settings_window)
        button1=Radiobutton(self.settings_window,text="RSI",variable=self.settings_string_var,value="1",command=self.settings_view_selected)
        button1.place(x=x_cordinate,y=y_cordinate)
        x_cordinate=x_cordinate+100
        button2=Radiobutton(self.settings_window,text="MACD",variable=self.settings_string_var,value="2",command=self.settings_view_selected)
        button2.place(x=x_cordinate,y=y_cordinate)
        self.settings_window.mainloop()

    #Change trading strategy specific settings in settings window, based on user selection
    def settings_view_selected(self):
        choice = self.settings_string_var.get()
        if(choice=="1"):
            RSI_BUTTON=Label(text="RSI KEY :                        ")
            text_box3=Text(height=1,width=20)
            RSI_BUTTON.place(x=5,y=130)
            text_box3.place(x=120,y=130)
            RSI_TIME_PERIOD=Label(text="RSI PERIOD :           ")
            text_box4=Text(height=1,width=20)
            RSI_TIME_PERIOD.place(x=5,y=170)
            text_box4.place(x=130,y=170)
        else:
            MACD_LV=Label(text="MACD Lower limit :")
            text_box5=Text(height=1,width=20)
            MACD_LV.place(x=5,y=130)
            text_box5.place(x=120,y=130)
            MACD_UV=Label(text="MACD Upper limit :")
            text_box6=Text(height=1,width=20)
            MACD_UV.place(x=5,y=170)
            text_box6.place(x=130,y=170)

    def on_closing(self):
        plt.close('all')
        self.window.destroy()
        self.trading_strategies.continue_trading_flag = False



