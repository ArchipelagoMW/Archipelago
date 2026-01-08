import copy
import os
import json
from pathlib import Path
from typing import Callable, Optional

from . import rust, version


class BaseProgressNotifier:
    def notify_total_bytes(self, total_size: int):
        raise NotImplementedError()

    def notify_writing_file(self, file_name: bytes, file_bytes: int):
        raise NotImplementedError()

    def notify_writing_header(self):
        raise NotImplementedError()

    def notify_flushing_to_disk(self):
        raise NotImplementedError()


class ProgressNotifier(BaseProgressNotifier):
    total_size: int = 0
    bytes_so_far: int = 0

    def __init__(self, callback: Callable[[float, str], None]):
        self.callback = callback

    def notify_total_bytes(self, total_size: int):
        self.total_size += total_size

    def notify_writing_file(self, file_name: bytes, file_bytes: int):
        self.callback(self.bytes_so_far / self.total_size, "Writing file {}".format(file_name.decode("utf-8")))
        self.bytes_so_far += file_bytes

    def notify_writing_header(self):
        self.callback(self.bytes_so_far / self.total_size, "Writing ISO header")

    def notify_flushing_to_disk(self):
        self.callback(1, "Flushing written data to the disk")


def patch_iso_raw(config_str: str, notifier: BaseProgressNotifier):
    if notifier is None:
        raise ValueError("notifier is None")
    return rust.patch_iso(config_str, notifier)


def patch_iso(input_iso: Path, output_iso: Path, config: dict, notifier: BaseProgressNotifier):
    new_config = copy.copy(config)
    new_config["inputIso"] = os.fspath(input_iso)
    new_config["outputIso"] = os.fspath(output_iso)
    return patch_iso_raw(json.dumps(new_config), notifier)


def symbols_for_file(input_file: Path) -> Optional[dict]:
    v = rust.get_iso_mp1_version(os.fspath(input_file))
    if v is not None:
        return rust.get_mp1_symbols(v)


def symbols_for_version(v: str) -> Optional[dict]:
    return rust.get_mp1_symbols(v)

    
__version__ = version.version
VERSION = version.version