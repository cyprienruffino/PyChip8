#!/usr/bin/env python
import sys

from api.API import API
from emulator.Controller import Controller
from display.CursesDisplay import CursesDisplay
from display.PoorDisplay import PoorGraphics
from sample_hooks.HelloWorldHook import HelloWorldHook
from sample_hooks.OpcodeHook import OpcodeHook


def run_emulator(rom):
    controller = Controller()
    controller.add_display("curses", CursesDisplay())
    #controller.add_display("curses", PoorGraphics())
    controller.set_frame_limit(True)

    api = API(controller)
    # controller.add_init_hook("helloworld", api.create_hook(HelloWorldHook))
    # controller.add_pre_cycle_hook("opcode", api.create_hook(OpcodeHook))

    controller.load_rom(rom)
    controller.start()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py rompath")
        exit(0)
    run_emulator(sys.argv[1])
