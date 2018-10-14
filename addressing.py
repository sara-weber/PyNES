from typing import Optional
import cpu as c


class Addressing(object):
    data_length = 0

    @classmethod
    def get_instruction_length(cls):
        return cls.data_length + 1

    @classmethod
    def get_offset(cls, cpu):
        return 0


class XRegOffset(object):
    @classmethod
    def get_offset(cls, cpu):
        return cpu.x_reg


class YRegOffset(object):
    @classmethod
    def get_offset(cls, cpu):
        return cpu.y_reg


class ImplicitAddressing(Addressing):
    """ Instructions that have data passed
        ex: CLD
    """
    data_length = 0


class ImmediateReadAddressing(Addressing):
    """ Takes a value from the instruction data.
        ex: STA #7 => $8D 07
    """
    data_length = 1

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes: bytes) -> Optional[int]:
        return data_bytes[0]


class AbsoluteAddressing(Addressing):
    """ Looks up an absolute memory address and returns the value.
        ex: STA $12 34 => $8D 34 12
    """
    data_length = 2

    @classmethod
    def get_address(cls, cpu, data_bytes: bytes) -> Optional[int]:
        return int.from_bytes(data_bytes, byteorder='little') + cls.get_offset(cpu)


class AbsoluteAddressingXOffset(XRegOffset, AbsoluteAddressing):
    """ Adds the X reg offset to an absolute memory location """


class AbsoluteAddressingYOffset(YRegOffset, AbsoluteAddressing):
    """ Adds the Y reg offset to an absolute memory location """


class ZeroPageAddressing(Addressing):
    """ look up an absolute memory address in the first 256 bytes
        ex: STA $12
        memory_address: $12
        Note: can overflow
    """
    data_length = 1

    @classmethod
    def get_address(cls, cpu, data_bytes: bytes) -> Optional[int]:
        address = int.from_bytes(data_bytes, byteorder='little') + cls.get_offset(cpu)
        # Check for overflow
        if address > 255:
            address %= 256  # Mod it if it's too large
        return address


class ZeroPageAddressingWithX(XRegOffset, ZeroPageAddressing):
    """ Adds the X reg offset to an absolute memory address in the first 256 bytes """


class ZeroPageAddressingWithY(YRegOffset, ZeroPageAddressing):
    """ Adds the Y reg offset to an absolute memory address in the first 256 bytes """


class RelativeAddressing(Addressing):
    """ Offset from current PC, can only jump 256 bytes """
    # TODO: Check if signed
    data_length = 1

    @classmethod
    def get_address(cls, cpu, data_bytes: bytes) -> Optional[int]:
        # TODO: Off by one error
        # Get the program counter
        current_address = cpu.pc_reg

        # Offset by the value in the instruction
        return current_address + int.from_bytes(data_bytes, byteorder='little')


class IndirectBase(Addressing):
    @classmethod
    def get_address(cls, cpu: 'c.CPU', data_bytes: bytes):
        # look up the bytes at [base_address, base_address + 1]
        lsb_location = super().get_address(cpu, data_bytes)
        msb_location = lsb_location + 1

        lsb = cpu.get_memory(lsb_location)
        msb = cpu.get_memory(msb_location)

        return int.from_bytes(bytes([lsb, msb]), byteorder='little') + cls.get_offset(cpu)


class IndirectAddressing(IndirectBase, AbsoluteAddressing):
    """ Indirect addressing """


# TODO: Fix bugs with these ⬇⬇⬇

class IndexedIndirectAddressing(IndirectBase, ZeroPageAddressingWithX):
    """ Indexed indirect addressing """


class IndirectIndexedAddressing(IndirectBase, YRegOffset, ZeroPageAddressing):
    """ Take a single byte address, add the X reg, then use that to look up a new address """

