from view.IControls import IControls


class ControlsStub(IControls):

    def __init__(self):
        pass

    def get_keys_pressed(self) -> list:
        return []

    def get_keys_released(self) -> list:
        return []


