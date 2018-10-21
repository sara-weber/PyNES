import re
from typing import List

from cpu import CPU


class NesTestLog:
    def __init__(self, lines: List[str]):
        self.lines = []  # type: List[NesTestLine]
        self.index = 0
        pattern = r'(.{4})\s*(.{8})\s*(.{4})\s*(.{28})\s*A\:(.{2})\sX\:(.{2})\sY\:(.{2})\sP\:(.{2})\sSP\:(.{2})\sCYC\:\s*(\d*)\s'
        compiled = re.compile(pattern)
        for line in lines:
            self.lines.append(NesTestLine(line, compiled))

    def compare(self, cpu: CPU):
        self.lines[self.index].compare(cpu)

        self.index += 1


class NesTestLine:
    """
    PC Bytes Instruction A X Y P SP CYC
    C000  4C F5 C5  JMP $C5F5                       A:00 X:00 Y:00 P:24 SP:FD CYC:  0
    """

    def __init__(self, line: str, compiled_pattern):
        self.line = line

        matches = re.match(compiled_pattern, self.line)

        self.expected_pc_reg = int(matches.group(1), 16)
        expected_data = matches.group(2)[3:].strip()
        if expected_data:
            self.expected_bytes = bytes((int(x, 16) for x in expected_data.split(' ')))
        else:
            self.expected_bytes = bytes()
        self.expected_instruction = matches.group(3).strip()
        self.expected_data = matches.group(4).strip()

        self.expected_a = int(matches.group(5), 16)
        self.expected_x = int(matches.group(6), 16)
        self.expected_y = int(matches.group(7), 16)
        self.expected_p = int(matches.group(8), 16)
        self.expected_sp = int(matches.group(9), 16)
        self.expected_cyc = int(matches.group(10))

    def compare(self, cpu: CPU):
        """ Checks a cpu against a log line """
        pc_match = self.expected_pc_reg == cpu.pc_reg
        instruction_match = self.expected_instruction in cpu.instruction.__name__.upper()
        data_bytes_match = self.expected_bytes == cpu.data_bytes
        a_match = self.expected_a == cpu.a_reg
        x_match = self.expected_x == cpu.x_reg
        y_match = self.expected_y == cpu.y_reg
        p_match = self.expected_p == cpu.status_reg.to_int()
        sp_match = self.expected_sp == cpu.sp_reg

        valid = pc_match and instruction_match and data_bytes_match and a_match and x_match and y_match and p_match and sp_match

        if not valid:
            raise Exception('Instruction results not expected\n\n{0:^39}\n'
                            '---------------------------------------\n'
                            '   | Match |   Expected  |   Actual\n'
                            'PC | {1:^5} | {2:^11} | {3:^11}\n'
                            'in | {4:^5} | {5:^11} | {6:^11}\n'
                            'db | {7:^5} | {8:^11} | {9:^11}\n'
                            ' A | {10:^5} | {11:^11} | {12:^11}\n'
                            ' X | {13:^5} | {14:^11} | {15:^11}\n'
                            ' Y | {16:^5} | {17:^11} | {18:^11}\n'
                            ' P | {19:^5} | {20:^11} | {21:^11}\n'
                            'SP | {22:^5} | {23:^11} | {24:^11}\n'.
                            format(cpu.instruction.__name__.upper(), str(bool(pc_match)), hex(self.expected_pc_reg),
                                   hex(cpu.pc_reg), str(bool(instruction_match)), self.expected_instruction,
                                   cpu.instruction.__name__.upper(), str(bool(data_bytes_match)),
                                   str(self.expected_bytes), str(cpu.data_bytes), str(bool(a_match)),
                                   hex(self.expected_a), hex(cpu.a_reg), str(bool(x_match)),
                                   hex(self.expected_x), hex(cpu.x_reg), str(bool(y_match)), hex(self.expected_y),
                                   hex(cpu.y_reg), str(bool(p_match)), bin(self.expected_p),
                                   bin(cpu.status_reg.to_int()), str(bool(sp_match)), hex(self.expected_sp),
                                   hex(cpu.sp_reg),
                                   ))
