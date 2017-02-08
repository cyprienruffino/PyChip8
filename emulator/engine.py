#
# Emulator engine main class
#
import random

from emulator.modules.graphics import Graphics
from emulator.modules.controls import Controls
from emulator.modules.sound import Sound

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

        # Registers : 15 usable, 1 for the carry flag
        self.V = bytearray(16)

        # Index register and program counter
        self.I = 0x0000
        self.pc = 0x0200

        # Timers
        self.delay_timer = 0
        self.sound_timer = 0

        # Hooks for the environment
        self.init_hooks = dict()
        self.pre_frame_hooks= dict()
        self.post_frame_hooks = dict()

        # Modules
        self.controls:Controls = None
        self.gfx:Graphics = None
        self.sound:Sound = None

        # Flags
        self.graphics_enabled = False
        self.controls_enabled = False
        self.sound_enabled = False
        self.debug = False

        self.draw_flag = False
        self.beep_flag = False

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

    def load_rom(self, f):
        with open(f, "rb") as f:
            byte = f.read(1)
            i=0
            while byte != b'':
                self.memory[i+512] = byte[0]
                byte = f.read(1)
                i+=1


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
        if(self.opcode & 0x000F)==0x0004:
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
        print("toto")
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


    def xD000(self):
        #TODO Do display
        self.pc += 2


    def xE000(self):
        #TODO Controls
        if self.opcode & 0xFF == 0x9E:
            pass

        if self.opcode & 0xFF == 0xA1:
            pass

        self.pc += 2

    def xF000(self):
        # FX07 => VX = get_delay()
        if (self.opcode & 0x00FF) == 0x0007:
            self.V[(self.opcode & 0x0F00) >> 8] = self.delay_timer

        # FX0A => VX = get_key() (Blocking!)
        if (self.opcode & 0x00FF) == 0x000A:
            self.V[(self.opcode & 0x0F00) >> 8] = self.controls.get_key()

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
        # TODO When the font set implementation is done
        if (self.opcode & 0x00FF) == 0x0029:
            pass

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
        self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]

        self.opcode_switch.get(self.opcode & 0xF000)()



#### Engine

    def gameloop(self):

        # Calls the graphics module, if present
        if self.graphics_enabled:
            if self.draw_flag:
                self.gfx.draw(self.gfx_pixels)
                self.draw_flag = False

        # Calls the controls module, if present
        if self.controls_enabled:
            self.controls.get_key(self)

        if self.delay_timer > 0:
            self.delay_timer -= 1


        if self.sound_timer > 0:
            if self.sound_timer == 1:
                # Calls the sound module, if present
                if self.controls_enabled:
                    self.sound.beep()
                self.beep_flag = False
            self.sound_timer -= 1

        self.process_opcode()


#### Modules

    def add_gfx(self, gfx:Graphics):
        self.gfx=gfx

    def add_sound(self, sound:Sound):
        self.sound=sound

    def add_controls(self, controls:Controls):
        self.controls=controls

    def start_cycle_timer(self):
        pass

    def wait_for_timer(self):
        pass


#### Hooks

    def add_init_hook(self, name:str, function):
        self.init_hooks[name]=function

    def add_pre_frame_hook(self, name:str, function):
        self.pre_frame_hooks[name]=function

    def add_post_frame_hook(self, name:str, function):
        self.post_frame_hooks[name]=function

    def call_init_hooks(self):
        for k, v in self.init_hooks.items():
            v()

    def call_pre_hooks(self):
        for k, v in self.pre_frame_hooks.items():
            v()

    def call_post_hooks(self):
        for k, v in self.post_frame_hooks.items():
            v()


#### Debug

    def enable_debug(self):
        self.debug=True

    def print_status(self):

        #print("Memory")
        #for i in self.memory: print(i)

        #print("Graphics")

        #for y in range(0, 32):
        #    line = ""
        #    for x in range(0, 64):
        #        line+= " "+str(self.gfx_pixels[x*32+y])
        #    print(line)

        print("Current op "+str(self.opcode))

        print("Registers")
        regs=""
        for i in range(0,16):
            regs+=" V"+str(i)+" "+str(self.V[i])
        print(regs)

        print("Index "+str(self.I))
        print("Program counter "+str(self.pc))
        #print("Delay timer "+str(self.delay_timer))
        #print("Soundtimer "+str(self.sound_timer))


#### Start

    def start(self):

        self.call_init_hooks()

        while True:
            self.start_cycle_timer()

            self.call_pre_hooks()
            self.gameloop()
            self.call_post_hooks()

            self.wait_for_timer()