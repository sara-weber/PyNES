from typing import List

import instructions as instructions_file
from generic_instructions import Instruction
from memory_owner import MemoryOwnerMixin
from ppu import PPU
from ram import RAM
from rom import ROM
from status import Status


class CPU(object):
    def __init__(self, ram: RAM, ppu: PPU):
        self.ram = ram
        self.ppu = ppu
        self.rom = None

        self.memory_owners = [  # type: List[MemoryOwnerMixin]
            self.ram,
            self.ppu
        ]

        # status registers: store a single byte
        self.status_reg = None  # status register

        # counter registers: store a single byte
        self.pc_reg = None  # program counter
        self.sp_reg = None  # stack pointer

        # data registers: store a single byte
        self.x_reg = None  # x register
        self.y_reg = None  # y register
        self.a_reg = None  # a register

        # Program counter will store current execution point
        self.running = True

    def start_up(self):
        """ set the initial values of the registers
            Status (P) = $34
            A, X, Y = 0
            Stack Pointer = $FD
            $4017 = $00 (frame irq enabled)
            $4015 = $00 (all channels enabled)
            $4000-$400F = $00 (disabled)
        """
        # TODO Hex vs Binary
        self.pc_reg = 0
        self.status_reg = Status()
        self.sp_reg = 0xFD

        self.x_reg = 0
        self.y_reg = 0
        self.a_reg = 0

        # TODO: Implement memory addresses

    def get_memory(self, location: int) -> int:
        """ Gets a byte from a given memory location
        @param location: the memory location
        @return: a byte from a given memory location
        """
        memory_owner = self.get_memory_owner(location)
        return memory_owner.get(location)

    def get_memory_owner(self, location: int) -> MemoryOwnerMixin:
        """ return the owner of a memory function"""
        for memory_owner in self.memory_owners:
            if memory_owner.memory_start_location <= location <= memory_owner.memory_end_location:
                return memory_owner

        raise Exception('Cannot find memory owner')

    def find_instructions(self, cls):
        """ Finds all available instructions """
        subclasses = [subc for subc in cls.__subclasses__() if subc.identifier_byte is not None]
        return subclasses + [g for s in cls.__subclasses__() for g in self.find_instructions(s)]

    def run_rom(self, rom: ROM):
        # unload old rom
        if self.rom is not None:
            self.memory_owners.remove(self.rom)

        # load rom
        self.rom = rom
        self.pc_reg = 0xC000

        # load the rom program instructions into memory
        self.memory_owners.append(self.rom)

        # get instructions as a list and convert to dict { byte: class }
        instructions_list = self.find_instructions(Instruction)
        instructions = {}
        for instruction in instructions_list:
            instructions[instruction.identifier_byte] = instruction

        # run program
        while self.running:
            # get current bye at pc
            starting_pc_reg = self.pc_reg
            identifier_byte = self.get_memory_owner(self.pc_reg).get(self.pc_reg)

            # turn the byte into an Instruction
            instruction = instructions.get(identifier_byte, None)
            if instruction is None:
                raise Exception("Instruction not found: 0x" + identifier_byte.hex())

            # get the data bytes
            data_bytes = self.rom.get(self.pc_reg + 1, instruction.data_length)

            # print out diagnostic information
            print("{0:6}, {1:6}, {2:6}, A:{3:4}, X:{4:4}, Y:{5:4}, P:{6:4}, SP:{7:4}".format(hex(self.pc_reg),
                                                                     (identifier_byte + data_bytes).hex(),
                                                                     instruction.__name__,
                                                                     hex(self.a_reg),
                                                                     hex(self.x_reg),
                                                                     hex(self.y_reg),
                                                                     hex(self.status_reg.to_int()),
                                                                     hex(self.sp_reg)))

            # increment the pc_reg
            self.pc_reg += instruction.get_instruction_length()

            # valid instruction
            instruction.execute(self, data_bytes)
