from typing import List
from memory_owner import MemoryOwnerMixin

KB = 1024


class ROM(MemoryOwnerMixin, object):
    # ROM memory is duplicated around 0xC000
    memory_start_location = 0x8000
    memory_end_location = 0xFFFF

    def __init__(self, rom_bytes: bytes):
        self.header_size = 0x10  # 16

        # TODO: Pull this value from rom header
        self.num_prg_blocks = 2

        # Program data starts after head and lasts for a set number of 16 KB blocks
        self.rom_bytes = rom_bytes
        self.prg_bytes = rom_bytes[self.header_size:self.header_size + (16 * KB * self.num_prg_blocks)]

    def get_memory(self) -> List[bytes]:
        return self.prg_bytes

    def get(self, position, size: int = 1):
        """ Gets bytes at a given position, could be multiple bytes. Memory is duplicated around 0xC000"""
        if position >= 0xC000:  # If in the second program ROM, normalize so it's like it's in the first ROM
            position -= 0x4000
        return self.get_memory()[position - self.memory_start_location:position - self.memory_start_location + size]

    def set(self, position: int, value: int):
        raise Exception('Can\'t set read only memory')
