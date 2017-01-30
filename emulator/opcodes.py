from emulator.engine import Emulator

def none(e:Emulator):
    pass

def x0000(e:Emulator):
   pass

def x1000(e:Emulator):
    pass

def x2000(e:Emulator):
    e.stack[e.sp] = e.pc
    e.sp+=1
    e.pc = e.opcode & 0x0FFF

def x3000(e:Emulator):
    pass

def x4000(e:Emulator):
    pass

def x5000(e:Emulator):
    pass

def x6000(e:Emulator):
    pass

def x7000(e:Emulator):
    pass

#Binary ops
def x8000(e:Emulator):

    # 8XY0 => VX = VY
    if (e.opcode & 0x000F) == 0x0000:
        e.V[(e.opcode & 0x0F00) >> 8] = e.V[(e.opcode & 0x00F0) >> 4]
        e.pc += 2

    # 8XY1 => VX |= VY
    if (e.opcode & 0x000F) == 0x0001:
        e.V[(e.opcode & 0x0F00) >> 8] |= e.V[(e.opcode & 0x00F0) >> 4]
        e.pc += 2

    # 8XY2 => VX &= VY
    if (e.opcode & 0x000F) == 0x0002:
        e.V[(e.opcode & 0x0F00) >> 8] &= e.V[(e.opcode & 0x00F0) >> 4]
        e.pc += 2

    # 8XY3 => VX ^= VY
    if (e.opcode & 0x000F) == 0x0003:
        e.V[(e.opcode & 0x0F00) >> 8] ^= e.V[(e.opcode & 0x00F0) >> 4]
        e.pc += 2

    # 8XY4 => VX += VY
    if(e.opcode & 0x000F)==0x0004:
        if e.V[(e.opcode & 0x00F0) >> 4] > (0xFF - e.V[(e.opcode & 0x0F00) >> 8]):
            e.V[0xF] = 1
        else:
            e.V[0xF] = 0
        e.V[(e.opcode & 0x0F00) >> 8] += e.V[(e.opcode & 0x00F0) >> 4]
        e.pc += 2

    # 8XY5 => VX -= VY
    if (e.opcode & 0x000F) == 0x0005:
        if e.V[(e.opcode & 0x00F0) >> 4] > (e.V[(e.opcode & 0x0F00) >> 8]):
            e.V[0xF] = 1
        else:
            e.V[0xF] = 0
        e.V[(e.opcode & 0x0F00) >> 8] -= e.V[(e.opcode & 0x00F0) >> 4]
        e.pc += 2

    # 8XY6 => VX >>= 1
    if (e.opcode & 0x000F) == 0x0006:
        e.V[0xF] = e.V[(e.opcode & 0x0F00) >> 8] & 1
        e.V[(e.opcode & 0x0F00) >> 8] >>= 1
        e.pc += 2

    # 8XY7 => VX = VY - VX
    if (e.opcode & 0x000F) == 0x0007:
        if e.V[(e.opcode & 0x00F0) >> 4] < (e.V[(e.opcode & 0x0F00) >> 8]):
            e.V[0xF] = 1
        else:
            e.V[0xF] = 0

        e.V[(e.opcode & 0x0F00) >> 8] >>= 1
        e.pc += 2

    # 8XY7 => VX <<= 1
    if (e.opcode & 0x000F) == 0x000E:
        if e.V[(e.opcode & 0x0F00) >> 8] & 0b10000000 == 0b10000000:
            e.V[0xF] = 1
        e.V[(e.opcode & 0x0F00) >> 8] <<= 1
        e.pc += 2


def x9000(e:Emulator):
    pass

def xA000(e:Emulator):
    pass

def xB000(e:Emulator):
    pass

def xC000(e:Emulator):
    pass

def xD000(e:Emulator):
    pass

def xE000(e:Emulator):
    pass

def xF000(e:Emulator):
    pass


def process_opcode(e: Emulator):
    e.opcode = e.memory[e.pc] << 8 | e.memory[e.pc + 1]

    mswitch = {
        0x0000: x0000, 0x1000: x1000,
        0x2000: x2000, 0x3000: x3000,
        0x4000: x4000, 0x5000: x5000,
        0x6000: x6000, 0x7000: x7000,
        0x8000: x8000, 0x9000: x9000,
        0xA000: xA000, 0xB000: xB000,
        0xC000: xC000, 0xD000: xD000,
        0xE000: xE000, 0xF000: xF000,
    }
    mswitch.get(e.opcode & 0xF000, none)(e)

