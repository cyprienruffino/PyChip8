# The low level API, to interact directly with the CPU memory
from emulator.Controller import Controller


class MachineAPI:
    def __init__(self, controller: Controller):
        self.__controller = controller

    def get_memory(self) -> bytearray:
        return self.__controller.CPU.memory

    def set_memory(self, memory: bytearray) -> None:
        self.__controller.CPU.memory = memory

    def get_stack(self) -> bytearray:
        return self.__controller.CPU.memory

    def set_stack(self, stack: bytearray) -> None:
        self.__controller.CPU.stack = stack

    def get_stack_pointer(self) -> int:
        return self.__controller.CPU.sp

    def set_stack_pointer(self, stack_pointer: int) -> None:
        self.__controller.CPU.sp = stack_pointer

    def get_opcode(self) -> int:
        return self.__controller.CPU.opcode

    def set_opcode(self, opcode: int) -> None:
        self.__controller.CPU.opcode = opcode

    def get_V_registers_array(self) -> bytearray:
        return self.__controller.CPU.V

    def get_V_register(self, register: int) -> int:
        return self.__controller.CPU.V[register]

    def set_V_registers_array(self, vregisters: bytearray) -> None:
        self.__controller.CPU.V = vregisters

    def set_V_register(self, register: int, value: int) -> None:
        self.__controller.CPU.V[register] = value

    def get_I_register(self) -> int:
        return self.__controller.CPU.I

    def set_I_register(self, value: int) -> None:
        self.__controller.CPU.I = value

    def get_program_counter(self) -> int:
        return self.__controller.CPU.pc

    def set_program_counter(self, value: int) -> None:
        self.__controller.CPU.pc = value

    def get_draw_flag(self) -> bool:
        return self.__controller.CPU.draw_flag

    def set_draw_flag(self, value: bool) -> None:
        self.__controller.CPU.draw_flag = value

    def get_beep_flag(self) -> bool:
        return self.__controller.CPU.beep_flag

    def set_beep_flag(self, value: bool) -> None:
        self.__controller.CPU.beep_flag = value

    def get_wait_flag(self) -> bool:
        return self.__controller.CPU.key_wait_flag

    def wait_flag(self, value: bool) -> None:
        self.__controller.CPU.wait_flag = value

    def get_graphics_array(self) -> bytearray:
        return self.__controller.CPU.display_pixels

    def set_graphics_array(self, graphics: bytearray) -> None:
        self.__controller.CPU.gfx_pixels = graphics

    def get_keys_list(self) -> list:
        return self.__controller.CPU.key

    def set_keys_list(self, keys: list) -> None:
        self.__controller.CPU.key = keys

    """
Necessary data to retrieve from the CPU:
-Memory
-Stack
-Stack Pointer
-Current opcode
-Registers (VX, I, PC and timers)
-Flags
-Graphics array
-Key list
    """
