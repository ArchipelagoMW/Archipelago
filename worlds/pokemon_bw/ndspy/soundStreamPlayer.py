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
Support for stream players.
"""


class StreamPlayer:
    """
    A stream player.
    """
    def __init__(self, channels=None):
        self.channels = channels if channels is not None else []


    def save(self):
        """
        Return this sequence player's .channels attribute. This matches
        the parameter of the default class constructor.
        """
        return list(self.channels)


    def __str__(self):
        return f'<stream-player {self.channels}>'


    def __repr__(self):
        if self.channels:
            return f'{type(self).__name__}()'
        else:
            return f'{type(self).__name__}({self.channels!r})'
