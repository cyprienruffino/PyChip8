import time

from api.hooks import Hook
from emulator.Chip8 import Chip8
from display.IDisplay import IDisplay
from sound.ISound import ISound

FPS = 20


class Controller:
    def __init__(self):

        self.CPU: Chip8 = Chip8()

        self.__display: dict = dict()
        self.__sound: dict = dict()
        self.__controls: dict = dict()

        self.__pre_cycle_hooks: dict = dict()
        self.__pre_frame_hooks = dict()
        self.__post_cycle_hooks: dict = dict()
        self.__post_frame_hooks = dict()
        self.__init_hooks: dict = dict()

        self.__looping: bool = False
        self.__frame_limit: bool = True
        self.__debug: bool = False

        self.__started: bool = False

        self.__time: float = 0

    # Private
    def __call_graphics(self):
        for _, v in self.__display.items():
            v.draw(self.CPU.display_pixels)

    def __call_presses(self):
        for _, v in self.__display.items():
            for i in v.get_keys_pressed():
                self.CPU.press_key(i)

    def __call_sound(self):
        for _, v in self.__sound.items():
            if self.CPU.beep_flag:
                v.beep()

    def __start_cycle_timer(self):
        self.__time = time.clock()

    def __wait_for_timer(self):
        elapsed = time.clock() - self.__time
        if elapsed < (1 / FPS):
            time.sleep((1 / FPS) - elapsed)

    # Hooks calls
    def __call_init_hooks(self):
        for _, v in self.__init_hooks.items():
            v.call()

    def __call_pre_hooks(self):
        for _, v in self.__pre_cycle_hooks.items():
            v.call()

    def __call_pre_frame_hooks(self):
        for _, v in self.__pre_frame_hooks.items():
            v.call()

    def __call_post_hooks(self):
        for _, v in self.__post_cycle_hooks.items():
            v.call()

    def __call_post_frame_hooks(self):
        for _, v in self.__post_frame_hooks.items():
            v.call()

    def __start(self):
        self.__started = True
        self.__call_init_hooks()

    # Modules

    def add_display(self, name: str, display: IDisplay):
        self.__display[name] = display

    def add_sound(self, name: str, sound: ISound):
        self.__sound[name] = sound

    # Hooks

    def add_init_hook(self, name: str, hook: Hook):
        self.__init_hooks[name] = hook

    def add_pre_cycle_hook(self, name: str, hook: Hook):
        self.__pre_cycle_hooks[name] = hook

    def add_post_cycle_hook(self, name: str, hook: Hook):
        self.__post_cycle_hooks[name] = hook

    def add_pre_frame_hook(self, name: str, hook: Hook):
        self.__pre_frame_hooks[name] = hook

    def add_post_frame_hook(self, name: str, hook: Hook):
        self.__post_frame_hooks[name] = hook

    def remove_init_hook(self, name: str) -> bool:
        if self.__init_hooks[name]:
            del self.__init_hooks[name]
            return True
        return False

    def remove_pre_cycle_hook(self, name: str) -> bool:
        if self.__pre_cycle_hooks[name]:
            del self.__pre_cycle_hooks[name]
            return True
        return False

    def remove_post_cycle_hook(self, name: str) -> bool:
        if self.__post_cycle_hooks[name]:
            del self.__post_cycle_hooks[name]
            return True
        return False

    # Controls

    def load_rom(self, path: str) -> bytearray:
        with open(path, "rb") as f:
            rom = bytearray(512)
            byte = f.read(1)
            i = 0
            while byte != b'':
                rom[i] = byte[0]
                byte = f.read(1)
                i += 1

        self.CPU.load_rom(rom)
        return rom

    def step(self):
        if not self.__started:
            self.__start()

        if self.CPU.draw_flag:
            self.__call_pre_frame_hooks()
            if self.__frame_limit:
                self.__start_cycle_timer()

                self.__call_graphics()

        self.__call_presses()
        self.__call_sound()

        self.__call_pre_hooks()
        self.CPU.gamestep()
        self.__call_post_hooks()

        if self.CPU.draw_flag:
            self.__call_post_frame_hooks()
            if self.__frame_limit:
                self.__wait_for_timer()

    def start(self):
        if not self.__started:
            self.__start()

        self.__looping = True
        while self.__looping:
            self.step()

    def stop_looping(self):
        self.__looping = False

    def next_frame(self):
        while not self.CPU.draw_flag:
            self.step()
        self.step()

    def set_frame_limit(self, val: bool):
        self.__frame_limit = val
