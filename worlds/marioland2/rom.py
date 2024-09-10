import hashlib
import os
import pkgutil

import Utils

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings

from .rom_addresses import rom_addresses
from .sprites import sprite_name_to_id


def randomize_music(patch, random):
    # overworld
    overworld_music_tracks = [0x05, 0x06, 0x0D, 0x0E, 0x10, 0x12, 0x1B, 0x1C, 0x1E]
    random.shuffle(overworld_music_tracks)
    for i, track in zip([0x3004F, 0x3EA9B, 0x3D186, 0x3D52B, 0x3D401, 0x3D297, 0x3D840, 0x3D694, 0x3D758],
                        overworld_music_tracks):
        patch.write_bytes(i, track)
    # levels
    for i in range(0x5619, 0x5899, 0x14):
        patch.write_bytes(i, random.choice([0x01, 0x0B, 0x11, 0x13, 0x14, 0x17, 0x1D, 0x1F, 0x28]))


def generate_output(self, output_directory: str):

    patch = SuperMarioLand2ProcedurePatch(player=self.player, player_name=self.player_name)

    patch.write_file("basepatch.bsdiff4", pkgutil.get_data(__name__, "basepatch.bsdiff4"))
    random = self.random

    if self.options.marios_castle_midway_bell:
        # Remove Question Mark Block
        patch.write_bytes(0x4F012, 0x5D)
        # Fix level pointer to read midway bell flag
        patch.write_bytes(0x3E569, 0x18)
        patch.write_bytes(0x3E56A, 0x18)
        # Position and screen coordinates
        patch.write_bytes(0x383B, [0xD4, 0x01, 0x4D, 0x0A, 0xC0, 0x01, 0x50, 0x0A])

    if self.options.coinsanity:
        # Add platform to return to start of Pumpkin Zone Secret Course 1
        patch.write_bytes(0x258B6, 0x3B)
        patch.write_bytes(0x258F8, 0x7a)
        patch.write_bytes(0x2594D, 0x67)
        patch.write_bytes(0x259A8, 0x68)
        patch.write_bytes(0x259A9, 0x60)

    i = 0xe077
    for level, sprites in self.sprite_data.items():
        for sprite_data in sprites:
            sprite_id = sprite_name_to_id[sprite_data["sprite"]]
            data = [((sprite_id & 0b01000000) >> 2) | ((sprite_id & 0b00111000) << 2) | sprite_data["screen"],
                    ((sprite_id & 0b00000111) << 5) | sprite_data["x"],
                    sprite_data["misc"] | sprite_data["y"]]
            patch.write_bytes(i, data)
            i += 3
        patch.write_bytes(i, 255)
        i += 1

    if self.options.randomize_music:
        randomize_music(patch, random)

    if self.options.shuffle_golden_coins:
        patch.write_bytes(rom_addresses["Coin_Shuffle"], 0x40)
    if self.options.shuffle_midway_bells:
        patch.write_bytes(rom_addresses["Disable_Midway_Bell"], 0xC9)

    if self.options.coinsanity:
        for section in ("A", "B"):
            for i in range(0, 30):
                patch.write_bytes(rom_addresses[f"Coinsanity_{section}"] + i, 0x00)

    star_count = max(len([loc for loc in self.multiworld.get_filled_locations() if loc.item.player == self.player
                          and loc.item.name == "Super Star Duration Increase"]), 1)
    patch.write_bytes(rom_addresses["Star_Count"], star_count // 256)
    patch.write_bytes(rom_addresses["Star_Count"] + 1, star_count - (star_count // 256))
    if self.options.shuffle_golden_coins == "mario_coin_fragment_hunt":
        patch.write_bytes(rom_addresses["Coins_Required"], self.coin_fragments_required // 256)
        patch.write_bytes(rom_addresses["Coins_Required"] + 1, self.coin_fragments_required % 256)
        patch.write_bytes(rom_addresses["Required_Golden_Coins"], 6)
    else:
        patch.write_bytes(rom_addresses["Coins_Required"] + 1, self.options.required_golden_coins.value)
        patch.write_bytes(rom_addresses["Required_Golden_Coins"], self.options.required_golden_coins.value)
    patch.write_bytes(rom_addresses["Midway_Bells"], self.options.shuffle_midway_bells.value)
    patch.write_bytes(rom_addresses["Energy_Link"], self.options.energy_link.value)
    patch.write_bytes(rom_addresses["Difficulty_Mode"], self.options.difficulty_mode.value)
    patch.write_bytes(rom_addresses["Coin_Mode"], self.options.shuffle_golden_coins.value)

    for level, i in enumerate(self.auto_scroll_levels):
        # We set 0 if no auto scroll or auto scroll trap, so it defaults to no auto scroll. 1 if always or cancel items.
        patch.write_bytes(rom_addresses["Auto_Scroll_Levels"] + level, max(0, i - 1))
        patch.write_bytes(rom_addresses["Auto_Scroll_Levels_B"] + level, i)

    if self.options.energy_link:
        # start with 1 life if Energy Link is on so that you don't deposit lives at the start of the game.
        patch.write_bytes(rom_addresses["Starting_Lives"], 1)

    rom_name = bytearray(f'AP{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0',
                         'utf8')[:21]
    rom_name.extend([0] * (21 - len(rom_name)))
    patch.write_bytes(0x77777, rom_name)
    patch.write_file("tokens.bin", patch.get_token_binary())
    patch.write(os.path.join(output_directory,
                             f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))


class SuperMarioLand2ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = "a8413347d5df8c9d14f97f0330d67bce"
    patch_file_ending = ".apsml2"
    game = "Super Mario Land 2"
    result_file_ending = ".gb"
    procedure = [
        ("apply_bsdiff4", ["basepatch.bsdiff4"]),
        ("apply_tokens", ["tokens.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_bytes(self, offset, value):
        if isinstance(value, int):
            value = [value]
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def get_base_rom_bytes():
    file_name = get_base_rom_path()
    with open(file_name, "rb") as file:
        base_rom_bytes = bytes(file.read())

    basemd5 = hashlib.md5()
    basemd5.update(base_rom_bytes)
    if SuperMarioLand2ProcedurePatch.hash != basemd5.hexdigest():
        raise Exception("Supplied Base Rom does not match known MD5 for Super Mario Land 1.0. "
                        "Get the correct game and version, then dump it")
    return base_rom_bytes


def get_base_rom_path():
    file_name = get_settings()["sml2_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name