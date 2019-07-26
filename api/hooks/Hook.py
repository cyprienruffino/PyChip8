from tools.AbstractError import AbstractError


class Hook:
    # A HookAPI object is injected by the controller in this class, with the name API
    def __init__(self):
        self.API = None
        raise AbstractError()

    def call(self) -> None:
        raise AbstractError()


