from addressing import *
from base_instructions import SetBit, ClearBit, Nop
from status import Status


    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                                 NOP Instructions                                #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #


class NopImp(ImplicitAddressing, Nop):
    identifier_byte = bytes([0xEA])


    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                               Status Instructions                               #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #

# Set

class Sec(SetBit):
    identifier_byte = bytes([0x38])
    bit = Status.StatusTypes.carry


class Sei(SetBit):
    identifier_byte = bytes([0x78])
    bit = Status.StatusTypes.interrupt


class Sed(SetBit):
    identifier_byte = bytes([0xF8])
    bit = Status.StatusTypes.decimal


# Clear

class Cld(ClearBit):
    identifier_byte = bytes([0xD8])
    bit = Status.StatusTypes.decimal


class Clv(ClearBit):
    identifier_byte = bytes([0xB8])
    bit = Status.StatusTypes.overflow


class Clc(ClearBit):
    identifier_byte = bytes([0x18])
    bit = Status.StatusTypes.carry


class Cli(ClearBit):
    identifier_byte = bytes([0x58])
    bit = Status.StatusTypes.interrupt
