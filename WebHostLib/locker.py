import os
import sys


class CommonLocker:
    """Uses a file lock to signal that something is already running"""
    lock_folder = "file_locks"

    def __init__(self, lockname: str, folder=None):
        if folder:
            self.lock_folder = folder
        os.makedirs(self.lock_folder, exist_ok=True)
        self.lockname = lockname
        self.lockfile = os.path.join(self.lock_folder, f"{self.lockname}.lck")


class AlreadyRunningException(Exception):
    pass


if sys.platform == 'win32':
    class Locker(CommonLocker):
        def __enter__(self):
            try:
                if os.path.exists(self.lockfile):
                    os.unlink(self.lockfile)
                self.fp = os.open(
                    self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            except OSError as e:
                raise AlreadyRunningException() from e

        def __exit__(self, _type, value, tb):
            fp = getattr(self, "fp", None)
            if fp:
                os.close(self.fp)
                os.unlink(self.lockfile)
else:  # unix
    import fcntl


    class Locker(CommonLocker):
        def __enter__(self):
            try:
                self.fp = open(self.lockfile, "wb")
                fcntl.flock(self.fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as e:
                raise AlreadyRunningException() from e

        def __exit__(self, _type, value, tb):
            fcntl.flock(self.fp.fileno(), fcntl.LOCK_UN)
            self.fp.close()
