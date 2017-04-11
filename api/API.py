from api.APIs.ControlAPI import ControlAPI
from api.APIs.HooksAPI import HooksAPI
from api.APIs.MachineAPI import MachineAPI
from api.APIs.ToolsAPI import ToolsAPI
from api.APIs.ViewsAPI import ViewsAPI
from emulator.Controller import Controller
from api.hooks.Hook import Hook


class API:
    def __init__(self, controller:Controller):
        self.__controller = controller
        self.machine:MachineAPI = MachineAPI(self.__controller)
        self.tools:ToolsAPI = ToolsAPI(self.__controller)
        self.views:ViewsAPI = ViewsAPI(self.__controller)
        self.hooks:HooksAPI = HooksAPI(self.__controller)
        self.control:ControlAPI = ControlAPI(self.__controller)


    def create_hook(self, hook_type: type) -> Hook:
        hook: Hook = hook_type()
        hook.API = self
        return hook