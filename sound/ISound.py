from tools.AbstractError import AbstractError

class ISound:

    def __init__(self):
        raise AbstractError()

    def beep(self) -> None:
        raise AbstractError()

