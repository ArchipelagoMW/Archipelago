from abc import ABC, abstractmethod
from typing import Generator, Optional, Sequence


class AbstractSearchAlgorithm(ABC):
    @abstractmethod
    def __init__(self, pattern: Sequence, pattern_length: Optional[int] = None):
        raise NotImplementedError()

    @abstractmethod
    def search(self, sequence: Sequence, length: Optional[int] = None) -> Generator[int, None, None]:
        raise NotImplementedError()
