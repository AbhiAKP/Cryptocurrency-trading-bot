import os
import cryptocurrency_trading_bot as ctb

def main():
    user = ctb.User()
    binance_end_point = ctb.BinanceEndpoint()
    binance_end_point.get_historical_price_data("BTCUSDT", user.get_client())
    os.rmdir("pricedatafiles")

if __name__=="__main__":
    main()