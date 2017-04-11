from emulator.Controller import Controller


class ControlAPI:
    def __init__(self, controller: Controller):
        self.__controller = controller

    def pause(self) -> None:
        self.__controller.stop_looping_backwards()
        self.__controller.stop_looping_forwards()

        """
        Piloting commands:
        -Pause/unpause emulation
        -Tweak emulation speed
        -Emulate key press/release
        -Skip frames
        -Load a rom
        -Reflexion and hooks management
        """