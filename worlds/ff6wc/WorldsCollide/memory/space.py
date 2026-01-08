from ..memory.rom import ROM
from ..memory.heap import Heap
from ..memory.label import Label, LabelPointer
from .. import args as args

from enum import IntEnum
BANK_SIZE = 0x10000
Bank = IntEnum("Bank", [(f"{value:X}", (value - 0xc0) * BANK_SIZE) for value in range(0xc0, 0x100)])

START_ADDRESS_SNES = 0xc00000

class Space():
    rom = None
    heaps = { bank : Heap() for bank in Bank }
    spaces = []

    def __init__(self, start_address, end_address, description, clear_value = None):
        self._start_address = start_address
        self._end_address = end_address
        self._next_address = self.start_address
        assert self._start_address <= self._end_address

        # description of what the space contains or is being used for
        self._description = description

        self.instructions = {}
        if clear_value is not None:
            self.clear(clear_value)

        self.labels = {}
        self.label_pointers = []

        # check if space conflicts with any existing spaces
        from bisect import bisect
        dest_index = bisect(self.spaces, self)
        if args.debug:
            if dest_index < len(self.spaces) and self.end_address >= self.spaces[dest_index].start_address:
                message = str(self) + " conflicts with existing spaces:\n"
                while dest_index < len(self.spaces) and self.end_address >= self.spaces[dest_index].start_address:
                    message += str(self.spaces[dest_index]) + "\n"
                    dest_index += 1
                raise RuntimeError(message)
        self.spaces.insert(dest_index, self)

    def __lt__(self, other):
        return self.start_address <= other.end_address # for bisect

    def __len__(self):
        return self.end_address - self.start_address + 1

    @property
    def start_address(self):
        return self._start_address

    @property
    def start_address_snes(self):
        return self.start_address + START_ADDRESS_SNES

    @property
    def next_address(self):
        return self._next_address

    @property
    def next_address_snes(self):
        return self.next_address + START_ADDRESS_SNES

    @property
    def end_address(self):
        return self._end_address

    @property
    def end_address_snes(self):
        return self.end_address + START_ADDRESS_SNES

    @property
    def description(self):
        return self._description

    def write(self, *values):
        from ..ff6wcutils.flatten import flatten
        values = flatten(values)
        values = self._invoke_callables(values)
        values = self._parse_labels(values)

        self._next_address = Space.rom.set_bytes(self.next_address, values)
        if(self.next_address - 1 > self.end_address):
            raise MemoryError(f"Not enough room in space \"{self.description}\": Next (0x{self.next_address -1:x}) > End (0x{self.end_address:x}). Diff: {(self.next_address - 1) - (self.end_address)}")

        self._update_label_pointers()

    def clear(self, value):
        try:
            values = [value] * (len(self) // len(value))
        except:
            values = [value] * len(self)

        values = self._invoke_callables(values)
        assert len(self) == len(values) # do values evenly fill space?

        Space.rom.set_bytes(self.start_address, values)
        self._next_address = self.start_address

    def copy_from(self, start_address, end_address):
        self.write(Space.rom.get_bytes(start_address, end_address - start_address + 1))

    def add_label(self, name, address):
        self.labels[name] = Label(name)
        self.labels[name].address = address

    def label_address(self, name):
        return self._label_pointer(name, LabelPointer.ABSOLUTE)

    def label_address16(self, name):
        return self._label_pointer(name, LabelPointer.ABSOLUTE16)

    def label_address24(self, name):
        return self._label_pointer(name, LabelPointer.ABSOLUTE24)

    def label_distance(self, name):
        return self._label_pointer(name, LabelPointer.RELATIVE)

    def absolute_distance(self, name):
        return self._label_pointer(name, LabelPointer.ABSOLUTE_RELATIVE)

    def branch_distance(self, name):
        return self._label_pointer(name, LabelPointer.BRANCH_RELATIVE)

    def _label_pointer(self, name, mode):
        label_pointer = LabelPointer(Label(name), None, mode)
        self.label_pointers.append(label_pointer)
        return label_pointer # return a new pointer to a new label

    def _invoke_callables(self, values):
        from ..ff6wcutils.flatten import flatten
        result = []
        index = 0
        for value in values:
            if callable(value):
                result.extend(flatten(value(self)))
                self.instructions[self._next_address + index] = value
                index += len(value)
            else:
                result.append(value)
                if not isinstance(value, str):
                    self.instructions.pop(self._next_address + index, None)
                    index += 1
        return result

    def _parse_labels(self, values):
        # find labels (strs) in given values list and update the addresses of the labels and the label pointers
        index = 0
        new_values = []
        for value in values:
            if isinstance(value, str):
                if value in self.labels:
                    raise ValueError(f"Label '{value}' already exists in space '{str(self)}'")

                self.add_label(value, self.next_address + index)
            elif isinstance(value, LabelPointer):
                value.address = self.next_address + index

                if value.mode == LabelPointer.ABSOLUTE24:
                    size = 3
                elif value.mode == LabelPointer.ABSOLUTE16:
                    size = 2
                else:
                    size = 1

                if size > 1:
                    if value.label.name in self.labels:
                        value.label.address = self.labels[value.label.name].address
                        new_values.extend(value.to_bytes(size, "little"))
                    else:
                        new_values.extend([None] * size)  # temp values until label found
                else:
                    new_values.append(value)
                index += size
            else:
                new_values.append(value)
                try:
                    index += len(value)
                except:
                    index += 1
        return new_values

    def _update_label_pointers(self):
        # update allocated labels pointed to found so far
        for label_pointer in self.label_pointers:
            if label_pointer.label.name in self.labels:
                label_pointer.label.address = self.labels[label_pointer.label.name].address

                # overwrite temp values if 16/24 bit labels
                if label_pointer.mode == LabelPointer.ABSOLUTE24:
                    Space.rom.set_bytes(label_pointer.address, label_pointer.to_bytes(3, "little"))
                elif label_pointer.mode == LabelPointer.ABSOLUTE16:
                    Space.rom.set_bytes(label_pointer.address, label_pointer.to_bytes(2, "little"))

    def __str__(self):
        return f"[0x{self.start_address:06x} - 0x{self.end_address:06x}] \"{self.description}\""

    def __repr__(self):
        address_width = 6
        values_per_line = 6

        start_column = address_width + 4 # lines start with 2 spaces, address, and ': '
        values_padding = values_per_line * 5 # each value is 4 hex digits and a space
        address_value_width = start_column + values_padding # length of line up until '|'

        # invert labels to addresses map without removing duplicate addresses (two labels at same address)
        address_label = {}
        for k, v in self.labels.items():
            address_label.setdefault(v.address, []).append(k)

        def get_labels(address, address_label):
            labels = ""
            if address in address_label:
                for label in address_label[address]:
                    labels += f"{label + ':':<{address_value_width}}|\n"
            return labels

        # format instructions/values/labels in space with their address
        index = 0
        result = f"{str(self)}\n"
        while index < len(self):
            address = self.start_address + index
            result += get_labels(address, address_label)

            result += f"  {address:0{address_width}x}: "
            if address in self.instructions:
                instruction = self.instructions[address]
                instruction_values = Space.rom.get_bytes(address, len(instruction))

                value_strings = []
                for value in instruction_values:
                    if isinstance(value, LabelPointer) and value.label.address is None:
                        value_strings.append("????")     # label not found yet
                    else:
                        value_strings.append(f"0x{int(value):02x}")

                lines = []
                for value_index in range(0, len(value_strings), values_per_line):
                    lines.append(' '.join(value_strings[value_index : value_index + values_per_line]))

                lines[0] = f"{lines[0]:<{values_padding}}| {str(instruction)}"
                for line_index in range(1, len(lines)):
                    lines[line_index] = f"{' ' * start_column}{lines[line_index]:<{values_padding}}|"

                result += '\n'.join(lines) + "\n"
                index += len(self.instructions[address])
            else:
                line = f"0x{int(Space.rom.get_byte(address)):02x}"
                result += f"{line:<{values_padding}}|\n"
                index += 1

        # one last check for labels at the end of space (after every address)
        result += get_labels(self.end_address + 1, address_label)

        return result[:-1]

    def print(self):
        print(str(self))

    def printr(self):
        print(repr(self))

def Reserve(start_address, end_address, description, clear_value = None):
    bank_start = (start_address // BANK_SIZE) * BANK_SIZE
    heap = Space.heaps[Bank(bank_start)]
    heap.reserve(start_address, end_address)

    return Space(start_address, end_address, description, clear_value)

def Allocate(bank, size, description, clear_value = None):
    heap = Space.heaps[bank]
    start_address = heap.allocate(size)
    end_address = start_address + size - 1

    return Space(start_address, end_address, description, clear_value)

def Free(start_address, end_address):
    bank_start = (start_address // BANK_SIZE) * BANK_SIZE
    heap = Space.heaps[Bank(bank_start)]
    heap.free(start_address, end_address)

def Write(destination, data, description):
    from ..ff6wcutils.flatten import flatten

    size = 0
    data = flatten(data)
    for value in data:
        if not isinstance(value, str):
            try:
                size += len(value)
            except TypeError:
                size += 1

    if isinstance(destination, Bank):
        space = Allocate(destination, size, description)
    else:
        space = Reserve(destination, destination + size - 1, description)
    space.write(data)
    return space

def Read(start_address, end_address):
    return Space.rom.get_bytes(start_address, end_address - start_address + 1)
