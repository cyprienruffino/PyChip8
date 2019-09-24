#
# CPU engine main class
#
import random


class Chip8:
    # RAM and operations initialisation

    def __init__(self):

        # The whole RAM of the CHIP-8
        # 0x000 -> 0x1FF : CHIP-8 Interpreter
        # 0x050 -> 0x0A0 : Font set (4x5 pixel, 0-F)
        # 0x200 -> 0xFFF : Program ROM and work RAM
        self.memory: bytearray = bytearray(4096)

        # Stack
        # 16*2 bytes and stack pointer
        self.stack: bytearray = bytearray(32)
        self.sp: int = 0x00

        # Graphics array (64*32px), black and white
        self.display_pixels: list = [0] * 2048

        # Current operation
        self.op: int = 0x0000

        # Current keys
        self.key: list = [0x00] * 16

        # Registers : 15 usable, 1 for the carry flag
        self.V: bytearray = bytearray(16)

        # Index register and program counter
        self.I: int = 0x0000
        self.pc: int = 0x0200

        # Register which will receive the key when waiting for key
        self.__key_register: int = 0x0

        # Timers
        self.delay_timer: int = 0
        self.sound_timer: int = 0

        # Fontset
        # 16 pre-loaded sprites : 0-F
        # 1 Sprite : 5x4 px
        # 5 bytes each
        fontset: bytearray = bytearray([
            0xF0, 0x90, 0x90, 0x90, 0xF0,
            0x20, 0x60, 0x20, 0x20, 0x70,
            0xF0, 0x10, 0xF0, 0x80, 0xF0,
            0xF0, 0x10, 0xF0, 0x10, 0xF0,
            0x90, 0x90, 0xF0, 0x10, 0x10,
            0xF0, 0x80, 0xF0, 0x10, 0xF0,
            0xF0, 0x80, 0xF0, 0x90, 0xF0,
            0xF0, 0x80, 0xF0, 0x90, 0xF0,
            0xF0, 0x10, 0x20, 0x40, 0x40,
            0xF0, 0x90, 0xF0, 0x90, 0xF0,
            0xF0, 0x90, 0xF0, 0x10, 0xF0,
            0xF0, 0x90, 0xF0, 0x90, 0x90,
            0xE0, 0x90, 0xE0, 0x90, 0xE0,
            0xF0, 0x80, 0x80, 0x80, 0xF0,
            0xE0, 0x90, 0x90, 0x90, 0xE0,
            0xF0, 0x80, 0xF0, 0x80, 0xF0,
            0xF0, 0x90, 0xF0, 0x90, 0x80,
        ])

        for i in range(0, len(fontset)):
            self.memory[i] = fontset[i]

        del fontset

        # Flags
        self.draw_flag: bool = False
        self.beep_flag: bool = False
        self.key_wait_flag: bool = False

        self.__op_switch = {
            0x0000: self.__x0000, 0x1000: self.__x1000,
            0x2000: self.__x2000, 0x3000: self.__x3000,
            0x4000: self.__x4000, 0x5000: self.__x5000,
            0x6000: self.__x6000, 0x7000: self.__x7000,
            0x8000: self.__x8000, 0x9000: self.__x9000,
            0xA000: self.__xA000, 0xB000: self.__xB000,
            0xC000: self.__xC000, 0xD000: self.__xD000,
            0xE000: self.__xE000, 0xF000: self.__xF000,
        }

    def __x0000(self):
        # Clear screen
        if self.op == 0x00E0:
            self.display_pixels = bytearray(64 * 32)

        # Return
        if self.op == 0x00EE:
            self.pc = self.stack[self.sp] << 8
            self.pc += self.stack[self.sp + 1]
            self.stack[self.sp] = 0
            self.stack[self.sp + 1] = 0
            self.sp -= 2

        self.pc += 2

    # 1XXX => Jump(XXX)
    def __x1000(self):
        self.pc = self.op & 0x0FFF

    # 2XXX => Call(XXX)
    def __x2000(self):
        try:
            self.sp += 2
            self.stack[self.sp] = (self.pc & 0xFF00) >> 8
            self.stack[self.sp + 1] = (self.pc & 0x00FF)
            self.pc = self.op & 0x0FFF
        except IndexError:
            pass

    # 3XKK => skip_next(VX == KK)
    def __x3000(self):
        self.pc += 2
        if self.V[(self.op & 0x0F00) >> 8] == self.op & 0x00FF:
            self.pc += 2

    # 4XKK => skip_next(VX != KK)
    def __x4000(self):
        self.pc += 2
        if self.V[(self.op & 0x0F00) >> 8] != self.op & 0x00FF:
            self.pc += 2

    # 5XY0 => skip_next(VX == VY)
    def __x5000(self):
        self.pc += 2
        if self.V[(self.op & 0x0F00) >> 8] == self.V[(self.op & 0x00F0) >> 4]:
            self.pc += 2

    # 6XKK => VX = KK
    def __x6000(self):
        self.V[(self.op & 0x0F00) >> 8] = self.op & 0x00FF
        self.pc += 2

    # 7XKK => VX += KK
    def __x7000(self):
        self.V[(self.op & 0x0F00) >> 8] = (self.V[(self.op & 0x0F00) >> 8] + self.op & 0x00FF) % 256
        self.pc += 2

    # Binary ops
    def __x8000(self):
        # 8XY0 => VX = VY
        if (self.op & 0x000F) == 0x0000:
            self.V[(self.op & 0x0F00) >> 8] = self.V[(self.op & 0x00F0) >> 4]
            self.pc += 2

        # 8XY1 => VX |= VY
        if (self.op & 0x000F) == 0x0001:
            self.V[(self.op & 0x0F00) >> 8] |= self.V[(self.op & 0x00F0) >> 4]
            self.pc += 2

        # 8XY2 => VX &= VY
        if (self.op & 0x000F) == 0x0002:
            self.V[(self.op & 0x0F00) >> 8] &= self.V[(self.op & 0x00F0) >> 4]
            self.pc += 2

        # 8XY3 => VX ^= VY
        if (self.op & 0x000F) == 0x0003:
            self.V[(self.op & 0x0F00) >> 8] ^= self.V[(self.op & 0x00F0) >> 4]
            self.pc += 2

        # 8XY4 => VX += VY
        if (self.op & 0x000F) == 0x0004:
            if self.V[(self.op & 0x00F0) >> 4] + self.V[(self.op & 0x0F00) >> 8] > 0xFF:
                self.V[0xF] = 1
            else:
                self.V[0xF] = 0
            self.V[(self.op & 0x0F00) >> 8] = (self.V[(self.op & 0x0F00) >> 8] + self.V[(self.op & 0x00F0) >> 4]) % 0xFF
            self.pc += 2

        # 8XY5 => VX -= VY
        if (self.op & 0x000F) == 0x0005:
            if self.V[(self.op & 0x00F0) >> 4] > (self.V[(self.op & 0x0F00) >> 8]):
                self.V[0xF] = 1
            else:
                self.V[0xF] = 0
            self.V[(self.op & 0x0F00) >> 8] = (self.V[(self.op & 0x0F00) >> 8] - self.V[(self.op & 0x00F0) >> 4]) % 0xFF
            self.pc += 2

        # 8XY6 => VX >>= 1
        if (self.op & 0x000F) == 0x0006:
            self.V[0xF] = self.V[(self.op & 0x0F00) >> 8] & 1
            self.V[(self.op & 0x0F00) >> 8] = (self.V[(self.op & 0x0F00) >> 8] >> 1) % 0xFF
            self.pc += 2

        # 8XY7 => VX = VY - VX
        if (self.op & 0x000F) == 0x0007:
            if self.V[(self.op & 0x00F0) >> 4] > (self.V[(self.op & 0x0F00) >> 8]):
                self.V[0xF] = 1
            else:
                self.V[0xF] = 0

            self.V[(self.op & 0x0F00) >> 8] = (self.V[(self.op & 0x00F0) >> 4] - self.V[(self.op & 0x0F00) >> 8]) % 0xFF
            self.pc += 2

        # 8XYE => VX <<= 1
        if (self.op & 0x000F) == 0x000E:
            if self.V[(self.op & 0x0F00) >> 8] & 0b10000000 == 0b10000000:
                self.V[0xF] = 1
            else:
                self.V[0xF] = 0

            self.V[(self.op & 0x0F00) >> 8] = (self.V[(self.op & 0x0F00) >> 8] << 1) % 0xFF
            self.pc += 2

    # 9XY0 => skip_next(VX!=VY)
    def __x9000(self):
        self.pc += 2
        if self.V[(self.op & 0x0F00) >> 8] != self.V[(self.op & 0x00F0) >> 4]:
            self.pc += 2

    # AKKK => I=KKK
    def __xA000(self):
        self.I = self.op & 0x0FFF
        self.pc += 2

    # BKKK => Jump(V0+KKK)
    def __xB000(self):
        self.pc = self.op & 0x0FFF + self.V[0x0]

    # CXKK => VX=Rand(V0,255)+KK
    def __xC000(self):
        self.V[(self.op & 0x0F00) >> 8] = random.randint(0, 255) & self.op & 0x00FF
        self.pc += 2

    # DXYN = draw(VX,VY,N)
    def __xD000(self):
        x = self.V[((self.op & 0x0F00) >> 8)]
        y = self.V[((self.op & 0x00F0) >> 4)]
        height = self.op & 0x000F

        self.V[0xF] = 0x0
        try:
            for ty in range(height):
                pixel = self.memory[self.I + ty]
                for tx in range(8):
                    if (pixel & (0x80 >> tx)) != 0:
                        if self.display_pixels[(x + tx + ((y + ty) * 64))] == 1:
                            self.V[0xF] = 1
                        else:
                            self.V[0xF] = 0
                        self.display_pixels[x + tx + ((y + ty) * 64)] ^= 1
        except Exception as e:
            pass
        # for ty in range(height):
        #    pixel = self.memory[self.I + ty]
        #    for tx in range(8):
        #        if (pixel & (0x80 >> tx)) != 0:
        #            if self.display_pixels[(x + tx + ((y + ty) * 64))] == 1:
        #                self.V[0xF] = 1
        #            self.display_pixels[x + tx + ((y + ty) * 64)] ^= 1

        self.draw_flag = True
        self.pc += 2

    def __xE000(self):
        # EX9E = skip(if_pressed(VX))
        if self.op & 0x00FF == 0x009E:
            if self.key[self.V[((self.op & 0x0F00) >> 8)]]:
                self.pc += 2
                self.key[self.V[((self.op & 0x0F00) >> 8)]] = 0

        # EXA1 = skip(if_not_pressed(VX))
        if self.op & 0x00FF == 0x00A1:
            if not self.key[self.V[((self.op & 0x0F00) >> 8)]]:
                self.pc += 2
            else:
                self.key[self.V[((self.op & 0x0F00) >> 8)]] = 0

        self.pc += 2

    def __xF000(self):
        # FX07 => VX = get_delay()
        if (self.op & 0x00FF) == 0x0007:
            self.V[(self.op & 0x0F00) >> 8] = self.delay_timer

        # FX0A => VX = get_key()
        if (self.op & 0x00FF) == 0x000A:
            self.key_wait_flag = True
            self.__key_register = (self.op & 0x0F00) >> 8

        # FX15 => set_delay(VX)
        if (self.op & 0x00FF) == 0x0015:
            self.delay_timer = self.V[(self.op & 0x0F00) >> 8]

        # FX18 => VX = set_sound(VX)
        if (self.op & 0x00FF) == 0x0018:
            self.sound_timer = self.V[(self.op & 0x0F00) >> 8]
            if self.sound_timer > 0:
                self.beep_flag = True

        # FX1E => I += VX
        if (self.op & 0x00FF) == 0x001E:
            self.I += self.V[(self.op & 0x0F00) >> 8]

        # FX29 => I = get_char_addr[VX]
        if (self.op & 0x00FF) == 0x0029:
            self.I = self.V[((self.op & 0x0F00) >> 8)] * 5

        # FX33 => memory[I, I+1, I+2 = binary_coded_decimal(VX)
        if (self.op & 0x00FF) == 0x0033:
            t = self.V[(self.op & 0x0F00) >> 8]
            self.memory[self.I] = int(t / 100)
            self.memory[self.I + 1] = int(t / 10) - 10 * int(t / 100)
            self.memory[self.I + 2] = t - 10 * (int(t / 10) - 10 * int(t / 100)) - 100 * int(t / 100)

        # FX55 => save(VX, &I)
        if (self.op & 0x00FF) == 0x0055:
            for i in range(0, ((self.op & 0x0F00) >> 8) + 1):
                self.memory[i + self.I] = self.V[i]
            self.I += ((self.op & 0x0F00) >> 8) + 1

        # FX65 => load(VX, &I)
        if (self.op & 0x00FF) == 0x0065:
            for i in range(0, ((self.op & 0x0F00) >> 8) + 1):
                self.V[i] = self.memory[i + self.I]
            self.I += ((self.op & 0x0F00) >> 8) + 1

        self.pc += 2

    def __process_op(self):
        self.op = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.__op_switch.get(self.op & 0xF000)()

    # Public functions
    def load_rom(self, rom: bytearray) -> bytearray:
        for i in range(0, len(rom)):
            self.memory[i + 0x200] = rom[i]
        return rom

    def gamestep(self) -> None:
        if not self.key_wait_flag:
            if self.draw_flag:
                self.draw_flag = False

            if self.delay_timer > 0:
                self.delay_timer -= 1

            if self.sound_timer > 0:
                self.sound_timer = 0
                self.beep_flag = False

            self.__process_op()

    def press_key(self, key: int) -> None:
        self.key[key] = 1
        if self.key_wait_flag:
            self.key_wait_flag = False
            self.V[self.__key_register] = key
