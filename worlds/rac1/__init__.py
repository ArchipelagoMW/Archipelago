from typing import Dict, Optional

from BaseClasses import Item, ItemClassification, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, SuffixIdentifier, Type
from . import ItemPool
from .data import Items, Locations, Planets
from .data.Items import CollectableData, ItemData
from .data.Planets import PlanetData
from .RacOptions import RacOptions
from .Regions import create_regions


def run_client(_url: Optional[str] = None):
    # from .RacClient import launch
    # launch_subprocess(launch, name="RacClient")
    components.append(Component("Ratchet & Clank Client", func=run_client, component_type=Type.CLIENT,
                                file_identifier=SuffixIdentifier(".aprac")))


# class RacSettings(settings.Group):


class RacWeb(WebWorld):
    tutorials = [Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Ratchet & Clank for Archipelago",
            "English",
            "setup.md",
            "setup/en",
            ["Panad"]
    )]


class RacItem(Item):
    game: str = "Ratchet & Clank"


class RacWorld(World):
    """
    Ratchet & Clank is a third-person shooter platform video game developed by Insomniac Games
    and published by Sony Computer Entertainment for the PlayStation 2 in 2002. It is the first
    game in the Ratchet & Clank series and the first game developed by Insomniac to not be owned by Universal
    Interactive.
    """
    game = "Ratchet & Clank"
    web = RacWeb()
    options_dataclass = RacOptions
    options: RacOptions
    topology_present = True
    item_name_to_id = {item.name: item.item_id for item in Items.ALL}
    location_name_to_id = {location.name: location.location_id for location in Planets.ALL_LOCATIONS if
                           location.location_id}
    # item_name_groups = Items.get_item_groups()
    # location_name_groups = Planets.get_location_groups()
    # settings: RacSettings
    starting_planet: Optional[PlanetData] = None
    starting_weapons: list[ItemData] = []
    prefilled_item_map: Dict[str, str] = {}  # Dict of location name to item name

    # def get_filler_item_name(self) -> str:
    #     return Items.BOLT_PACK.name

    def create_regions(self) -> None:
        create_regions(self)

    def create_item(self, name: str, override: Optional[ItemClassification] = None) -> "Item":
        if override:
            return RacItem(name, override, self.item_name_to_id[name], self.player)
        item_data = Items.from_name(name)
        return RacItem(name, ItemPool.get_classification(item_data), self.item_name_to_id[name], self.player)

    def create_event(self, name: str) -> "Item":
        return RacItem(name, ItemClassification.progression, None, self.player)

    def pre_fill(self) -> None:
        for location_name, item_name in self.prefilled_item_map.items():
            location = self.get_location(location_name)
            item = self.create_item(item_name, ItemClassification.progression)
            location.place_locked_item(item)

    def create_items(self) -> None:
        items_to_add: list["Item"] = []
        items_to_add += ItemPool.create_planets(self)
        items_to_add += ItemPool.create_equipment(self)
        items_to_add += ItemPool.create_collectables(self)

        # add platinum bolts in whatever slots we have left
        # unfilled = [i for i in self.multiworld.get_unfilled_locations(self.player) if not i.is_event]
        # print(self.multiworld.get_filled_locations(self.player))
        # print(f"{len(items_to_add)} {len(unfilled)}")
        # remain = len(unfilled) - len(items_to_add)
        # assert remain >= 0, "There are more items than locations. This is not supported."
        # print(f"Not enough items to fill all locations. Adding {remain} filler items to the item pool")
        # for _ in range(remain):
        #     items_to_add.append(self.create_item(Items.GOLD_BOLT.name, ItemClassification.filler))

        self.multiworld.itempool += items_to_add

    def set_rules(self) -> None:
        boss_location = self.multiworld.get_location(Locations.VELDIN_DREK.name, self.player)
        boss_location.place_locked_item(self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        # def generate_output(self, output_directory: str) -> None:
        #     aprac2 = Rac2ProcedurePatch(player=self.player, player_name=self.multiworld.get_player_name(self.player))
        #     generate_patch(self, aprac2)
        #     rom_path = os.path.join(output_directory,
        #                             f"{self.multiworld.get_out_file_name_base(self.player)}{
        #                             aprac2.patch_file_ending}")
        # aprac2.write(rom_path)

        # def get_options_as_dict(self) -> Dict[str, Any]:
        #    return self.options.as_dict(
        #             "death_link",
        #             "starting_weapons",
        #    )
        #
        # def fill_slot_data(self) -> Mapping[str, Any]:
        #    return self.get_options_as_dict()

    # def post_fill(self) -> None:
    #    from Utils import visualize_regions
    #    visualize_regions(self.multiworld.get_region("Menu", self.player), f"{self.player_name}_world.puml",
    #                      regions_to_highlight=self.multiworld.get_all_state(False).reachable_regions[
    #                          self.player])
