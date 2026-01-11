import json
import os
import re
from typing import List, Any, Dict

from BaseClasses import Region, Tutorial, ItemClassification, CollectionState, Callable, LocationProgressType, \
    MultiWorld, Item
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule
from worlds.LauncherComponents import launch_subprocess, components, Component, Type

from .Items import FF12OpenWorldItem, item_data_table, FF12OW_BASE_ID, item_table, filler_items, filler_weights
from .Locations import FF12OpenWorldLocation, location_data_table, location_table
from .Options import FF12OpenWorldGameOptions
from .Regions import region_data_table
from .Rules import rule_data_table
from .Events import event_data_table, FF12OpenWorldEventData
from .RuleLogic import state_has_characters


def launch_client(*args):
    from .Client import launch
    launch_subprocess(launch, name="FF12 Open World Client", args=args)


components.append(Component("FF12 Open World Client", "FF12OpenWorldClient",
                            func=launch_client, component_type=Type.CLIENT,
                            game_name="Final Fantasy 12 Open World", supports_uri=True))

FF12OW_VERSION = "0.5.3"
character_names = ["Vaan", "Ashe", "Fran", "Balthier", "Basch", "Penelo"]


class FF12OpenWorldWebWorld(WebWorld):
    theme = "ocean"

    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Final Fantasy 12 Open World multiworld.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Bartz24"]
    )]


class FF12OpenWorldWorld(World):
    """TODO"""

    game = "Final Fantasy 12 Open World"
    data_version = 3
    web = FF12OpenWorldWebWorld()
    options_dataclass = FF12OpenWorldGameOptions
    options: FF12OpenWorldGameOptions
    location_name_to_id = location_table
    item_name_to_id = item_table

    ut_can_gen_without_yaml = True

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.selected_treasures = []
        self.used_items: set[str] = set()
        self.character_order = list(range(6))
        # Dictionary of excluded location names to their item name and count
        self.excluded_locations: Dict[str, tuple[str, int]] = {}
        self.re_gen_data: Dict[str, Any] = {}

    def create_item(self, name: str) -> FF12OpenWorldItem:
        return FF12OpenWorldItem(name, item_data_table[name].classification, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        self.used_items.clear()
        item_pool: List[FF12OpenWorldItem] = []
        progression_items = [name for name, data in item_data_table.items()
                             if data.classification & ItemClassification.progression and
                             name != "Writ of Transit"]
        if self.options.bahamut_unlock == "random_location":
            progression_items.append("Writ of Transit")

        for name in progression_items:
            for _ in range(item_data_table[name].duplicateAmount):
                item_pool.append(self.create_item(name))

        abilities = [name for name, data in item_data_table.items()
                     if item_data_table["Cure"].code <= data.code <= item_data_table["Gil Toss"].code]
        # Select a random 50% to 75% of the abilities
        ability_count = self.multiworld.random.randint(len(abilities) // 2, len(abilities) * 3 // 4)
        selected_abilities = self.multiworld.random.sample(abilities, k=ability_count)
        self.add_to_pool(item_pool, selected_abilities)

        other_useful_items = [name for name, data in item_data_table.items()
                              if data.classification & ItemClassification.useful and name not in abilities]
        self.add_to_pool(item_pool, other_useful_items)

        # Get count of non event locations
        non_events = len([location for location in self.multiworld.get_locations(self.player)
                          if location.name not in event_data_table.keys()])

        filler_count = non_events - len(item_pool)
        if self.options.bahamut_unlock != "random_location":
            filler_count -= 1

        # Add filler items to the pool
        for _ in range(filler_count):
            filler = self.get_filler_item_name()
            self.used_items.add(filler)
            item_pool.append(self.create_item(filler))

        # Set excluded location filler items
        for location_name, _ in self.excluded_locations.items():
            filler = self.get_excluded_filler_item_name(location_name)
            self.used_items.add(filler)

            item_name = filler
            count = item_data_table[filler].amount
            self.excluded_locations[location_name] = (item_name, count)

        self.multiworld.itempool += item_pool

    def add_to_pool(self, item_pool, other_useful_items):
        for name in other_useful_items:
            self.used_items.add(name)
            for _ in range(item_data_table[name].duplicateAmount):
                item_pool.append(self.create_item(name))

    def create_regions(self) -> None:
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Add connections
        for region_name, data in region_data_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_exits(region_data_table[region_name].connecting_regions)

        if len(self.re_gen_data) > 0:
            locations_to_add = self.re_gen_data["re_gen_locations"]
            self.selected_treasures = self.re_gen_data["treasures"]

            # Place randomly selected locations.
            for location_name in locations_to_add:
                if location_name in location_data_table:
                    location_data = location_data_table[location_name]
                    region = self.multiworld.get_region(location_data.region, self.player)

                    # If it's excluded, add it to the excluded locations dictionary with an empty item
                    classification = self.get_loc_classification(location_name)
                    if classification == LocationProgressType.EXCLUDED:
                        self.excluded_locations[location_name] = ("", 0)
                        continue

                    region.add_locations({location_name: location_data.address}, FF12OpenWorldLocation)
                    self.multiworld.get_location(location_name, self.player).progress_type = classification

            # Add events
            for event_name, data in event_data_table.items():
                region = self.multiworld.get_region("Ivalice", self.player)
                region.locations.append(FF12OpenWorldLocation(self.player, event_name, None, region))
            return

        # Select 255 random treasure type locations.
        treasure_names = [name for name, data in location_data_table.items()
                          if data.type == "treasure"]
        locations_to_add = self.multiworld.random.sample(treasure_names,
                                                         k=255)

        self.selected_treasures = [loc for loc in locations_to_add]

        # Select 50% of the random secondary reward locations (2nd and 3rd indices).
        secondary_reward_names = [name for name, data in location_data_table.items()
                                  if data.type == "reward" and data.secondary_index > 0]
        locations_to_add += self.multiworld.random.sample(secondary_reward_names,
                                                          k=len(secondary_reward_names) // 2)

        # Select 5-10 random starting inventory locations for each character.
        for character in range(6):
            starting_inventory_names = [name for name, data in location_data_table.items()
                                        if data.type == "inventory" and int(data.str_id) == character]
            locations_to_add += self.multiworld.random.sample(starting_inventory_names,
                                                              k=self.multiworld.random.randint(5, 9))

        # Add first fixed index rewards.
        locations_to_add += [name for name, data in location_data_table.items()
                             if data.type == "reward" and data.secondary_index == 0]

        # Place randomly selected locations.
        for location_name in locations_to_add:
            location_data = location_data_table[location_name]
            region = self.multiworld.get_region(location_data.region, self.player)

            # If it's excluded, add it to the excluded locations dictionary with an empty item
            classification = self.get_loc_classification(location_name)
            if classification == LocationProgressType.EXCLUDED:
                self.excluded_locations[location_name] = ("", 0)
                continue

            region.add_locations({location_name: location_data.address}, FF12OpenWorldLocation)
            self.multiworld.get_location(location_name, self.player).progress_type = classification

        # Add events
        for event_name, data in event_data_table.items():
            region = self.multiworld.get_region("Ivalice", self.player)
            region.locations.append(FF12OpenWorldLocation(self.player, event_name, None, region))

    def get_loc_classification(self, location_name: str) -> LocationProgressType:
        location_data = location_data_table[location_name]

        # Check for special progression locations which unlock Bahamut and must be available for progression.
        if (self.options.bahamut_unlock == "defeat_cid_2" and
                location_name == "Pharos of Ridorana - Defeat Famfrit and Cid 2 Reward (1)"):
            return LocationProgressType.DEFAULT
        if (self.options.bahamut_unlock == "collect_pinewood_chops" and
                location_name == "Archades - Sandalwood Chop Reward (1)"):
            return LocationProgressType.DEFAULT
        if (self.options.bahamut_unlock == "collect_espers" and
                location_name == "Clan Hall - Clan Esper: Control 13 Reward (1)"):
            return LocationProgressType.DEFAULT

        if location_data.type == "treasure" and not self.options.include_treasures:
            return LocationProgressType.EXCLUDED
        if location_data.type == "reward":
            if 0x9134 <= int(location_data.str_id, 16) <= 0x914F and not self.options.include_chops:
                return LocationProgressType.EXCLUDED
            if 0x9153 <= int(location_data.str_id, 16) <= 0x916A and not self.options.include_black_orbs:
                return LocationProgressType.EXCLUDED
            if 0x9090 <= int(location_data.str_id, 16) <= 0x90AE and not self.options.include_trophy_rare_games:
                return LocationProgressType.EXCLUDED
            if 0x90F9 <= int(location_data.str_id, 16) <= 0x90FE and not self.options.include_trophy_rare_games:
                return LocationProgressType.EXCLUDED
            if re.search(r"Hunt \d+:", location_name) and not self.options.include_hunt_rewards:
                return LocationProgressType.EXCLUDED
            if location_data.str_id == "916D" and not self.options.include_hunt_rewards:  # Flowering Cactoid
                return LocationProgressType.EXCLUDED
            if location_data.str_id == "9172" and not self.options.include_hunt_rewards:  # White Mousse
                return LocationProgressType.EXCLUDED
            if location_data.str_id == "9174" and not self.options.include_hunt_rewards:  # Enkelados
                return LocationProgressType.EXCLUDED
            if location_data.str_id == "9177" and not self.options.include_hunt_rewards:  # Vorpal Bunny
                return LocationProgressType.EXCLUDED
            if location_data.str_id == "9178" and not self.options.include_hunt_rewards:  # Croakadile
                return LocationProgressType.EXCLUDED
            if location_data.str_id == "9179" and not self.options.include_hunt_rewards:  # Lindwyrm
                return LocationProgressType.EXCLUDED
            if location_data.str_id == "917B" and not self.options.include_hunt_rewards:  # Orthros
                return LocationProgressType.EXCLUDED
            if location_data.str_id == "917F" and not self.options.include_hunt_rewards:  # Fafnir
                return LocationProgressType.EXCLUDED
            if location_data.str_id == "9180" and not self.options.include_hunt_rewards:  # Marilith
                return LocationProgressType.EXCLUDED
            if location_data.str_id == "9181" and not self.options.include_hunt_rewards:  # Vyraal
                return LocationProgressType.EXCLUDED
            if "Clan Rank:" in location_name and not self.options.include_clan_hall_rewards:
                return LocationProgressType.EXCLUDED
            if "Clan Boss:" in location_name and not self.options.include_clan_hall_rewards:
                return LocationProgressType.EXCLUDED
            if "Clan Esper:" in location_name and not self.options.include_clan_hall_rewards:
                return LocationProgressType.EXCLUDED
        return location_data.classification

    def get_filler_item_name(self) -> str:
        filler = self.multiworld.random.choices(filler_items, weights=filler_weights)[0]
        if filler == "Seitengrat" and not self.options.allow_seitengrat:
            filler = "Dhanusha"
        return filler

    # Special filler item for excluded locations which are limited based on the type and index of the location.
    def get_excluded_filler_item_name(self, location_name: str) -> str:
        location = location_data_table[location_name]

        valid = False
        filler = ""
        while not valid:
            filler = self.get_filler_item_name()
            if location.type == "reward":
                # The first index of a reward location must be gil.
                if location.secondary_index == 0:
                    valid = item_data_table[filler].code >= item_data_table["1 Gil"].code
                    continue
                # The second index of a reward location must not be gil.
                else:
                    valid = item_data_table[filler].code < item_data_table["1 Gil"].code
                    continue
            elif location.type == "inventory":
                # Inventory locations cannot have gil.
                valid = item_data_table[filler].code < item_data_table["1 Gil"].code
                continue

            valid = True

        return filler

    def set_rules(self) -> None:
        # Set location rules
        for location in self.multiworld.get_locations(self.player):
            add_rule(location, self.create_rule(location.name))
            if self.options.character_progression_scaling:
                add_rule(location, self.create_chara_rule(location.name))

        # Set event locked items
        for event_name, event_data in event_data_table.items():
            location = self.multiworld.get_location(event_name, self.player)
            location.place_locked_item(self.create_event(event_data.item))

        if self.options.bahamut_unlock == "defeat_cid_2":
            self.multiworld.get_location("Pharos of Ridorana - Defeat Famfrit and Cid 2 Reward (1)", self.player).place_locked_item(
                self.create_item("Writ of Transit"))
        elif self.options.bahamut_unlock == "collect_pinewood_chops":
            self.multiworld.get_location("Archades - Sandalwood Chop Reward (1)", self.player).place_locked_item(
                self.create_item("Writ of Transit"))
        elif self.options.bahamut_unlock == "collect_espers":
            self.multiworld.get_location("Clan Hall - Clan Esper: Control 13 Reward (1)", self.player).place_locked_item(
                self.create_item("Writ of Transit"))

        # TODO: Disabled for now. May add back in later if needed.
        '''
        # Fill excluded locations with local locked items
        excluded = [location for location in self.multiworld.get_locations(self.player)
                    if location.progress_type == LocationProgressType.EXCLUDED and location.item is None]
        Shuffle the excluded locations
        self.multiworld.random.shuffle(excluded)

        # Place filler trophies in excluded locations
        trophy_fillers = [name for name, data in item_data_table.items()
                          if data.classification == ItemClassification.filler and name.endswith(" Trophy")]

        for location in excluded:
            # If there are still trophy fillers to place, place one
            if trophy_fillers:
                location.place_locked_item(self.create_item(trophy_fillers.pop()))
            else:
                location.place_locked_item(self.create_item(self.get_filler_item_name()))
        '''

        # Completion condition.
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_rule(self, location_name: str) -> Callable[[CollectionState], bool]:
        return lambda state: rule_data_table[location_name](state, self.player)

    def create_chara_rule(self, location_name: str) -> Callable[[CollectionState], bool]:
        if location_name in location_data_table.keys():
            return lambda state: state_has_characters(state,
                                                      location_data_table[location_name].difficulty,
                                                      self.player)
        elif location_name in event_data_table.keys():
            return lambda state: state_has_characters(state,
                                                      event_data_table[location_name].difficulty,
                                                      self.player)

    def create_event(self, event_item: str) -> FF12OpenWorldItem:
        name = event_item
        if name in character_names:
            name = character_names[self.character_order[character_names.index(name)]]
        return FF12OpenWorldItem(name, ItemClassification.progression, None, self.player)

    def generate_early(self) -> None:
        if self.options.shuffle_main_party:
            self.multiworld.random.shuffle(self.character_order)

        # Universal tracker stuff, shouldn't do anything in standard gen
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if self.game in self.multiworld.re_gen_passthrough:
                self.re_gen_data = self.multiworld.re_gen_passthrough[self.game]
                self.character_order = self.re_gen_data["characters"]
                options = self.re_gen_data["options"]
                self.options.shuffle_main_party = options["shuffle_main_party"]
                self.options.character_progression_scaling = options["character_progression_scaling"]
                self.options.include_treasures = options["include_treasures"]
                self.options.include_chops = options["include_chops"]
                self.options.include_black_orbs = options["include_black_orbs"]
                self.options.include_trophy_rare_games = options["include_trophy_rare_games"]
                self.options.include_hunt_rewards = options["include_hunt_rewards"]
                self.options.include_clan_hall_rewards = options["include_clan_hall_rewards"]
                self.options.allow_seitengrat = options["allow_seitengrat"]
                self.options.bahamut_unlock = options["bahamut_unlock"]

    def generate_output(self, output_directory: str) -> None:
        spheres: List[Dict[str, Any]] = []
        cur_sphere = 0
        for locations in self.multiworld.get_spheres():
            for loc in locations:
                # Skip locations that are not for this player
                if loc.player != self.player:
                    continue

                if loc.name in location_data_table.keys():
                    spheres.append({"name": loc.name,
                                    "id": location_data_table[loc.name].str_id,
                                    "index": location_data_table[loc.name].secondary_index,
                                    "sphere": cur_sphere})
                elif loc.name in event_data_table.keys():
                    spheres.append({"name": loc.name,
                                    "id": loc.name[:loc.name.index(" Event ")],
                                    "item": event_data_table[loc.name].item,
                                    "sphere": cur_sphere})
            cur_sphere += 1

        seed_name = self.multiworld.seed_name + "_" + self.multiworld.get_player_name(self.player)
        data = {
            "seed": seed_name,  # to identify the seed
            "type": "archipelago",  # to identify the seed type
            "archipelago": {
                "version": FF12OW_VERSION,
                "used_items": list(self.used_items),  # Lets the seed generator fill shops with unused items
                # Store selected treasures for tracking
                "treasures": [
                    {"map": location_data_table[loc].str_id, "index": location_data_table[loc].secondary_index}
                    for loc in self.selected_treasures],
                "character_order": self.character_order,
                "allow_seitengrat": self.options.allow_seitengrat.value,
                "spheres": spheres,
                "filler_item_placements": [
                    {"id": location_data_table[loc].str_id,
                     "index": location_data_table[loc].secondary_index,
                     "item": self.excluded_locations[loc][0],
                     "amount": self.excluded_locations[loc][1]}
                    for loc in self.excluded_locations.keys()
                ]
            }
        }
        mod_name = self.multiworld.get_out_file_name_base(self.player)
        with open(os.path.join(output_directory, mod_name + ".json"), "w") as f:
            json.dump(data, f)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "treasures": self.selected_treasures,
            "re_gen_locations": [location.name for location in self.multiworld.get_locations(self.player)],
            "characters": self.character_order,
            "options": {
                "shuffle_main_party": self.options.shuffle_main_party.value,
                "character_progression_scaling": self.options.character_progression_scaling.value,
                "include_treasures": self.options.include_treasures.value,
                "include_chops": self.options.include_chops.value,
                "include_black_orbs": self.options.include_black_orbs.value,
                "include_trophy_rare_games": self.options.include_trophy_rare_games.value,
                "include_hunt_rewards": self.options.include_hunt_rewards.value,
                "include_clan_hall_rewards": self.options.include_clan_hall_rewards.value,
                "allow_seitengrat": self.options.allow_seitengrat.value,
                "bahamut_unlock": self.options.bahamut_unlock.value
            }
        }

    # From Tunic implementation
    # For the universal tracker, doesn't get called in standard gen
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        return slot_data
