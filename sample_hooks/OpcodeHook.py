from api.hooks.Hook import Hook


class OpcodeHook(Hook):
    def __init__(self):
        pass

    def call(self):
        print(self.API.machine.get_opcode())