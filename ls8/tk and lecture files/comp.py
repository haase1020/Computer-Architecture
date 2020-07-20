"""
Computer emulator

software that pretends to be hardware

Turing Complete -- it can solve any problem for which there is an algorithm.
"""

import sys
# memory -- like a big array
# "index into the memory array" == "address" == "pointer"

# memory = [0] * 256    # RAM
PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3  # SAVE_REG R1, 37  register[1] = 37
PRINT_REG = 4  # PRINT_REG R1   print(register[1])
ADD = 5

memory = [
    PRINT_BEEJ,
    PRINT_BEEJ,
    PRINT_BEEJ,
    SAVE_REG,  # SAVE_REG, R1, 37 (3 byte instruction)
    1, # <-- index into the register array
    37, # <-- value that we want to store there
    SAVE_REG,
    2, # <-- index into the register array
    11, # <-- value that we want to store there
    ADD,  # ADD R1, R2 register[1] += register[2]
    1,
    2,
    PRINT_REG,  # PRINT_REG, R1 (2 byte instruction)
    1,
    HALT,
]

# 8 general purpose registers, like variables, R), R!, R2....R7
register = [0] * 8
pc = 0  # Program Counter, index of the current instruction
running = True

while running:
    ir = memory[pc]  # instruction register

    if ir == PRINT_BEEJ:
        print("Beej")
        pc += 1

    elif ir == SAVE_REG:
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        register[reg_num] = value
        pc += 3

    elif ir == PRINT_REG:
        reg_num = memory[pc + 1]
        print(register[reg_num])
        pc += 2

    elif ir == ADD:
        reg_num1 = memory[pc + 1]
        reg_num2 = memory[pc + 2]
        register[reg_num1] += register[reg_num2]
        pc += 3

    elif ir == HALT:
        running = False
        pc += 1
    else:
        print(f"unknown instruction {ir} at address {pc}")
        sys.exit(1)
