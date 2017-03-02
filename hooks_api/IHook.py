

class IHook:

    def __init__(self, name:str):
        raise "Abstract class, cannot be instanciated"

    def call(self):
        raise "Abstract class, cannot be instanciated"