# C8
 CHIP-8 Emulator

The goal here is to create a flexible CHIP-8 emulator with hooks and tools to experiment with emulation and hopefully create a machine learning environment.

It only provides a curses view, I will maybe add a PyGame view.

# Depenencies
- curses


# Usage
$ python main.py path_to_rom

# Keybindings
| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
|1|2|3|C|/|1|2|3|4|
|4|5|6|D|/|a|z|e|r|
|7|8|9|E|/|q|s|d|f|
|A|0|B|F|/|w|x|c|v|

# API
## Under development
The emulator provides an API class that can be used to control the emulation. It provides the following tools:
- API.machine: Direct access to the memory, registers and flags
- API.tools: Provides tools such as a disassembler
- API.hooks: Add and remove hooks
- API.control: Pause, load rom, emulate key press, ...

# Hooks
Hook routines can be added via the hooks API. Currently, hooks are:
- init_hooks: Called at emulator startup
- pre_hooks: Called before each cpu update
- pre_frame_hooks: Called before each frame rendering
- post_hooks: Called after each cpu update
- post_frame_hooks: Called after each frame rendering

# Known issues
- The current display is really ugly
- The curses view screws up the terminal display when killed
- The APIs are under development
- No sound

# ROMs
I don't own any of the provided ROMs, you can find them on 
https://github.com/dmatlack/chip8/tree/master/roms
