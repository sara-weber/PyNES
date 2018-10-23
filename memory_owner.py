from abc import abstractmethod, ABC
from typing import List

from helpers import short_to_bytes, Numbers, bytes_to_short


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

    def get(self, position: int, size: int=1):
        """ gets int at a given position """
        if size == Numbers.BYTE.value:
            return self.get_memory()[position - self.memory_start_location]
        elif size == Numbers.SHORT.value:
            upper = self.get_memory()[position - self.memory_start_location]
            lower = self.get_memory()[position - self.memory_start_location - 1]
            return bytes_to_short(upper=upper, lower=lower)
        else:
            raise Exception('Unknown number size')



    def set(self, position: int, value: int, size: int = 2):
        """ sets int at a given position to value """
        if size == Numbers.BYTE.value:
            self.get_memory()[position - self.memory_start_location] = value
        elif size == Numbers.SHORT.value:
            upper, lower = short_to_bytes(value)
            self.get_memory()[position - self.memory_start_location] = upper
            self.get_memory()[position - self.memory_start_location - 1] = lower
