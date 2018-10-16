from enum import Enum
from typing import List


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
