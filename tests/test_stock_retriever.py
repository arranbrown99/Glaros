# tests for StockRetriever
import StockRetriever

# list for good test input
good_l = ['amzn', 'goog', 'msft', ]

# list for bad test input
bad_l = ['foooo']


class TestStockRetrieverMethods(unittest.TestCase):

    def test_get_stock_price(self):
        """test  a correct and incorrect input for get_stock_price
        """
        # Test good input
        self.assertIsNotNone(StockRetriever.get_stock_price(good_l[0]))
        self.assertIsNotNone(StockRetriever.get_stock_price(good_l[1]))
        self.assertIsNotNone(StockRetriever.get_stock_price(good_l[2]))
        # Test bad input
        self.assertIsNone(StockRetriever.get_stock_price(bad_l[0]))

    def test_calculate_difference(self):
        """test a correct and incorrect input for calculate_difference
        """
        # Test good input
        self.assertIsNotNone(StockRetriever.calculate_difference(good_l[0]))
        # Test bad input
        self.assertIsNone(StockRetriever.calculate_difference(bad_l[0]))

    def test_get_stock_data(self):
        """test that get_stock_data returns a dictionary
        """
        self.assertIs(type(StockRetriever.get_stock_data(good_l)), dict)

    def test_best_stock(self):
        """test that best_stock returns a string
        """
        self.assertIs(type(StockRetriever.best_stock(good_l)), str)


if __name__ == '__main__':
    unittest.main()
