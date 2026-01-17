

import struct

from . import Alignment
from . import _common


# NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE
# NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE
# WHEN THIS GETS STABILIZED, DOCUMENT (OR GET RID OF) __init__.Alignment
# NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE
# NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE



class BNCLImagePosition:
    def __init__(self, x=0, y=0, alignment=Alignment.TOP|Alignment.LEFT, imageID=0):
        self.x = x
        self.y = y
        self.alignment = alignment
        self.imageID = imageID


    @classmethod
    def fromData(cls, data):
        xPack, yPack, imageID = struct.unpack_from('<HHI', data)
        x, y, align = _common.unpackAlignmentFromPos(xPack, yPack)
        return cls(x, y, align, imageID)


    def save(self):
        return struct.pack('<HHI',
            *_common.packAlignmentIntoPos(self.x, self.y, self.alignment),
            self.imageID)


    def __str__(self):
        x, y = self.x, self.y
        id = self.imageID
        alignStr = _common.getAlignmentName(self.alignment)
        return f'<bncl image position: {alignStr} of image {id} at ({x}, {y})>'


    def __repr__(self):
        return (f'{type(self).__name__}({self.x!r}, {self.y!r},'
                f' {self.alignment!r}, {self.imageID!r})')



class BNCL:
    def __init__(self, data=None):
        self.unk04 = 0
        self.imagePositions = []

        if data is not None:
            self._initFromData(data)


    def _initFromData(self, data):
        if data[:4] != b'JNCL':
            raise ValueError('Not a BNCL file.')

        self.unk04, numEntries = struct.unpack_from('<HH', data, 4)

        for i in range(numEntries):
            offs = 8 + i * 8
            self.imagePositions.append(BNCLImagePosition.fromData(data[offs : offs+8]))


    @classmethod
    def fromImagePositions(cls, imagePositions, unk04=0):
        self = cls()
        self.imagePositions = imagePositions
        self.unk04 = unk04
        return self


    @classmethod
    def fromFile(cls, filePath, *args, **kwargs):
        """
        Load a BNCL from a filesystem file.
        """
        with open(filePath, 'rb') as f:
            return cls(f.read(), *args, **kwargs)


    def save(self):
        data = bytearray()

        data.extend(struct.pack('<4sHH', b'JNCL', self.unk04, len(self.imagePositions)))

        for ip in self.imagePositions:
            data.extend(ip.save())

        return bytes(data)


    def saveToFile(self, filePath):
        """
        Generate file data representing this BNCL, and save it to a
        filesystem file.
        """
        d = self.save()
        with open(filePath, 'wb') as f:
            f.write(d)


    def __str__(self):
        if self.unk04 == 0:
            linesList = ['<bncl']
        else:
            linesList = [f'<bncl unk04={self.unk04}']
        linesList.extend(_common.enumeratedListOfStrs(self.imagePositions))
        linesList.append('>')
        return '\n'.join(linesList)


    def __repr__(self):
        extra = ''
        if self.unk04 != 0:
            extra = f', {self.unk04!r}'

        return (f'{type(self).__name__}'
                f'.fromImagePositions({self.imagePositions!r}{extra})')
