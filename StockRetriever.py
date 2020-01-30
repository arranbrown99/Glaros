# import stock_info module from yahoo_fin
from yahoo_fin import stock_info as si
import datetime
import numpy as np


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


def percentage_difference(opening, closing):
    """Returns the percentage difference between the specified opening and closing prices
    """
    diff = closing - opening  # find % difference from opening and closing price
    return (diff / opening) * 100  # to get the percentage


def calculate_difference(stock_name):
    """returns difference between market open
    and close for a given stock
    """
    try:
        # get latest data for stock
        last = si.get_data(stock_name).values[-1]  # todays stock data
        last_open = last[0]  # opening price of stock
        last_close = last[4]  # adjusted closing price of stock
        return percentage_difference(last_open, last_close)
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


def get_N_last_stock_differences_for(stock_names, N=10, interval='1d'):
    """Takes in a list of stock_names eg. ['amzn', 'msft'], an integer N
    for how many records to retrieve, and an interval:
    (i.e.'1d' for 1 day, '1wk' for 1 week or '1mo' for 1 month interval)
    Returns the last N calculated percentages differences for each stock_name
    based on the interval specified.
    Defaults: N=10, interval='1d'

    """
    output = {}
    separate_stock_dates = []
    for stock_name in stock_names:
        # Request the stock records from yahoo-fin for this stock_name
        stock_data = si.get_data(stock_name, interval=interval, index_as_date=False)[-N:]

        # Separate the columns that we are interested in
        open_col = stock_data['open']
        close_col = stock_data['close']
        date_col = stock_data['date']

        # The dates returned by each stock_name are stored in a list
        # so that we can later ensure that all dates match
        separate_stock_dates.append(date_col)

        # We form a list with percentage differences using the open and close stock prices
        perc_diff = [percentage_difference(open_col.iloc[i], close_col.iloc[i]) for i in range(N)]
        output[stock_name] = perc_diff

    # Check that dates retrieved by each CSP are the same
    current_date_list = []
    for dates in separate_stock_dates:
        if len(current_date_list) == 0:  # first iteration only
            current_date_list = dates
        else:
            if not all(dates.values == current_date_list.values):
                # In the case that at least one date list differs from the rest
                raise Exception("The returned dates from each Cloud Service Provider don't match.")

    # Convert Pandas.Timestamp to datetime.date objects because they are Serializable by JavaScript
    output['dates'] = [timestamp.date() for timestamp in current_date_list]
    return output