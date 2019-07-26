from tools.AbstractError import AbstractError

class IDisplay:
    def __init__(self):
        raise AbstractError()

    def draw(self, gfx: bytearray) -> None:
        raise AbstractError()

    def get_keys_pressed(self) -> list:
        raise AbstractError()

    def get_keys_released(self) -> list:
        raise AbstractError()

