class Label:
    def __init__(self, name):
        self.name = name
        self.address = None

    def __repr__(self):
        return f"{self.name} ({hex(self.address)})"

class LabelPointer:
    ABSOLUTE, ABSOLUTE16, ABSOLUTE24, RELATIVE, ABSOLUTE_RELATIVE, BRANCH_RELATIVE = range(6)

    def __init__(self, label, address, mode):
        self.label = label          # reference to the label pointed to
        self.offset = 0             # offset to apply to label (i.e. pointer arithmetic)
        self.address = address      # address of the pointer itself
        self.mode = mode            # absolute, relative, branch_relative

    def __int__(self):
        value = self.label.address + self.offset
        if self.mode == self.RELATIVE:
            return value - self.address
        elif self.mode == self.ABSOLUTE_RELATIVE:
            return abs(value - self.address)
        elif self.mode == self.BRANCH_RELATIVE:
            value -= self.address
            if value > 127 or value < -128:
                raise ValueError(f"Error on Branch to label {self.label.name}. Branch distance: {value-1}")
            if value > 0:
                return value - 1
            elif value < 0:
                return value + 0xff
        return value

    def to_bytes(self, length, byteorder, *, signed = False):
        return int(self).to_bytes(length, byteorder, signed = signed)

    def __index__(self):
        return int(self)

    def __add__(self, value):
        self.offset += value
        return self

    def __sub__(self, value):
        self.offset -= value
        return self

    # compares the place pointed to
    def __lt__(self, other):
        return int(self) < other

    def __le__(self, other):
        return int(self) <= other

    def __gt__(self, other):
        return int(self) > other

    def __ge__(self, other):
        return int(self) >= other

    def __repr__(self):
        return f"{hex(int(self))}, *{hex(self.address)} = {repr(self.label)} + {hex(self.offset)}"
