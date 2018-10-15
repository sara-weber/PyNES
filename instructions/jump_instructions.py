from addressing import AbsoluteAddressing, IndirectAddressing, RelativeAddressing
from instructions.base_instructions import Jmp, Jsr, BranchSet, BranchClear

# #     # #     # #     # #     # #     # #     # #     # #     # #     # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                                 JMP Instructions                                #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #
from status import Status


class JmpAbs(AbsoluteAddressing, Jmp):
    identifier_byte = bytes([0x4C])


class JmpInd(IndirectAddressing, Jmp):
    identifier_byte = bytes([0x6C])


    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                                 JSR Instructions                                #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #


class JsrAbs(AbsoluteAddressing, Jsr):
    identifier_byte = bytes([0x20])


    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                               Branch Instructions                               #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #


# Carry

class Bcs(RelativeAddressing, BranchSet):
    identifier_byte = bytes([0xB0])
    bit = Status.StatusTypes.carry


class Bcc(RelativeAddressing, BranchClear):
    identifier_byte = bytes([0x90])
    bit = Status.StatusTypes.carry


# Negative

class Bpl(RelativeAddressing, BranchClear):
    identifier_byte = bytes([0x10])
    bit = Status.StatusTypes.negative


class Bmi(RelativeAddressing, BranchSet):
    identifier_byte = bytes([0x30])
    bit = Status.StatusTypes.negative


# Overflow

class Bvc(RelativeAddressing, BranchClear):
    identifier_byte = bytes([0x50])
    bit = Status.StatusTypes.overflow


class Bvs(RelativeAddressing, BranchSet):
    identifier_byte = bytes([0x70])
    bit = Status.StatusTypes.overflow


# Zero

class Bne(RelativeAddressing, BranchClear):
    identifier_byte = bytes([0xD0])
    bit = Status.StatusTypes.zero


class Beq(RelativeAddressing, BranchSet):
    identifier_byte = bytes([0xF0])
    bit = Status.StatusTypes.zero
