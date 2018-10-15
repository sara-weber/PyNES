from addressing import ImplicitAddressing
from generic_instructions import Instruction, WritesToMem
import cpu as c
from status import Status


class Jmp(Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.pc_reg = memory_address


class Jsr(Jmp):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        # store the pc reg on the stack
        cpu.set_memory(cpu.sp_reg, cpu.pc_reg, num_bytes=2)

        # increases the size of the stack
        cpu.sp_reg -= 2

        # jump to the memory location
        super().write(cpu, memory_address, value)


class BranchClear(Instruction):
    """
    N Z C I D V
    - - - - - -
    """

    @classmethod
    def write(cls, cpu, memory_address, value):
        if not cpu.status_reg.bits[cls.bit]:
            super().write(cpu, memory_address, value)


class BranchSet(Instruction):
    """
    N Z C I D V
    - - - - - -
    """

    @classmethod
    def write(cls, cpu, memory_address, value):
        if cpu.status_reg.bits[cls.bit]:
            super().write(cpu, memory_address, value)


class Nop(Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    pass


class Ld(Instruction):
    """
    N Z C I D V
    + + - - - -
    """
    sets_zero_bit = True
    sets_negative_bit = True



class Lda(Ld):
    """
    N Z C I D V
    + + - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class Ldx(Ld):
    """
    N Z C I D V
    + + - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = value


class Ldy(Ld):
    """
    N Z C I D V
    + + - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg = value


class Sta(WritesToMem, Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes: bytes):
        return cpu.a_reg


class Stx(WritesToMem, Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes: bytes):
        return cpu.x_reg


class Sty(WritesToMem, Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes: bytes):
        return cpu.y_reg


class SetBit(ImplicitAddressing, Instruction):
    """ Sets a bit to be True
    N Z C I D V
    x x x x x x
    """
    @classmethod
    def apply_side_effects(cls, cpu: 'c.CPU'):
        cpu.status_reg.bits[cls.bit] = True


class ClearBit(ImplicitAddressing, Instruction):
    """ Clears a bit by setting it to be False
    N Z C I D V
    x x x x x x
    """
    @classmethod
    def apply_side_effects(cls, cpu: 'c.CPU'):
        cpu.status_reg.bits[cls.bit] = False
