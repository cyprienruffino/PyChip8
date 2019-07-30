#!/usr/bin/env python

import sys

from tools import assembler


def assemble(rompath, outpath):
    assembler.assemble_file(rompath, outpath)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python disassemble_rom.py rompath output_path")
        exit(0)
    assemble(sys.argv[1], sys.argv[2])
