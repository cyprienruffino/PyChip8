
class IControls:

    def __init__(self):
        raise NotImplementedError("Abstract class, cannot be instanciated")

    def get_keys_pressed(self) -> list:
        raise NotImplementedError("Abstract class, cannot be instanciated")

    def get_keys_released(self) -> list:
        raise NotImplementedError("Abstract class, cannot be instanciated")

