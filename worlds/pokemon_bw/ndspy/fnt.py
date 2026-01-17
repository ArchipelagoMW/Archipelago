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
Support for filename tables in ROMs and NARCs.
"""

from __future__ import annotations

import struct
from typing import NoReturn

from . import _common


class Folder:
    """
    A single folder within a filename table, or an entire filename
    table.
    """
    folders: list[tuple[str, Folder]]
    files: list[str]
    firstID: int

    def __init__(
        self,
        folders: list[tuple[str, Folder]] | None = None,
        files: list[str] | None = None,
        firstID: int = 0,
    ):
        if folders is not None:
            self.folders = folders
        else:
            self.folders = []
        if files is not None:
            self.files = files
        else:
            self.files = []
        self.firstID = firstID


    def __iter__(self):
        raise ValueError('Sorry, Folders are not iterable. Maybe you want to iterate over `.files` or `.folders`?')


    def __getitem__(self, key: int | str) -> Folder | str | int | NoReturn:
        """
        Convenience function:
        - for an integer key, calls filenameOf()
        - for a string key:
            - calls idOf() if key refers to a file, or
            - calls subfolder() if key refers to a directory.
        """
        if isinstance(key, int):
            fn = self.filenameOf(key)
            if fn is not None:
                return fn
        elif isinstance(key, str):
            fileID = self.idOf(key)
            if fileID is None:
                sbf = self.subfolder(key)
                if sbf is not None:
                    return sbf
            else:
                return fileID
        else:
            raise TypeError('Folders can only convert between strings'
                            f' and ints, not "{type(key)}".')
        raise KeyError(f'Unknown key: {key}')


    def __contains__(self, key: int | str) -> bool:
        try:
            self.__getitem__(key)
            return True
        except Exception:
            return False


    def idOf(self, path: str) -> int | None:
        """
        Find the file ID for the given filename, or for the given file
        path (using "/" as the separator) relative to this folder.
        """

        def findInFolder(requestedPath: list[str], searchFolder: Folder) -> int | None:
            """
            Attempt to find filename in the given folder.
            pathSoFar is the path up through this point, as a list.
            """
            pathPart = requestedPath[0]
            if len(requestedPath) == 1:
                # It's hopefully a file in this folder.
                if pathPart in searchFolder.files:
                    # Yay!
                    return searchFolder.firstID + searchFolder.files.index(pathPart)
                else:
                    # Not here.
                    return None

            # Hopefully we have the requested subfolder...
            for subfolderName, subfolder in searchFolder.folders:
                if subfolderName == pathPart:
                    # Yup.
                    return findInFolder(requestedPath[1:], subfolder)
            # Welp.
            return None

        pathList = path.split('/')
        while not pathList[-1]: pathList = pathList[:-1]
        while not pathList[0]: pathList = pathList[1:]
        return findInFolder(pathList, self)


    def subfolder(self, path: str) -> Folder | None:
        """
        Find the Folder instance for the given subfolder name, or for
        the given folder path (using "/" as the separator) relative to
        this folder.
        """

        def findInFolder(requestedPath: list[str], searchFolder: Folder) -> Folder | None:
            """
            Attempt to find filename in the given folder.
            pathSoFar is the path up through this point, as a list.
            """
            pathPart = requestedPath[0]
            for subfolderName, subfolder in searchFolder.folders:
                if subfolderName == pathPart:
                    if len(requestedPath) == 1:
                        # Found the actual folder that was requested!
                        return subfolder
                    else:
                        # Search another level down
                        return findInFolder(requestedPath[1:], subfolder)
            # Welp.
            return None

        pathList = path.split('/')
        while not pathList[-1]: pathList = pathList[:-1]
        while not pathList[0]: pathList = pathList[1:]
        return findInFolder(pathList, self)


    def filenameOf(self, id: int) -> str | None:
        """
        Find the filename of the file with the given ID. If it exists
        in a subfolder, the filename will be returned as a path
        separated by "/"s.
        """

        def findInFolder(pathSoFar: list[str], searchFolder: Folder) -> list[str] | None:
            """
            Attempt to find id in the given folder.
            pathSoFar is the path up through this point, as a list.
            """
            # Check if it's in this folder
            firstID = searchFolder.firstID
            if firstID <= id < firstID + len(searchFolder.files):
                # Found it!
                filename = searchFolder.files[id - firstID]
                return [*pathSoFar, filename]

            # Check subfolders
            for subfolderName, subfolder in searchFolder.folders:
                result = findInFolder([*pathSoFar, subfolderName], subfolder)
                if result is not None:
                    # Found it in that folder!
                    return result
                # Otherwise, keep checking other subfolders.

            # Didn't find it.
            return None

        result = findInFolder([], self)
        if result is not None:
            return '/'.join(result)
        else:
            return None


    def _strListUncombined(self,
        indent: int = 0,
        fileList: list[str] | None = None,
    ) -> list[tuple[str, str | None]]:
        """
        Return a list of (line, preview) pairs, where line is a whole
        printout line except for the preview, and preview is the
        preview. This lets _strList pad the previews to all fall in the
        same column.
        """
        L = []
        indentStr = ' ' * (indent + 1)

        # Print filenames first, since those have file IDs less than
        # those of files contained in subfolders

        for i, fileName in enumerate(self.files):

            fid = self.firstID + i

            if fileList is None or fid >= len(fileList):
                preview = None
            else:
                preview = _common.shortBytesRepr(fileList[fid], 0x10)

            L.append((f'{fid:04d}' + indentStr + fileName, preview))

        for folderName, folder in self.folders:
            L.append((f'{folder.firstID:04d}' + indentStr + folderName + '/', None))
            L.extend(folder._strListUncombined(indent + 4, fileList))

        return L


    def _strList(self, indent: int = 0, fileList: list[str] | None = None) -> list[str]:
        """
        Return a list of lines that could be useful for a printout of
        the folder. fileList can be used to add previews of files.

        Even though this is an internal function, other ndspy modules
        (narc, for one) call it directly, so be careful if you change
        it!
        """

        strings = []

        uncombined = self._strListUncombined(indent, fileList)

        if uncombined:
            previewColumn = max(len(entry[0]) for entry in uncombined) + 4
        else:
            previewColumn = 4

        for line, preview in uncombined:
            if preview is not None:
                line += ' ' * (previewColumn - len(line))
                line += preview
            strings.append(line)

        return strings


    def __str__(self):
        return '\n'.join(self._strList())


    def __repr__(self):
        return (f'{type(self).__name__}({self.folders!r}'
                f', {self.files!r}'
                f', {self.firstID!r})')


def load(fnt: bytes) -> Folder:
    """
    Create a Folder from filename table data. This is the inverse of
    save().
    """
    def loadFolder(folderId: int) -> Folder:
        """
        Load the folder with ID `folderId` and return it as a Folder.
        """
        folderObj = Folder()

        # Get the entries table offset and file ID from the top of the
        # fnt file
        off = 8 * (folderId & 0xFFF)
        entriesTableOff, fileID = struct.unpack_from('<IH', fnt, off)
        folderObj.firstID = fileID

        off = entriesTableOff

        # Read file and folder entries from the entries table
        while True:
            control, = struct.unpack_from('B', fnt, off); off += 1
            if control == 0:
                break

            # That first byte is a control byte that includes the length
            # of the upcoming string and if this entry is a folder
            len_, isFolder = control & 0x7F, control & 0x80

            name = fnt[off : off+len_].decode('latin-1'); off += len_

            if isFolder:
                # There's an additional 2-byte value with the subfolder
                # ID. Get that and load the folder
                subFolderID, = struct.unpack_from('<H', fnt, off); off += 2
                folderObj.folders.append((name, loadFolder(subFolderID)))
            else:
                folderObj.files.append(name)

        return folderObj

    # Root folder is always 0xF000
    return loadFolder(0xF000)


def save(root: Folder) -> bytes:
    """
    Generate a bytes object representing this root folder as a filename
    table. This is the inverse of load().
    """

    # folderEntries is a dict of tuples:
    # {
    #     folderID: (initialFileID, parentFolderID, b'file entries data'),
    #     folderID: (initialFileID, parentFolderID, b'file entries data'),
    # }
    # This is an intermediate representation of the filenames data that
    # can be converted to the final binary representation much more
    # easily than the nested lists can.
    folderEntries = {}

    # nextFolderID allows us to assign folder IDs in sequential order.
    # The root folder always has ID 0xF000.
    nextFolderID = 0xF000

    def parseFolder(d: Folder, parentID: int) -> int:
        """
        Parse a Folder and add its entries to folderEntries.
        `parentID` is the ID of the folder containing this one.
        """

        # Grab the next folder ID
        nonlocal nextFolderID
        folderID = nextFolderID
        nextFolderID += 1

        # Create an entries table and add filenames and folders to it
        entriesTable = bytearray()
        for file in d.files:
            # Each file entry is preceded by a 1-byte length value.
            # Top bit must be 0 or else it'll be interpreted as a
            # folder.
            if len(file) > 127:
                raise ValueError(f'Filename "{file}" is {len(file)}'
                    ' characters long (maximum is 127)!')
            entriesTable.append(len(file))
            entriesTable.extend(file.encode('latin-1'))

        for folderName, folder in d.folders:
            # First, parse the subfolder and get its ID, so we can save
            # that to the entries table.
            otherID = parseFolder(folder, folderID)

            # Folder name is preceded by a 1-byte length value, OR'ed
            # with 0x80 to mark it as a folder.
            if len(folderName) > 127:
                raise ValueError(f'Folder name "{folderName}" is'
                    f' {len(folderName)} characters long (maximum is'
                     ' 127)!')
            entriesTable.append(len(folderName) | 0x80)
            entriesTable.extend(folderName.encode('latin-1'))

            # And the ID of the subfolder goes after its name, as a
            # 2-byte value.
            entriesTable.extend(struct.pack('<H', otherID))

        # And the entries table needs to end with a null byte to mark
        # its end.
        entriesTable.extend(b'\0')

        folderEntries[folderID] = (d.firstID, parentID, entriesTable)
        return folderID

    # The root folder's parent's ID is the total number of folders.
    def countFoldersIn(folder: Folder) -> int:
        folderCount = 0
        for _, f in folder.folders:
            folderCount += countFoldersIn(f)
        return folderCount + 1
    rootParentId = countFoldersIn(root)

    # Ensure that the root folder has the proper folder ID.
    rootId = parseFolder(root, rootParentId)
    assert rootId == 0xF000, f'Root FNT folder has incorrect root folder ID: {hex(rootId)}'

    # Allocate space for the folders table at the beginning of the file
    fnt = bytearray(len(folderEntries) * 8)

    # We need to iterate over the folders in order of increasing ID.
    for currentFolderID in sorted(folderEntries.keys()):
        fileID, parentID, entriesTable = folderEntries[currentFolderID]

        # Add the folder entries to the folder table
        offsetInFolderTable = 8 * (currentFolderID & 0xFFF)
        struct.pack_into('<IHH', fnt, offsetInFolderTable,
            len(fnt), fileID, parentID)

        # And tack the folder's entries table onto the end of the file
        fnt.extend(entriesTable)

    return fnt
