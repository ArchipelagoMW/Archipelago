import logging

import yaml
import os
import io
from typing import TYPE_CHECKING, Dict, List, Optional, cast
import Utils
import zipfile
import json

from .Locations import KH1Location, location_table

from worlds.Files import APPlayerContainer



class KH1Container(APPlayerContainer):
    game: str = 'Kingdom Hearts'
    patch_file_ending = ".zip"

    def __init__(self, patch_data: Dict[str, str] | io.BytesIO, base_path: str = "", output_directory: str = "",
        player: Optional[int] = None, player_name: str = "", server: str = ""):
        self.patch_data = patch_data
        self.file_path = base_path
        container_path = os.path.join(output_directory, base_path + ".zip")
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        for filename, text in self.patch_data.items():
            opened_zipfile.writestr(filename, text)
        super().write_contents(opened_zipfile)


def generate_json(world, output_directory):
    mod_name = f"AP-{world.multiworld.seed_name}-P{world.player}-{world.multiworld.get_file_safe_player_name(world.player)}"
    mod_dir = os.path.join(output_directory, mod_name + "_" + Utils.__version__)
    
    item_location_map = get_item_location_map(world)
    settings = get_settings(world)
    
    files = {
        "item_location_map.json":  json.dumps(item_location_map),
        "keyblade_stats.json":     json.dumps(world.get_keyblade_stats()),
        "settings.json":           json.dumps(settings),
        "ap_costs.json":           json.dumps(world.get_ap_costs())
    }

    mod = KH1Container(files, mod_dir, output_directory, world.player,
            world.multiworld.get_file_safe_player_name(world.player))
    mod.write()

def get_item_location_map(world):
    location_item_map = {}
    for location in world.multiworld.get_filled_locations(world.player):
        if location.name != "Final Ansem":
            if world.player != location.item.player or (world.player == location.item.player and world.options.remote_items.current_key == "full" and (location_table[location.name].code < 2656800 or location_table[location.name].code > 2656814)):
                item_id = 2641230
            else:
                item_id = location.item.code
            location_data = location_table[location.name]
            location_id = location_data.code
            location_item_map[location_id] = item_id
    return location_item_map

def get_settings(world):
    settings = world.fill_slot_data()
    return settings