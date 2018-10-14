from addressing import ImplicitAddressing
from generic_instructions import Instruction, WritesToMem
import cpu as c


class Lda(Instruction):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class Ldx(Instruction):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = value


class Ldy(Instruction):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg = value


class Sta(WritesToMem, Instruction):
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes: bytes):
        return cpu.a_reg


class SetBit(ImplicitAddressing, Instruction):
    """ Sets a bit to be True """
    @classmethod
    def apply_side_effects(cls, cpu: 'c.CPU'):
        cpu.status_reg.interrupt_bit = True


class ClearBit(ImplicitAddressing, Instruction):
    """ Clears a bit by setting it to be False """
    @classmethod
    def apply_side_effects(cls, cpu: 'c.CPU'):
        cpu.status_reg.interrupt_bit = False
