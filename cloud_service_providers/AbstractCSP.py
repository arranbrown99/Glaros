from abc import ABC, abstractmethod


class AbstractCSP(ABC):
    class Error(Exception):
        '''
        Base class for exceptions
        '''
        pass

    class InvalidCSPError(Error):
        '''
        Exception raised for errors in the input.

        Attributes
        ------
            expression -- input expression in which the error occurred
            message -- explanation of the error
        '''

        def __init__(self, expression, message):
            self.expression = expression
            self.message = message

    stock_name = ""
    username = ""
    ui_colour = "rgb(0,0,0)"
    formal_name = ""

    @classmethod
    def get_csp(cls, stock_string):
        types = cls.__subclasses__()
        for concrete in types:
            if concrete.stock_name == stock_string:
                return concrete()
        raise cls.InvalidCSPError(stock_string, "Invalid Input Parameter ")

    @classmethod
    def get_stock_names(cls, ):
        types = cls.__subclasses__()
        print(types)
        all_stock_names = []
        for concrete in types:
            stock_name = concrete.stock_name
            all_stock_names.append(stock_name)
        return all_stock_names

    @abstractmethod
    def identify(self):
        pass

    @abstractmethod
    def get_ip(self):
        pass

    @abstractmethod
    def start_vm(self):
        pass

    @abstractmethod
    def stop_vm(self):
        pass

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def is_running(self):
        pass

    def get_username(self):
        """
        returns the username to needed to login used with ssh
        """
        return self.username

    def get_stock_name(self):
        """
        Returns the short (stock) name for CSP instance (eg. "amzn", "msft", "goog").
        The stock_name field is set once a derived class is instantiated.
        """
        return self.stock_name

    def get_formal_name(self):
        """
        Returns the formal name for CSP instance (eg. "Azure", "Aws", "Google").
        """
        return self.formal_name

    # @staticmethod
    # def wait_until(condition):
    #     while condition:
    #         time.sleep(1)
