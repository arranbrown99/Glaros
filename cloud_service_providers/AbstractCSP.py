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
    ui_colour = "rgb(153,153,153)"
    formal_name = ""

    @classmethod
    def get_csp(cls, stock_string):
        """
        Given a stock name will return the corresponding CSP object
        Allows us to not need to hard code the CSP in the driver and front end as we can
        Dynamically retrieve the CSP object from abstracts children

        Parameters
        ----------
        stock_string : the stock string that you want to get the concrete CSP for

        Returns the corresponding concrete CSP object
        -------

        """
        types = cls.__subclasses__()
        for concrete in types:
            if concrete.stock_name == stock_string:
                return concrete()
        raise cls.InvalidCSPError(stock_string, "Invalid Input Parameter ")

    @classmethod
    def get_stock_names(cls, ):
        """

        Returns a list of all of the stock names of abstracts children
        -------

        """
        types = cls.__subclasses__()
        all_stock_names = []
        for concrete in types:
            stock_name = concrete.stock_name
            all_stock_names.append(stock_name)
        return all_stock_names

    @abstractmethod
    def identify(self):
        """
        Returns the id of the VM
        """
        pass

    @abstractmethod
    def get_ip(self):
        """
        Returns the ip address of the VM
        """
        pass

    @abstractmethod
    def start_vm(self):
        """
        Starts the remote VM
        """
        pass

    @abstractmethod
    def stop_vm(self):
        """
        Stops the remote VM
        """
        pass

    @abstractmethod
    def get_info(self):
        """
        Returns the information abouut the VM including ip address,running status etc
        """
        pass

    @abstractmethod
    def is_running(self):
        """
        return True if VM is turned on

        Returns
        -------
        bool
        """
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
