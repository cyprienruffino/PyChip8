from view.IControls import Controls


class ControlsStub(Controls):

    def __init__(self):
        pass

    def get_keys_pressed(self):
        return []

    def get_keys_released(self):
        return []


