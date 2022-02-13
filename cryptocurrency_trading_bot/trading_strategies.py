import pandas as pd

class Trading_Strategies:
    def __init__(self):
        self.df = None
    
    def rsi(self, df, window_length):
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

        if(curr_val > 65):
            return "SELL"
        elif(curr_val < 35):
            return "BUY"
        return "current rsi value is "+str(curr_val)+", waiting for optimal buy/sell points"
