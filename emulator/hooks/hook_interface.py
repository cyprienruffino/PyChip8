import types

from emulator.engine import Emulator


class Hook:
    def __init__(self):
        self.name = ""
        raise Exception("Abstract class, cannot be instanciated")

    def apply(self,e:Emulator):
        raise Exception("Abstract class, cannot be instanciated")

def createHook(name:str, l:types.FunctionType) -> Hook:
    type(name, (Hook, object), {"apply": l})