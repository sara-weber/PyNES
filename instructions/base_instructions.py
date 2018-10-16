from addressing import ImplicitAddressing, RelativeAddressing
from helpers import Numbers
from instructions.generic_instructions import Instruction, WritesToMem, ReadsFromMem
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
        cpu.set_memory(cpu.sp_reg, cpu.pc_reg, num_bytes=Numbers.SHORT.value)

        # increases the size of the stack
        cpu.increase_stack_size(Numbers.SHORT.value)

        # jump to the memory location
        super().write(cpu, memory_address, value)


class Rts(Jmp):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        # decrease the size of the stack
        cpu.decrease_stack_size(Numbers.SHORT.value)

        # pop the pc reg on the stack
        old_pc_reg = cpu.get_memory(cpu.sp_reg, num_bytes=Numbers.SHORT.value)

        # jump to the memory location
        super().write(cpu, old_pc_reg, value)


class BranchClear(RelativeAddressing, Jmp):
    """
    N Z C I D V
    - - - - - -
    """

    @classmethod
    def write(cls, cpu, memory_address, value):
        if not cpu.status_reg.bits[cls.bit]:
            super().write(cpu, memory_address, value)


class BranchSet(RelativeAddressing, Jmp):
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


class Bit(ReadsFromMem, Instruction):
    """
    N Z C I D V
    + x - - - +
    """
    sets_negative_bit = True
    sets_overflow_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        # set the zero flag based on value & a_reg
        cpu.status_reg.bits[Status.StatusTypes.zero] = not bool(value & cpu.a_reg)


class Ld(ReadsFromMem, Instruction):
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


class And(Instruction):
    """
    Pushes data onto stack
    N Z C I D V
    + + - - - -
    """
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        # set the zero flag based on value & a_reg
        cpu.a_reg &= value
        return cpu.a_reg


class StackPush(Instruction):
    """
    Pushes data onto stack
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        # grab the data
        data_to_push = cls.data_to_push(cpu)

        # write the data to the stack
        cpu.set_memory(cpu.sp_reg, data_to_push)

        # increases the size of the stack
        cpu.increase_stack_size(Numbers.BYTE.value)


class StackPull(Instruction):
    """
    Pulls data from the stack
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        # decreases the size of the stack
        cpu.decrease_stack_size(Numbers.BYTE.value)

        # write the status to the stack
        pulled_data = cpu.get_memory(cpu.sp_reg)

        # grab the data to write
        cls.write_pulled_data(cpu, pulled_data)


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
