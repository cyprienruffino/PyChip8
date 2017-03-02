import time

from model.Emulator import Emulator
from view.IControls import IControls
from view.IGraphics import IGraphics
from view.ISound import ISound


class Controller:
    def __init__(self, gfx:IGraphics=None, sound:ISound=None, controls:IControls=None):

        self.emulator:Emulator=Emulator()
        self.gfx:IGraphics = gfx
        self.sound:ISound = sound
        self.controls:IControls = controls

        self.pre_cycle_hooks:dict = dict()
        self.post_cycle_hooks:dict = dict()
        self.init_hooks:dict = dict()

        self.__looping_forwards:bool = False
        self.__looping_backwards:bool = False
        self.__frame_limit:bool = False
        self.__debug:bool = False

        self.__time:float = 0




    #### Private

    def __call_graphics(self):
        if self.gfx is not None: # Calls the graphics module, if present
            if self.emulator.draw_flag:
                self.gfx.draw(self.emulator.gfx_pixels)

    def __call_controls(self):
        if self.controls is not None: # Calls the controls module, if present
            for i in self.controls.get_keys_pressed():
                self.emulator.press_key(i)

            for i in self.controls.get_keys_released():
                self.emulator.release_key(i)


    def __call_sound(self):
        if self.controls is not None: # Calls the sound module, if present
            if self.emulator.beep_flag:
                self.sound.beep()

    def __start_cycle_timer(self):
        self.__time = time.clock()

    def __wait_for_timer(self):
        elapsed = time.clock() - self.__time
        if elapsed < (1/60):
            time.sleep((1/60) - elapsed)

    def __call_init_hooks(self) -> None:
        for k, v in self.init_hooks.items():
            v()

    def __call_pre_hooks(self) -> None:
        for k, v in self.pre_cycle_hooks.items():
            v()

    def __call_post_hooks(self) -> None:
        for k, v in self.post_cycle_hooks.items():
            v()

    #### Modules

    def add_gfx(self, gfx: IGraphics) -> None:
        self.gfx = gfx

    def add_sound(self, sound: ISound) -> None:
        self.sound = sound

    def add_controls(self, controls: IControls) -> None:
        self.controls = controls

    #### Hooks

    def add_init_hook(self, name: str, function) -> None:
        self.init_hooks[name] = function

    def add_pre_frame_hook(self, name: str, function) -> None:
        self.pre_cycle_hooks[name] = function

    def add_post_frame_hook(self, name: str, function) -> None:
        self.post_cycle_hooks[name] = function


    #### Debug

    def enable_debug(self) -> None:
        self.__debug = True


    def print_status(self) -> None:

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

    def load_rom(self, path) -> None:
        with open(path, "rb") as f:
            rom = bytearray(512)
            byte = f.read(1)
            i = 0
            while byte != b'':
                rom[i] = byte[0]
                byte = f.read(1)
                i += 1

        self.emulator.load_rom(rom)

    def step(self) -> None:
        self.__call_pre_hooks()
        self.__call_graphics()
        self.__call_graphics()
        self.__call_controls()
        self.__call_sound()
        self.emulator.gamestep()
        self.__call_post_hooks()


    def step_backwards(self) -> None:
        self.__call_pre_hooks()
        self.__call_graphics()
        self.__call_controls()
        self.__call_sound()
        self.emulator.gamestep_backwards()
        self.__call_post_hooks()


    def begin_loop_forwards(self) -> None:
        self.__looping_forwards = True
        while self.__looping_forwards:

            if self.__frame_limit:
                self.__start_cycle_timer()

            self.step()

            if self.__frame_limit:
                self.__wait_for_timer()

    def begin_loop_backwards(self) -> None:
        self.__looping_backwards = True
        while self.__looping_backwards:

            if self.__frame_limit:
                self.__start_cycle_timer()

            self.step_backwards()

            if self.__frame_limit:
                self.__wait_for_timer()

    def end_looping_forwards(self) -> None:
        self.__looping_forwards = False

    def end_loop_backwards(self) -> None:
        self.__looping_backwards = False
