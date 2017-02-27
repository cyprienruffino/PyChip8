###
# Simple example
###

from view.stub.controls_stub import ControlsStub
from view.stub.graphics_stub import GraphicsStub

from controller import Controller
from view.stub.sound_stub import SoundStub


def main():
    gfx = GraphicsStub()
    sound = SoundStub()
    controls = ControlsStub()
    runner = Controller(gfx, sound, controls)

    runner.load_rom("TETRIS.bin")
    runner.begin_loop_forwards()



if __name__=="__main__":
    main()