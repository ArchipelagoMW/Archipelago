from __future__ import annotations

import os
import sys
from typing import Tuple, Optional, TypedDict

if __name__ == "__main__":
    import ModuleUpdate
    ModuleUpdate.update()

from worlds.Files import AutoPatchRegister, APDeltaPatch


GAME_ALTTP = "A Link to the Past"
GAME_SM = "Super Metroid"
GAME_SOE = "Secret of Evermore"
GAME_SMZ3 = "SMZ3"
GAME_DKC3 = "Donkey Kong Country 3"

GAME_SMW = "Super Mario World"

GAME_CV64 = "Castlevania 64"

class RomMeta(TypedDict):
    server: str
    player: Optional[int]
    player_name: str


def create_rom_file(patch_file: str) -> Tuple[RomMeta, str]:
    auto_handler = AutoPatchRegister.get_handler(patch_file)
    if auto_handler:
        handler: APDeltaPatch = auto_handler(patch_file)
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
