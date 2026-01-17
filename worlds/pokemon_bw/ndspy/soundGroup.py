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
Support for sound groups within SDATs.
"""


import enum


class GroupEntryType(enum.IntEnum):
    """
    An enumeration that distinguishes between the types of files that
    a group entry can refer to.
    """
    SSEQ = 0
    SBNK = 1
    SWAR = 2
    SSAR = 3


class SWARLoadMethod(enum.IntEnum):
    """
    An enumeration that distinguishes between the ways in which a *SWAR*
    can be loaded.
    """
    FILE_IDS = 0
    SWAR_IDS = 1


class GroupEntry:
    """
    An entry in a sound group.
    """

    # Default options value is "2" to set SWAR load method to SWAR IDs,
    # which is what we want to be the default
    def __init__(self, type=GroupEntryType.SSEQ, options=2, id=0):
        self.type = GroupEntryType(type)
        self.id = id

        # The variable names are based on actual code RE.

        # Note that a SSEQ will pass its "options" value on to the
        # SBNK it loads, and a SBNK will do the same with the SWARs it
        # loads.

        self.loadSSEQ = bool(options & 1)
        self.loadSBNKSWARsFrom = SWARLoadMethod(bool(options & 2))
        self.loadSWAR = bool(options & 4)
        self.loadSSAR = bool(options & 8)


    @classmethod
    def fromFlags(cls, type, id, loadSSEQ=False,
            loadSBNKSWARsFrom=SWARLoadMethod.SWAR_IDS, loadSWAR=False,
            loadSSAR=False):
        """
        Create a sound group entry from individual attribute values.
        """

        self = cls(type, 0, id)

        self.loadSSEQ = loadSSEQ
        self.loadSBNKSWARsFrom = loadSBNKSWARsFrom
        self.loadSWAR = loadSWAR
        self.loadSSAR = loadSSAR

        return self


    def save(self):
        """
        Return this sound group entry's type, options value, and ID as a
        3-tuple. This matches the parameters of the default class
        constructor.
        """

        options = 0
        if self.loadSSEQ: options |= 1
        if self.loadSBNKSWARsFrom == SWARLoadMethod.SWAR_IDS: options |= 2
        if self.loadSWAR: options |= 4
        if self.loadSSAR: options |= 8

        return self.type, options, self.id


    def __str__(self):
        typeName = {
            GroupEntryType.SSEQ: 'sseq',
            GroupEntryType.SBNK: 'sbnk',
            GroupEntryType.SWAR: 'swar',
            GroupEntryType.SSAR: 'ssar',
            }.get(self.type, str(int(self.type)))

        optionsL = []
        if self.loadSSEQ: optionsL.append('load-sseq')
        if self.loadSBNKSWARsFrom:
            method = {
                SWARLoadMethod.FILE_IDS: 'file-id',
                SWARLoadMethod.SWAR_IDS: 'swar-id',
                }[self.loadSBNKSWARsFrom]
            optionsL.append('load-swars-by-' + method)
        if self.loadSWAR: optionsL.append('load-swar')
        if self.loadSSAR: optionsL.append('load-ssar')
        options = ' '.join(optionsL)

        return f'<group-entry-{typeName} {self.id}{" " if options else ""}{options}>'


    def __repr__(self):
        args = []

        args.append(repr(self.type))
        args.append(repr(self.id))

        if self.loadSSEQ:
            args.append(f'loadSSEQ={self.loadSSEQ!r}')
        if self.loadSBNKSWARsFrom != SWARLoadMethod.SWAR_IDS:
            args.append(f'loadSBNKSWARsFrom={self.loadSBNKSWARsFrom!r}')
        if self.loadSWAR:
            args.append(f'loadSWAR={self.loadSWAR!r}')
        if self.loadSSAR:
            args.append(f'loadSSAR={self.loadSSAR!r}')

        return f'{type(self).__name__}.fromFlags({", ".join(args)})'
