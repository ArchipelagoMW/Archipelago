from __future__ import annotations

import os
import sys
from typing import Tuple, Optional, TypedDict

if __name__ == "__main__":
    import ModuleUpdate
    ModuleUpdate.update()

from worlds.Files import AutoPatchRegister, APAutoPatchInterface
from worlds.AutoWorld import AutoWorldRegister
from Utils import messagebox


class RomMeta(TypedDict):
    server: str
    player: Optional[int]
    player_name: str


def create_rom_file(patch_file: str) -> Tuple[RomMeta, str]:
    auto_handler = AutoPatchRegister.get_handler(patch_file)
    if auto_handler:
        handler: APAutoPatchInterface = auto_handler(patch_file)
        handler.read()
        game_version = AutoWorldRegister.world_types[handler.game].world_version
        if handler.world_version and game_version != handler.world_version:
            info_msg = "This patch was generated with " \
                       f"{handler.game} version {handler.world_version.as_simple_string()}, " \
                       f"but its currently installed version is {game_version.as_simple_string()}. " \
                       "You may encounter errors while patching or connecting."
            messagebox("APWorld version mismatch", info_msg, False)
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
