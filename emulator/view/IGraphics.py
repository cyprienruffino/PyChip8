
class IGraphics:

    def __init__(self):
        raise "Abstract class, cannot be instanciated"

    def open_view(self) -> None:
        raise "Abstract class, cannot be instanciated"

    def draw(self, gfx:bytearray) -> None:
        raise "Abstract class, cannot be instanciated"

