from typing import List

KB = 1024


class ROM(object):
    def __init__(self, rom_bytes: bytes):
        self.header_size = 16

        # TODO: Pull this value from rom header
        self.num_prg_blocks = 2

        # Program data starts after head and lasts for a set number of 16 KB blocks
        self.rom_bytes = rom_bytes
        self.prg_bytes = rom_bytes[self.header_size:self.header_size + (16 * KB * self.num_prg_blocks)]

    def get_byte(self, position: int) -> bytes:
        """ gets byte at a given position """
        return self.rom_bytes[position:position+1]