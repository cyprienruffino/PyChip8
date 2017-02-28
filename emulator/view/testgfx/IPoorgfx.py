from view.IGraphics import Graphics

class PoorGraphics(Graphics):
    def __init__(self):
        pass

    def open_view(self):
        pass

    def draw(self, gfx:bytearray):
        line=""
        for y in range(0,32):
            for x in range(0,64):
                if gfx[x]: line += '#'
                else: line += " "
            print(line)
            line = ""
        print("-"*64)

