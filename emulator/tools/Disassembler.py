#
# Emulator engine main class
#

class Disassembler:

    def __init__(self, rom_path, romsize):
        self.opcode_switch = {
            0x0000: self.x0000, 0x1000: self.x1000,
            0x2000: self.x2000, 0x3000: self.x3000,
            0x4000: self.x4000, 0x5000: self.x5000,
            0x6000: self.x6000, 0x7000: self.x7000,
            0x8000: self.x8000, 0x9000: self.x9000,
            0xA000: self.xA000, 0xB000: self.xB000,
            0xC000: self.xC000, 0xD000: self.xD000,
            0xE000: self.xE000, 0xF000: self.xF000,
        }
        self.opcode = 0

        self.rom = bytearray(romsize)

        with open(rom_path, "rb") as f:
            byte = f.read(1)
            i = 0
            while byte != b'':
                self.rom[i] = byte[0]
                byte = f.read(1)
                i += 1

        self.romsize = romsize


    def none(self):
       return "NOP"

    def x0000(self):
        #Clear screen
        if self.opcode == 0x00E0:
            return "CLS"

        #Return
        if self.opcode == 0x00EE:
            return "RET"


    # 1XXX => Jump(XXX)
    def x1000(self):
        return "JP " + str(self.opcode & 0x0FFF)

    # 2XXX => Call(XXX)
    def x2000(self):
        return "CALL "+ str(self.opcode & 0x0FFF)

    # 3XKK => skip_next(VX == KK)
    def x3000(self):
        return "SE V"+str((self.opcode & 0x0F00) >> 8)+ " "+str(self.opcode & 0x00FF)


    # 4XKK => skip_next(VX != KK)
    def x4000(self):
        return "SNE V" + str((self.opcode & 0x0F00) >> 8) + " " + str(self.opcode & 0x00FF)

    # 5XY0 => skip_next(VX == VY)
    def x5000(self):
        return "SE V" + str((self.opcode & 0x0F00) >> 8) + " V" + str((self.opcode & 0x00F0) >> 4)


    # 6XKK => VX = KK
    def x6000(self):
        return "LD V" + str((self.opcode & 0x0F00) >> 8) + " " + str(self.opcode & 0x00FF)

    # 7XKK => VX += KK
    def x7000(self):
        return "ADD V" + str((self.opcode & 0x0F00) >> 8) + " " + str(self.opcode & 0x00FF)

    #Binary ops
    def x8000(self):
        # 8XY0 => VX = VY
        if (self.opcode & 0x000F) == 0x0000:
            return "LD V" + str((self.opcode & 0x0F00) >> 8) + " V" + str((self.opcode & 0x00F0) >> 4)

        # 8XY1 => VX |= VY
        if (self.opcode & 0x000F) == 0x0001:
            return "OR V" + str((self.opcode & 0x0F00) >> 8) + " V" + str((self.opcode & 0x00F0) >> 4)

        # 8XY2 => VX &= VY
        if (self.opcode & 0x000F) == 0x0002:
            return "AND V" + str((self.opcode & 0x0F00) >> 8) + " V" + str((self.opcode & 0x00F0) >> 4)

        # 8XY3 => VX ^= VY
        if (self.opcode & 0x000F) == 0x0003:
            return "XOR V" + str((self.opcode & 0x0F00) >> 8) + " V" + str((self.opcode & 0x00F0) >> 4)

        # 8XY4 => VX += VY
        if(self.opcode & 0x000F) == 0x0004:
            return "ADD V" + str((self.opcode & 0x0F00) >> 8) + " V" + str((self.opcode & 0x00F0) >> 4)

        # 8XY5 => VX -= VY
        if (self.opcode & 0x000F) == 0x0005:
            return "SUB V" + str((self.opcode & 0x0F00) >> 8) + " V" + str((self.opcode & 0x00F0) >> 4)

        # 8XY6 => VX >>= 1
        if (self.opcode & 0x000F) == 0x0006:
            return "SHR V" + str((self.opcode & 0x0F00) >> 8) + " V" + str((self.opcode & 0x00F0) >> 4)

        # 8XY7 => VX = VY - VX
        if (self.opcode & 0x000F) == 0x0007:
            return "SUBN V" + str((self.opcode & 0x0F00) >> 8) + " V" + str((self.opcode & 0x00F0) >> 4)

        # 8XYE => VX <<= 1
        if (self.opcode & 0x000F) == 0x000E:
            return "SHL V" + str((self.opcode & 0x0F00) >> 8) + " V" + str((self.opcode & 0x00F0) >> 4)

    # 9XY0 => skip_next(VX!=VY)
    def x9000(self):
        return "SNE V" + str((self.opcode & 0x0F00) >> 8) + " V" + str((self.opcode & 0x00F0) >> 4)

    # AKKK => I=KKK
    def xA000(self):
        return "LD I, "+str(self.opcode & 0x0FFF)

    # BKKK => Jump(V0+KKK)
    def xB000(self):
        return "JP V0"+str(self.opcode & 0x0FFF)

    # CXKK => VX=Rand(V0,255)+KK
    def xC000(self):
        return "RND V" + str((self.opcode & 0x0F00) >> 8) + " " + str(self.opcode & 0x00FF)

    # DXYN = draw(VX,VY,N)
    def xD000(self):
        return "DRW V" + str((self.opcode & 0x0F00) >> 8) + " V" + str((self.opcode & 0x00F0) >> 4) + " " + str((self.opcode & 0x000F))



    def xE000(self):
        # EX9E = skip(if_pressed(VX))
        if self.opcode & 0x00FF == 0x009E:
            return "SKP V" + str((self.opcode & 0x0F00) >> 8)

        # EXA1 = skip(if_not_pressed(VX))
        if self.opcode & 0x00FF == 0x00A1:
            return "SKNP V" + str((self.opcode & 0x0F00) >> 8)


    def xF000(self):
        # FX07 => VX = get_delay()
        if (self.opcode & 0x00FF) == 0x0007:
            return "LD V" + str((self.opcode & 0x0F00) >> 8) + " DT"

        # FX0A => VX = get_key() (Blocking!)
        if (self.opcode & 0x00FF) == 0x000A:
            return "LD V" + str((self.opcode & 0x0F00) >> 8) + " K"

        # FX15 => set_delay(VX)
        if (self.opcode & 0x00FF) == 0x0015:
            return "LD DT V" + str((self.opcode & 0x0F00) >> 8)

        # FX18 => VX = set_sound(VX)
        if (self.opcode & 0x00FF) == 0x0018:
            return "LD ST V" + str((self.opcode & 0x0F00) >> 8)

        # FX1E => I += VX
        if (self.opcode & 0x00FF) == 0x001E:
            return "ADD I V" + str((self.opcode & 0x0F00) >> 8)

        # FX29 => I = get_char_addr[VX]
        if (self.opcode & 0x00FF) == 0x0029:
            return "LD F V" + str((self.opcode & 0x0F00) >> 8)

        # FX33 => memory[I, I+1, I+2] = binary_coded_decimal(VX)
        if (self.opcode & 0x00FF) == 0x0033:
            return "LD B V" + str((self.opcode & 0x0F00) >> 8)

        # FX55 => save(VX, &I)
        if (self.opcode & 0x00FF) == 0x0055:
            return "LD [I] V" + str((self.opcode & 0x0F00) >> 8)

        # FX65 => load(VX, &I)
        if (self.opcode & 0x00FF) == 0x0065:
            return "LD V" + str((self.opcode & 0x0F00) >> 8)+ " [I]"



    def disassemble(self):
        assembly = ""
        for i in range(0,self.romsize,2):
            self.opcode=(self.rom[i] << 8) + self.rom[i+1]
            assembly += str(self.opcode_switch[(self.opcode & 0xF000)]()) + "\n"

        return assembly.replace("None","NOP")

    def disassemble_op(self, opcode):
        self.opcode = opcode
        return str(self.opcode_switch[(self.opcode & 0xF000)]())