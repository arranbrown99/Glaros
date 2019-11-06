# import stock_info module from yahoo_fin
from yahoo_fin import stock_info as si


print(si.get_live_price("amzn"))