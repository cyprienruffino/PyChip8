###
# Simple example
###

from Controller import Controller
from sample_hooks.HelloWorldHook import HelloWorldHook
from tools.Disassembler import Disassembler
from view.stub.ControlsStub import ControlsStub
from view.stub.SoundStub import SoundStub
from view.testgfx.Poorgfx import PoorGraphics


def run_emulator():

    controller = Controller()
    controller.add_sound("stub", SoundStub())
    controller.add_gfx("poor", PoorGraphics())
    controller.add_controls("stub",ControlsStub())

    controller.add_init_hook("helloworld", HelloWorldHook())

    controller.load_rom("ROMs/TETRIS.bin")
    #controller.begin_loop_forwards()
    controller.step()

def disassemble():
    dis = Disassembler()
    print(dis.disassemble_rom("ROMs/TETRIS.bin",512))


if __name__=="__main__":
    run_emulator()
    #disassemble()