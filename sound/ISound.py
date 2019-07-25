
class ISound:

    def __init__(self):
        raise NotImplementedError("Abstract class, cannot be instanciated")

    def beep(self) -> None:
        raise NotImplementedError("Abstract class, cannot be instanciated")

