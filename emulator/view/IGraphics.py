
class IGraphics:

    def __init__(self):
        raise NotImplementedError("Abstract class, cannot be instanciated")

    def open_view(self) -> None:
        raise NotImplementedError("Abstract class, cannot be instanciated")

    def draw(self, gfx:bytearray) -> None:
        raise NotImplementedError("Abstract class, cannot be instanciated")

