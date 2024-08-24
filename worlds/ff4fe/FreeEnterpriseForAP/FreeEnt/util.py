def byte_string(bytes_iterable):
    return ' '.join([f'{b:02X}' for b in bytes_iterable])

def value_byte_string(val, byte_length):
    byte_vals = []
    while len(byte_vals) < byte_length:
        byte_vals.append(val & 0xFF)
        val >>= 8
    return byte_string(byte_vals)


class Distribution:
    def __init__(self, named_weights=None, **kw_named_weights):
        self._thresholds = []
        self._sum = 0

        if named_weights is None:
            named_weights = kw_named_weights

        for name in named_weights:
            self._sum += named_weights[name]
            self._thresholds.append( (name, self._sum) )

    def choose(self, rnd):
        v = rnd.random() * self._sum
        for threshold in self._thresholds:
            if v < threshold[1]:
                return threshold[0]
        return None

    def choose_many(self, rnd, count):
        counts = {}
        for i in range(count):
            v = self.choose(rnd)
            counts.setdefault(v, 0)
            counts[v] += 1
        return counts


# awkward spot for it, but it needs to go somewhere
BOOST_MATRIX = {
    1: [(1, 7/8)],
    2: [(1, 1/8), (2, 6/8)],
    3: [(2, 2/8), (3, 5/8)],
    4: [(3, 3/8), (4, 4/8)],
    5: [(4, 4/8), (5, 3/8)],
    6: [(5, 5/8), (6, 2/8)],
    7: [(6, 6/8), (7, 1/8)],
    8: [(7, 7/8), (8, 1)],
}

def get_boosted_weights(weights):
    boosted_weights = {i : 0 for i in range(1,9)}

    for i in boosted_weights:
        for chunk in BOOST_MATRIX[i]:
            boosted_weights[i] += weights[chunk[0]] * chunk[1]

    return boosted_weights
