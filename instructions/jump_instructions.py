from addressing import AbsoluteAddressing, IndirectAddressing, RelativeAddressing, ImplicitAddressing
from instructions.base_instructions import Jmp, Jsr, BranchSet, BranchClear, Rts, Rti, Brk

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
#                                 RTS Instructions                                #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #


class RtsImp(ImplicitAddressing, Rts):
    identifier_byte = bytes([0x60])


    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                                 RTI Instructions                                #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #


class RtiImp(ImplicitAddressing, Rti):
    identifier_byte = bytes([0x40])


    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                                 BRK Instructions                                #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #


class BrkImp(ImplicitAddressing, Brk):
    identifier_byte = bytes([0x00])


    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                               Branch Instructions                               #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #


# Carry

class Bcs(BranchSet):
    identifier_byte = bytes([0xB0])
    bit = Status.StatusTypes.carry


class Bcc(BranchClear):
    identifier_byte = bytes([0x90])
    bit = Status.StatusTypes.carry


# Negative

class Bpl(BranchClear):
    identifier_byte = bytes([0x10])
    bit = Status.StatusTypes.negative


class Bmi(BranchSet):
    identifier_byte = bytes([0x30])
    bit = Status.StatusTypes.negative


# Overflow

class Bvc(BranchClear):
    identifier_byte = bytes([0x50])
    bit = Status.StatusTypes.overflow


class Bvs(BranchSet):
    identifier_byte = bytes([0x70])
    bit = Status.StatusTypes.overflow


# Zero

class Bne(BranchClear):
    identifier_byte = bytes([0xD0])
    bit = Status.StatusTypes.zero


class Beq(BranchSet):
    identifier_byte = bytes([0xF0])
    bit = Status.StatusTypes.zero
