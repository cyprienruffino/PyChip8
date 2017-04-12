#
# Emulator engine main class
#


class Disassembler:
    def __init__(self):
        self.__opcode_switch = {
            0x0000: self.__x0000, 0x1000: self.__x1000,
            0x2000: self.__x2000, 0x3000: self.__x3000,
            0x4000: self.__x4000, 0x5000: self.__x5000,
            0x6000: self.__x6000, 0x7000: self.__x7000,
            0x8000: self.__x8000, 0x9000: self.__x9000,
            0xA000: self.__xA000, 0xB000: self.__xB000,
            0xC000: self.__xC000, 0xD000: self.__xD000,
            0xE000: self.__xE000, 0xF000: self.__xF000,
        }
        self.__opcode = 0

    def __x0000(self):
        # Clear screen
        if self.__opcode == 0x00E0:
            return "CLS"

        # Return
        if self.__opcode == 0x00EE:
            return "RET"

    # 1XXX => Jump(XXX)
    def __x1000(self):
        return "JP " + str(self.__opcode & 0x0FFF)

    # 2XXX => Call(XXX)
    def __x2000(self):
        return "CALL " + str(self.__opcode & 0x0FFF)

    # 3XKK => skip_next(VX == KK)
    def __x3000(self):
        return "SE V" + str((self.__opcode & 0x0F00) >> 8) + ", " + str(self.__opcode & 0x00FF)

    # 4XKK => skip_next(VX != KK)
    def __x4000(self):
        return "SNE V" + str((self.__opcode & 0x0F00) >> 8) + ", " + str(self.__opcode & 0x00FF)

    # 5XY0 => skip_next(VX == VY)
    def __x5000(self):
        return "SE V" + str((self.__opcode & 0x0F00) >> 8) + ", V" + str((self.__opcode & 0x00F0) >> 4)

    # 6XKK => VX = KK
    def __x6000(self):
        return "LD V" + str((self.__opcode & 0x0F00) >> 8) + ", " + str(self.__opcode & 0x00FF)

    # 7XKK => VX += KK
    def __x7000(self):
        return "ADD V" + str((self.__opcode & 0x0F00) >> 8) + ", " + str(self.__opcode & 0x00FF)

    # Binary ops
    def __x8000(self):
        # 8XY0 => VX = VY
        if (self.__opcode & 0x000F) == 0x0000:
            return "LD V" + str((self.__opcode & 0x0F00) >> 8) + ", V" + str((self.__opcode & 0x00F0) >> 4)

        # 8XY1 => VX |= VY
        if (self.__opcode & 0x000F) == 0x0001:
            return "OR V" + str((self.__opcode & 0x0F00) >> 8) + ", V" + str((self.__opcode & 0x00F0) >> 4)

        # 8XY2 => VX &= VY
        if (self.__opcode & 0x000F) == 0x0002:
            return "AND V" + str((self.__opcode & 0x0F00) >> 8) + ", V" + str((self.__opcode & 0x00F0) >> 4)

        # 8XY3 => VX ^= VY
        if (self.__opcode & 0x000F) == 0x0003:
            return "XOR V" + str((self.__opcode & 0x0F00) >> 8) + ", V" + str((self.__opcode & 0x00F0) >> 4)

        # 8XY4 => VX += VY
        if (self.__opcode & 0x000F) == 0x0004:
            return "ADD V" + str((self.__opcode & 0x0F00) >> 8) + ", V" + str((self.__opcode & 0x00F0) >> 4)

        # 8XY5 => VX -= VY
        if (self.__opcode & 0x000F) == 0x0005:
            return "SUB V" + str((self.__opcode & 0x0F00) >> 8) + ", V" + str((self.__opcode & 0x00F0) >> 4)

        # 8XY6 => VX >>= 1
        if (self.__opcode & 0x000F) == 0x0006:
            return "SHR V" + str((self.__opcode & 0x0F00) >> 8) + ", V" + str((self.__opcode & 0x00F0) >> 4)

        # 8XY7 => VX = VY - VX
        if (self.__opcode & 0x000F) == 0x0007:
            return "SUBN V" + str((self.__opcode & 0x0F00) >> 8) + ", V" + str((self.__opcode & 0x00F0) >> 4)

        # 8XYE => VX <<= 1
        if (self.__opcode & 0x000F) == 0x000E:
            return "SHL V" + str((self.__opcode & 0x0F00) >> 8) + ", V" + str((self.__opcode & 0x00F0) >> 4)

    # 9XY0 => skip_next(VX!=VY)
    def __x9000(self):
        return "SNE V" + str((self.__opcode & 0x0F00) >> 8) + ", V" + str((self.__opcode & 0x00F0) >> 4)

    # AKKK => I=KKK
    def __xA000(self):
        return "LD I, " + str(self.__opcode & 0x0FFF)

    # BKKK => Jump(V0+KKK)
    def __xB000(self):
        return "JP V0, " + str(self.__opcode & 0x0FFF)

    # CXKK => VX=Rand(V0,255)+KK
    def __xC000(self):
        return "RND V" + str((self.__opcode & 0x0F00) >> 8) + ", " + str(self.__opcode & 0x00FF)

    # DXYN = draw(VX,VY,N)
    def __xD000(self):
        return "DRW V" + str((self.__opcode & 0x0F00) >> 8) + ", V" + str((self.__opcode & 0x00F0) >> 4) + " " + str(
            (self.__opcode & 0x000F))

    def __xE000(self):
        # EX9E = skip(if_pressed(VX))
        if self.__opcode & 0x00FF == 0x009E:
            return "SKP V" + str((self.__opcode & 0x0F00) >> 8)

        # EXA1 = skip(if_not_pressed(VX))
        if self.__opcode & 0x00FF == 0x00A1:
            return "SKNP V" + str((self.__opcode & 0x0F00) >> 8)

    def __xF000(self):
        # FX07 => VX = get_delay()
        if (self.__opcode & 0x00FF) == 0x0007:
            return "LD V" + str((self.__opcode & 0x0F00) >> 8) + ", DT"

        # FX0A => VX = get_key() (Blocking!)
        if (self.__opcode & 0x00FF) == 0x000A:
            return "LD V" + str((self.__opcode & 0x0F00) >> 8) + ", K"

        # FX15 => set_delay(VX)
        if (self.__opcode & 0x00FF) == 0x0015:
            return "LD DT, V" + str((self.__opcode & 0x0F00) >> 8)

        # FX18 => VX = set_sound(VX)
        if (self.__opcode & 0x00FF) == 0x0018:
            return "LD ST, V" + str((self.__opcode & 0x0F00) >> 8)

        # FX1E => I += VX
        if (self.__opcode & 0x00FF) == 0x001E:
            return "ADD I, V" + str((self.__opcode & 0x0F00) >> 8)

        # FX29 => I = get_char_addr[VX]
        if (self.__opcode & 0x00FF) == 0x0029:
            return "LD F, V" + str((self.__opcode & 0x0F00) >> 8)

        # FX33 => memory[I, I+1, I+2] = binary_coded_decimal(VX)
        if (self.__opcode & 0x00FF) == 0x0033:
            return "LD B, V" + str((self.__opcode & 0x0F00) >> 8)

        # FX55 => save(VX, &I)
        if (self.__opcode & 0x00FF) == 0x0055:
            return "LD [I], V" + str((self.__opcode & 0x0F00) >> 8)

        # FX65 => load(VX, &I)
        if (self.__opcode & 0x00FF) == 0x0065:
            return "LD V" + str((self.__opcode & 0x0F00) >> 8) + ", [I]"

    def disassemble_rom(self, rom_path, romsize) -> str:
        assembly = ""
        rom = bytearray(romsize)
        with open(rom_path, "rb") as f:
            byte = f.read(1)
            i = 0
            while byte != b'':
                rom[i] = byte[0]
                byte = f.read(1)
                i += 1

        romsize = romsize
        for i in range(0, romsize, 2):
            self.__opcode = (rom[i] << 8) + rom[i + 1]
            assembly += str(self.__opcode_switch[(self.__opcode & 0xF000)]()) + "\n"

        return assembly.replace("None", "NOP")

    def disassemble_op(self, opcode) -> str:
        self.__opcode = opcode
        return str(self.__opcode_switch[(self.__opcode & 0xF000)]())
