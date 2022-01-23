"""
Bedirhan Sarıhan 150119692
Onur Kaya 150119860
Emre Sağıroğlu 150119766
Yasin Alper Bingül 170517033
"""

import typing
def registers_to_binary(*args) -> typing.List:

    registers_binary_values = []

    for register in args:
        register = register_dict[register]
        registers_binary_values.append(register)


    return registers_binary_values

def immediate_to_binary(imm: int) -> str:

    if imm < 0:

        abs_imm = abs(imm)
        binary_value = decimal_to_binary(abs_imm, 6)

        inverted_bin = ["1" if i == "0" else "0" for i in binary_value]
        inverted_bin = "".join(inverted_bin)
        added_one = bin(int(inverted_bin, 2) + int('1', 2))[2:]

    bin_value = decimal_to_binary(imm, 6)

    return bin_value

def addr_to_binary(addr: int, bit: int) ->str:

    if addr < 0:

        abs_addr = abs(addr)
        binary_value = decimal_to_binary(abs_addr, 6)

        inverted_bin = ["1" if i == "0" else "0" for i in binary_value]
        inverted_bin = "".join(inverted_bin)
        added_one = bin(int(inverted_bin, 2) + int('1', 2))[2:]

    bin_value = decimal_to_binary(addr, bit)

    return bin_value

def decimal_to_binary(n, bit) -> str:
    bin_result = ""
    for i in range(bit):
        r = n % 2
        n = n // 2
        bin_result += str(r)

    return bin_result[::-1]

def binary_to_hex(binary_values: typing.List):

    return [hex(int(_bin, 2))[2:].zfill(5).upper() for _bin in binary_values]

def read_file(input_file_name: str):

    with open(input_file_name) as f:
        instructions = [line.strip() for line in f]

    return instructions

def write_file(output_list: typing.List):
    with open('instruction_memory.txt', 'w') as filehandle:
        filehandle.write('v2.0 raw\n')
        filehandle.write('00000\n')
        for hex in output_list:
            filehandle.write('%s\n' % hex)

if __name__ == '__main__':
    opcode_dict= {
        "AND": "0000",
        "OR": "0001",
        "ADD": "0010",
        "LD": "0011",
        "ST": "0100",
        "ANDI": "0101",
        "ORI": "0110",
        "ADDI": "0111",
        "XOR": "1000",
        "XORI": "1001",
        "JUMP": "1010",
        "BEQ": "1011",
        "BGT": "1011",
        "BLT": "1011",
        "BGE": "1011",
        "BLE": "1011"
    }
    register_dict = {
        "R0": "0000",
        "R1": "0001",
        "R2": "0010",
        "R3": "0011",
        "R4": "0100",
        "R5": "0101",
        "R6": "0110",
        "R7": "0111",
        "R8": "1000",
        "R9": "1001",
        "R10": "1010",
        "R11": "1011",
        "R12": "1100",
        "R13": "1101",
        "R14": "1110",
        "R15": "1111"
    }

    nzp_dict = {
        "BEQ": "010",
        "BLT": "001",
        "BGT": "100",
        "BLE": "011",
        "BGE": "110"
    }
    output_binary_result = []

    instructions: typing.List = read_file("input.txt")

    for instruction in instructions:
        binary_value = ""
        # ex. "ADD R5,R0,R2"
        splitted_instruction = instruction.split(' ')   #["ADD", "R5,R0,R2"]
        operation = splitted_instruction[0] # "ADD"

        right_side = splitted_instruction[1] # "R5,R0,R2"
        splitted_right_side = right_side.split(',') #["R5", "R0", "R2"]


        opcode = opcode_dict[operation]
        binary_value += opcode
        if operation in ["AND", "OR","ADD", "XOR"]:
            dest = splitted_right_side[0]
            src1 = splitted_right_side[1]
            src2 = splitted_right_side[2]


            registers = registers_to_binary(dest, src1, src2) # dest, src1, src2
            binary_value += f"{registers[0]}{registers[1]}00{registers[2]}"




        elif operation in ["ANDI", "ORI", "ADDI", "XORI"]:
            dest = splitted_right_side[0]
            src1 = splitted_right_side[1]
            imm = int(splitted_right_side[2])

            registers: typing.List = registers_to_binary(dest, src1)
            immediate: str = immediate_to_binary(imm)

            binary_value += f"{registers[0]}{registers[1]}{immediate}"




        elif operation in ["BEQ", "BGT", "BLT", "BGE", "BLE"]:

            op1 = splitted_right_side[0]
            op2 = splitted_right_side[1]
            addr = int(splitted_right_side[2])
            nzp = nzp_dict[operation]


            registers: typing.List = registers_to_binary(op1, op2)
            address = addr_to_binary(addr, 3)

            msb_addr = address[0]
            addr_without_msb = address[1:]
            binary_value += f"{msb_addr}{nzp}{registers[0]}{addr_without_msb}{registers[1]}"



        elif operation == "LD":
            dest = splitted_right_side[0]
            addr = int(splitted_right_side[1])

            register:typing.List = registers_to_binary(dest)
            address = addr_to_binary(addr, 10)

            binary_value += f"{register[0]}{address}"

        elif operation == "ST":
            src = splitted_right_side[0]
            addr = int(splitted_right_side[1])

            register:typing.List = registers_to_binary(src)
            source = addr_to_binary(addr, 10)

            binary_value += f"{register[0]}{source}"

        elif operation == "JUMP":
            addr = int(splitted_right_side[0])

            address = addr_to_binary(addr,14)
            binary_value += f"{address}"

        output_binary_result.append(binary_value)

    output_hex_result: typing.List = binary_to_hex(output_binary_result)
    write_file(output_hex_result)