from .IDisplay import IDisplay


class DisplayStub(IGraphics):
    def __init__(self):
        pass

    def open_view(self) -> None:
        pass

    def draw(self, gfx: bytearray) -> None:
        pass
