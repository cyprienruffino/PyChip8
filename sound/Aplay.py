import os

from sound.ISound import ISound

path = os.path.join("resources", "beep.wav")


class Aplay(ISound):
    def __init__(self):
        pass

    def beep(self) -> None:
        os.system("aplay " + path + "> /dev/null 2> /dev/null")
