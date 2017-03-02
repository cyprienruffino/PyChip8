

class IHook:

    def __init__(self):
        raise NotImplementedError("Abstract class, cannot be instanciated")

    def call(self):
        raise NotImplementedError("Abstract class, cannot be instanciated")