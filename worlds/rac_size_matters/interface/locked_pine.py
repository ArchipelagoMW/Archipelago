from ..pypine import Pine
from threading import RLock

class LockedPine(Pine):
    DataSize = Pine.DataSize
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = RLock()

    def __getattribute__(self, name):
        """
        The Laziest Override i could have possibly done;
        This wraps all read and write methods into locks so multiple threads can safely use the same LockedPine instance.
        """
        attr = super().__getattribute__(name)
        if name.startswith(("read_", "write_")) and callable(attr):
            lock = super().__getattribute__("lock")
            def locked(*args, **kwargs):
                with lock:
                    return attr(*args, **kwargs)
            return locked
        return attr

    def read_int(self, address: int, size: Pine.DataSize) -> int:
        """
        Generic read_int method that uses pine reads and size to read an int of any size.
        """
        match(size):
            case Pine.DataSize.INT8:
                return self.read_int8(address)
            case Pine.DataSize.INT16:
                return self.read_int16(address)
            case Pine.DataSize.INT32:
                return self.read_int32(address)
            case Pine.DataSize.INT64:
                return self.read_int64(address)
            case _:
                return self.read_bytes(address, size)

    def write_int(self, address: int, value: int, size: Pine.DataSize) -> None:
        """
        Generic write_int method that uses pine writes and size to write an int of any size.
        """
        match(size):
            case Pine.DataSize.INT8:
                self.write_int8(address, value)
            case Pine.DataSize.INT16:
                self.write_int16(address, value)
            case Pine.DataSize.INT32:
                self.write_int32(address, value)
            case Pine.DataSize.INT64:
                self.write_int64(address, value)
            case _:
                self.write_bytes(address, value.to_bytes(size, "little"))
        
    def run_locked(self, func):
        """
        Runs func() while holding the lock, so callers can group several
        pine calls into one atomic critical section.
        """
        with self.lock:
            return func()