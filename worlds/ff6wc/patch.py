
import hashlib
import json
import logging
import os
from pathlib import Path
import threading
import traceback
from typing import Any
import zipfile

from typing_extensions import override

from worlds.Files import APAutoPatchInterface
import Utils

from .gen_data import GenData
from .WorldsCollide.wc import WC

NA10HASH = 'e986575b98300f721ce27c180264d890'


class FF6WCPatch(APAutoPatchInterface):
    hash = NA10HASH
    game = "Final Fantasy 6 Worlds Collide"
    patch_file_ending = ".apff6wc"

    gen_data_str: str
    """ JSON encoded """

    def __init__(self, *args: Any, gen_data_str: str = "", **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.gen_data_str = gen_data_str

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    @override
    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super().write_contents(opened_zipfile)
        opened_zipfile.writestr("gen_data.json",
                                self.gen_data_str,
                                compress_type=zipfile.ZIP_DEFLATED)

    @override
    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> dict[str, Any]:
        manifest = super().read_contents(opened_zipfile)
        self.gen_data_str = opened_zipfile.read("gen_data.json").decode()
        return manifest

    @override
    def patch(self, target: str) -> None:
        self.read()
        write_rom_from_gen_data(self.gen_data_str, target)


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if NA10HASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for NA (1.0) release. '
                            'Get the correct game and version, then dump it')
        setattr(get_base_rom_bytes, "base_rom_bytes", base_rom_bytes)
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    from . import FF6WCSettings, FF6WCWorld
    settings = FF6WCWorld.settings
    assert isinstance(settings, FF6WCSettings)
    if not file_name:
        file_name = settings.rom_file
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name


_wc_lock = threading.Lock()


def write_rom_from_gen_data(gen_data_str: str, output_rom_file_name: str | Path) -> None:
    """ take the output of `GenData.to_json`, and create rom from it """
    gen_data = GenData.from_json(gen_data_str)

    base_rom_path = get_base_rom_path()
    output_rom_file_name = Path(output_rom_file_name)
    output_directory = output_rom_file_name.parent
    name_base = output_rom_file_name.stem

    placement_file = os.path.join(output_directory, f'{name_base}' + '.applacements')
    with open(placement_file, "w") as file:
        json.dump(gen_data.locations, file, indent=2)

    wc_args = ["-i", f"{base_rom_path}", "-o", f"{output_rom_file_name}", "-ap", placement_file]
    wc_args.extend(gen_data.flag_string)
    logging.debug(wc_args)
    # We probably don't need this lock and module management. This was moved from a multithreaded context.
    # (It probably doesn't hurt to keep it.)
    with _wc_lock:
        try:
            import sys
            from copy import deepcopy
            module_keys = deepcopy(list(sys.modules.keys()))
            for module in module_keys:
                if str(module).startswith("worlds.ff6wc.WorldsCollide"):
                    del sys.modules[module]
            wc = WC()
            wc.main(wc_args)
            os.remove(placement_file)
        except Exception as ex:
            print(''.join(traceback.format_tb(ex.__traceback__)))
            print(ex)
            raise ex
