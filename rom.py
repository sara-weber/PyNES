from typing import List
from memory_owner import MemoryOwnerMixin

KB = 1024


class ROM(MemoryOwnerMixin, object):
    memory_start_location = 0x4020
    memory_end_location = 0xFFFF

    def __init__(self, rom_bytes: bytes):
        self.header_size = 16

        # TODO: Pull this value from rom header
        self.num_prg_blocks = 2

        # Program data starts after head and lasts for a set number of 16 KB blocks
        self.rom_bytes = rom_bytes
        self.prg_bytes = rom_bytes[self.header_size:self.header_size + (16 * KB * self.num_prg_blocks)]

    def get_memory(self) -> List[bytes]:
        return self.rom_bytes

    def get(self, position, size: int=1):
        """ gets bytes at a given position, could be multiple bytes"""
        return self.get_memory()[position:position+size]

    def set(self, position: int, value: bytes):
        """ Read only memory! Return error """
        raise Exception("Trying to write to read only memory!")