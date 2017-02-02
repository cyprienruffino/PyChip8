from emulator.engine import Emulator


class Graphics:

    def __init__(self):
        raise "Abstract class, cannot be instanciated"

    def open_view(self):
        raise "Abstract class, cannot be instanciated"

    def draw(self, e:Emulator):
        raise "Abstract class, cannot be instanciated"

    def draw_sprite(self, e:Emulator, VX, VY, N):
        raise "Abstract class, cannot be instanciated"

