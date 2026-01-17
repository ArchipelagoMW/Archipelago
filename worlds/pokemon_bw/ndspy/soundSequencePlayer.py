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
Support for sequence players.
"""

class SequencePlayer:
    """
    A sequence player.
    """
    def __init__(self, maxSequences=1, channels=None, heapSize=0):
        self.maxSequences = maxSequences
        self.channels = channels if channels is not None else set()
        self.heapSize = heapSize


    def save(self):
        """
        Return this sequence player's .maxSequences, .channels, and
        .heapSize as a triple. This matches the parameters of the
        default class constructor.
        """
        return (self.maxSequences, self.channels, self.heapSize)


    def __str__(self):
        c = str(sorted(self.channels))
        return f'<sequence-player maxSequences={self.maxSequences} channels={c} heapSize={self.heapSize}>'


    def __repr__(self):
        return f'{type(self).__name__}({self.maxSequences!r}, {self.channels!r}, {self.heapSize!r})'
