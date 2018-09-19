from abc import abstractmethod, ABC
from typing import List


class MemoryOwnerMixin(ABC):
    @property
    def memory_start_location(self) -> int:
        """ inclusive """
        pass

    @property
    def memory_end_location(self) -> int:
        """ inclusive """
        pass

    @abstractmethod
    def get_memory(self) -> List[int]:
        pass

    def get(self, position: int) -> int:
        """ gets int at a given position """
        return self.get_memory()[position - self.memory_start_location]

    def set(self, position: int, value: int):
        """ sets int at a given position to value """
        self.get_memory()[position - self.memory_start_location] = value
