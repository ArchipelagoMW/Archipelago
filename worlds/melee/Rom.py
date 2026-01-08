import os
import Utils
import typing
import struct
import settings
import zipfile
from worlds.Files import APPlayerContainer
from typing import TYPE_CHECKING, Optional, Any
from logging import warning
from typing_extensions import override

if TYPE_CHECKING:
    from . import SSBMWorld

class MeleePlayerContainer(APPlayerContainer):
    game = "Super Smash Bros. Melee"
    compression_method = zipfile.ZIP_DEFLATED
    patch_file_ending = ".zip"

    def __init__(self, output_patch, output_file_path: str, player_name: str, player: int, patch_name,
        server: str = ""):
        self.output_patch = output_patch
        self.patch_name = patch_name
        super().__init__(output_file_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr(f"{self.patch_name}.xml", self.output_patch)
        super().write_contents(opened_zipfile)


def apply_patch(world, basepatch, output):
    from jinja2 import Template
    template = Template(basepatch)
    if world.options.lottery_pool_mode:
        disable_class_upgrades = True
    else:
        disable_class_upgrades = False
        
    result = template.render(
            PLAYER_NAME = world.player_name,
            GAME_FILE_NAME = world.encoded_slot_name,
            SLOT_NUM = world.player,
            AUTH_ID = world.authentication_id,
            CSTICK_SMASH_SOLO = world.options.solo_cstick_smash,
            DISABLE_TAP_JUMP = world.options.disable_tap_jump,
            TROPHYCLASS_IN_POOL = disable_class_upgrades)
    return result
    