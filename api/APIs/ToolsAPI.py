#API to use predefined tools such as the Disassembler
from emulator.Controller import Controller
from tools.Disassembler import Disassembler


class ToolsAPI:
    def __init__(self, controller:Controller):
        self.__controller=controller

    def disassemble_opcode(self, opcode:int) -> str:
        if self.__disassembler is None:
            self.__disassembler: Disassembler = Disassembler()
        return self.__disassembler.disassemble_op(opcode)

    def disassemble_ROM(self, rom_path:str, rom_size:int) -> str:
        if self.__disassembler is None:
            self.__disassembler: Disassembler = Disassembler()
        return self.__disassembler.disassemble_rom(rom_path, rom_size)
