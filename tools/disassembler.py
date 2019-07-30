#
# Emulator engine main class
#
def dhex(number: int) -> str:
    return "0x{:04x}".format(number)


def x0000(opcode):
    # Clear screen
    if opcode == 0x00E0:
        return "CLS"

    # Return
    if opcode == 0x00EE:
        return "RET"


# 1XXX => Jump(XXX)
def x1000(opcode):
    return "JP " + dhex(opcode & 0x0FFF)


# 2XXX => Call(XXX)
def x2000(opcode):
    return "CALL " + dhex(opcode & 0x0FFF)


# 3XKK => skip_next(VX == KK)
def x3000(opcode):
    return "SEB " + dhex((opcode & 0x0F00) >> 8) + " " + dhex(opcode & 0x00FF)


# 4XKK => skip_next(VX != KK)
def x4000(opcode):
    return "SNE " + dhex((opcode & 0x0F00) >> 8) + " " + dhex(opcode & 0x00FF)


# 5XY0 => skip_next(VX ==Y)
def x5000(opcode):
    return "SE" + dhex((opcode & 0x0F00) >> 8) + " " + dhex((opcode & 0x00F0) >> 4)


# 6XKK =>X = KK
def x6000(opcode):
    return "LD " + dhex((opcode & 0x0F00) >> 8) + " " + dhex(opcode & 0x00FF)


# 7XKK =>X += KK
def x7000(opcode):
    return "ADDB " + dhex((opcode & 0x0F00) >> 8) + " " + dhex(opcode & 0x00FF)


# Binary ops
def x8000(opcode):
    # 8XY0 =>X =Y
    if (opcode & 0x000F) == 0x0000:
        return "LD " + dhex((opcode & 0x0F00) >> 8) + " " + dhex((opcode & 0x00F0) >> 4)

    # 8XY1 =>X |=Y
    if (opcode & 0x000F) == 0x0001:
        return "OR " + dhex((opcode & 0x0F00) >> 8) + " " + dhex((opcode & 0x00F0) >> 4)

    # 8XY2 =>X &=Y
    if (opcode & 0x000F) == 0x0002:
        return "AND " + dhex((opcode & 0x0F00) >> 8) + " " + dhex((opcode & 0x00F0) >> 4)

    # 8XY3 =>X ^=Y
    if (opcode & 0x000F) == 0x0003:
        return "XOR " + dhex((opcode & 0x0F00) >> 8) + " " + dhex((opcode & 0x00F0) >> 4)

    # 8XY4 =>X +=Y
    if (opcode & 0x000F) == 0x0004:
        return "ADD " + dhex((opcode & 0x0F00) >> 8) + " " + dhex((opcode & 0x00F0) >> 4)

    # 8XY5 =>X -=Y
    if (opcode & 0x000F) == 0x0005:
        return "SUB " + dhex((opcode & 0x0F00) >> 8) + " " + dhex((opcode & 0x00F0) >> 4)

    # 8XY6 =>X >>= 1
    if (opcode & 0x000F) == 0x0006:
        return "SHR " + dhex((opcode & 0x0F00) >> 8) + " " + dhex((opcode & 0x00F0) >> 4)

    # 8XY7 =>X =Y -X
    if (opcode & 0x000F) == 0x0007:
        return "SUBN " + dhex((opcode & 0x0F00) >> 8) + " " + dhex((opcode & 0x00F0) >> 4)

    # 8XYE =>X <<= 1
    if (opcode & 0x000F) == 0x000E:
        return "SHL " + dhex((opcode & 0x0F00) >> 8) + " " + dhex((opcode & 0x00F0) >> 4)


# 9XY0 => skip_next(VX!=VY)
def x9000(opcode):
    return "SNE " + dhex((opcode & 0x0F00) >> 8) + " " + dhex((opcode & 0x00F0) >> 4)


# AKKK => I=KKK
def xA000(opcode):
    return "LD I " + dhex(opcode & 0x0FFF)


# BKKK => Jump(V0+KKK)
def xB000(opcode):
    return "JP V0 " + dhex(opcode & 0x0FFF)


# CXKK =>X=Rand(V0,255)+KK
def xC000(opcode):
    return "RND " + dhex((opcode & 0x0F00) >> 8) + " " + dhex(opcode & 0x00FF)


# DXYN = draw(VX,VY,N)
def xD000(opcode):
    return "DRW " + dhex((opcode & 0x0F00) >> 8) + " " + dhex((opcode & 0x00F0) >> 4) + " " + dhex((opcode & 0x000F))


def xE000(opcode):
    # EX9E = skip(if_pressed(VX))
    if opcode & 0x00FF == 0x009E:
        return "SKP " + dhex((opcode & 0x0F00) >> 8)

    # EXA1 = skip(if_not_pressed(VX))
    if opcode & 0x00FF == 0x00A1:
        return "SKNP " + dhex((opcode & 0x0F00) >> 8)


def xF000(opcode):
    # FX07 =>X = get_delay()
    if (opcode & 0x00FF) == 0x0007:
        return "LD " + dhex((opcode & 0x0F00) >> 8) + " DT"

    # FX0A =>X = get_key() (Blocking!)
    if (opcode & 0x00FF) == 0x000A:
        return "LD " + dhex((opcode & 0x0F00) >> 8) + ", K"

    # FX15 => set_delay(VX)
    if (opcode & 0x00FF) == 0x0015:
        return "LD DT " + dhex((opcode & 0x0F00) >> 8)

    # FX18 =>X = set_sound(VX)
    if (opcode & 0x00FF) == 0x0018:
        return "LD ST " + dhex((opcode & 0x0F00) >> 8)

    # FX1E => I +=X
    if (opcode & 0x00FF) == 0x001E:
        return "ADD I " + dhex((opcode & 0x0F00) >> 8)

    # FX29 => I = get_char_addr[VX]
    if (opcode & 0x00FF) == 0x0029:
        return "LD F " + dhex((opcode & 0x0F00) >> 8)

    # FX33 => memory[I, I+1, I+2] = binary_coded_decimal(VX)
    if (opcode & 0x00FF) == 0x0033:
        return "LD B " + dhex((opcode & 0x0F00) >> 8)

    # FX55 => save(VX, &I)
    if (opcode & 0x00FF) == 0x0055:
        return "LD [I] " + dhex((opcode & 0x0F00) >> 8)

    # FX65 => load(VX, &I)
    if (opcode & 0x00FF) == 0x0065:
        return "LD " + dhex((opcode & 0x0F00) >> 8) + " [I]"


opcode_switch = {
    0x0000: x0000, 0x1000: x1000,
    0x2000: x2000, 0x3000: x3000,
    0x4000: x4000, 0x5000: x5000,
    0x6000: x6000, 0x7000: x7000,
    0x8000: x8000, 0x9000: x9000,
    0xA000: xA000, 0xB000: xB000,
    0xC000: xC000, 0xD000: xD000,
    0xE000: xE000, 0xF000: xF000,
}


def disassemble_rom(rom_path, output_path):
    assembly = ""
    rom = []
    with open(rom_path, "rb") as f:
        byte = f.read(1)
        i = 0
        while byte != b'':
            rom.append(byte[0])
            byte = f.read(1)
            i += 1

    for i in range(0, len(rom), 2):
        opcode = (rom[i] << 8) + rom[i + 1]
        assembly += str(opcode_switch[(opcode & 0xF000)](opcode)) + "\n"

    assembly = assembly.replace("None", "NOP")
    with open(output_path, "w") as f:
        f.write(assembly)


def disassemble_op(opcode) -> str:
    opcode = opcode
    return str(opcode_switch[(opcode & 0xF000)]())
