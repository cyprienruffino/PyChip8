#
# Emulator engine main class
#
import random

class Emulator:

#### RAM and operations initialisation

    def __init__(self):

        # The whole RAM of the CHIP-8
        # 0x000 -> 0x1FF : CHIP-8 Interpreter
        # 0x050 -> 0x0A0 : Font set (4x5 pixel, 0-F)
        # 0x200 -> 0xFFF : Program ROM and work RAM
        self.memory = bytearray(4096)

        # Stack
        # 16*2 bytes and stack pointer
        self.stack = bytearray(32)
        self.sp = 0x00

        # Graphics array (64*32px), black and white
        self.gfx_pixels = bytearray(64*32)

        # Current operation
        self.opcode = 0x0000

        # Current keys
        self.key = [False] * 16

        # Registers : 15 usable, 1 for the carry flag
        self.V = bytearray(16)

        # Index register and program counter
        self.I = 0x0000
        self.pc = 0x0200

        # Timers
        self.delay_timer = 0
        self.sound_timer = 0

        # Fontset
        # 16 pre-loaded sprites : 0-F
        # 1 Sprite : 8x5 px
        # 5 bytes each
        fontset = bytearray(
            b'\xF0\x90\x90\x90\xF0'
            b'\x20\x60\x20\x20\x70'
            b'\xF0\x10\xF0\x80\xF0'
            b'\xF0\x10\xF0\x10\xF0'
            b'\x90\x90\xF0\x10\x10'
            b'\xF0\x80\xF0\x10\xF0'
            b'\xF0\x80\xF0\x90\xF0'
            b'\xF0\x10\x20\x40\x40'
            b'\xF0\x90\xF0\x90\xF0'
            b'\xF0\x90\xF0\x10\xF0'
            b'\xF0\x90\xF0\x90\x90'
            b'\xE0\x90\xE0\x90\xE0'
            b'\xF0\x80\x80\x80\xF0'
            b'\xE0\x90\x90\x90\xE0'
            b'\xF0\x80\xF0\x80\xF0'
            b'\xF0\x90\xF0\x90\x80'
        )

        for i in range(0,len(fontset)):
            self.memory[i]=fontset[i]

        del fontset

        # Flags
        self.draw_flag = False
        self.beep_flag = False
        self.key_wait_flag = True

        self.key_register = 0x0 # Register which will receive the key when waiting for key

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

    def none(self):
        self.pc += 2

    def x0000(self):
        #Clear screen
        if self.opcode == 0x00E0:
            self.gfx_pixels = bytearray(64 * 32)

        #Return
        if self.opcode == 0x00EE:
            self.pc = self.stack[self.sp] << 8
            self.pc += self.stack[self.sp+1]
            self.stack[self.sp] = 0
            self.stack[self.sp+1] = 0
            self.sp -= 2

        self.pc+=2

    # 1XXX => Jump(XXX)
    def x1000(self):
        self.pc = self.opcode & 0x0FFF

    # 2XXX => Call(XXX)
    def x2000(self):
        try:
            self.sp += 2
            self.stack[self.sp] = (self.pc & 0xFF00) >> 8
            self.stack[self.sp+1] = (self.pc & 0x00FF)
            self.pc = self.opcode & 0x0FFF
        except IndexError:
            pass

    # 3XKK => skip_next(VX == KK)
    def x3000(self):
        self.pc+=2
        if self.V[(self.opcode & 0x0F00) >> 8] == self.opcode & 0x00FF:
            self.pc += 2

    # 4XKK => skip_next(VX != KK)
    def x4000(self):
        self.pc += 2
        if self.V[(self.opcode & 0x0F00) >> 8] != self.opcode & 0x00FF:
            self.pc += 2

    # 5XY0 => skip_next(VX == VY)
    def x5000(self):
        self.pc += 2
        if self.V[(self.opcode & 0x0F00) >> 8] == self.V[(self.opcode & 0x00F0) >> 4]:
            self.pc += 2

    # 6XKK => VX = KK
    def x6000(self):
        self.V[(self.opcode & 0x0F00) >> 8] = self.opcode & 0x00FF
        self.pc += 2

    # 7XKK => VX += KK
    def x7000(self):
        self.V[(self.opcode & 0x0F00) >> 8] = (self.V[(self.opcode & 0x0F00) >> 8] + self.opcode & 0x00FF) % 256
        self.pc += 2

    #Binary ops
    def x8000(self):
        # 8XY0 => VX = VY
        if (self.opcode & 0x000F) == 0x0000:
            self.V[(self.opcode & 0x0F00) >> 8] = self.V[(self.opcode & 0x00F0) >> 4]
            self.pc += 2

        # 8XY1 => VX |= VY
        if (self.opcode & 0x000F) == 0x0001:
            self.V[(self.opcode & 0x0F00) >> 8] |= self.V[(self.opcode & 0x00F0) >> 4]
            self.pc += 2

        # 8XY2 => VX &= VY
        if (self.opcode & 0x000F) == 0x0002:
            self.V[(self.opcode & 0x0F00) >> 8] &= self.V[(self.opcode & 0x00F0) >> 4]
            self.pc += 2

        # 8XY3 => VX ^= VY
        if (self.opcode & 0x000F) == 0x0003:
            self.V[(self.opcode & 0x0F00) >> 8] ^= self.V[(self.opcode & 0x00F0) >> 4]
            self.pc += 2

        # 8XY4 => VX += VY
        if(self.opcode & 0x000F) == 0x0004:
            if self.V[(self.opcode & 0x00F0) >> 4] > (0xFF - self.V[(self.opcode & 0x0F00) >> 8]):
                self.V[0xF] = 1
            else:
                self.V[0xF] = 0
            self.V[(self.opcode & 0x0F00) >> 8] += self.V[(self.opcode & 0x00F0) >> 4]
            self.pc += 2

        # 8XY5 => VX -= VY
        if (self.opcode & 0x000F) == 0x0005:
            if self.V[(self.opcode & 0x00F0) >> 4] > (self.V[(self.opcode & 0x0F00) >> 8]):
                self.V[0xF] = 1
            else:
                self.V[0xF] = 0
            self.V[(self.opcode & 0x0F00) >> 8] -= self.V[(self.opcode & 0x00F0) >> 4]
            self.pc += 2

        # 8XY6 => VX >>= 1
        if (self.opcode & 0x000F) == 0x0006:
            self.V[0xF] = self.V[(self.opcode & 0x0F00) >> 8] & 1
            self.V[(self.opcode & 0x0F00) >> 8] >>= 1
            self.pc += 2

        # 8XY7 => VX = VY - VX
        if (self.opcode & 0x000F) == 0x0007:
            if self.V[(self.opcode & 0x00F0) >> 4] < (self.V[(self.opcode & 0x0F00) >> 8]):
                self.V[0xF] = 1
            else:
                self.V[0xF] = 0

            self.V[(self.opcode & 0x0F00) >> 8] >>= 1
            self.pc += 2

        # 8XYE => VX <<= 1
        if (self.opcode & 0x000F) == 0x000E:
            if self.V[(self.opcode & 0x0F00) >> 8] & 0b10000000 == 0b10000000:
                self.V[0xF] = 1
            self.V[(self.opcode & 0x0F00) >> 8] <<= 1
            self.pc += 2

    # 9XY0 => skip_next(VX!=VY)
    def x9000(self):
        self.pc += 2
        if self.V[(self.opcode & 0x0F00) >> 8] != self.V[(self.opcode & 0x00F0) >> 4]:
            self.pc += 2

    # AKKK => I=KKK
    def xA000(self):
        self.I=self.opcode & 0x0FFF
        self.pc += 2

    # BKKK => Jump(V0+KKK)
    def xB000(self):
        self.pc = self.opcode & 0x0FFF + self.V[0]

    # CXKK => VX=Rand(V0,255)+KK
    def xC000(self):
        self.V[(self.opcode & 0x0F00) >> 8] = random.randint(0,255) & self.opcode & 0x00FF
        self.pc += 2

    # DXYN = draw(VX,VY,N)
    def xD000(self):
        x = self.V[((self.opcode & 0x0F00) >> 8)] -1
        y = self.V[((self.opcode & 0x00F0) >> 4)] -1
        height = self.opcode & 0x000F
        self.V[0xF] = 0x0


        for ty in range(0,height):
            pixel = self.memory[self.I + ty]
            for tx in range(0,8):
                if (pixel & (0x80 >> tx)) != 0:
                    if self.gfx_pixels[(x + tx + ((y + ty) * 64))] == 1:
                        self.V[0xF] = 1
                    self.gfx_pixels[x + tx + ((y + ty) * 64)] |= 1
        self.draw_flag = True
        self.pc += 2


    def xE000(self):
        # EX9E = skip(if_pressed(VX))
        if self.opcode & 0x00FF == 0x009E:
            if self.key[self.V[((self.opcode & 0x0F00) >> 8)]]:
                self.pc += 2

        # EXA1 = skip(if_not_pressed(VX))
        if self.opcode & 0x00FF == 0x00A1:
            if not self.key[self.V[((self.opcode & 0x0F00) >> 8)]]:
                self.pc += 2

        self.pc += 2

    def xF000(self):
        # FX07 => VX = get_delay()
        if (self.opcode & 0x00FF) == 0x0007:
            self.V[(self.opcode & 0x0F00) >> 8] = self.delay_timer

        # FX0A => VX = get_key() (Blocking!)
        if (self.opcode & 0x00FF) == 0x000A:
            self.key_wait_flag = True
            self.key_register = (self.opcode & 0x0F00) >> 8

        # FX15 => set_delay(VX)
        if (self.opcode & 0x00FF) == 0x0015:
            self.delay_timer = self.V[(self.opcode & 0x0F00) >> 8]

        # FX18 => VX = set_sound(VX)
        if (self.opcode & 0x00FF) == 0x0018:
            self.sound_timer = self.V[(self.opcode & 0x0F00) >> 8]

        # FX1E => I += VX
        if (self.opcode & 0x00FF) == 0x001E:
            self.I += self.V[(self.opcode & 0x0F00) >> 8]

        # FX29 => I = get_char_addr[VX]
        if (self.opcode & 0x00FF) == 0x0029:
            self.I = self.V[((self.opcode & 0x0F00) >> 8) * 5]

        # FX33 => memory[I, I+1, I+2] = binary_coded_decimal(VX)
        if (self.opcode & 0x00FF) == 0x0033:
            X=self.opcode & 0x0F00
            t=self.V[X >> 8]
            self.memory[self.I] = int(t/100)
            self.memory[self.I+1] = int(t/10)-10*int(t/100)
            self.memory[self.I+2] = t-10*(int(t/10)-10*int(t/100))-100*int(t/100)

        # FX55 => save(VX, &I)
        if (self.opcode & 0x00FF) == 0x0055:
            for i in range(0, self.V[(self.opcode & 0x0F00) >> 8]+1):
                self.memory[i+self.I]=self.V[i]

        # FX65 => load(VX, &I)
        if (self.opcode & 0x00FF) == 0x0065:
            for i in range(0, self.V[(self.opcode & 0x0F00) >> 8]+1):
                self.V[i]=self.memory[i+self.I]

        self.pc += 2


    def process_opcode(self):
        self.opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.opcode_switch.get(self.opcode & 0xF000)()



    #### Engine
    def load_rom(self, rom):
        for i in range(0,len(rom)):
            self.memory[i+512] = rom[i]

    def gamestep(self):
        if not self.key_wait_flag:
            if self.draw_flag:
                self.draw_flag = False

            if self.delay_timer > 0:
                self.delay_timer -= 1


            if self.sound_timer > 0:
                if self.sound_timer == 1:
                    self.beep_flag = False
                self.sound_timer -= 1

        self.process_opcode()


    def gamestep_backwards(self):
        pass

    def press_key(self, key):
        self.key[key] = True
        if self.key_wait_flag:
            self.key_wait_flag = False
            self.V[self.key_register] = key


    def release_key(self, key):
        self.key[key] = False
