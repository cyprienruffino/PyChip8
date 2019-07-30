def process_line(line) -> int:
    tokens = line.split(";")[0].strip(",").strip("\n").split(" ")

    if tokens[0] == "CLS":
        return 0x00E0

    if tokens[0] == "RET":
        return 0x00EE

    if tokens[0] == "JP":
        if tokens[1] == "V0":
            return 0xB000 + int(tokens[1], base=16)
        else:
            return 0x1000 + int(tokens[1], base=16)

    if tokens[0] == "CALL":
        return 0x2000 + int(tokens[1], base=16)

    if tokens[0] == "SE":
        return 0x5000 + int(tokens[1], base=16) << 8 + int(tokens[2], base=16) << 4

    if tokens[0] == "SEB":
        return 0x3000 + int(tokens[1], base=16) << 8 + int(tokens[2], base=16)



    if tokens[0] == "SNE":
        if len(tokens[2]) == 4:  # SNE Vx kk
            return 0x4000 + int(tokens[1], base=16) << 8 + int(tokens[2], base=16)

        if len(tokens[2]) == 3:  # SNE Vx Vy
            return 0x9000 + int(tokens[1], base=16) << 8 + int(tokens[2], base=16) << 4

    if tokens[0] == "LD":
        if tokens[1] == "I":
            return 0xA000 + int(tokens[2], base=16)
        if tokens[2] == "DT":
            return 0xF007 + int(tokens[1], base=16) << 8
        if tokens[2] == "K":
            return 0xF00A + int(tokens[1], base=16) << 8
        if tokens[1] == "DT":
            return 0xF015 + int(tokens[2], base=16) << 8
        if tokens[1] == "ST":
            return 0xF018 + int(tokens[2], base=16) << 8
        if tokens[1] == "F":
            return 0xF029 + int(tokens[2], base=16) << 8
        if tokens[1] == "[I]":
            return 0xF055 + int(tokens[2], base=16) << 8
        if tokens[2] == "[I]":
            return 0xF065 + int(tokens[1], base=16) << 8

    if tokens[0] == "ADD":
        if tokens[1] == "I":
            return 0xF01E + int(tokens[2], base=16) << 8

        if len(tokens[2]) == 3:  # ADD Vx Vy
            return 0x8004 + int(tokens[1], base=16) << 8 + int(tokens[2], base=16) << 4

    if tokens[0] == "ADDB":
        return 0x7000 + int(tokens[1], base=16) << 8 + int(tokens[2], base=16)

    if tokens[0] == "OR":
        return 0x8001 + int(tokens[1], base=16) << 8 + int(tokens[2], base=16) << 4

    if tokens[0] == "AND":
        return 0x8002 + int(tokens[1], base=16) << 8 + int(tokens[2], base=16) << 4

    if tokens[0] == "XOR":
        return 0x8003 + int(tokens[1], base=16) << 8 + int(tokens[2], base=16) << 4

    if tokens[0] == "SUB":
        return 0x8005 + int(tokens[1], base=16) << 8 + int(tokens[2], base=16) << 4

    if tokens[0] == "SHR":
        return 0x8006 + int(tokens[1], base=16) << 8

    if tokens[0] == "SHL":
        return 0x800E + int(tokens[1], base=16) << 8

    if tokens[0] == "SUBN":
        return 0x8007 + int(tokens[1], base=16) << 8 + int(tokens[2], base=16) << 4

    if tokens[0] == "RND":
        return 0xC000 + int(tokens[1], base=16) << 8 + int(tokens[2], base=16)

    if tokens[0] == "DRW":
        return 0xD000 + int(tokens[1], base=16) << 8 + int(tokens[2], base=16) << 4 + int(tokens[3], base=16)

    if tokens[0] == "SKP":
        return 0xE092 + int(tokens[1], base=16) << 8

    if tokens[0] == "SKNP":
        return 0xE0A1 + int(tokens[1], base=16) << 8


def assemble_program(assembly) -> list:
    opcodes = []
    for line in assembly:
        opcodes.append(process_line(line))
    #opcodes = list(filter(lambda x: x is not None, opcodes))

    bytearr = []
    for i in range(0, len(opcodes), 2):
        bytearr.append((opcodes[i] & 0xFF00) >> 8)
        bytearr.append(opcodes[i] & 0x00FF)

    return bytearr


def assemble_file(code_path, output_file):
    with open(code_path, "r") as f:
        assembly = f.readlines()

    with open(output_file, "wb") as f:
        f.write(bytearray(assemble_program(assembly)))
