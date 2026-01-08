import itertools

from .Rom import openFile

def range_union(ranges):
    ret = []
    for rg in sorted([[r.start, r.stop] for r in ranges]):
        begin, end = rg[0], rg[-1]
        if ret and ret[-1][1] > begin:
            ret[-1][1] = max(ret[-1][1], end)
        else:
            ret.append([begin, end])
    return [range(r[0], r[1]) for r in ret]

# adapted from ips-util for python 3.2 (https://pypi.org/project/ips-util/)
class IPS_Patch(object):
    def __init__(self, patchDict=None):
        self.records = []
        self.truncate_length = None
        self.max_size = 0
        if patchDict is not None:
            for addr, data in patchDict.items():
                byteData = bytearray(data)
                self.add_record(addr, byteData)

    def toDict(self):
        ret = {}
        for record in self.records:
            if 'rle_count' in record:
                ret[record['address']] = [int.from_bytes(record['data'],'little')]*record['rle_count']
            else:
                ret[record['address']] = [int(b) for b in record['data']]
        return ret

    @staticmethod
    def load(filename):
        loaded_patch = IPS_Patch()
        with openFile(filename, 'rb') as file:
            header = file.read(5)
            if header != b'PATCH':
                raise Exception('Not a valid IPS patch file!')
            while True:
                address_bytes = file.read(3)
                if address_bytes == b'EOF':
                    break
                address = int.from_bytes(address_bytes, byteorder='big')
                length = int.from_bytes(file.read(2), byteorder='big')
                rle_count = 0
                if length == 0:
                    rle_count = int.from_bytes(file.read(2), byteorder='big')
                    length = 1
                data = file.read(length)
                if rle_count > 0:
                    loaded_patch.add_rle_record(address, data, rle_count)
                else:
                    loaded_patch.add_record(address, data)

            truncate_bytes = file.read(3)
            if len(truncate_bytes) == 3:
                loaded_patch.set_truncate_length(int.from_bytes(truncate_bytes, byteorder='big'))
        return loaded_patch

    @staticmethod
    def create(original_data, patched_data):
        # The heuristics for optimizing a patch were chosen with reference to
        # the source code of Flips: https://github.com/Alcaro/Flips

        patch = IPS_Patch()

        run_in_progress = False
        current_run_start = 0
        current_run_data = bytearray()

        runs = []

        if len(original_data) > len(patched_data):
            patch.set_truncate_length(len(patched_data))
            original_data = original_data[:len(patched_data)]
        elif len(original_data) < len(patched_data):
            original_data += bytes([0] * (len(patched_data) - len(original_data)))

            if original_data[-1] == 0 and patched_data[-1] == 0:
                patch.add_record(len(patched_data) - 1, bytes([0]))

        for index, (original, patched) in enumerate(zip(original_data, patched_data)):
            if not run_in_progress:
                if original != patched:
                    run_in_progress = True
                    current_run_start = index
                    current_run_data = bytearray([patched])
            else:
                if original == patched:
                    runs.append((current_run_start, current_run_data))
                    run_in_progress = False
                else:
                    current_run_data.append(patched)
        if run_in_progress:
            runs.append((current_run_start, current_run_data))

        for start, data in runs:
            if start == int.from_bytes(b'EOF', byteorder='big'):
                start -= 1
                data = bytes([patched_data[start - 1]]) + data

            grouped_byte_data = list([
                {'val': key, 'count': sum(1 for _ in group), 'is_last': False}
                for key,group in itertools.groupby(data)
            ])

            grouped_byte_data[-1]['is_last'] = True

            record_in_progress = bytearray()
            pos = start

            for group in grouped_byte_data:
                if len(record_in_progress) > 0:
                    # We don't want to interrupt a record in progress with a new header unless
                    # this group is longer than two complete headers.
                    if group['count'] > 13:
                        patch.add_record(pos, record_in_progress)
                        pos += len(record_in_progress)
                        record_in_progress = bytearray()

                        patch.add_rle_record(pos, bytes([group['val']]), group['count'])
                        pos += group['count']
                    else:
                        record_in_progress += bytes([group['val']] * group['count'])
                elif (group['count'] > 3 and group['is_last']) or group['count'] > 8:
                    # We benefit from making this an RLE record if the length is at least 8,
                    # or the length is at least 3 and we know it to be the last part of this diff.

                    # Make sure not to overflow the maximum length. Split it up if necessary.
                    remaining_length = group['count']
                    while remaining_length > 0xffff:
                        patch.add_rle_record(pos, bytes([group['val']]), 0xffff)
                        remaining_length -= 0xffff
                        pos += 0xffff

                    patch.add_rle_record(pos, bytes([group['val']]), remaining_length)
                    pos += remaining_length
                else:
                    # Just begin a new standard record.
                    record_in_progress += bytes([group['val']] * group['count'])

                if len(record_in_progress) > 0xffff:
                    patch.add_record(pos, record_in_progress[:0xffff])
                    record_in_progress = record_in_progress[0xffff:]
                    pos += 0xffff

            # Finalize any record still in progress.
            if len(record_in_progress) > 0:
                patch.add_record(pos, record_in_progress)

        return patch

    def add_record(self, address, data):
        if address == int.from_bytes(b'EOF', byteorder='big'):
            raise RuntimeError('Start address {0:x} is invalid in the IPS format. Please shift your starting address back by one byte to avoid it.'.format(address))
        if address > 0xffffff:
            raise RuntimeError('Start address {0:x} is too large for the IPS format. Addresses must fit into 3 bytes.'.format(address))
        if len(data) > 0xffff:
            raise RuntimeError('Record with length {0} is too large for the IPS format. Records must be less than 65536 bytes.'.format(len(data)))
        if len(data) == 0: # ignore empty records
            return
        record = {'address': address, 'data': data, 'size':len(data)}
        self.appendRecord(record)

    def add_rle_record(self, address, data, count):
        if address == int.from_bytes(b'EOF', byteorder='big'):
            raise RuntimeError('Start address {0:x} is invalid in the IPS format. Please shift your starting address back by one byte to avoid it.'.format(address))
        if address > 0xffffff:
            raise RuntimeError('Start address {0:x} is too large for the IPS format. Addresses must fit into 3 bytes.'.format(address))
        if count > 0xffff:
            raise RuntimeError('RLE record with length {0} is too large for the IPS format. RLE records must be less than 65536 bytes.'.format(count))
        if len(data) != 1:
            raise RuntimeError('Data for RLE record must be exactly one byte! Received {0}.'.format(data))
        record = {'address': address, 'data': data, 'rle_count': count, 'size': count}
        self.appendRecord(record)

    def appendRecord(self, record):
        sz = record['address'] + record['size']
        if sz > self.max_size:
            self.max_size = sz
        self.records.append(record)

    def set_truncate_length(self, truncate_length):
        self.truncate_length = truncate_length

    def encode(self):
        encoded_bytes = bytearray()

        encoded_bytes += 'PATCH'.encode('ascii')

        for record in self.records:
            encoded_bytes += record['address'].to_bytes(3, byteorder='big')
            if 'rle_count' in record:
                encoded_bytes += (0).to_bytes(2, byteorder='big')
                encoded_bytes += record['rle_count'].to_bytes(2, byteorder='big')
            else:
                encoded_bytes += len(record['data']).to_bytes(2, byteorder='big')
            encoded_bytes += record['data']

        encoded_bytes += 'EOF'.encode('ascii')

        if self.truncate_length is not None:
            encoded_bytes += self.truncate_length.to_bytes(3, byteorder='big')

        return encoded_bytes

    # save patch into IPS file
    def save(self, path):
        with open(path, 'wb') as ipsFile:
            ipsFile.write(self.encode())

    # applies patch on an existing bytearray
    def apply(self, in_data):
        out_data = bytearray(in_data)

        for record in self.records:
            if record['address'] >= len(out_data):
                out_data += bytes([0] * (record['address'] - len(out_data) + 1))

            if 'rle_count' in record:
                out_data[record['address'] : record['address'] + record['rle_count']] = b''.join([record['data']] * record['rle_count'])
            else:
                out_data[record['address'] : record['address'] + len(record['data'])] = record['data']

        if self.truncate_length is not None:
            out_data = out_data[:self.truncate_length]

        return out_data

    # applies patch on an opened file
    def applyFile(self, handle):
        for record in self.records:
            handle.seek(record['address'])
            if 'rle_count' in record:
                handle.write(bytearray(b'').join([record['data']]) * record['rle_count'])
            else:
                handle.write(record['data'])

    # appends an IPS_Patch on top of this one
    def append(self, patch):
        if patch.truncate_length is not None and (self.truncate_length is None or patch.truncate_length > self.truncate_length):
            self.set_truncate_length(patch.truncate_length)
        for record in patch.records:
            if record['size'] > 0: # ignore empty records
                self.appendRecord(record)

    # gets address ranges written to by this patch
    def getRanges(self):
        def getRange(record):
            return range(record['address'], record['address']+record['size'])
        return range_union([getRange(record) for record in self.records])
