from __future__ import annotations

import os
import sys
from typing import Tuple, Optional, TypedDict

if __name__ == "__main__":
    import ModuleUpdate
    ModuleUpdate.update()

from worlds.Files import AutoPatchRegister, APAutoPatchInterface


class RomMeta(TypedDict):
    server: str
    player: Optional[int]
    player_name: str


class IncompatiblePatchError(Exception):
    """
    Used to report a version mismatch between a patch's world version and
    a user's installed world version that is too important to be compatible
    """
    pass


def create_rom_file(patch_file: str) -> Tuple[RomMeta, str]:
    auto_handler = AutoPatchRegister.get_handler(patch_file)
    if auto_handler:
        handler: APAutoPatchInterface = auto_handler(patch_file)
        handler.read()
        handler.verify_version()
        target = os.path.splitext(patch_file)[0]+handler.result_file_ending
        handler.patch(target)
        return {"server": handler.server,
                "player": handler.player,
                "player_name": handler.player_name}, target
    raise NotImplementedError(f"No Handler for {patch_file} found.")


if __name__ == "__main__":
    for file in sys.argv[1:]:
        meta_data, result_file = create_rom_file(file)
        print(f"Patch with meta-data {meta_data} was written to {result_file}")
