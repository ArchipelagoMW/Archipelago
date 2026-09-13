from collections.abc import Mapping
from typing import Any

from entrance_rando import randomize_entrances, disconnect_entrance_for_randomization, EntranceType
from worlds.AutoWorld import World

# from Utils import visualize_regions

from . import constants
from . import locations, regions, rules, web_world
from . import (
    options as tomba_options,
)
from .constants import Regions
from .locations import LocationHandler
from .items import ItemHandler, TombaItem
from .regions import get_randomizable_doors


class TombaWorld(World):
    """
    Tomba! is a platform/adventure/puzzle game for the PSX
    """

    game = constants.GAME
    web = web_world.APQuestWebWorld()

    options_dataclass = tomba_options.TombaOptions
    options: tomba_options.TombaOptions

    location_name_to_id = LocationHandler.name_to_id
    item_name_to_id = ItemHandler.name_to_id

    origin_region_name = Regions.VILLAGE_OF_ALL_BEGINNINGS

    entrance_pairings: dict[str, dict[int, tuple[int, int, int]]]

    explicit_indirect_conditions = True

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        ItemHandler.create_all_items(self)

    def create_item(self, name: str) -> TombaItem:
        return ItemHandler.create_item(self, name)

    def connect_entrances(self):
        self.entrance_pairings = {}
        if self.options.entrance_randomization:
            doors = get_randomizable_doors(self.player)
            by_name = {door.name: door for door in doors} | {door.back_name: door for door in doors}

            # Disconnects existing entrances
            for door in doors:
                one_way_target_name = None

                entrance = self.get_entrance(door.name)
                entrances = [entrance]

                if entrance.randomization_type is EntranceType.TWO_WAY:
                    # We disconnect the return edge too
                    entrances.append(self.get_entrance(door.back_name))
                else:
                    one_way_target_name = door.back_name

                for entrance in entrances:
                    disconnect_entrance_for_randomization(entrance, one_way_target_name=one_way_target_name)

            placement = randomize_entrances(self, coupled=True, target_group_lookup={0: [0]})

            for pairing in placement.pairings:
                source, target = pairing

                # print(f"{source} -> {target}")

                # Fetch the paired doors
                source_door = by_name[source]
                target_door = by_name[target]

                # Fetch the correct source section and exit ID
                # Depending on if the source is the forward or backward direction from its door
                source_section = source_door.source
                start_id = source_door.start_id
                if not source_door.is_forward(source):
                    source_section = source_door.target
                    start_id = source_door.back_start_id

                # Fetch the correct target section and entry ID
                # Depending on if the target is the forward or backward direction from its door
                target_section = target_door.source
                end_id = target_door.back_end_id
                if not target_door.is_forward(target):
                    target_section = target_door.target
                    end_id = target_door.end_id

                assert start_id is not None
                assert end_id is not None

                section_key = source_section.network_key()
                if section_key not in self.entrance_pairings:
                    self.entrance_pairings[section_key] = {}

                self.entrance_pairings[section_key][start_id] = (
                    target_section.area_id,
                    target_section.section_id,
                    end_id,
                )

            # print("RE output:")
            # print(self.entrance_pairings)

        # visualize_regions(self.get_region("Menu"), "tomba_debug.dot")

    def get_filler_item_name(self) -> str:
        return ItemHandler.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = self.options.as_dict(
            "bell_warp",
            "keep_blackjack",
            "emulator",
            "optional_randomized",
            "bonus_chests_randomized",
            "cleared_event_rewards",
            "chick_amount",
            "deathlink",
            "god_mode",
            "entrance_randomization",
            "fast_motocross_retry",
        )

        slot_data["world_version"] = self.world_version.as_simple_string()

        slot_data["entrance_pairings"] = self.entrance_pairings

        return slot_data
