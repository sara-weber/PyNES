import numpy as np
from typing import List

import instructions.instructions as i_file
import instructions.jump_instructions as j_file
import instructions.load_instructions as l_file
import instructions.store_instructions as s_file
import instructions.bit_instructions as b_file
import instructions.arithmetic_instructions as a_file
from helpers import Numbers

from instructions.generic_instructions import Instruction
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

        # instruction to execute
        self.instruction = None
        self.data_bytes = None

        # status registers: store a single byte
        self.status_reg = None  # status register

        # counter registers: store a single byte
        self.pc_reg = None  # program counter
        self.sp_reg = None  # stack pointer
        self.stack_offset = 0x100  # stack offset

        # data registers: store a single byte
        self.x_reg = None  # x register
        self.y_reg = None  # y register
        self.a_reg = None  # a register

        # create the instructions that the CPU can interpret
        instructions_list = self._find_instructions(Instruction)
        self.instructions = {}
        for instruction in instructions_list:
            if instruction in self.instructions:
                raise Exception('Duplicate instruction identifier bytes:', instruction.__name__)
            self.instructions[instruction.identifier_byte] = instruction

    def _find_instructions(self, cls):
        """ Finds all available instructions """
        subclasses = [subc for subc in cls.__subclasses__() if subc.identifier_byte is not None]
        return subclasses + [g for s in cls.__subclasses__() for g in self._find_instructions(s)]

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
        self.pc_reg = np.uint16(0)
        self.status_reg = Status()
        self.sp_reg = np.uint16(0xFD)

        self.x_reg = np.uint8(0)
        self.y_reg = np.uint8(0)
        self.a_reg = np.uint8(0)

        # TODO: Implement memory addresses

    def get_memory(self, location: int, num_bytes: int=1) -> int:
        """ Gets a byte from a given memory location
        @param location: the memory location
        @param num_bytes: number of bytes to pull from the memory location
        @return: a byte from a given memory location
        """
        memory_owner = self._get_memory_owner(location)
        return memory_owner.get(location, num_bytes)

    def _get_memory_owner(self, location: int) -> MemoryOwnerMixin:
        """ return the owner of a memory function"""
        for memory_owner in self.memory_owners:
            if memory_owner.memory_start_location <= location <= memory_owner.memory_end_location:
                return memory_owner

        raise Exception('Cannot find memory owner')

    def set_memory(self, location: int, value: int, num_bytes: int=1):
        """ Sets the memory at a location to a value """
        memory_owner = self._get_memory_owner(location)
        memory_owner.set(location, value, num_bytes)

    def set_stack_value(self, value: int, num_bytes: int):
        """ Sets a value on the stack and decrements the stack pointer """
        # store the value on the stack
        self.set_memory(self.stack_offset + self.sp_reg, value, num_bytes=num_bytes)

        # increases the size of the stack
        self.sp_reg -= np.uint8(num_bytes)

    def get_stack_value(self, num_bytes: int):
        """ Sets a value on the stack and decrements the stack pointer """
        # decrease the size of the stack
        self.sp_reg += np.uint8(num_bytes)

        # grab the stored value from the stack
        return self.get_memory(self.stack_offset + self.sp_reg, num_bytes=num_bytes)

    def load_rom(self, rom: ROM):
        # unload old rom
        if self.rom is not None:
            self.memory_owners.remove(self.rom)

        # load rom
        self.rom = rom
        self.pc_reg = np.uint16(0xC000)

        # load the rom program instructions into memory
        self.memory_owners.append(self.rom)

    def identify(self):
        # get current bye at pc
        rom_instruction = True
        identifier_byte = self._get_memory_owner(self.pc_reg).get(self.pc_reg)
        if type(identifier_byte) is not bytes:
            rom_instruction = False
            identifier_byte = bytes([identifier_byte])


        # turn the byte into an Instruction
        self.instruction = self.instructions.get(identifier_byte, None)
        if self.instruction is None:
            raise Exception("Instruction not found: 0x" + identifier_byte.hex())

        # get the data bytes
        if rom_instruction:
            self.data_bytes = self.rom.get(self.pc_reg + np.uint16(1), self.instruction.data_length)
        else:
            if self.instruction.data_length > 0:
                self.data_bytes = bytes([self.get_memory(self.pc_reg + np.uint16(1), self.instruction.data_length)])
            else:
                self.data_bytes = bytes()

        # print out diagnostic information
        print("{0:6}, {1:6}, {2:12}, A:{3:4}, X:{4:4}, Y:{5:4}, P:{6:4}, SP:{7:4}"
              .format(hex(self.pc_reg),
                      (identifier_byte + self.data_bytes).hex(),
                      self.instruction.__name__,
                      hex(self.a_reg),
                      hex(self.x_reg),
                      hex(self.y_reg),
                      hex(self.status_reg.to_int()),
                      hex(self.sp_reg)))

    def execute(self):
        # increment the pc_reg
        self.pc_reg += np.uint16(self.instruction.get_instruction_length())

        # valid instruction
        value = self.instruction.execute(self, self.data_bytes)

        #
        self.status_reg.update(self.instruction, value)
