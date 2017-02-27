###
# Simple example
###

from model.modules.modules_stub.controls_stub import ControlsStub
from model.modules.modules_stub.graphics_stub import GraphicsStub
from model.modules.modules_stub.sound_stub import SoundStub
from runner import Runner




def main():
    gfx = GraphicsStub()
    sound = SoundStub()
    controls = ControlsStub()
    runner = Runner(gfx,sound,controls)

    runner.load_rom("TETRIS.bin")
    runner.begin_loop_forwards()



if __name__=="__main__":
    main()