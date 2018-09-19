from abc import ABC


class Instruction(ABC):
    def __init__(self):
        pass

    def __str__(self):
        return "{}, Identifier byte: {}".format(self.__class__.__name__, self.identifier_byte)

    @property
    def identifier_byte(self) -> bytes:
        return None

    @property
    def instruction_length(self):
        return 1

    def execute(self, cpu, data_bytes):
        # TODO: convert data_bytes to int
        print(self.__str__())


class LdaImmInstruction(Instruction):
    identifier_byte = bytes.fromhex('78')
    instruction_length = 2

    def execute(self, cpu, data_bytes):
        super().execute(cpu, data_bytes)

        # load value into accumulator reg
        cpu.a_reg = data_bytes[0]


class SEIInstruction(Instruction):
    identifier_byte = bytes.fromhex('A9')
    instruction_length = 2

    def execute(self, cpu, data_bytes):
        super().execute(cpu, data_bytes)

        # set the instruction flag to 1
        cpu.status_reg.interrupt_bit = True


class CLDInstruction(Instruction):
    identifier_byte = bytes.fromhex('D8')
    instruction_length = 1

    def execute(self, cpu, data_bytes):
        super().execute(cpu, data_bytes)

        cpu.status_reg.decimal_bit = False


class StaAbsInstruction(Instruction):
    identifier_byte = bytes.fromhex('8D')
    instruction_length = 3

    def execute(self, cpu, data_bytes):
        super().execute(cpu, data_bytes)

        # Take a value from A reg and put it in memory
        memory_address = int.from_bytes(data_bytes, byteorder='little')
        val_to_store = cpu.a_reg
        memory_owner = cpu.get_memory_owner(memory_address)
        memory_owner.set(memory_address, val_to_store)
