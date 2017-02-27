from model.emulator import Emulator
from model.modules.controls import Controls
from model.modules.graphics import Graphics
from model.modules.sound import Sound


class Runner:
    def __init__(self, gfx:Graphics=None, sound:Sound=None, controls:Controls=None):

        self.emulator=Emulator()
        self.gfx = gfx
        self.sound = sound
        self.controls = controls

        self.pre_cycle_hooks = dict()
        self.post_cycle_hooks = dict()
        self.init_hooks = dict()

        self.__looping_forwards = False
        self.__looping_backwards = False
        self.__frame_limit = False
        self.__debug = False


    #### Private

    def __call_graphics(self):
        if self.gfx is not None: # Calls the graphics module, if present
            if self.emulator.draw_flag:
                self.gfx.draw(self.emulator.gfx_pixels)

    def __call_controls(self):
        if self.controls is not None: # Calls the controls module, if present
            self.emulator.set_key(self.controls.get_key())

    def __call_sound(self):
        if self.controls is not None: # Calls the sound module, if present
            if self.emulator.beep_flag:
                self.sound.beep()

    def __start_cycle_timer(self):
        pass

    def __wait_for_timer(self):
        pass

    #### Modules

    def add_gfx(self, gfx: Graphics):
        self.gfx = gfx

    def add_sound(self, sound: Sound):
        self.sound = sound

    def add_controls(self, controls: Controls):
        self.controls = controls

    #### Hooks

    def add_init_hook(self, name: str, function):
        self.init_hooks[name] = function

    def add_pre_frame_hook(self, name: str, function):
        self.pre_cycle_hooks[name] = function

    def add_post_frame_hook(self, name: str, function):
        self.post_cycle_hooks[name] = function

    def call_init_hooks(self):
        for k, v in self.init_hooks.items():
            v()

    def call_pre_hooks(self):
        for k, v in self.pre_cycle_hooks.items():
            v()

    def call_post_hooks(self):
        for k, v in self.post_cycle_hooks.items():
            v()

    #### Debug

    def enable_debug(self):
        self.__debug = True

    def print_status(self):

        # print("Memory")
        # for i in self.memory: print(i)

        # print("Graphics")

        # for y in range(0, 32):
        #    line = ""
        #    for x in range(0, 64):
        #        line+= " "+str(self.gfx_pixels[x*32+y])
        #    print(line)

        print("Current op " + str(self.emulator.opcode))

        print("Registers")
        regs = ""
        for i in range(0, 16):
            regs += " V" + str(i) + " " + str(self.emulator.V[i])
            print(regs)

            print("Index " + str(self.emulator.I))
            print("Program counter " + str(self.emulator.pc))
            # print("Delay timer "+str(self.delay_timer))
            # print("Soundtimer "+str(self.sound_timer))

    #### Runner

    def load_rom(self, path):
        with open(path, "rb") as f:
            rom = bytearray(512)
            byte = f.read(1)
            i = 0
            while byte != b'':
                rom[i] = byte[0]
                byte = f.read(1)
                i += 1

        self.emulator.load_rom(rom)

    def step(self):
        self.call_pre_hooks()
        self.__call_graphics()
        self.__call_controls()
        self.__call_sound()
        self.emulator.gamestep()
        self.call_post_hooks()


    def step_backwards(self):
        self.call_pre_hooks()
        self.__call_graphics()
        self.__call_controls()
        self.__call_sound()
        self.emulator.gamestep_backwards()
        self.call_post_hooks()


    def begin_loop_forwards(self):
        self.__looping_forwards = True
        while self.__looping_forwards:

            if self.__frame_limit:
                self.__start_cycle_timer()

            self.step()

            if self.__frame_limit:
                self.__wait_for_timer()

    def begin_loop_backwards(self):
        self.__looping_backwards = True
        while self.__looping_backwards:

            if self.__frame_limit:
                self.__start_cycle_timer()

            self.step_backwards()

            if self.__frame_limit:
                self.__wait_for_timer()

    def end_looping_forwards(self):
        self.__looping_forwards = False

    def end_loop_backwards(self):
        self.__looping_backwards = False
