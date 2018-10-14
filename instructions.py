from addressing import *
from base_instructions import Lda, Sta, SetBit, ClearBit, Ldx, Ldy, Jmp, Stx
from status import Status


    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                               JMP Instructions                                  #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #


class JmpAbs(AbsoluteAddressing, Jmp):
    identifier_byte = bytes([0x4C])


    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                               JMP Instructions                                  #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #


class JsrAbs(AbsoluteAddressing, Jmp):
    identifier_byte = bytes([0x20])


    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                               LDA Instructions                                  #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #


class LdaImm(ImmediateReadAddressing, Lda):
    identifier_byte = bytes([0xA9])


class LdaIndexedIndirect(IndexedIndirectAddressing, Lda):
    identifier_byte = bytes([0xA1])


class LdaZeroPage(ZeroPageAddressing, Lda):
    identifier_byte = bytes([0xA5])


class LdaZeroPageX(ZeroPageAddressingWithX, Lda):
    identifier_byte = bytes([0xB5])


class LdaAbs(AbsoluteAddressing, Lda):
    identifier_byte = bytes([0xAD])


class LdaAbsY(AbsoluteAddressingYOffset, Lda):
    identifier_byte = bytes([0xB9])


class LdaAbsX(AbsoluteAddressingXOffset, Lda):
    identifier_byte = bytes([0xBD])


class LdaIndirectIndexed(IndirectIndexedAddressing, Lda):
    identifier_byte = bytes([0xB6])


    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                               STX Instructions                                  #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # #     # #     # #     # #     # #     # #     # #     # #     # #     # #


class StxZeroPage(ZeroPageAddressing, Stx):
    identifier_byte = bytes([0x86])


class StxZeroPageY(ZeroPageAddressingWithY, Stx):
    identifier_byte = bytes([0x96])


class StxAbs(AbsoluteAddressing, Stx):
    identifier_byte = bytes([0x8E])


# Other Instructions


class LdyImm(ImmediateReadAddressing, Ldy):
    identifier_byte = bytes([0x00])


class LdxImm(ImmediateReadAddressing, Ldx):
    identifier_byte = bytes([0xA2])


class StaAbs(AbsoluteAddressing, Sta):
    identifier_byte = bytes([0x8D])


class Sei(SetBit):
    identifier_byte = bytes([0x78])
    bit = Status.StatusTypes.interrupt


class Cld(ClearBit):
    identifier_byte = bytes([0xD8])
    bit = Status.StatusTypes.decimal
