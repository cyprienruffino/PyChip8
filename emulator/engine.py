#
# Emulator engine main class
#
from emulator.hooks.hook_interface import Hook
from emulator.modules.graphics import Graphics
from emulator.modules.sound import Sound

from emulator.modules.controls import Controls
from emulator.opcodes import process_opcode


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
        self.gfx_pixels = bytearray(64*32)

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


    def gameloop(self):

        # Calls the graphics module, if present
        if self.graphics_enabled:
            if self.draw_flag:
                self.gfx.draw(self)
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

        process_opcode(self)



    def start(self):
        self.call_init_hooks()

        while True:
            self.start_cycle_timer()

            self.call_pre_hooks()
            self.gameloop()
            self.call_post_hooks()

            self.wait_for_timer()


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

    def add_init_hook(self, hook:Hook):
        self.init_hooks[hook.name]=hook

    def add_pre_frame_hook(self, hook:Hook):
        self.pre_frame_hooks[hook.name]=hook

    def add_post_frame_hook(self, hook:Hook):
        self.post_frame_hooks[hook.name]=hook

    def call_init_hooks(self):
        for k, v in self.init_hooks.items():
            v.apply(self)

    def call_pre_hooks(self):
        for k, v in self.pre_frame_hooks.items():
            v.apply(self)

    def call_post_hooks(self):
        for k, v in self.post_frame_hooks.items():
            v.apply(self)


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







