# -*- coding: utf-8 -*-
from enum import Enum


class ScanTypesEnum(Enum):
    """
    Enum with scan types.
    """
    EXACT_VALUE = 0
    NOT_EXACT_VALUE = 1
    BIGGER_THAN = 2
    SMALLER_THAN = 3
    BIGGER_THAN_OR_EXACT_VALUE = 4
    SMALLER_THAN_OR_EXACT_VALUE = 5
    VALUE_BETWEEN = 6
    NOT_VALUE_BETWEEN = 7
