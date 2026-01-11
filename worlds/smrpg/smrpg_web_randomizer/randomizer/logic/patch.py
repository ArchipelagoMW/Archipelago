
class Patch:
    """Class representing a patch for a specific seed that can be added to as we build it."""

    def __init__(self):
        self._data = {}

    def __add__(self, other):
        """Add another patch to this patch and return a new Patch object.

        :type other: Patch
        :rtype: Patch
        """
        if not isinstance(other, Patch):
            raise TypeError("Other object is not Patch type")

        patch = Patch()
        patch += self
        patch += other
        return patch

    def __iadd__(self, other):
        """Add another patch to this patch in place.

        :type other: Patch
        :rtype: Patch
        """
        if not isinstance(other, Patch):
            raise TypeError("Other object is not Patch type")

        for addr in other.addresses:
            self.add_data(addr, other.get_data(addr))

        return self

    @property
    def addresses(self):
        """
        :return: List of all addresses in the patch.
        :rtype: list[int]
        """
        return list(self._data.keys())

    def get_data(self, addr):
        """Get data in the patch for this address.  If the address is not present in the patch, returns empty bytes.

        :param addr: Address for the start of the data.
        :type addr: int
        :rtype: bytearray|bytes|list[int]
        """
        return self._data.get(addr, bytes())

    def add_data(self, addr, data):
        """Add data to the patch.

        :param addr: Address for the start of the data.
        :type addr: int
        :param data: Patch data as raw bytes.
        :type data: bytearray|bytes|list[int]|int|str
        """
        # For integers and strings, convert them to byte representations.
        if isinstance(data, int) and data <= 0xff:
            data = data.to_bytes(1, 'little')
        elif isinstance(data, str):
            data = data.encode('latin1')
        self._data[addr] = data

    def remove_data(self, addr):
        """Remove data from the patch.

        :param addr: Address the data was added to.
        :type addr: int
        """
        if addr in self._data:
            del self._data[addr]

    def for_json(self):
        """Return patch as a JSON serializable object.

        :rtype: list[dict]
        """
        patch = []
        addrs = list(self._data.keys())
        addrs.sort()

        for addr in addrs:
            patch.append({addr: self._data[addr]})

        return patch


class PatchJSONEncoder():
    """Extension of the Django JSON serializer to support randomizer patch data."""

    def default(self, o):
        # Support bytes and bytearray objects, which are just lists of integers.
        if isinstance(o, (bytearray, bytes)):
            return list(o)
        elif isinstance(o, Patch):
            return o.for_json()
        return super().default(o)
