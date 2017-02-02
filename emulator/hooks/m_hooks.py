from emulator.engine import Emulator
from emulator.hooks.hook_interface import Hook


class MemoryPrintHook(Hook):
    def apply(self,e:Emulator):
        print(e.memory)

class GraphicsPrintHook(Hook):
    def apply(self, e: Emulator):
        print(e.gfx_pixels)
