import pandas as pd
import tkinter as tk
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Gui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Cryptocurrency trading bot") 
        self.window.geometry('1270x720')
        self.window.configure(bg="#02082b")

        self.graphFrame = tk.Frame(window, width=790, height= 600, bg='#34568B')
        self.graphFrame.grid(row=0, column=0, padx=10)
        self.graphFrame.pack_propagate(False)

        self.recentTradesFrame = tk.Frame(window, width=390, height=600, bg='#340d69' )
        self.recentTradesFrame.grid(row=0, column=1, padx=10)
        self.recentTradesFrame.grid_propagate(False)
        tk.Label(recentTradesFrame, text="Recently Executed Trades", bg="#340d69", fg="#ffffff", font=("Verdana",15)).grid(row=0, column=0, padx=8, pady=5)
        
        self.window.protocol("WM_DELETE_WINDOW",self.on_closing)
        self.window.mainloop()
    
    def create_chart():
        pass

    def on_closing(self):
        plt.close('all')
        window.destroy()
