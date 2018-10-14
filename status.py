from enum import Enum


class Status:
    """
    7  bit  0
    ---- ----
    NVss DIZC
    |||| ||||
    |||| |||+- Carry: 1 if last addition or shift resulted in a carry, or if
    |||| |||     last subtraction resulted in no borrow
    |||| ||+-- Zero: 1 if last operation resulted in a 0 value
    |||| |+--- Interrupt: Interrupt inhibit
    |||| |       (0: /IRQ and /NMI get through; 1: only /NMI gets through)
    |||| +---- Decimal: 1 to make ADC and SBC use binary-coded decimal arithmetic
    ||||         (ignored on second-source 6502 like that in the NES)
    ||++------ s: No effect, used by the stack copy, see note below
    |+-------- Overflow: 1 if last ADC or SBC resulted in signed overflow,
    |            or D6 from last BIT
    +--------- Negative: Set to bit 7 of the last operation
    """

    class StatusTypes(Enum):
        carry = 0
        zero = 1
        interrupt = 2
        decimal = 3
        unused1 = 4
        unused2 = 5
        overflow = 6
        negative = 7

    def __init__(self):
        self.bits = {
            Status.StatusTypes.carry: False,
            Status.StatusTypes.zero: False,
            Status.StatusTypes.interrupt: True,
            Status.StatusTypes.decimal: False,
            Status.StatusTypes.unused1: False,
            Status.StatusTypes.unused2: False,
            Status.StatusTypes.overflow: False,
            Status.StatusTypes.negative: False
        }
        self.negative_bit = False  # type: bool
        self.overflow_bit = False  # type: bool
        self.decimal_bit = False  # type: bool
        self.interrupt_bit = True  # type: bool
        self.zero_bit = False  # type: bool
        self.carry_bit = False  # type: bool

    def is_interrupt(self):
        return not bool((self.reg[0] >> 2) & 1)

    def set_interruptable(self, interruptable: bool):
        if interruptable:
            # set the second bit to 0
            self.reg &= 251
        else:
            # set the second bit to 1
            self.reg |= 4
