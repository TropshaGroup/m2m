from m2m.repurpose.interface.cli import CLIInterface

class InterfaceFactory:
    """ A central place for creating hypothesis generating interfaces. """
    def __init__(self):
        self.interfaces = {
            "CLI" : CLIInterface ()
        }
    def get_interface(self, name):
        return self.interfaces[name]

