#
# Emulator engine main class
#

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

        # Debug flag
        self.debug = False

        # Graphics flag
        self.graphics_enabled = False


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

    def emulate_cycle(self):

        process_opcode(self)

        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            if self.sound_timer == 1:
                self.play_sound()

            self.sound_timer-=1


    def capture_keys(self):
        pass

    def draw(self):
        pass

    def gameloop(self):

        # Main function of the loop
        self.emulate_cycle()

        # Call the graphical engine, if present
        if self.graphics_enabled:
            self.draw()

        # Capture the key state
        self.capture_keys()



    def start(self):
        self.initialize_chip_8()
        self.call_init_hooks()

        while True:
            self.call_pre_hooks()
            self.gameloop()
            self.call_post_hooks()



    def enable_debug(self):
        self.debug=True

    def enable_graphics(self):
        pass

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

    def print_status(self):
        print("Memory"+self.memory)
        print("Graphics"+self.gfx)
        print("Current op"+self.opcode)
        print("Registers"+self.V)
        print("Index"+self.I)
        print("Program counter"+self.pc)
        print("Delay timer"+self.delay_timer)
        print("Soundtimer"+self.sound_timer)






