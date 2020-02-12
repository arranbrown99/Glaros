from abc import ABC, abstractmethod


class AbstractCSP(ABC):
    stock_name = ""
    username = ""
    ui_colour = "rgb(0,0,0)"
    formal_name = ""

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

    # @staticmethod
    # def wait_until(condition):
    #     while condition:
    #         time.sleep(1)
