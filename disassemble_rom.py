#!/usr/bin/env python

import sys

from tools import disassembler


def disassemble(rompath, outpath):
    disassembler.disassemble_rom(rompath, outpath)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python disassemble_rom.py rompath output_path")
        exit(0)
    disassemble(sys.argv[1], sys.argv[2])
