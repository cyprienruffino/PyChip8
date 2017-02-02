from emulator.engine import Emulator
from emulator.modules_stub.controls_stub import ControlsStub
from emulator.modules_stub.graphics_stub import GraphicsStub
from emulator.modules_stub.sound_stub import SoundStub


def main():
    emulator=Emulator()
    emulator.add_gfx(GraphicsStub())
    emulator.add_controls(ControlsStub())
    emulator.add_sound(SoundStub())

    emulator.load_rom("./TETRIS")
    emulator.start()


if __name__=="__main__":
    main()