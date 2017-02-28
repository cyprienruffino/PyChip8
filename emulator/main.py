###
# Simple example
###

from Controller import Controller
from tools.Disassembler import Disassembler
from view.stub.Controls_stub import ControlsStub
from view.stub.Sound_stub import SoundStub
from view.testgfx.IPoorgfx import PoorGraphics


def run_emulator():

    gfx = PoorGraphics()
    sound = SoundStub()
    controls = ControlsStub()
    runner = Controller(gfx, sound, controls)

    runner.load_rom("TETRIS.bin")
    runner.begin_loop_forwards()


def disassemble():
    dis = Disassembler("TETRIS.bin",512)
    print(dis.disassemble())


if __name__=="__main__":
    run_emulator()
    #disassemble()