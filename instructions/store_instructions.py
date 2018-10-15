from addressing import AbsoluteAddressing, ZeroPageAddressing, ZeroPageAddressingWithY, ZeroPageAddressingWithX, \
    AbsoluteAddressingWithX, AbsoluteAddressingWithY, IndexedIndirectAddressing, IndirectIndexedAddressing
from instructions.base_instructions import Sta, Stx, Sty


    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                                 STA Instructions                                #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #


class StaZpg(ZeroPageAddressing, Sta):
    identifier_byte = bytes([0x85])


class StaZpgX(ZeroPageAddressingWithX, Sta):
    identifier_byte = bytes([0x95])


class StaAbs(AbsoluteAddressing, Sta):
    identifier_byte = bytes([0x8D])


class StaAbsWithX(AbsoluteAddressingWithX, Sta):
    identifier_byte = bytes([0x9D])


class StaAbsWithY(AbsoluteAddressingWithY, Sta):
    identifier_byte = bytes([0x99])


class StaIndX(IndexedIndirectAddressing, Sta):
    identifier_byte = bytes([0x81])


class StaIndY(IndirectIndexedAddressing, Sta):
    identifier_byte = bytes([0x91])


    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                                 STX Instructions                                #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #


class StxZpg(ZeroPageAddressing, Stx):
    identifier_byte = bytes([0x86])


class StxZpgY(ZeroPageAddressingWithY, Stx):
    identifier_byte = bytes([0x96])


class StxAbs(AbsoluteAddressing, Stx):
    identifier_byte = bytes([0x8E])


    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                                 STY Instructions                                #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #


class StyZpg(ZeroPageAddressing, Sty):
    identifier_byte = bytes([0x84])


class StyZpgX(ZeroPageAddressingWithX, Sty):
    identifier_byte = bytes([0x94])


class StyAbs(AbsoluteAddressing, Sty):
    identifier_byte = bytes([0x8C])
