# Copyright 2019 RoadrunnerWMC
#
# This file is part of ndspy.
#
# ndspy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ndspy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ndspy.  If not, see <https://www.gnu.org/licenses/>.
"""
Functions and classes that don't need their own modules.
"""

import enum
from typing import NamedTuple


class Version(NamedTuple):
    major: int
    minor: int
    patch: int

VERSION = Version(4, 2, 0)
try: VERSION.__class__.__name__ = 'ndspy.version'
except: pass


class Processor(enum.IntEnum):
    """
    An enumeration that can be used to distinguish between the Nintendo
    DS's two processors.
    """
    ARM9 = 9
    ARM7 = 7


class WaveType(enum.IntEnum):
    """
    An enumeration that distinguishes between the three types of wave
    data that the Nintendo DS sound hardware understands.
    """
    PCM8 = 0
    PCM16 = 1
    ADPCM = 2


class Alignment:
    """
    An enumeration that defines common alignment types.
    """
    # Based on Qt's Qt::AlignmentFlag enum, which has always been very
    # intuitive to use and I've never had a problem with
    LEFT = 0x01
    RIGHT = 0x02
    H_CENTER = 0x04

    TOP = 0x10
    BOTTOM = 0x20
    V_CENTER = 0x40

    CENTER = H_CENTER | V_CENTER


def indexInNamedList(L, name):
    """
    Find the index of the item with a particular name in a list
    containing name-value pairs.
    """
    for i, (nameN, entry) in enumerate(L):
        if nameN == name:
            return i
    raise KeyError(f'{name} not found in the list...')


def findInNamedList(L, name):
    """
    Find the value of the item with a particular name in a list
    containing name-value pairs.
    """
    return L[indexInNamedList(L, name)][1]


def setInNamedList(L, name, value):
    """
    Find the item with a particular name in a list containing name-value
    pairs, and replace its value with a new one. The previous value is
    discarded.
    """
    # Can't assign to tuples, so we need to make a new one
    L[indexInNamedList(L, name)] = (name, value)
