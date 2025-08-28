# -*- coding: utf-8 -*-
from .abstract import AbstractSearchAlgorithm
from typing import Generator, Optional, Sequence


class KMPSearch(AbstractSearchAlgorithm):
    """
    Algorithm Knuth-Morris-Pratt (KMP) for matching pattern in sequences.
    """
    def __init__(self, pattern: Sequence, pattern_length: Optional[int] = None):
        if pattern_length is None:
            pattern_length = len(pattern)

        # Instantiate the parameters.
        self.__pattern = pattern
        self.__pattern_length = pattern_length

        self.__lps: list = [0]  # List to save the LPS (longest prefix which is also a suffix).

        # Process the pattern.
        for index in range(1, self.__pattern_length):
            j = self.__lps[index - 1]

            while j > 0 and pattern[j] != pattern[index]:
                j = self.__lps[j - 1]

            self.__lps.append(j + 1 if pattern[j] == pattern[index] else j)

    def search(self, sequence: Sequence, length: Optional[int] = None) -> Generator[int, None, None]:
        """
        Return all the matching position of pattern.
        """
        if length is None:
            length = len(sequence)

        offset = 0

        for index in range(length):
            while offset > 0 and sequence[index] != self.__pattern[offset]:
                offset = self.__lps[offset - 1]

            if sequence[index] == self.__pattern[offset]:
                offset += 1

            if offset == self.__pattern_length:
                yield index - (offset - 1)
                offset = self.__lps[offset - 1]
