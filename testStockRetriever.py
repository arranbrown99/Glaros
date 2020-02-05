# tests for StockRetriever
import StockRetriever

# list for good test input
good_l = ['amzn', 'goog', 'msft', ]

# list for bad test input
bad_l = ['foooo']


def test_get_stock_price():
    """test  a correct and incorrect input for get_stock_price
    """
    assert StockRetriever.get_stock_price(good_l[0]) is not None
    assert StockRetriever.get_stock_price(good_l[1]) is not None
    assert StockRetriever.get_stock_price(good_l[2]) is not None

    assert StockRetriever.get_stock_price(bad_l[0]) is None


def test_calculate_difference():
    """test  a correct and incorrect input for calculate_difference
    """
    assert StockRetriever.calculate_difference(good_l[0]) is not None
    assert StockRetriever.calculate_difference(bad_l[0]) is None


def test_get_stock_data():
    """test that get_stock_data returns a dictioanry
    """
    assert type(StockRetriever.get_stock_data(good_l)) == dict


def test_best_stock():
    """test that best_stock returns a string
    """
    assert type(StockRetriever.best_stock(good_l)) == str


if __name__ == '__main__':
    test_get_stock_price()
    test_calculate_difference()
    test_get_stock_data()
    test_best_stock()
    print("Tests passed OK.")
