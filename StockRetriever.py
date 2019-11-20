# import stock_info module from yahoo_fin
from yahoo_fin import stock_info as si
import sys

# Amazon = amzn
# Microsoft = msft
# Google = goog

# function for retrieving stock price
def get_stock_price(stock_name):

    # check stock_name is valid stock name
    try:
        si.get_live_price(stock_name)
        return si.get_live_price(stock_name)
    except ValueError as e:
        print("Invalid stock name")


#print(get_stock_price(sys.argv[1]))

