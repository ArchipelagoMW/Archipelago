
import struct

from . import Alignment
from . import _common


# NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE
# NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE
# WHEN THIS GETS STABILIZED, DOCUMENT (OR GET RID OF) __init__.Alignment
# NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE
# NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE




class BNBLTouchArea:
    def __init__(self, x=0, y=0, width=0, height=0, alignment=Alignment.TOP|Alignment.LEFT):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.alignment = alignment


    @classmethod
    def fromData(cls, data):
        xPack, yPack, w, h = struct.unpack_from('<HHBB', data)
        x, y, align = _common.unpackAlignmentFromPos(xPack, yPack)
        return cls(x, y, w, h, align)


    def getTopLeft(self):
        return _common.getTopLeftOfAlignedRect(self.x, self.y,
                                               self.width, self.height,
                                               self.alignment)


    def save(self):
        return struct.pack('<HHBB',
            *_common.packAlignmentIntoPos(self.x, self.y, self.alignment),
            self.width, self.height)


    def __str__(self):
        x, y = self.x, self.y
        w, h = self.width, self.height
        alignStr = _common.getAlignmentName(self.alignment)
        return f'<bnbl touch area: {alignStr} at ({x}, {y}), size {w}x{h}>'


    def __repr__(self):
        return (f'{type(self).__name__}({self.x!r}, {self.y!r},'
                f' {self.width!r}, {self.height!r}, {self.alignment!r})')



class BNBL:
    def __init__(self, data=None):
        self.unk04 = 0
        self.touchAreas = []

        if data is not None:
            self._initFromData(data)


    def _initFromData(self, data):
        if data[:4] != b'JNBL':
            raise ValueError('Not a BNBL file.')

        self.unk04, numEntries = struct.unpack_from('<HH', data, 4)

        for i in range(numEntries):
            offs = 8 + i * 6
            self.touchAreas.append(BNBLTouchArea.fromData(data[offs : offs+6]))


    @classmethod
    def fromTouchAreas(cls, touchAreas, unk04=0):
        self = cls()
        self.touchAreas = touchAreas
        self.unk04 = unk04
        return self


    @classmethod
    def fromFile(cls, filePath, *args, **kwargs):
        """
        Load a BNBL from a filesystem file.
        """
        with open(filePath, 'rb') as f:
            return cls(f.read(), *args, **kwargs)


    def save(self):
        data = bytearray()

        data.extend(struct.pack('<4sHH', b'JNBL', self.unk04, len(self.touchAreas)))

        for ta in self.touchAreas:
            data.extend(ta.save())

        return bytes(data)


    def saveToFile(self, filePath):
        """
        Generate file data representing this BNBL, and save it to a
        filesystem file.
        """
        d = self.save()
        with open(filePath, 'wb') as f:
            f.write(d)


    def _draw(self):
        canvas = [' '] * (32 * 12)

        def setAt(x, y, char):
            if x < 0 or y < 0: return
            if x >= 32 or y >= 12: return
            canvas[y * 32 + x] = char

        for i, ta in enumerate(self.touchAreas):
            x, y = ta.getTopLeft()
            left = x // 8
            right = (x + ta.width) // 8
            top = y // 16
            bottom = (y + ta.height) // 16

            setAt(left, top, '.')
            setAt(right, top, '.')
            setAt(left, bottom, "'")
            setAt(right, bottom, "'")

            for j in range(left + 1, right):
                setAt(j, top, '-')
                setAt(j, bottom, '-')
            for j in range(top + 1, bottom):
                setAt(left, j, '|')
                setAt(right, j, '|')

            setAt((left + right) // 2, (top + bottom) // 2, str(i))

        # Join everything and return it
        lines = []
        lines.append('.' + '=' * 34 + '.')
        for i in range(12):
            content = ''.join(canvas[i * 32 : i * 32 + 32])
            lines.append('| ' + content + ' |')
        lines.append("'" + '=' * 34 + "'")
        return lines


    def __str__(self):

        if self.unk04 == 0:
            linesList = ['<bnbl']
        else:
            linesList = [f'<bnbl unk04={self.unk04}']
        linesList.extend(_common.enumeratedListOfStrs(self.touchAreas))


        drawingCol = max(len(s) for s in linesList) + 4

        for i, drawingLine in enumerate(self._draw()):
            if i < len(linesList):
                numSpaces = (drawingCol - len(linesList[i]))
                linesList[i] += ' ' * numSpaces + drawingLine
            else:
                linesList.append(' ' * drawingCol + drawingLine)

        linesList.append('>')
        return '\n'.join(linesList)


    def __repr__(self):
        extra = ''
        if self.unk04 != 0:
            extra = f', {self.unk04!r}'

        return (f'{type(self).__name__}'
                f'.fromTouchAreas({self.touchAreas!r}{extra})')
