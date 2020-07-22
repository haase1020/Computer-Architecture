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
PUSH = 6
POP = 7
CALL = 9
RET = 9


memory = [0] * 256

# 8 general purpose registers, like variables, R), R!, R2....R7
register = [0] * 8
# -- load program --
filename = sys.argv[1]
# TODO: error checking on sys.argv

with open(filename) as f:

    # address is a temp variable; a loading construct. will later use pc
    for address, line in enumerate(f):

        line = line.split('#')
        try:
            v = int(line[0], 10)  # 2nd arg is num base
        except ValueError:
            continue

        memory[address] = v


# -- run loop--


pc = 0  # Program Counter, index of the current instruction
SP = 7  # stack pointer
register[SP] = 0xf4   # this is the stack pointer
running = True

while running:
    ir = memory[pc]  # instruction register # pointer in array

    # convert if/ elif statement to branch_table
    # f = branch_table[ir]
    # f()

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

    elif ir == PUSH:  # PUSH R2
        # decrement SP
        register[SP] -= 1
        # get the value we want to store from the register
        reg_num = memory[pc + 1]
        value = register[reg_num]  # <-- this is the value that we want to push
        # figure out where to store it
        top_of_stack_addr = register[SP]
        # store it
        memory[top_of_stack_addr] = value
        pc += 2

    elif ir == POP:
        reg_num = memory[pc + 1]
        register[reg_num] = memory[register[SP]]
        register[SP] += 1
        pc += 2

    elif ir == CALL:
        # takes in register/ calls a subroutine(function) at the address stored in the register
        # total instruction length of call will always be PC + 2
        return_addr = pc + 2
        # push on the stack
        register[SP] -= 1
        memory[register[SP]] = return_addr
        # get the address to call
        reg_num = memory[pc + 1]
        subroutine_addr = register[reg_num]
        # call it
        pc = subroutine_addr

    elif ir == HALT:
        running = False
        pc += 1
    else:
        print(f"unknown instruction {ir} at address {pc}")
        sys.exit(1)
