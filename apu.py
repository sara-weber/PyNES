from typing import List

from memory_owner import MemoryOwnerMixin


class APU(MemoryOwnerMixin, object):
    memory_start_location = 0x4000
    memory_end_location = 0x4015

    def __init__(self):
        self.memory = [0 for _ in range(0x20)]  # type: List[int]

    def get_memory(self) -> List[int]:
        return self.memory