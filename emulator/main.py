###
# Simple example
###

from Controller import Controller
from tools.Disassembler import Disassembler
from view.stub.ControlsStub import ControlsStub
from view.stub.SoundStub import SoundStub
from view.testgfx.Poorgfx import PoorGraphics


def run_emulator():

    gfx = PoorGraphics()
    sound = SoundStub()
    controls = ControlsStub()
    runner = Controller(gfx, sound, controls)

    runner.load_rom("TETRIS.bin")
    runner.begin_loop_forwards()


def disassemble():
    dis = Disassembler()
    print(dis.disassemble_rom("TETRIS.bin",512))


if __name__=="__main__":
    run_emulator()
    #disassemble()