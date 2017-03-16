#The low level API, to interact directly with the emulator memory
from Controller import Controller


class MachineAPI:
    def __init__(self, controller:Controller):
        self.__controller=controller

    def get_memory(self) -> bytearray:
        return self.__controller.emulator.memory

    def set_memory(self, memory:bytearray) -> None:
        self.__controller.emulator.memory = memory

    def get_stack(self) -> bytearray:
        return self.__controller.emulator.memory

    def set_stack(self, stack:bytearray) -> None:
        self.__controller.emulator.stack = stack

    def get_stack_pointer(self) -> int:
        return self.__controller.emulator.sp

    def set_stack_pointer(self, stack_pointer:int) -> None:
        self.__controller.emulator.sp = stack_pointer

    def get_opcode(self) -> int:
        return self.__controller.emulator.opcode

    def set_opcode(self, opcode:int) -> None:
        self.__controller.emulator.opcode = opcode

    def get_V_registers_array(self) -> bytearray:
        return self.__controller.emulator.V

    def get_V_register(self, register:int) -> int:
        return self.__controller.emulator.V[register]

    def set_V_registers_array(self, vregisters:bytearray) -> None:
        self.__controller.emulator.V = vregisters

    def set_V_register(self, register: int, value:int) -> None:
        self.__controller.emulator.V[register] = value

    def get_I_register(self) -> int:
        return self.__controller.emulator.I

    def set_I_register(self, value:int) -> None:
        self.__controller.emulator.I = value

    def get_program_counter(self) -> int:
        return self.__controller.emulator.pc

    def set_program_counter(self, value:int) -> None:
        self.__controller.emulator.pc = value

    def get_draw_flag(self) -> bool:
        return self.__controller.emulator.draw_flag

    def set_draw_flag(self, value:bool) -> None:
        self.__controller.emulator.draw_flag = value

    def get_beep_flag(self) -> bool:
        return self.__controller.emulator.beep_flag

    def set_beep_flag(self, value:bool) -> None:
        self.__controller.emulator.beep_flag = value

    def get_wait_flag(self) -> bool:
        return self.__controller.emulator.wait_flag

    def wait_flag(self, value: bool) -> None:
        self.__controller.emulator.wait_flag = value

    def get_graphics_array(self) -> bytearray:
        return self.__controller.emulator.gfx_pixels

    def set_graphics_array(self, graphics: bytearray) -> None:
        self.__controller.emulator.gfx_pixels = graphics

    def get_keys_list(self) -> list:
        return self.__controller.emulator.key

    def set_keys_list(self, keys:list) -> list:
        self.__controller.emulator.key = keys

    """
Necessary data to retrieve from the emulator:
-Memory
-Stack
-Stack Pointer
-Current opcode
-Registers (VX, I, PC and timers)
-Flags
-Graphics array
-Key list
    """