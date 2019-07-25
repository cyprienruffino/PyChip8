from emulator.view.IGraphics import IGraphics


class GraphicsStub(IGraphics):
    def __init__(self):
        pass

    def open_view(self) -> None:
        pass

    def draw(self, gfx: bytearray) -> None:
        pass
