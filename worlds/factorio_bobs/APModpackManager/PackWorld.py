from pathlib import Path

from worlds.AutoWorld import World
from . import get_items, get_locations, get_item_groups, get_location_groups, BaseModpack, modpacks, logger
from .PackOptions import PackOptions


class PackWorld(World):
    options: PackOptions

    item_name_to_id = get_items()
    location_name_to_id = get_locations()
    item_name_groups = get_item_groups()
    location_name_groups = get_location_groups()

    def __init__(self, world, player: int):
        super().__init__(world, player)
        self.modpack: BaseModpack | None = None


    def generate_early(self):
        modpack_name = self.options.packname.value
        if modpack_name not in modpacks:
            raise Exception(f"Modpack name '{modpack_name}' not found.")
        self.modpack = modpacks[modpack_name]
        self.modpack.init_pack_check()