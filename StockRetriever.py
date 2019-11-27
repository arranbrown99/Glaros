# import stock_info module from yahoo_fin
from yahoo_fin import stock_info as si

# Amazon = amzn
# Microsoft = msft
# Google = goog

def get_stock_price(stock_name):
    """retrieves stock price for given
    stock name
    """
    # check stock_name is valid stock name
    try:
        si.get_live_price(stock_name)
        return si.get_live_price(stock_name)
    except ValueError:
        print("Invalid stock name")
        return
    except Exception:
        return

def calculate_difference(stock_name):
    """returns difference between market open
    and close for a given stock
    """
    try:
        # get latest data for stock
        last = si.get_data(stock_name).values[-1] # todays stock data
        last_open = last[0] # opening price of stock
        last_close = last[4] # adjusted closing price of stock
        diff = last_close - last_open # find % difference from opening and closing price
        diff_percentage = (diff/last_open)*100
        return diff_percentage
    except ValueError:
        print("Invalid stock name")
        return
    except ZeroDivisionError:
        print("Can't divide by 0.")
        return
    except Exception:
        return

def get_stock_data(stock_name_list):
    """creates dictionary of market open/close differences
    for a given list of stocks
    """
    stock_data = {}
    for name in stock_name_list:
        stock_data[name] = calculate_difference(name)
    return stock_data
        

def best_stock(list_of_stocks):
    """returns stock with the highest market open/close
    difference
    """
    stock_data = get_stock_data(list_of_stocks)
    greatest = list_of_stocks[0]
    for key, value in stock_data.items():
        if value > stock_data[greatest]:
            greatest = key
    return greatest
