#
# Emulator engine main class
#
from emulator.controls import Controls
from emulator.graphics import Graphics
from emulator.opcodes import process_opcode
from emulator.sound import Sound


class Emulator:
    def __init__(self):

        # The whole RAM of the CHIP-8
        # 0x000 -> 0x1FF : CHIP-8 Interpreter
        # 0x050 -> 0x0A0 : Font set (4x5 pixel, 0-F)
        # 0x200 -> 0xFFF : Program ROM and work RAM
        self.memory = bytearray(4096)

        # Stack
        # 16*2 bytes and stack pointer
        self.stack = bytearray(32)
        self.sp = 0x0200

        # Graphics array (64*32px), black and white
        self.gfx = bytearray(64*32)

        # Current operation
        self.opcode = 0x0000

        # Registers : 15 usable, 1 for the carry flag
        self.V = bytearray(16)

        # Index register and program counter
        self.I = 0x0000
        self.pc = 0x0000

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



    def load_rom(self, f):
        with open(f, "rb") as f:
            byte = f.read(1)
            i=0
            while byte != "":
                self.memory[i+512] = byte
                byte = f.read(1)
                i+=1

    def setup_graphics(self):
        pass

    def setup_sound(self):
        pass




    def gameloop(self):

        # Call the graphical engine, if present
        if self.graphics_enabled:
            if self.draw_flag:
                self.gfx.draw()
                self.draw_flag = False

        # Capture the key state
        if self.controls_enabled:
            self.controls.get_key()

        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            if self.sound_timer == 1:
                self.sound.beep()
                self.beep_flag = False
            self.sound_timer -= 1

        process_opcode(self)



    def start(self):
        self.call_init_hooks()

        while True:
            self.call_pre_hooks()
            self.gameloop()
            self.call_post_hooks()




#### Engines

    def add_gfx(self, gfx:Graphics):
        self.gfx=gfx

    def add_sound(self, sound:Sound):
        self.sound=sound

    def add_controls(self, controls:Controls):
        self.controls=controls



#### Hooks

    def add_init_hook(self, hook_name, hook_function):
        self.init_hooks[hook_name]=hook_function

    def add_pre_frame_hook(self, hook_name, hook_function):
        self.pre_frame_hooks[hook_name]=hook_function

    def add_post_frame_hook(self, hook_name, hook_function):
        self.post_frame_hooks[hook_name]=hook_function

    def call_init_hooks(self):
        for k, v in self.init_hooks.items():
            v[0](self, v[1:])

    def call_pre_hooks(self):
        for k, v in self.pre_frame_hooks.items():
            v[0](self, v[1:])

    def call_post_hooks(self):
        for k, v in self.post_frame_hooks.items():
            v[0](self, v[1:])


#### Debug

    def enable_debug(self):
        self.debug=True

    def print_status(self):
        print("Memory"+self.memory)
        print("Graphics"+self.gfx)
        print("Current op"+self.opcode)
        print("Registers"+self.V)
        print("Index"+self.I)
        print("Program counter"+self.pc)
        print("Delay timer"+self.delay_timer)
        print("Soundtimer"+self.sound_timer)






