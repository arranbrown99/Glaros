from abc import ABC, abstractmethod


class AbstractCSP(ABC):
    stock_name = ""

    @abstractmethod
    def identify(self):
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
    def execute_commands(self, commands):
        pass

    @abstractmethod
    def upload_file(self):
        pass

    @abstractmethod
    def is_running(self):
        pass

    def get_stock_name(self):
        """
        Returns the short (stock) name for CSP instance (eg. "amzn", "msft", "goog").
        The stock_name field is set once a derived class is instantiated.
        """
        return self.stock_name
