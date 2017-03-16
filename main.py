###
# Simple example
###
from API import API
from Controller import Controller
from OpcodeHook import OpcodeHook
from sample_hooks.HelloWorldHook import HelloWorldHook
from tools.Disassembler import Disassembler
from view.stub.ControlsStub import ControlsStub
from view.stub.SoundStub import SoundStub
from view.testgfx.Poorgfx import PoorGraphics


def run_emulator():

    controller = Controller()
    controller.add_sound("stub", SoundStub())
    controller.add_gfx("poor", PoorGraphics())
    #controller.add_gfx("stub", GraphicsStub())
    controller.add_controls("stub",ControlsStub())


    api = API(controller)
    #controller.add_init_hook("helloworld", api.create_hook(HelloWorldHook))
    #controller.add_pre_cycle_hook("opcode", api.create_hook(OpcodeHook))
    #controller.add_pre_frame_hook("opcode", api.create_hook(OpcodeHook))

    controller.load_rom("ROMs/TETRIS.bin")
    for i in range(0,3):
        controller.next_frame()

    # controller.start_looping_forwards()

def disassemble():
    dis = Disassembler()
    print(dis.disassemble_rom("ROMs/TETRIS.bin",512))


if __name__=="__main__":
    run_emulator()
    #disassemble()