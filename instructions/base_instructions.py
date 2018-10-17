import numpy as np

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
        cpu.a_reg = np.uint8(value)
        return cpu.a_reg


class Ldx(Ld):
    """
    N Z C I D V
    + + - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = np.uint8(value)
        return cpu.x_reg


class Ldy(Ld):
    """
    N Z C I D V
    + + - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg = np.uint8(value)
        return cpu.y_reg


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


class Or(Instruction):
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
        cpu.a_reg |= value
        return cpu.a_reg


class Eor(Instruction):
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
        cpu.a_reg ^= value
        return cpu.a_reg


class Adc(Instruction):
    """
    A + M + C -> A, C
    N Z C I D V
    + + + - - +
    """
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        # set the zero flag based on value & a_reg
        result = cpu.a_reg + value + int(cpu.status_reg.bits[Status.StatusTypes.carry])
        # if value and a_reg have different signs than result, set overflow
        # i.e. positive + positive != negative
        overflow = bool((cpu.a_reg ^ result) & (value ^ result) & 0x80)
        cpu.status_reg.bits[Status.StatusTypes.overflow] = overflow

        # if greater than 255, carry
        if result >= 256:
            result %= 256
            cpu.status_reg.bits[Status.StatusTypes.carry] = True
        else:
            cpu.status_reg.bits[Status.StatusTypes.carry] = False

        cpu.a_reg = result
        return cpu.a_reg


class Sbc(Adc):
    """
    A - M - C -> A
    N Z C I D V
    + + + - - +
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):  # SBC is the same as the ADC with the bits inverted
        return super().write(cpu, memory_address, value ^ 0xFF)


class Compare(Instruction):
    """ Compare the given value with the accumulator
        N Z C I D V
        + + + - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True
    sets_carry_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        # set the zero flag based on value & a_reg
        cpu.status_reg.bits[Status.StatusTypes.carry] = not bool(value & 256)  # value - cpu.a_reg <= 0
        return value


class Cmp(Compare):
    """ Compare the given value with the accumulator
        N Z C I D V
        + + + - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True
    sets_carry_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        # set the zero flag based on value & a_reg
        result = cpu.a_reg - value
        return super().write(cpu, memory_address, result)


class Cpx(Compare):
    """ Compare the given value with the X reg
        N Z C I D V
        + + + - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True
    sets_carry_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        # set the zero flag based on value & a_reg
        result = cpu.x_reg - value
        return super().write(cpu, memory_address, result)


class Cpy(Compare):
    """ Compare the given value with the Y reg
        N Z C I D V
        + + + - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True
    sets_carry_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        # set the zero flag based on value & a_reg
        result = cpu.y_reg - value
        return super().write(cpu, memory_address, result)




class StackPush(Instruction):
    """
    Pushes data onto stack
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        # grab the data
        data_to_push = cls.data_to_push(cpu)

        # write the data to the stack
        cpu.set_memory(cpu.sp_reg, data_to_push)

        # increases the size of the stack
        cpu.increase_stack_size(Numbers.BYTE.value)

        return data_to_push


class StackPull(Instruction):
    """
    Pulls data from the stack
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        # decreases the size of the stack
        cpu.decrease_stack_size(Numbers.BYTE.value)

        # write the status to the stack
        pulled_data = cpu.get_memory(cpu.sp_reg)

        # grab the data to write
        return cls.write_pulled_data(cpu, pulled_data)


class RegisterModifier(Instruction):
    """
    N Z C I D V
    + + - - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True


class Tax(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0xAA])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = cpu.a_reg
        return cpu.x_reg


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
