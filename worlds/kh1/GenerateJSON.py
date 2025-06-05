import logging

import yaml
import os
import Utils
import zipfile
import json

from .Locations import KH1Location, location_table

from worlds.Files import APContainer



class KH1Container(APContainer):
    game: str = 'Kingdom Hearts'

    def __init__(self, patch_data: dict, base_path: str, output_directory: str,
        player=None, player_name: str = "", server: str = ""):
        self.patch_data = patch_data
        self.file_path = base_path
        container_path = os.path.join(output_directory, base_path + ".zip")
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        for filename, text in self.patch_data.items():
            opened_zipfile.writestr(filename, text)
        super().write_contents(opened_zipfile)


def generate_json(self, output_directory):
    mod_name = f"AP-{self.multiworld.seed_name}-P{self.player}-{self.multiworld.get_file_safe_player_name(self.player)}"
    mod_dir = os.path.join(output_directory, mod_name + "_" + Utils.__version__)
    
    item_location_map = get_item_location_map(self)
    settings = get_settings(self)
    
    files = {
        "item_location_map.json":  json.dumps(item_location_map),
        "keyblade_stats.json":     json.dumps(self.get_keyblade_stats()),
        "settings.json":           json.dumps(settings),
        "ap_costs.json":           json.dumps(self.get_ap_costs())
    }

    mod = KH1Container(files, mod_dir, output_directory, self.player,
            self.multiworld.get_file_safe_player_name(self.player))
    mod.write()

def get_item_location_map(self):
    location_item_map = {}
    for location in self.multiworld.get_filled_locations(self.player):
        if location.name != "Final Ansem":
            if self.player != location.item.player or (self.player == location.item.player and self.options.remote_items.current_key == "full" and (location_table[location.name].code < 2656800 or location_table[location.name].code > 2656814)):
                item_id = 2641230
            else:
                item_id = location.item.code
            location_data = location_table[location.name]
            location_id = location_data.code
            location_item_map[location_id] = item_id
    return location_item_map

def get_settings(self):
    settings = self.fill_slot_data()
    return settings