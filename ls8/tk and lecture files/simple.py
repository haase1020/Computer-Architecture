# from day1 lecture with Tim


PRINT_TIM = 0b00000001
HALT = 0b10
PRINT_NUM = 0b00000011  # opcode 3
SAVE = 0b100
PRINT_REG = 0b101  # opcode 5


memory = [
    PRINT_TIM,
    PRINT_TIM,
    PRINT_TIM,
    PRINT_NUM,
    42,
    SAVE,
    2,
    99,
    PRINT_REG,
    2,  # register to look at
    HALT,
]

# register aka memory
# registers are R0 through R7
registers = [0] * 8
# [0,0,0,0,0,0,0,0]

pc = 0  # program counter

running = True
while running:
    command = memory[pc]

    if command == PRINT_TIM:
        print("Tim!")

    if command == HALT:
        running = False

    if command == PRINT_NUM:
        num_to_print = memoery[pc + 1]
        print(num_to_print)

        pc += 1
    if command == SAVE:
        reg = pc + 1
        num_to_save = pc + 2
        registers[reg] = num_to_save

        pc += 2

    if command == PRINT_REG:

    pc += 1
