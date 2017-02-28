###
# Simple example
###

from view.stub.controls_stub import ControlsStub
from view.stub.graphics_stub import GraphicsStub

from controller import Controller
from view.stub.sound_stub import SoundStub
from disassembler import Disassembler

def main():

    disassembler = Disassembler("TETRIS.bin", 512)
    print(disassembler.disassemble())

if __name__=="__main__":
    main()