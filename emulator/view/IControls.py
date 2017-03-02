
class IControls:

    def __init__(self):
        raise "Abstract class, cannot be instanciated"

    def get_keys_pressed(self) -> list:
        raise "Abstract class, cannot be instanciated"

    def get_keys_released(self) -> list:
        raise "Abstract class, cannot be instanciated"
