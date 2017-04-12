# API to control views
from emulator.Controller import Controller


class ViewsAPI:
    def __init__(self, controller: Controller):
        self.__controller = controller
