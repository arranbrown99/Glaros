# tests for StockRetriever
import sys
my_file = 'C:/Users/andre/cs27-main/'
import StockRetriever

# list for test input
l = ['amzn', 'goog', 'msft']

def test_get_stock_price():
    """test  a correct and incorrect input for get_stock_price
    """
    assert StockRetriever.get_stock_price('amzn') != None
    assert StockRetriever.get_stock_price('foo') == None

def test_calculate_difference():
    """test  a correct and incorrect input for calculate_difference
    """
    assert StockRetriever.calculate_difference('amzn') != None
    assert StockRetriever.calculate_difference('foo') == None

def test_get_stock_data():
    """test that get_stock_data returns a dictioanry
    """
    assert type(StockRetriever.get_stock_data(l)) == dict

def test_best_stock():
    """test that best_stock returns a string
    """
    assert type(StockRetriever.best_stock(l)) == str




if __name__ == '__main__':
    test_get_stock_price()
    test_calculate_difference()
    test_get_stock_data()
    test_best_stock()
    print("Tests passed OK.")

