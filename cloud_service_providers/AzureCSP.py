from cloud_service_providers.AbstractCSP import AbstractCSP


class AzureCSP(AbstractCSP):

    def __init__(self):
        self.stock_name = "msft"
        # Here we need to configure all the things necessary to connect
        # to the Azure instance.

    def identify(self):
        print("This was called from an AzureCSP instance.")

    def start_vm(self):
        pass

    def stop_vm(self):
        pass

    def get_info(self):
        pass

    def execute_command(self):
        pass

    def upload_file(self):
        pass
