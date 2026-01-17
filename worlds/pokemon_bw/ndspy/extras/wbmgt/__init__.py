# Copyright 2020 RoadrunnerWMC
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
Support for loading and saving BMG files in the WBGMT text format.
"""

from ... import bmg as ndspy_bmg

from . import _load
from . import _save


# This module is basically just convenience wrapper functions around the
# _load and _save modules, which do the actual work.


def load(data, **kwargs):
    """
    Load wbmgt text data
    """
    bmg = ndspy_bmg.BMG()
    patch(bmg, data, **kwargs)
    return bmg


def loadFromFile(filePath, **kwargs):
    """
    Load wbmgt text data from a filesystem file
    """
    with open(filePath, 'r', encoding='utf-8') as f:
        return load(f.read(), **kwargs)


def patch(bmg, data, **kwargs):
    """
    Load wbmgt text data, and apply it as a patch to a BMG object
    """
    _load.patch(bmg, data, **kwargs)


def patchFromFile(bmg, filePath, **kwargs):
    """
    Load wbmgt text data from a filesystem file, and apply it as a patch
    to a BMG object
    """
    with open(filePath, 'r', encoding='utf-8') as f:
        patch(bmg, f.read(), **kwargs)


def save(bmg):
    """
    Create a wbmgt file string from the provided BMG object
    """
    return _save.save(bmg)


def saveToFile(bmg, filePath):
    """
    Generate wbmgt file data representing the provided BMG, and save it
    to a filesystem file.
    """
    d = save(bmg)
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(d)
