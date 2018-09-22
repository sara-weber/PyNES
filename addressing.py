from typing import List, Optional


class AddressingMixin(object):
    data_length = 0

    @property
    def instruction_length(self):
        return self.data_length + 1


class NoAddressingMixin(AddressingMixin):
    """ Instructions that have data passed
        ex: CLD
    """
    data_length = 0


class ImmediateReadAddressingMixin(AddressingMixin):
    """ Takes a value from the instruction data.
        ex: STA #7 => $8D 07
    """
    data_length = 1

    def get_data(self, cpu, memory_address, data_bytes: bytes) -> Optional[int]:
        return data_bytes[0]


class AbsoluteAddressingMixin(AddressingMixin):
    """ Looks up an absolute memory address and returns the value.
        ex: STA $12 34 => $8D 34 12
    """
    data_length = 2

    def get_address(self, data_bytes: bytes) -> Optional[int]:
        return int.from_bytes(data_bytes, byteorder='little')


class AbsoluteAddressingWithXMixin(AddressingMixin):
    """ Looks up an absolute memory address including adding the x reg to that
        address, returns the value at that address.
        ex: STA $12 34 => $8D 34 12
    """
    data_length = 2

    def get_address(self, data_bytes: bytes) -> Optional[int]:
        return int.from_bytes(data_bytes, byteorder='little')
