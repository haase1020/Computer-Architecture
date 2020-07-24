"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256  # hold 256 bytes of memory 8 bit 2^8 = 256
        self.reg = [0] * 8  # hold 8 general-purpose registers
        self.sp = 7  # stack pointer/ sets to value F4
        self.fl = 0b00000000  # flags register is a special register
        self.reg[self.sp] = 0b11110100  # 0xf4

    def ram_read(self, address):
        # should accept the address to read and return the value stored there.
        return self.ram[address]

    def ram_write(self, value, address):
        # should accept a value to write, and the address to write it to.
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0
        filename = sys.argv[1]

        with open(filename) as f:
            for line in f:
                string_value = line.split("#")[0].strip()
                if string_value == '':
                    continue
                binary_value = int(string_value, 2)
                # print(binary_value)
                self.ram[address] = binary_value
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations. ALU stands for Arithmetic Logic Unit"""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010  # Set the value of a register to an integer.
        PRN = 0b01000111  # Print numeric value stored in the given register.
        HLT = 0b00000001  # Halt the CPU (and exit the emulator).
        ADD = 0b10100000
        MUL = 0b10100010
        PUSH = 0b01000101  # Push the value in the given register on the stack
        # Pop the value at the top of the stack into the given register.
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        CMP = 0b10100111  # compare the values in two registers
        JMP = 0b01010100  # jump to the address stored in the given register
        # if 'equal' flag is set (true), jump to the address stored in given register
        JEQ = 0b01010101
        # if 'E' flag is clear (false, 0) jump to the address stored in the given register
        JNE = 0b01010110

        running = True

        while running:
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == LDI:
                # set value of a register to an integer
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif instruction == PRN:
                # Print numeric value stored in a given register
                # print to the console the demial integer value that is stored in a given register
                print(self.reg[operand_a])
                self.pc += 2

            elif instruction == ADD:
                self.reg[operand_a] += self.reg[operand_b]
                self.pc += 3

            elif instruction == MUL:
                # multiply the values in two registers and the result in register A.
                self.reg[operand_a] *= self.reg[operand_b]
                # result = self.reg[operand_a] * self.reg[operand_b]
                # print("multiply result", result)
                self.pc += 3

            elif instruction == PUSH:
                # push the value in the given register on the stack
                val = self.reg[operand_a]
                # decrement the SP
                self.reg[self.sp] -= 1
                # store value in memory at SP
                self.ram[self.reg[self.sp]] = val
                self.pc += 2

            elif instruction == POP:
                # get the register number
                # get value out of the register
                val = self.ram[self.reg[self.sp]]
                # store value in memeroy at SP
                self.reg[operand_a] = val
                # increment the SP
                self.reg[self.sp] += 1
                self.pc += 2

            elif instruction == CALL:
                # push command after CALL onto the stack
                return_address = self.pc + 2
                # push if on the stack
                # decrement stack pointer
                self.reg[self.sp] -= 1
                top_of_stack_add = self.reg[self.sp]
                # put return address on the stack
                self.ram[top_of_stack_add] = return_address
                # set the PC to the subroutine address
                subroutine_address = self.reg[operand_a]
                self.pc = subroutine_address

            elif instruction == RET:
                # pop the return address off the stack
                top_of_stack_add = self.reg[self.sp]
                print("sp", self.sp)
                print("reg", self.reg)
                print("top of stack add", top_of_stack_add)
                return_address = self.ram[top_of_stack_add]
                self.reg[self.sp] += 1
                # store in the PC
                self.pc = return_address

            elif instruction == CMP:
                if self.reg[operand_a] == self.reg[operand_b]:
                    self.fl = 1
                else:
                    self.fl = 0
                self.pc += 3

            elif instruction == JMP:
                self.pc = self.reg[operand_a]

            elif instruction == JEQ:
                if self.fl == 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            elif instruction == JNE:
                if self.fl == 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            elif instruction == HLT:
                # halt the CPU (and exit the emulator)
                running = False  # get out of while loop

            else:
                print(
                    F" unknown instruction {instruction} at address {self.pc}")
                sys.exit()  # halts the python program wherever it is
