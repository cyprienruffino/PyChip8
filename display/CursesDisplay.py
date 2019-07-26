from .IDisplay import IDisplay

import curses
from typing import List

from numpy.core.multiarray import ndarray

from tools.singleton import singleton

HEIGHT = 32
WIDTH = 64

keymap = {
    38: 0, 195: 1, 34: 2, 39: 3,
    ord("a"): 4, ord("z"): 5, ord("e"): 6, ord("r"): 7,
    ord("q"): 8, ord("s"): 9, ord("d"): 10, ord("f"): 11,
    ord("w"): 12, ord("x"): 13, ord("c"): 14, ord("v"): 15
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
        except Exception as e:
            self.__console.close()
            raise e

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

    def get_keys_released(self) -> set:
        return set(range(16)) - self.get_keys_pressed()
