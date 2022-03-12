import time
import pandas as pd

class Trading_Strategies:
    status = "Waiting for Trading to start"
    trades = []
    continue_trading_flag = True

    #Gets ticker(Ticker name of crypto to be traded), binance endpoint, investment_amount(amount of usdt to be invested in each trade), 
    # initial_balance(incase of paper trading), real_trading(bool value indicating whether the bot should do paper trading or real trading)
    def __init__(self, ticker, binance_end_point, user,  paper_trading):
        self.ticker = ticker
        self.binance_end_point = binance_end_point
        self.user = user
        self.paper_trading = paper_trading
    
    #Creates a paper buy order
    def paper_buy(self):
        if(self.user.investment_amount < self.user.paper_balance):
            time, price = self.binance_end_point.get_current_price(self.ticker)
            self.user.holding_amount += self.user.investment_amount/float(price)
            self.user.paper_balance -= self.user.investment_amount
            self.trades.append({"Ticker":self.ticker, "btc_amount":self.user.investment_amount/float(price), "trade_type":"PAPER_BUY", "account_balance": self.user.paper_balance, "btc_balance": self.user.holding_amount ,"time":time, "price":price})
            print(self.trades)

    def paper_sell(self):
        if(self.user.holding_amount > 0.0):
            time, price = self.binance_end_point.get_current_price(self.ticker)
            self.user.paper_balance += price*self.user.holding_amount
            self.trades.append({"Ticker":self.ticker, "amount":price*self.user.holding_amount, "trade_type":"PAPER_SELL", "time":time, "price": price})
            self.user.holding_amount = 0.0

    def rsi(self, window_length):
        while(self.continue_trading_flag):
            df = self.binance_end_point.get_historical_price_data("BTCUSDT", "200 minute ago UTC", self.user.get_client().KLINE_INTERVAL_1MINUTE)
            pd.options.mode.chained_assignment = None
            df['diff'] = df["Close"].diff(1)

            df['gain'] = df['diff'].clip(lower=0)
            df['loss'] = df['diff'].clip(upper=0).abs()

            df['avg_gain'] = df['gain'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]
            df['avg_loss'] = df['loss'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]

            for i, row in enumerate(df['avg_gain'].iloc[window_length+1:]):
                df['avg_gain'].iloc[i + window_length + 1] =\
                    (df['avg_gain'].iloc[i + window_length] *
                    (window_length - 1) +
                    df['gain'].iloc[i + window_length + 1])\
                    / window_length

            for i, row in enumerate(df['avg_loss'].iloc[window_length+1:]):
                df['avg_loss'].iloc[i + window_length + 1] =\
                    (df['avg_loss'].iloc[i + window_length] *
                    (window_length - 1) +
                    df['loss'].iloc[i + window_length + 1])\
                    / window_length

            df['rs'] = df['avg_gain'] / df['avg_loss']
            df['rsi'] = 100 - (100 / (1.0 + df['rs']))

            curr_val = df.iloc[-1][-1]

            #TODO: fix this
            if(curr_val > 55):
                self.status = "Selling Assets"
                self.paper_sell()
            elif(curr_val < 45):
                self.status = "Buying Assets"
                self.paper_buy()
            else:
                self.status = "current rsi value is "+str(curr_val)+", waiting for optimal buy/sell points"
            
            print(self.status)
            
            i = 0
            while(self.continue_trading_flag and i < 115):
                time.sleep(0.5)
                i += 1
