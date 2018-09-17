from collections import defaultdict

from Instruction import *
from rom import *


class CPU(object):
    def __init__(self):
        # TODO: proper registers
        self.registers = []

        # Program counter will store current execution point
        self.running = True
        self.pc = 16

        self.instructions = [
            SEIInstruction,
            CLDInstruction,
            LDAInstruction,
        ]

        self.instruction_class_mapping = defaultdict()
        for instruction_class in self.instructions:
            self.instruction_class_mapping[instruction_class.identifier_byte] = instruction_class

        self.rom = None

    def run_rom(self, rom: ROM):
        # load rom
        self.rom = rom
        self.pc = self.rom.header_size

        # run program
        while self.running:
            # get current bye at pc
            identifier_byte = self.rom.get_byte(self.pc)

            # turn the byte into an Instruction
            instruction_class = self.instruction_class_mapping.get(identifier_byte, None)
            if instruction_class is None:
                raise Exception("Instruction not found", identifier_byte)

            # Valid instruction
            instruction = instruction_class()
            instruction.execute()

            self.pc += instruction.instruction_length

    def process_instructions(self, instruction: Instruction):
        instruction.execute()
