class Hook:
    # A HookAPI object is injected by the controller in this class, with the name API
    def __init__(self):
        self.API = None
        raise NotImplementedError("Abstract class, cannot be instanciated")

    def call(self) -> None:
        raise NotImplementedError("Abstract class, cannot be instanciated")


