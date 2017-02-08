###
# Simple example
###

from emulator.engine import Emulator
from emulator.modules.modules_stub.controls_stub import ControlsStub
from emulator.modules.modules_stub.graphics_stub import GraphicsStub
from emulator.modules.modules_stub.sound_stub import SoundStub


def printPreFrameHooks(e:Emulator):
    for i in e.pre_frame_hooks:
        print(i.name)

def main():
    emulator=Emulator()
    emulator.add_gfx(GraphicsStub())
    emulator.add_controls(ControlsStub())
    emulator.add_sound(SoundStub())

    emulator.add_pre_frame_hook("state", emulator.print_status)

    emulator.load_rom("TETRIS")
    emulator.start()


if __name__=="__main__":
    main()