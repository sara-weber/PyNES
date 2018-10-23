import re
from enum import Enum
from typing import List

from addressing import ZeroPageAddressing, AbsoluteAddressing, ImpliedAddressing, ImmediateReadAddressing, \
    ZeroPageAddressingWithX, AbsoluteAddressingWithX, AbsoluteAddressingWithY, IndirectAddressingWithX, \
    IndirectAddressingWithY, ZeroPageAddressingWithY, AccumulatorAddressing

class_pattern = r'(\S*)\s*(\w*).{11}(\w*).*'
compiled_class_pattern = re.compile(class_pattern)


class Numbers(Enum):
    BYTE = 1
    SHORT = 2


def int_to_byte(value: int) -> int:
    """ Casts a single int to a byte """
    # TODO: Fix for signed values
    return value % 256


def short_to_bytes(value: int) -> List[int]:
    """ Casts a short to 2 ints """
    upper = int_to_byte(value >> 8)
    lower = int_to_byte(value)
    return [upper, lower]


def bytes_to_short(*, upper: int, lower: int) -> int:
    """ casts 2 ints to a short """
    return (upper << 8) | lower


def description_to_addressing(description: str):
    """ Turns string description into an addressing type"""
    return {
        'immidiate': ImmediateReadAddressing,
        'zeropage': ZeroPageAddressing,
        'zeropage,X': ZeroPageAddressingWithX,
        'zeropage,Y': ZeroPageAddressingWithY,
        'absolute': AbsoluteAddressing,
        'absolute,X': AbsoluteAddressingWithX,
        'absolute,Y': AbsoluteAddressingWithY,
        '(indirect,X)': IndirectAddressingWithX,
        '(indirect),Y': IndirectAddressingWithY,
        'accumulator': AccumulatorAddressing,
        'implied': ImpliedAddressing
    }[description]


def generate_classes_from_string(class_type, class_string: str):
    """ Creates a list of classes from descriptor based on format from
        http://e-tradition.net/bytes/6502/6502_instruction_set.html
    """
    for class_entry in [line.strip() for line in class_string.split('\n') if line != '']:
        matches = compiled_class_pattern.match(class_entry)
        addressing = description_to_addressing(matches.group(1))
        class_name = matches.group(2) + matches.group(1)
        class_name = re.sub('[(),]', '', class_name)
        yield type(class_name, (addressing, class_type,), {'identifier_byte': bytes([int(matches.group(3), 16)])})
