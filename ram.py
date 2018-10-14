from typing import List

from memory_owner import MemoryOwnerMixin

KB = 1024


class RAM(MemoryOwnerMixin, object):
    memory_start_location = 0x0000
    memory_end_location = 0x1FFF

    def __init__(self):
        self.memory = [0 for _ in range(KB * 2)]  # type: List[int]

    def get_memory(self):
        return self.memory

