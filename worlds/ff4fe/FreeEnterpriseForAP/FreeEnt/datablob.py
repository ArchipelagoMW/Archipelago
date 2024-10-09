

class DataBlob:
    def __init__(self):
        self._datas = {}

    # if provided, the callback is invoked when the data
    # is placed within the blob, and passed a dict of where
    # the data is placed.
    # The callback should return a dict of additional addresses
    # to be returned from generate().
    def add(self, name, data, callback=None):
        self._datas[name] = {
            'data': data,
            'callback' : callback
            }

    def generate(self, size, base_addr, rnd=None):
        subblobs = []
        for name in self._datas:
            item = self._datas[name]
            data = list(item['data'])
            subblobs.append({
                'name' : name,
                'root' : name,
                'data' : data
                })

        if rnd:
            rnd.shuffle(subblobs)

        paddings = []
        padding_remaining = size - sum(map(lambda subblob: len(subblob['data']), subblobs))
        for subblob in subblobs:
            padding = (rnd.randint(0, padding_remaining) if rnd else 0)
            padding_remaining -= padding
            paddings.append(padding)
        paddings.append(padding_remaining)
        if rnd:
            rnd.shuffle(paddings)
            paddings = [[rnd.randint(0x00, 0xFF) for i in range(p)] for p in paddings]
        else:
            paddings = [[0x00] * p for p in paddings]

        blob = []
        addresses = {}
        address_groups = {}
        for subblob in subblobs:
            blob.extend(paddings.pop(0))
            offset = len(blob)
            blob.extend(subblob['data'])

            address = base_addr + offset
            addresses[subblob['name']] = address
            address_groups.setdefault(subblob['root'], {})[subblob['name']] = address

        blob.extend(paddings.pop(0))
        if len(blob) != size:
            raise Error("Generated data blob length is incorrect")
        elif paddings:
            raise Error("Leftover paddings, somehow?")

        for name in self._datas:
            item = self._datas[name]
            if item['callback']:
                addresses.update(item['callback'](address_groups[name]))
        
        return blob, addresses
