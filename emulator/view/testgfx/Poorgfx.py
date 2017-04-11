from emulator.view.IGraphics import IGraphics

class PoorGraphics(IGraphics):
    def __init__(self):
        pass

    def open_view(self) -> None:
        pass

    def draw(self, gfx:bytearray) -> None:
        line=""
        for y in range(0,32):
            for x in range(0,64):
                if gfx[x]: line += '#'
                else: line += " "
            print(line)
            line = ""
        print("-"*64)

