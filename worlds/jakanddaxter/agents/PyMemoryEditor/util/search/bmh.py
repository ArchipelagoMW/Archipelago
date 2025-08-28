# -*- coding: utf-8 -*-
from .abstract import AbstractSearchAlgorithm
from typing import Generator, Optional, Sequence, Union


class BMHSearch(AbstractSearchAlgorithm):
    """
    Algorithm Boyer-Moore-Horspool (BMH) for matching pattern in sequences.
    """
    def __init__(self, pattern: Sequence, pattern_length: Optional[int] = None, alphabet_length: int = 256):
        if pattern_length is None:
            pattern_length = len(pattern)

        self.__is_string = isinstance(pattern, str) or (pattern and isinstance(pattern[0], str))

        # Instantiate the parameters.
        self.__pattern = pattern
        self.__pattern_length = pattern_length

        self.__skip = [self.__pattern_length,] * alphabet_length

        for k in range(self.__pattern_length - 1):
            self.__skip[self.__get_value(pattern[k])] = self.__pattern_length - k - 1

    def __get_value(self, element: Union[str, int]) -> int:
        """
        Return the ID of the element, whether element is a string.
        If element is an integer, return itself or (256 + element) whether it is negative.
        """
        if self.__is_string: return ord(element)
        else: return (256 + element) if element < 0 else element

    def search(self, sequence: Sequence, length: Optional[int] = None) -> Generator[int, None, None]:
        """
        Return all the matching position of pattern.
        """
        if length is None:
            length = len(sequence)

        if self.__pattern_length > length:
            return

        k = self.__pattern_length - 1

        while k < length:
            j = self.__pattern_length - 1
            i = k

            while j >= 0 and sequence[i] == self.__pattern[j]:
                j -= 1
                i -= 1

            if j == -1:
                yield i + 1

            k += self.__skip[self.__get_value(sequence[k])]
