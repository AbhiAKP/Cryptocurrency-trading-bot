from tkinter.font import BOLD
import pandas as pd
from tkinter import *
from tkinter import ttk
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

canvas = None
a = 2

def on_closing():
    plt.close('all')
    window.destroy()

def animate(window):
    global canvas, a

    dataframe = pd.read_csv("BTC-USD.csv")
    dataframe.Date = pd.to_datetime(dataframe.Date)

    dataframe = dataframe.set_index("Date")

    market_colours = mpf.make_marketcolors(up='#23e851',down='#e04212',inherit=True)
    mpf_style  = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors=market_colours)

    fig, _ = mpf.plot(dataframe["2021-01":"2021-"+str(a)], type="candle", mav=(20), volume=True, tight_layout=True, style=mpf_style, returnfig=True)

    # canvas = FigureCanvasTkAgg(fig, graph_frame)
    # canvas.draw()
    # canvas.get_tk_widget().pack(side=LEFT, fill="both", expand=True, padx=35, pady=15)
    
    a = a + 1

def configureScroll(event):
    # canvas.configure(scrollregion=canvas.bbox("all"),width=900,height=400)
    pass


window = Tk()
window.title("Cryptocurrency trading bot") 
window.resizable(True, True)
window.config()
app_icon = PhotoImage(file="icons.png")
window.iconphoto(True, app_icon)


#constructing frames to bind widgets wherever required


#creating the menu frame which will consists of menubar
menu_frame = Frame(window, bg="#0b1047", width=1200, height=50, relief=SUNKEN, pady=10, padx=50, bd=10, borderwidth=5)
menu_frame.pack(side=TOP, fill="x", expand=False)


setting_photo = PhotoImage(file="user_icons.png")
user_icon = setting_photo.subsample(3, 3)

user_photo = PhotoImage(file="setting_icon.png")
setting_icon = user_photo.subsample(3, 3)

Button(menu_frame, image=user_icon, bg="white", activebackground="#1f2769", cursor="hand2").pack(side=RIGHT, padx=15)
Button(menu_frame, image=setting_icon, bg="white", activebackground="#1f2769", cursor="hand2").pack(side=RIGHT, padx=15)
Button(menu_frame, text="Menu1", font=('Helvetica', 12), activebackground="#1f2769", activeforeground="white", cursor="hand2").pack(side=LEFT, padx=15, ipadx=5)
Button(menu_frame, text="Menu2", font=('Helvetica', 12), activebackground="#1f2769", activeforeground="white", cursor="hand2").pack(side=LEFT, padx=15, ipadx=5)
Button(menu_frame, text="Menu3", font=('Helvetica', 12), activebackground="#1f2769", activeforeground="white", cursor="hand2").pack(side=LEFT, padx=15, ipadx=5)
Button(menu_frame, text="Menu4", font=('Helvetica', 12), activebackground="#1f2769", activeforeground="white", cursor="hand2").pack(side=LEFT, padx=15, ipadx=5)


#creaing the portfolio frame to show open orders and funds
portfolio_frame = Frame(window, width=1200, bg="#232a75", height=300, relief=GROOVE, bd=10, borderwidth=10)
portfolio_frame.pack(side=BOTTOM, fill="x", expand=False)


#creating a graph frame to plot the candle stick chart
graph_frame = Frame(window, width=800, bg="#232a75", height=500, relief=GROOVE, borderwidth=1)
graph_frame.pack(side=LEFT, fill="both", expand=True)
animate(window)


#creating trade frame and putting recent trade actions into the frame
trade_frame = Frame(window, bg="#5b64ba", width=400, height=500, relief=SUNKEN, bd=10)
trade_frame.pack(side=RIGHT, fill="both", expand=False)


green_bar_image = PhotoImage(file="green_bar.png")
# user_icon = setting_photo.subsample(3, 3)

red_bar_image = PhotoImage(file="red_bar.png")
# setting_icon = user_photo.subsample(3, 3)
Label(trade_frame, image=red_bar_image, bg="#c2c8ff", width=400).pack()
Label(trade_frame, text="Recent Trades", font=('Arial', 20, BOLD), bg="#c2c8ff").pack()
Label(trade_frame, image=green_bar_image, bg="#c2c8ff", width=400).pack()





#creating multiple tabs in the portfolio frame
s = ttk.Style()
s.configure('.', font=('Arial', 12))
notebook = ttk.Notebook(portfolio_frame)

open_orders = Frame(notebook, width=1200, height=260, bg="#4656fa")
order_history = Frame(notebook, width=1200, height=260, bg="#4656fa")
trade_history = Frame(notebook, width=1200, height=260, bg="#4656fa")
available_funds = Frame(notebook, width=1200, height=260, bg="#4656fa")

notebook.add(open_orders, text="   Open Orders   ")
notebook.add(order_history, text="   Order History   ")
notebook.add(trade_history, tex="   Trade History   ")
notebook.add(available_funds, text="   Funds   ")

notebook.pack(side=LEFT, fill="both", expand=True)






window.protocol("WM_DELETE_WINDOW",on_closing)
window.mainloop()
