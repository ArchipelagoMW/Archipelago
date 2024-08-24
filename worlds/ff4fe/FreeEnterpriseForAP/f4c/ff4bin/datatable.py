'''
Abstraction for ROM data that is stored with/without a pointer table.
'''

import struct
import math

class DataTable:
    def __init__(self, stream=None,
        pointer_address=None, data_address=None, data_count=None, 
        data_size=None, use_end_pointer=False, data_consume_func=None, 
        last_data_size=None, data_overflow_address=None, data_filler=None,
        nonlinear=False, pointer_offset_regions=None):

        self.pointer_address = pointer_address
        self._pointer_offset = 0
        self.data_address = data_address
        self.data_count = data_count
        self.data_size = data_size
        self.use_end_pointer = use_end_pointer
        self.data_consume_func = data_consume_func
        self.last_data_size = last_data_size
        self.data_overflow_address = data_overflow_address
        self.data_filler = [data_filler] if type(data_filler) is int else data_filler
        self.nonlinear = nonlinear
        self.pointer_offset_regions = pointer_offset_regions

        self.changed = False

        if stream is not None:
            self.load(stream)

    def load(self, stream):
        self._data = []

        pointer_table = None
        if self.pointer_address:
            num_pointers = self.data_count
            if self.use_end_pointer:
                num_pointers += 1

            stream.seek(self.pointer_address)
            pointer_table = list(struct.unpack('<{}H'.format(num_pointers), stream.read(num_pointers * 2)))

            if self.pointer_offset_regions:
                region_offset = 0
                for i in range(num_pointers):
                    if i in self.pointer_offset_regions:
                        region_offset = self.pointer_offset_regions[i]
                    pointer_table[i] += region_offset

            self._pointer_offset = min(pointer_table)
        else:
            stream.seek(self.data_address)

        if self.nonlinear:
            unique_pointers = sorted(set(pointer_table))
            unique_pointer_to_index = {}
            self._nonlinear_data_indices = []
            for i,pointer in enumerate(unique_pointers):
                stream.seek(self.data_address + pointer)
                self._data.append(self.data_consume_func(stream))
                unique_pointer_to_index[pointer] = i

            for i in range(self.data_count):
                pointer = pointer_table[i]
                nonlinear_index = unique_pointer_to_index[pointer]
                self._nonlinear_data_indices.append(nonlinear_index)

        else:
            for i in range(self.data_count):
                if pointer_table:
                    stream.seek(self.data_address + pointer_table[i])

                if self.data_consume_func is not None:
                    data = self.data_consume_func(stream)
                    if pointer_table and i < len(pointer_table) - 1 and pointer_table[i] + len(data) > pointer_table[i + 1]:
                        print("Warning: data table at {:X} entry {} ({:X}) overflows into next pointer area ({:X})".format(self.data_address, i, pointer_table[i], pointer_table[i+1]))
                else:
                    if self.data_size:
                        data_size = self.data_size
                    elif i == self.data_count - 1 and self.last_data_size is not None:
                        data_size = self.last_data_size
                    elif i == self.data_count - 1 and not self.use_end_pointer and self.data_overflow_address is not None:
                        data_size = (self.data_overflow_address - self.data_address) - pointer_table[i]
                    else:
                        data_size = pointer_table[i + 1] - pointer_table[i]
                        #print('{} {} {}'.format(data_size, pointer_table[i+1], pointer_table[i]))

                    data = struct.unpack('{}B'.format(data_size), stream.read(data_size))

                self._data.append(data)

    def save(self, stream):
        if self.data_overflow_address is not None:
            total_data_length = sum([len(d) for d in self._data])
            if self.data_address + total_data_length > self.data_overflow_address:
                raise ValueError("Can't write to data table at {:X} -- too much data (length {:X}), will overflow".format(self.data_address, total_data_length))

        if self.pointer_address:
            pointer_table = []
            num_pointers = len(self._data)
            if self.use_end_pointer:
                num_pointers += 1

            pointer = self._pointer_offset
            for i in range(num_pointers):
                pointer_table.append(pointer)
                if i < len(self._data):
                    pointer += len(self._data[i])

            if self.nonlinear:
                data_pointers = pointer_table
                pointer_table = []
                num_pointers = len(self._nonlinear_data_indices)
                for i in range(num_pointers):
                    pointer_table.append(data_pointers[self._nonlinear_data_indices[i]])

            if self.pointer_offset_regions:
                region_offset = 0
                for i in range(num_pointers):
                    if i in self.pointer_offset_regions:
                        region_offset = self.pointer_offset_regions[i]
                    pointer_table[i] -= region_offset

            stream.seek(self.pointer_address)
            stream.write(struct.pack('<{}H'.format(num_pointers), *pointer_table))
        
        stream.seek(self.data_address + self._pointer_offset)
        for data_id,d in enumerate(self._data):
            if not d:
                continue

            try:
                stream.write(struct.pack('{}B'.format(len(d)), *d))
            except Exception as e:
                print('{:X} : {}'.format(data_id, d))
                print("{:X}".format(self.data_address))
                raise e

        if self.data_overflow_address and self.data_filler:
            filler_length = self.data_overflow_address - stream.tell()
            filler = self.data_filler * int(math.ceil(float(filler_length) / len(self.data_filler)))
            stream.write(struct.pack('{}B'.format(filler_length), *filler[:filler_length]))

    def save_if_changed(self, stream):
        if self.changed:
            self.save(stream)

    def __len__(self):
        if self.nonlinear:
            return len(self._nonlinear_data_indices)
        else:
            return len(self._data)

    def __getitem__(self, key):
        if self.nonlinear:
            return self._data[self._nonlinear_data_indices[key]]
        else:
            return self._data[key]

    def __setitem__(self, key, value):
        if self.nonlinear:
            data_index = self._nonlinear_data_indices[key]
            reference_count = len([x for x in self._nonlinear_data_indices if x == data_index])
            if reference_count == 1:
                self._data[data_index] = value
            else:
                self._nonlinear_data_indices[key] = len(self._data)
                self._data.append(value)
        else:
            self._data[key] = value
        
        self.changed = True

    def __iter__(self):
        if self.nonlinear:
            for i in self._nonlinear_data_indices:
                yield self._data[i]
        else:
            for d in self._data:
                yield d

