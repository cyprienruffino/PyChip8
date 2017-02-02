from emulator.engine import Emulator
from emulator.modules.controls import Controls


class ControlsStub(Controls):

    def __init__(self):
        pass

    def get_key(self, e:Emulator):
        pass

