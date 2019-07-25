#!/usr/bin/env python

import sys

from tools.Disassembler import Disassembler

def disassemble():
    dis = Disassembler()
    print(dis.disassemble_rom("ROMs/TETRIS.bin", 512))


if __name__ == "__main__":
    if len(sys.argv < 2):
        print("Usage: python disassemble_rom.py rompath")
    disassemble(sys.argv[1])
