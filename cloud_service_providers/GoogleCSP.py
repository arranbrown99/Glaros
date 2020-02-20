class AbstractCSP(ABC):
    stock_name = "goog"
    username = ""
    ui_colour = "rgb(0,0,0)"
    formal_name = "Google"

    def identify(self):
        pass

    def get_ip(self):
        pass

    def start_vm(self):
        pass

    def stop_vm(self):
        pass

    def get_info(self):
        pass

    def is_running(self):
        pass
