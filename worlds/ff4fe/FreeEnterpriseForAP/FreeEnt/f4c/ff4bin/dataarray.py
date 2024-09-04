import struct

class DataArray:
    def __init__(self, infile, data_address, length, data_size=1):
        self.data_address = data_address
        infile.seek(data_address)
        if data_size == 1:
            self._format = '{}B'
        elif data_size == 2:
            self._format = '<{}H'
        else:
            raise ValueError("Data array cannot be initialized with data size {}".format(data_size))

        self._data_size = data_size
        self._data = list(struct.unpack(self._format.format(length), infile.read(length * self._data_size)))
        self._changed = False

    def __getitem__(self, k):
        return self._data[k]

    def __setitem__(self, k, v):
        if self._data[k] != v:
            self._changed = True
            self._data[k] = v

    def save_if_changed(self, outfile):
        if self._changed:
            outfile.seek(self.data_address)
            outfile.write(struct.pack(self._format.format(len(self._data)), *self._data))

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        for d in self._data:
            yield d
