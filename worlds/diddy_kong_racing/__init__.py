from __future__ import annotations

from typing import Any

from BaseClasses import Item, ItemClassification, MultiWorld, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, launch_subprocess, Type
from .DoorUnlocks import place_door_unlock_items, set_door_unlock_requirements, vanilla_door_unlock_info_list
from .Items import ALL_ITEM_TABLE, DiddyKongRacingItem, ITEM_NAME_GROUPS
from .Locations import ALL_LOCATION_TABLE
from .Names import ItemName, LocationName, RegionName
from .Options import DiddyKongRacingOptions, OPTION_GROUPS
from .Regions import connect_regions, connect_track_regions, create_regions, reconnect_found_entrance
from .Rules import set_door_unlock_rules, set_region_access_rules, set_race_2_location_rules, set_rules


def run_client():
    from worlds.diddy_kong_racing.DKRClient import main
    launch_subprocess(main)


components.append(Component("Diddy Kong Racing Client", func=run_client, component_type=Type.CLIENT))


class DiddyKongRacingWeb(WebWorld):
    setup = Tutorial("Setup Diddy Kong Racing",
                     """A guide to setting up Archipelago Diddy Kong Racing on your computer.""",
                     "English",
                     "setup_en.md",
                     "setup/en",
                     ["zakwiz"])

    tutorials = [setup]
    option_groups = OPTION_GROUPS


class DiddyKongRacingWorld(World):
    """Diddy Kong Racing is a kart racing game with a story mode, complete with bosses and hidden collectibles."""

    game = "Diddy Kong Racing"
    apworld_version = "DKRv1.1.3"
    web = DiddyKongRacingWeb()
    topology_preset = True
    item_name_to_id = {}

    for name, data in ALL_ITEM_TABLE.items():
        item_name_to_id[name] = data.dkr_id

    location_name_to_id = {name: data.dkr_id for name, data in ALL_LOCATION_TABLE.items()}

    item_name_groups = ITEM_NAME_GROUPS
    options_dataclass = DiddyKongRacingOptions
    options: DiddyKongRacingOptions
    origin_region_name: str = RegionName.TIMBERS_ISLAND
    slot_data: dict[str, Any] = {}
    found_entrances_datastorage_key: list[str] = []

    def __init__(self, world: MultiWorld, player: int) -> None:
        super(DiddyKongRacingWorld, self).__init__(world, player)
        self.track_versions: list[bool]
        self.music: list[int] = list(range(20))
        self.entrance_order: list[int] = list(range(20))
        self.door_unlock_requirements: list[int] = [0] * len(vanilla_door_unlock_info_list)

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)

    def create_items(self) -> None:
        for name, dkr_id in ALL_ITEM_TABLE.items():
            if not self.is_item_pre_filled(name):
                for _ in range(dkr_id.count):
                    item = self.create_item(name)
                    self.multiworld.itempool.append(item)

        # Skip for Universal Tracker, this will be done from slot_data
        if not hasattr(self.multiworld, "generation_is_fake"):
            set_door_unlock_requirements(self)
            place_door_unlock_items(self)

    def set_rules(self) -> None:
        set_rules(self)

    def generate_basic(self) -> None:
        self.set_track_versions()
        self.set_music()

    def pre_fill(self) -> None:
        if self.is_ffl_unused():
            future_fun_land_balloon = self.create_item(ItemName.FUTURE_FUN_LAND_BALLOON)
            for ffl_exit in self.multiworld.get_region(RegionName.FUTURE_FUN_LAND, self.player).exits:
                if ffl_exit.connected_region.name != RegionName.TIMBERS_ISLAND:
                    for ffl_location in ffl_exit.connected_region.locations:
                        self.place_locked_item(ffl_location.name, future_fun_land_balloon)

        if not self.options.shuffle_wizpig_amulet:
            wizpig_amulet_item = self.create_item(ItemName.WIZPIG_AMULET_PIECE)
            self.place_locked_item(LocationName.TRICKY_2, wizpig_amulet_item)
            self.place_locked_item(LocationName.BLUEY_2, wizpig_amulet_item)
            self.place_locked_item(LocationName.BUBBLER_2, wizpig_amulet_item)
            self.place_locked_item(LocationName.SMOKEY_2, wizpig_amulet_item)

        if not self.options.shuffle_tt_amulet:
            tt_amulet_item = self.create_item(ItemName.TT_AMULET_PIECE)
            self.place_locked_item(LocationName.FIRE_MOUNTAIN, tt_amulet_item)
            self.place_locked_item(LocationName.ICICLE_PYRAMID, tt_amulet_item)
            self.place_locked_item(LocationName.DARKWATER_BEACH, tt_amulet_item)
            self.place_locked_item(LocationName.SMOKEY_CASTLE, tt_amulet_item)

    def fill_slot_data(self) -> dict[str, Any]:
        dkr_options: dict[str, Any] = {
            "apworld_version": self.apworld_version,
            "player_name": self.multiworld.player_name[self.player],
            "seed": self.random.randint(12212, 69996),
            "victory_condition": self.options.victory_condition.value,
            "shuffle_wizpig_amulet": "true" if self.options.shuffle_wizpig_amulet else "false",
            "shuffle_tt_amulet": "true" if self.options.shuffle_tt_amulet else "false",
            "open_worlds": "true" if self.options.open_worlds else "false",
            "door_requirement_progression": self.options.door_requirement_progression.value,
            "maximum_door_requirement": self.options.maximum_door_requirement.value,
            "shuffle_door_requirements": "true" if self.options.shuffle_door_requirements.value else "false",
            "door_unlock_requirements": self.door_unlock_requirements,
            "shuffle_race_entrances": "true" if self.options.shuffle_race_entrances else "false",
            "entrance_order": self.entrance_order,
            "boss_1_regional_balloons": self.options.boss_1_regional_balloons.value,
            "boss_2_regional_balloons": self.options.boss_2_regional_balloons.value,
            "wizpig_1_amulet_pieces": self.options.wizpig_1_amulet_pieces.value,
            "wizpig_2_amulet_pieces": self.options.wizpig_2_amulet_pieces.value,
            "wizpig_2_balloons": self.options.wizpig_2_balloons.value,
            "randomize_character_on_map_change": "true" if self.options.randomize_character_on_map_change else "false",
            "track_versions": self.track_versions,
            "music": self.music,
            "power_up_balloon_type": self.options.power_up_balloon_type.value,
            "skip_trophy_races": "true" if self.options.skip_trophy_races else "false"
        }

        return dkr_options

    def is_item_pre_filled(self, item_name: str) -> bool:
        if self.is_ffl_unused() and item_name == ItemName.FUTURE_FUN_LAND_BALLOON:
            return True

        if not self.options.shuffle_wizpig_amulet and item_name == ItemName.WIZPIG_AMULET_PIECE:
            return True

        if not self.options.shuffle_tt_amulet and item_name == ItemName.TT_AMULET_PIECE:
            return True

        return False

    def create_item(self, item_name: str) -> Item:
        item = ALL_ITEM_TABLE.get(item_name)

        item_classification = ItemClassification.progression
        if self.options.victory_condition.value != 1:
            if item_name == ItemName.TT_AMULET_PIECE:
                item_classification = ItemClassification.filler

        created_item = DiddyKongRacingItem(
            self.item_id_to_name[item.dkr_id],
            item_classification,
            item.dkr_id,
            self.player
        )

        return created_item

    def create_event_item(self, name: str) -> Item:
        created_item = DiddyKongRacingItem(name, ItemClassification.progression, None, self.player)

        return created_item

    def place_locked_item(self, location_name: str, item: Item) -> None:
        self.multiworld.get_location(location_name, self.player).place_locked_item(item)

    def is_ffl_unused(self) -> bool:
        return self.options.victory_condition.value == 0 and not self.options.open_worlds

    def set_track_versions(self) -> None:
        num_tracks = 20
        if self.options.track_version.value == 0:
            self.track_versions = [False] * num_tracks
        elif self.options.track_version.value == 1:
            self.track_versions = [True] * num_tracks
        else:
            self.track_versions = []
            for _ in range(num_tracks):
                self.track_versions.append(bool(self.random.getrandbits(1)))

    def set_music(self) -> None:
        if self.options.randomize_music.value:
            self.random.shuffle(self.music)

    # For Universal Tracker
    def interpret_slot_data(self, slot_data: dict[str, Any]) -> None:
        self.entrance_order = slot_data["entrance_order"]
        connect_track_regions(self)
        self.door_unlock_requirements = slot_data["door_unlock_requirements"]
        place_door_unlock_items(self)
        set_region_access_rules(self)
        set_door_unlock_rules(self)
        set_race_2_location_rules(self)

    # For Universal Tracker
    def reconnect_found_entrances(self, found_key: str, data_storage_value: Any) -> None:
        if data_storage_value:
            reconnect_found_entrance(self, found_key)
