import ctypes
import struct

import pymem.memory
import pymem.exception


class RemotePointer(object):
    """Pointer capable of reading the value mapped into another process memory.

    Parameters
    ----------
    handle: int
        Handle to the process
    v: int, RemotePointer, any ctypes type
        The address value
    endianess: str
        The endianess of the remote pointer, defaulting to little-endian

    Raises
    ------
    PymemAlignmentError
        If endianess is not a valid alignment

    Notes
    -----
    The bool of RemotePointer checks if the internal value is 0
    """

    ALIGNMENTS = {
        'little-endian': '<',
        'big-endian': '>'
    }

    def __init__(self, handle, v, endianess='little-endian'):
        self._set_value(v)

        if endianess not in RemotePointer.ALIGNMENTS:
            # TODO: maybe make this a ValueError in next major version
            raise pymem.exception.PymemAlignmentError(
                "{endianess} is not a valid alignment, it should be one from: {alignments}".format(**{
                    'endianess': endianess,
                    'alignments': ', '.join(RemotePointer.ALIGNMENTS.keys())
                })
            )
        self.endianess = endianess

        self.handle = handle
        self._memory_value = None

    def __bool__(self):
        return bool(self.value)

    def _set_value(self, v):
        """Given a v value will set up the internal kitchen to map internal v to the correct
        type. self.v has to be a ctype instance.
        """
        if isinstance(v, RemotePointer):
            self.v = v.cvalue
        elif isinstance(v, int) and not hasattr(v, 'value'):
            if v > 2147483647:
                self.v = ctypes.c_ulonglong(v)
            else:
                self.v = ctypes.c_uint(v)
        elif isinstance(v, ctypes._SimpleCData):
            self.v = v
        else:
            raise pymem.exception.PymemTypeError(
                "{type} is not an allowed type, it should be one from: {allowed_types}".format(**{
                    'type': 'None' if not v else str(type(v)),
                    'allowed_types': ', '.join([
                        'RemotePointer', 'ctypes', 'int'
                    ])
                }))

    def __add__(self, a):
        self._memory_value = self.value + a
        return self.cvalue

    @property
    def value(self):
        """Reads targeted process memory and returns the value pointed by the given address.

        Returns
        -------
        int
            The value pointed at by this remote pointer
        """
        if self._memory_value:
            return self._memory_value
        content = pymem.memory.read_bytes(
            self.handle, self.v.value, struct.calcsize(self.v._type_)
        )
        fmt = '{alignment}{type}'.format(**{
            'alignment': RemotePointer.ALIGNMENTS[self.endianess],
            'type': self.v._type_
        })
        content = struct.unpack(fmt, content)
        self._memory_value = content[0]
        return self._memory_value

    @property
    def cvalue(self):
        """Reads targeted process memory and returns the value pointed by the given address.

        Returns
        -------
        a ctypes type
            The value pointed at by this remote pointer as a ctypes type instance
        """
        v = self.v.__class__(self.value)
        return v
