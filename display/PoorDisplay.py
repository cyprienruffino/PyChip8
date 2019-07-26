from .IDisplay import IDisplay


class PoorGraphics(IDisplay):
    def __init__(self):
        pass

    def open_view(self) -> None:
        pass

    def draw(self, gfx: bytearray) -> None:
        line = ""
        for y in range(0, 32):
            for x in range(0, 64):
                if gfx[x+64*y]:
                    line += '##'
                else:
                    line += "  "
            print(line)
            line = ""
        print("-" * 128)


    def get_keys_pressed(self) -> list:
        return []

    def get_keys_released(self) -> list:
        return []


