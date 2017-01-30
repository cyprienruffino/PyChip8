from emulator.engine import Emulator


class Controls:

    def __init__(self):
        raise "Abstract class, cannot be instanciated"

    def get_key(self, e:Emulator):
        raise "Abstract class, cannot be instanciated"

