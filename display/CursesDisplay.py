from .IDisplay import IDisplay

import curses
from typing import List

from numpy.core.multiarray import ndarray

from tools.singleton import singleton

HEIGHT = 32
WIDTH = 64

keymap = {
    38:       0x1, 195:      0x2,      34:  0x3,   39:     0xC,
    ord("a"): 0x4, ord("z"): 0x5, ord("e"): 0x6, ord("r"): 0xD,
    ord("q"): 0x7, ord("s"): 0x8, ord("d"): 0x9, ord("f"): 0xE,
ord("w"): 0xA, ord("x"): 0x0, ord("c"): 0xB, ord("v"): 0xF
}


@singleton
class Console:
    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.nodelay(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.clear()

    def close(self):
        """
        Returns to the normal console state
        """
        self.stdscr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def render(self, chars: list):
        """
        Render a frame
        :param chars: The characters map
        """
        # self.stdscr.clear()
        for line in range(HEIGHT):
            for char in range(WIDTH*2):
                self.stdscr.addch(line, char, ord(chars[line][char]))
        self.stdscr.refresh()


class CursesDisplay(IDisplay):
    def __init__(self):
        self.__console = Console()

    def draw(self, display: bytearray) -> None:
        screen = []
        line = ""
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if display[x + 64 * y]:
                    line += '##'
                else:
                    line += "  "
            screen.append(line)
            line = ""
        try:
            self.__console.render(screen)
        except Exception:
            self.__console.close()
            print("Display is too small, minimum size: 128*32")
            exit(0)

    def get_keys_pressed(self) -> set:
        keys = set()
        c = self.__console.stdscr.getch()
        while c != -1:
            try:
                keys.add(keymap[c])
            except KeyError:
                pass
            finally:
                c = self.__console.stdscr.getch()

        return keys
