
class Graphics:

    def __init__(self):
        raise "Abstract class, cannot be instanciated"

    def open_view(self):
        raise "Abstract class, cannot be instanciated"

    def draw(self, gfx:bytearray):
        raise "Abstract class, cannot be instanciated"

    def draw_sprite(self, sprite:bytearray, VX, VY, N):
        raise "Abstract class, cannot be instanciated"

