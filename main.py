#!/usr/bin/env python

from emulator.Controller import Controller
from display.CursesDisplay import CursesDisplay
from display.PoorDisplay import PoorGraphics

def run_emulator():
    controller = Controller()
    controller.add_display("curses", CursesDisplay())
    #controller.add_display("poor", PoorGraphics())
    controller.set_frame_limit(True)

    # api = API(controller)
    # controller.add_init_hook("helloworld", api.create_hook(HelloWorldHook))
    # controller.add_pre_cycle_hook("opcode", api.create_hook(OpcodeHook))

    controller.load_rom("ROMs/TETRIS.bin")
    #controller.load_rom("ROMs/Puzzle.ch8")
    #for i in range(1000): controller.next_frame()
    controller.start()

if __name__ == "__main__":
    run_emulator()
