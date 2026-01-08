from functools import total_ordering

@total_ordering
class DataPointer:
    def __init__(self, address, data_address):
        self.address = address
        self.data_address = data_address

    def __eq__(self, other):
        return ((self.data_address, self.address) == (other.data_address, other.address))

    def __lt__(self, other):
        return ((self.data_address, self.address) < (other.data_address, other.address))

# pointers to data
# number of pointers and pointer addresses do not change, only the data addresses they store change
class DataPointers:
    def __init__(self, rom, start_address, end_address, pointer_size):
        self.rom = rom
        self.start_address = start_address
        self.end_address = end_address
        self.pointer_size = pointer_size
        self.max_address = 2 ** (self.pointer_size * 8) - 1

        self.pointers = []
        pointer_count = self.size() // self.pointer_size
        for index in range(pointer_count):
            pointer_address = self.start_address + index * self.pointer_size

            if self.pointer_size == 4:
                # four byte pointers are stored as pairs of 2 bytes (e.g. 0x12345678 stored as 0x34127856)
                half_pointer_size = self.pointer_size // 2
                data_address_bytes = self.rom.get_bytes(pointer_address, half_pointer_size)
                data_address_high = int.from_bytes(data_address_bytes, byteorder="little")

                data_address_bytes = self.rom.get_bytes(pointer_address + half_pointer_size, half_pointer_size)
                data_address_low = int.from_bytes(data_address_bytes, byteorder="little")

                data_address = (data_address_high << 16) | data_address_low
            else:
                data_address_bytes = self.rom.get_bytes(pointer_address, self.pointer_size)
                data_address = int.from_bytes(data_address_bytes, byteorder="little")

            pointer = DataPointer(pointer_address, data_address)
            self.pointers.append(pointer)

    def size(self):
        # equivalent to len(self) * self.pointer_size
        return self.end_address - self.start_address + 1

    def __len__(self):
        return len(self.pointers)

    def __getitem__(self, index):
        return self.pointers[index].data_address

    def __setitem__(self, index, data_address):
        self.pointers[index].data_address = data_address

    def write(self):
        if self.pointer_size == 4:
            # write out four byte pointers as pairs of 2 bytes (e.g. 0x12345678 as 0x34127856)
            half_pointer_size = self.pointer_size // 2
            for pointer in self.pointers:
                data_address_high = (pointer.data_address >> 16).to_bytes(half_pointer_size, "little")
                data_address_low = (pointer.data_address & 0xffff).to_bytes(half_pointer_size, "little")

                self.rom.set_bytes(pointer.address, data_address_high)
                self.rom.set_bytes(pointer.address + half_pointer_size, data_address_low)
        else:
            for pointer in self.pointers:
                self.rom.set_bytes(pointer.address, pointer.data_address.to_bytes(self.pointer_size, "little"))

class DataElement:
    def __init__(self, data, address):
        self.data = data
        self.address = address

# contiguous bit field
class DataBits:
    def __init__(self, rom, start_address, end_address):
        self.rom = rom
        self.start_address = start_address
        self.end_address = end_address

        self.bytes = self.rom.get_bytes(self.start_address, self.size())

    def size(self):
        return self.end_address - self.start_address + 1

    def set_all(self):
        for byte_index in range(self.size()):
            self.bytes[byte_index] = 0xff

    def clear_all(self):
        for byte_index in range(self.size()):
            self.bytes[byte_index] = 0x00

    def __len__(self):
        return self.size() * 8

    def __getitem__(self, index):
        byte_index = index // 8
        bit_index = index % 8
        return (self.bytes[byte_index] >> bit_index) & 1

    def __setitem__(self, index, value):
        byte_index = index // 8
        bit_index = index % 8
        self.bytes[byte_index] = (self.bytes[byte_index] & ~(1 << bit_index)) | (value << bit_index)

    def __str__(self):
        result = ""
        for byte in self.bytes:
            for bit_index in range(8):
                if (1 << bit_index) & byte:
                    result += "1"
                else:
                    result += "0"
            result += " "
        return result

    def write(self):
        self.rom.set_bytes(self.start_address, self.bytes)

# array of data
# all elements are the same size and the size does not change but the number of elements can change
class DataArray:
    def __init__(self, rom, start_address, end_address, element_size):
        self.rom  = rom
        self.start_address = start_address
        self.end_address = end_address
        self.element_size = element_size

        self.elements = []
        self.element_capacity = self.size() // self.element_size
        for index in range(self.element_capacity):
            data_address = self.start_address + index * self.element_size
            data = self.rom.get_bytes(data_address, self.element_size)

            element = DataElement(data, data_address)
            self.elements.append(element)

    def size(self):
        # equivalent to len(self) * self.element_size
        return self.end_address - self.start_address + 1

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, index):
        return self.elements[index].data

    def __setitem__(self, index, data):
        assert(len(data) == self.element_size)
        self.elements[index].data = data

    def __delitem__(self, index):
        del self.elements[index]
        self.end_address -= self.element_size

    def append(self, data):
        assert(len(data) == self.element_size)
        self.elements.append(DataElement(data, self.end_address))
        self.end_address += self.element_size

    def write(self):
        if len(self) > self.element_capacity:
            raise MemoryError(f"{self.__class__.__name__} write(): Not enough space ({len(self)}/{self.element_capacity} elements)")

        for element in self.elements:
            self.rom.set_bytes(element.address, element.data)

# pointers to arrays of data
# each array pointed to can be zero or more elements long and each element is the same size
# the number of pointers/arrays does not change but the array sizes can change
class DataArrays:
    def __init__(self, rom, pointers_start_address, pointers_end_address, pointer_size, data_start_address, data_end_address, data_element_size):
        self.rom = rom
        self.pointers = DataPointers(rom, pointers_start_address, pointers_end_address, pointer_size)

        self.start_address = data_start_address
        self.end_address = data_end_address
        self.element_size = data_element_size

        self.data_arrays = []
        for index in range(len(self)):
            start_address = self.start_address + self.pointers[index]
            if index < len(self) - 1:
                end_address = self.start_address + self.pointers[index + 1]
            else:
                end_address = self.end_address

            data_array = DataArray(self.rom, start_address, end_address, self.element_size)
            self.data_arrays.append(data_array)

    def size(self):
        return self.end_address - self.start_address + 1

    def __len__(self):
        # equivalent to len(self.data_arrays) after initialization
        return len(self.pointers)

    def __getitem__(self, index):
        return self.data_arrays[index]

    def write(self):
        data_address = self.start_address
        for index in range(len(self)):
            self.pointers[index] = data_address - self.start_address
            for element in self.data_arrays[index].elements:
                self.rom.set_bytes(data_address, element.data)
                data_address += self.element_size

        if data_address > self.end_address:
            raise MemoryError(f"{self.__class__.__name__} write(): Not enough space ({(data_address - self.start_address + 1) // self.element_size - 1}/{len(self)} elements)")

        self.pointers.write()

# pointers to blocks of data
# pointers are all the same size but data blocks can vary in size (or all be the same size)
# the number of pointers/blocks does not change but the sizes of blocks can change
#
# DataList: pointers are in the same order as they blocks they point to
#           each block's index is the same as the index of the pointer pointing to it
#
# DataMap:  pointers are not in the same order as the blocks they point to
#           pointers must be sorted to find the size of each block
#
# DataList:
# pointer index:   0   1   2   3   4
#                ---------------------
#   block index: | 0 | 1 | 2 | 3 | 4 |
#                ---------------------
# pointer 0 points to block 0, pointer 1 points to block 1, pointer 2 points to block 2, ...
# NOTE: DataList can also handle pointers which wrap around (i.e. dialogs)
#       e.g. pointer 0 = 0xfffe (block 0 address = 0x0dfffe), pointer 1 = 0x000c (block 1 address = 0x0e000c)
#
# DataMap:
# pointer index:   0   1   2   3   4
#                ---------------------
#   block index: | 4 | 3 | 1 | 2 | 0 |
#                ---------------------
# pointer 0 points to block 4, pointer 1 points to block 3, pointer 2 points to block 1, ...
class _DataBlocks:
    def __init__(self, rom, pointers_start_address, pointers_end_address, pointer_size, pointer_offset, data_start_address, data_end_address):
        self.rom = rom
        self.pointers = DataPointers(rom, pointers_start_address, pointers_end_address, pointer_size)
        self.pointer_offset = pointer_offset
        self.data_blocks = [None] * len(self)

        self.start_address = data_start_address
        self.end_address = data_end_address
        self.free_space = 0

    def size(self):
        return self.end_address - self.start_address + 1

    def __len__(self):
        # equivalent to len(self.data_blocks) after initialization
        return len(self.pointers)

    def __getitem__(self, index):
        return self.data_blocks[index]

    def __setitem__(self, index, data):
        # NOTE: every pointer after given index must be updated making this an O(n) operation
        #       use assign to overwrite every data_block without O(n^2) complexity
        size_delta = len(self.data_blocks[index]) - len(data)
        self.data_blocks[index] = data

        if size_delta == 0:
            return
        self.free_space += size_delta

        for pointer_index in self.sorted_indices[index + 1:]:
            self.pointers[pointer_index] -= size_delta

    def assign(self, data_blocks):
        address = self.start_address - self.pointer_offset
        for index, pointer_index in enumerate(self.sorted_indices):
            self.pointers[pointer_index] = address % (self.pointers.max_address + 1)
            if pointer_index < len(data_blocks):
                self.data_blocks[pointer_index] = data_blocks[pointer_index]
                address += len(data_blocks[pointer_index])
            else:
                self.data_blocks[pointer_index] = []
        self.free_space = self.end_address - (address + self.pointer_offset) + 1

    def write(self):
        if self.free_space < 0:
            raise MemoryError(f"{self.__class__.__name__} write(): Not enough space ({self.free_space} bytes)")

        self.pointers.write()

        start_address = self.pointer_offset
        for index, pointer_index in enumerate(self.sorted_indices):
            if index > 0:
                prev_pointer_index = self.sorted_indices[index - 1]
                if self.pointers[pointer_index] < self.pointers[prev_pointer_index]:
                    start_address += self.pointers.max_address + 1  # pointer wrap around

            block_address = start_address + self.pointers[pointer_index]
            self.rom.set_bytes(block_address, self.data_blocks[pointer_index])

    def __str__(self):
        result = f"{len(self.pointers)} pointers [{hex(self.pointers.start_address)}, {hex(self.pointers.end_address)}]\n"
        result += f"{len(self.data_blocks)} blocks [{hex(self.start_address)}, {hex(self.end_address)}]"
        result += f", {self.free_space} free bytes\n"
        return result

    def __repr__(self):
        result = [""] * len(self)
        start_address = self.pointer_offset
        for index, pointer_index in enumerate(self.sorted_indices):
            if index > 0:
                prev_pointer_index = self.sorted_indices[index - 1]
                if self.pointers[pointer_index] < self.pointers[prev_pointer_index]:
                    start_address += self.pointers.max_address + 1  # pointer wrap around
            result[pointer_index] = f"{pointer_index}: {len(self.data_blocks[pointer_index])}, {hex(start_address + self.pointers[pointer_index])}: {[hex(x) for x in self.data_blocks[pointer_index]]}"

        result = '\n'.join(result)
        return str(self) + result

    def print(self):
        print(str(self))

    def printr(self):
        print(repr(self))

class DataList(_DataBlocks):
    def __init__(self, rom, pointers_start_address, pointers_end_address, pointer_size, pointer_offset, data_start_address, data_end_address):
        super().__init__(rom, pointers_start_address, pointers_end_address, pointer_size, pointer_offset, data_start_address, data_end_address)

        # pointers already sorted by address, create list of indices for base class convenience
        self.sorted_indices = list(range(len(self)))

        # original unused pointers can point beyond end address + 1, fix this first
        start_address = self.pointer_offset
        for index in range(len(self)):
            address = start_address + self.pointers[index]
            if address > self.end_address + 1:
                self.pointers[index] = (self.end_address + 1) % (self.pointers.max_address + 1)

            if index > 0 and self.pointers[index] < self.pointers[index - 1]:
                start_address += self.pointers.max_address + 1  # pointer wrap around

        # read data blocks
        start_address = self.pointer_offset
        for index in range(len(self)):
            block_address = start_address + self.pointers[index]
            if index < len(self) - 1:
                if self.pointers[index + 1] < self.pointers[index]:
                    start_address += self.pointers.max_address + 1 # pointer wrap around

                block_size = start_address + self.pointers[index + 1] - block_address
            else:
                block_size = self.end_address - block_address + 1

            data_block = self.rom.get_bytes(block_address, block_size)
            self.data_blocks[index] = data_block

class DataMap(_DataBlocks):
    def __init__(self, rom, pointers_start_address, pointers_end_address, pointer_size, pointer_offset, data_start_address, data_end_address):
        super().__init__(rom, pointers_start_address, pointers_end_address, pointer_size, pointer_offset, data_start_address, data_end_address)

        # sort pointer indices by the address they point to
        self.sorted_indices = sorted([index for index in range(len(self.pointers))], key = lambda index : self.pointers[index])

        # read data blocks (original order maintained but read in sorted order to calculate sizes)
        for index, pointer_index in enumerate(self.sorted_indices):
            block_address = self.pointers[pointer_index] + self.pointer_offset
            if index < len(self) - 1:
                next_pointer_index = self.sorted_indices[index + 1]
                block_size = self.pointers[next_pointer_index] + self.pointer_offset - block_address
            else:
                block_size = self.end_address - block_address + 1

            data_block = self.rom.get_bytes(block_address, block_size)
            self.data_blocks[pointer_index] = data_block
