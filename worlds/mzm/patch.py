"""
Classes and functions related to creating a ROM patch
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import TYPE_CHECKING, cast

from BaseClasses import Location
import Utils
from worlds.Files import APPatchExtension, APProcedurePatch

from .items import item_data_table, tank_data_table, major_item_data_table
from .locations import full_location_table as location_table
from .options import ChozodiaAccess, DisplayNonLocalItems, Goal, LayoutPatches
from .patcher import MD5_US, patch_rom
from .patcher.text import LINE_WIDTH, SPACE, Message, get_width_of_encoded_character
from .item_sprites import Sprite, get_zero_mission_sprite, unknown_item_alt_sprites

if TYPE_CHECKING:
    from . import MZMWorld


class MZMPatchExtensions(APPatchExtension):
    game = "Metroid Zero Mission"

    @staticmethod
    def apply_json(caller: APProcedurePatch, rom: bytes, file_name: str) -> bytes:
        return patch_rom(rom, json.loads(caller.get_file(file_name).decode()))


class MZMProcedurePatch(APProcedurePatch):
    game = "Metroid Zero Mission"
    hash = MD5_US
    patch_file_ending = ".apmzm"
    result_file_ending = ".gba"
    procedure = [("apply_json", ["patch.json"])]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_base_rom_path(), "rb") as stream:
            return stream.read()


def get_base_rom_path(file_name: str = "") -> Path:
    from . import MZMWorld
    if not file_name:
        file_name = MZMWorld.settings.rom_file

    file_path = Path(file_name)
    if file_path.exists():
        return file_path
    else:
        return Path(Utils.user_path(file_name))


goal_texts = {
    Goal.option_mecha_ridley: "Infiltrate and destroy\nthe Space Pirates' mother ship.",
    Goal.option_bosses: "Exterminate all Metroid\norganisms and defeat Mother Brain.",
    Goal.option_metroid_dna: "Locate Metroid DNA\nsamples and destroy the mother ship.",
}


def get_item_sprite(location: Location, world: MZMWorld) -> str:
    player = world.player
    nonlocal_item_handling = world.options.display_nonlocal_items
    item = location.item

    if location.native_item and (nonlocal_item_handling != DisplayNonLocalItems.option_none or item.player == player):
        other_world = cast("MZMWorld", world.multiworld.worlds[item.player])
        sprite = item_data_table[item.name].game_data.sprite
        if (item.name in unknown_item_alt_sprites and other_world.options.fully_powered_suit.use_alt_unknown_sprites()):
            sprite = unknown_item_alt_sprites[item.name]
        return sprite

    if nonlocal_item_handling == DisplayNonLocalItems.option_match_series:
        sprite = get_zero_mission_sprite(item)
        if sprite is not None:
            return sprite

    if item.advancement or item.trap:
        sprite = Sprite.APLogoProgression
    elif item.useful:
        sprite = Sprite.APLogoUseful
    else:
        sprite = Sprite.APLogo
    return sprite


space_width = get_width_of_encoded_character(SPACE)

def split_text(text: str):
    lines = [""]
    i = 0
    width = 0
    while i < len(text):
        next_space = text.find(" ", i)
        if next_space == -1:
            next_space = len(text)
        next_word = text[i:next_space]
        next_word_width = Message(next_word).display_width()
        if width + space_width + next_word_width <= LINE_WIDTH:
            lines[-1] = f"{lines[-1]}{next_word} "
            width += space_width + next_word_width
        else:
            lines[-1] = lines[-1][:-1]
            lines.append(text[i:next_space] + " ")
            width = next_word_width
        i = next_space + 1
    lines[-1] = lines[-1][:-1]
    return lines


def write_json_data(world: MZMWorld, patch: MZMProcedurePatch):
    multiworld = world.multiworld
    player = world.player
    data = {
        "player_name": world.player_name,
        "seed_name": multiworld.seed_name,
    }

    config = {
        "goal": world.options.goal.value,
        "difficulty": world.options.game_difficulty.value,
        "remove_gravity_heat_resistance": True,
        "power_bombs_without_bomb": True,
        "buff_power_bomb_drops": bool(world.options.buff_pb_drops),
        "separate_hijump_springball": bool(world.options.spring_ball),
        "skip_chozodia_stealth": bool(world.options.skip_chozodia_stealth),
        "chozodia_requires_mother_brain": world.options.chozodia_access.value == ChozodiaAccess.option_closed,
        "start_with_maps": bool(world.options.start_with_maps),
        "reveal_maps": bool(world.options.start_with_maps),
        "reveal_hidden_blocks": bool(world.options.reveal_hidden_blocks),
        "skip_tourian_opening_cutscenes": bool(world.options.skip_tourian_opening_cutscenes),
        "elevator_speed": world.options.elevator_speed.value,
    }
    if world.options.goal.value == Goal.option_metroid_dna:
        config["metroid_dna_required"] = world.options.metroid_dna_required.value
    data["config"] = config

    locations = []
    for location in multiworld.get_locations(player):
        item = location.item
        if item.code is None:
            continue

        sprite = get_item_sprite(location, world)
        if item.player == player:
            item_name = item.name
            message = None
        else:
            item_name = "Nothing"
            message = f"{item.name}\nSent to {multiworld.player_name[item.player]}"

        location_data = location_table[location.name]
        assert location_data.id is not None
        locations.append({
            "id": location_data.id,
            "item": item_name,
            "sprite": sprite,
            "message": message,
        })
    data["locations"] = locations

    precollected_items = Counter(item.name for item in multiworld.precollected_items[player])
    starting_inventory: dict[str, int | bool] = {}
    for item, count in precollected_items.items():
        if item == "Missile Tank":
            starting_inventory[item] = min(count, 999)
        elif item in tank_data_table:
            starting_inventory[item] = min(count, 99)
        elif item in major_item_data_table:
            starting_inventory[item] = count > 0
    data["start_inventory"] = starting_inventory

    text = {"Story": {}}

    ap_version = Utils.version_tuple.as_simple_string()
    world_version = world.world_version.as_simple_string()
    text["Story"]["Intro"] = (f"AP {multiworld.seed_name}\n"
                              f"P{player} - {world.player_name}\n"
                              f"AP {ap_version} / World version: {world_version}\n"
                              "\n"
                              f"YOUR MISSION: {goal_texts[world.options.goal.value]}")

    plasma_beam = world.create_item("Plasma Beam")
    if world.options.plasma_beam_hint.value and plasma_beam not in multiworld.precollected_items[player]:
        zss_text = ("With Mother Brain taken down, I needed\n"
                    "to get my suit back in the ruins.\n")
        location = multiworld.find_item(plasma_beam.name, player)
        if location.native_item:
            location_text = location.parent_region.hint_text
        else:
            location_text = f"at {location.name}"
        if location.player != player:
            player_text = f" in {multiworld.player_name[location.player]}'s world"
        else:
            player_text = ""
        lines = split_text(f"Could I find the Plasma Beam {location_text}{player_text}?")
        while len(lines) > 4:
            location_text = location_text[:location_text.rfind(" ")]
            lines = split_text(f"Could I find the Plasma Beam {location_text}{player_text}?")
        if len(lines) < 4:
            zss_text += "\n"
        zss_text += "\n".join(lines)
        text["Story"]["Escape 2"] = zss_text

    data["text"] = text

    if world.options.layout_patches.value == LayoutPatches.option_true:
        data["layout_patches"] = "all"
    else:
        data["layout_patches"] = world.enabled_layout_patches

    patch.write_file("patch.json", json.dumps(data).encode())
