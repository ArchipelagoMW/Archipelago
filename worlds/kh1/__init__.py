import logging
import re
from math import ceil

from BaseClasses import ItemClassification, Tutorial
from Fill import fill_restrictive
from worlds.AutoWorld import WebWorld, World
from .Items import KH1Item, event_item_table, get_items_by_group, item_name_groups, item_table
from .Locations import get_locations_by_group, location_name_groups, location_table
from .Options import KH1Options, kh1_option_groups
from .Regions import connect_entrances, create_regions
from .Rules import set_rules
from .GenerateJSON import generate_json
from . import Data
from .Data import CHAR_TO_KH, CHEST_KEYBLADES, POSSIBLE_SPELL_COSTS
from .Data import VANILLA_SPELL_COSTS, VANILLA_SPELL_EFFECTIVENESS, VANILLA_SPELL_LEVEL_COSTS
from .Data import VANILLA_LEVEL_UP_STATS, WORLD_KEY_ITEMS


POOL_ITEM_GROUPS = ("Key Items", "Spells", "Worlds", "Trinities", "Cups", "Summons", "Abilities", "Keyblades",
                    "Accessories", "Weapons", "Torn Pages")
STARTING_WORLD_CANDIDATES = ("Wonderland", "Olympus Coliseum", "Deep Jungle", "Agrabah", "Monstro", "Halloween Town",
                             "Neverland", "Hollow Bastion", "Atlantica", "Destiny Islands")
STARTING_TOOLS = ["Scan", "Dodge Roll"]
DOOR_KEY_LOCATIONS = {
    "sephiroth": "Olympus Coliseum Defeat Sephiroth Ansem's Report 12",
    "unknown": "Hollow Bastion Defeat Unknown Ansem's Report 13",
    "final_rest": "End of the World Final Rest Chest",
}


class KH1Web(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Kingdom Hearts Randomizer software on your computer. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "kh1_en.md",
        "kh1/en",
        ["Gicu"],
    )]
    option_groups = kh1_option_groups


class KH1World(World):
    """
    Kingdom Hearts is an action RPG following Sora on his journey
    through many worlds to find Riku and Kairi.
    """
    game = "Kingdom Hearts"
    options_dataclass = KH1Options
    options: KH1Options
    topology_present = True
    web = KH1Web()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups
    fillers = {
        **get_items_by_group("Consumables"),
        **get_items_by_group("Camping Items"),
        **get_items_by_group("Stat Ups"),
    }

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.level_check_locations = None
        self.starting_accessory_locations = None
        self.starting_accessories = None
        self.accessory_locations = None
        self.accessory_augments = None
        self.ap_costs = None
        self.mp_costs = None
        self.spell_effectiveness = None

    def generate_early(self):
        self.sort_lucky_emblem_counts()
        self.sort_raft_material_counts()
        self.force_bundles_for_stacking_world_items()
        self.force_puppy_value_for_vanilla_puppies()
        self.exclude_content()

    def create_regions(self):
        create_regions(self)

    def connect_entrances(self):
        connect_entrances(self)

    def create_items(self):
        self.place_final_door_key()
        self.place_victory()
        self.place_vanilla_emblem_pieces()
        self.place_vanilla_postcards()
        self.place_vanilla_puppies()

        starting_worlds = self.give_starting_worlds()
        starting_tools = self.give_starting_tools()
        self.place_starting_accessories()
        self.place_accessory_augments()
        self.place_level_up_stats()

        item_counts = self.build_base_item_counts()
        self.apply_randomize_puppies(item_counts)
        self.apply_extra_shared_abilities(item_counts)
        self.apply_end_of_the_world_unlock(item_counts)
        self.apply_exp_zero_in_pool(item_counts)
        self.apply_randomize_postcards(item_counts)
        self.apply_synthesis_materials(item_counts)
        self.apply_raft_materials(item_counts)
        self.apply_lucky_emblems(item_counts)
        self.apply_final_rest_door_key(item_counts)
        self.apply_randomize_emblem_pieces(item_counts)
        self.apply_additional_slots(item_counts)
        self.remove_items(item_counts, starting_worlds + starting_tools + self.get_starting_accessories())
        self.apply_augment_abilities_from_pool(item_counts)
        self.apply_bundles(item_counts)
        self.apply_stacking_world_items(item_counts)
        self.fill_item_pool(item_counts)

    def set_rules(self):
        set_rules(self)

    def pre_fill(self):
        if self.options.level_check_items == "stats_and_abilities":
            self.fill_level_checks_with_stats_and_abilities()

    def generate_output(self, output_directory: str):
        generate_json(self, output_directory)

    def create_item(self, name: str) -> KH1Item:
        return KH1Item(name, self.get_item_classification(name), item_table[name].code, self.player)

    def create_event(self, name: str) -> KH1Item:
        data = event_item_table[name]
        return KH1Item(name, data.classification, data.code, self.player)

    def get_item_classification(self, name: str) -> ItemClassification:
        if name in CHEST_KEYBLADES.values() and not self.options.keyblades_unlock_chests:
            return ItemClassification.useful
        if "Accessories" in item_table[name].groups and not self.options.accessory_augments:
            return ItemClassification.useful
        return item_table[name].classification

    def get_filler_item_name(self) -> str:
        weights = [data.weight for data in self.fillers.values()]
        return self.random.choices(list(self.fillers), weights)[0]

    def log_option_change(self, option_name: str, old_value, new_value) -> None:
        logging.info(f"{self.player_name}'s value {old_value} for \"{option_name}\" was invalid. "
                     f"Setting \"{option_name}\" to {new_value}")

    def sort_lucky_emblem_counts(self) -> None:
        eotw = self.options.required_lucky_emblems_eotw
        door = self.options.required_lucky_emblems_door
        in_pool = self.options.lucky_emblems_in_pool
        eotw_uses_emblems = self.options.end_of_the_world_unlock == "lucky_emblems"
        door_uses_emblems = self.options.final_rest_door_key == "lucky_emblems"
        if eotw_uses_emblems and door_uses_emblems:
            self.sort_option_values([eotw, door, in_pool])
        elif eotw_uses_emblems:
            self.sort_option_values([eotw, in_pool])
        elif door_uses_emblems:
            self.sort_option_values([door, in_pool])

    def sort_raft_material_counts(self) -> None:
        options = [self.options.day_1_materials, self.options.day_2_materials, self.options.materials_in_pool]
        self.sort_option_values(options)

    def sort_option_values(self, options: list) -> None:
        sorted_values = sorted(option.value for option in options)
        for option, value in zip(options, sorted_values):
            if option.value != value:
                self.log_option_change(option.display_name, option.value, value)
                option.value = value

    def force_bundles_for_stacking_world_items(self) -> None:
        if not self.options.stacking_world_items:
            return
        bundles = (
            self.options.halloween_town_key_item_bundle,
            self.options.slides_bundle,
            self.options.evidence_bundle,
        )
        for bundle in bundles:
            if not bundle:
                self.log_option_change(bundle.display_name, False, True)
                bundle.value = True

    def force_puppy_value_for_vanilla_puppies(self) -> None:
        if not self.options.randomize_puppies and self.options.puppy_value.value != 3:
            self.log_option_change("Puppy Value", self.options.puppy_value.value, 3)
            self.options.puppy_value.value = 3


    def exclude_content(self) -> None:
        for group in self.options.excluded_content.value:
            self.options.exclude_locations.value.update(location_name_groups[group])

    def place_final_door_key(self) -> None:
        location_name = self.get_final_door_key_location()
        if location_name:
            self.get_location(location_name).place_locked_item(self.create_item("Final Door Key"))

    def get_final_door_key_location(self) -> str | None:
        door_key = self.options.final_rest_door_key.current_key
        if door_key in DOOR_KEY_LOCATIONS:
            return DOOR_KEY_LOCATIONS[door_key]
        if door_key == "postcards":
            return f"Traverse Town Mail Postcard {self.options.required_postcards.value:02} Event"
        if door_key == "puppies":
            required_puppies = self.options.required_puppies.value
            if required_puppies in (50, 99):
                return f"Traverse Town Piano Room Return {required_puppies} Puppies Reward 2"
            return f"Traverse Town Piano Room Return {required_puppies} Puppies"
        return None

    def place_victory(self) -> None:
        self.get_location("Final Ansem").place_locked_item(self.create_event("Victory"))

    def place_vanilla_emblem_pieces(self) -> None:
        if self.options.randomize_emblem_pieces:
            return
        for emblem_piece in sorted(item_name_groups["Emblem Pieces"]):
            location = self.get_location(f"Hollow Bastion Entrance Hall {emblem_piece}")
            location.place_locked_item(self.create_item(emblem_piece))

    def place_vanilla_postcards(self) -> None:
        postcard_mode = self.options.randomize_postcards.current_key
        if postcard_mode == "all":
            return
        locations = location_name_groups["Postcard"]
        if postcard_mode == "chests":
            locations = locations - location_name_groups["Chest"]
        for location_name in sorted(locations):
            self.get_location(location_name).place_locked_item(self.create_item("Postcard"))

    def place_vanilla_puppies(self) -> None:
        if self.options.randomize_puppies:
            return
        for location_name in get_locations_by_group("Puppy"):
            self.get_location(location_name).place_locked_item(self.create_item("Puppy"))

    def give_starting_worlds(self) -> list[str]:
        if self.options.starting_worlds.value == 0:
            return []
        candidates = list(STARTING_WORLD_CANDIDATES)
        if self.options.end_of_the_world_unlock == "item":
            candidates.append("End of the World")
        starting_worlds = self.random.sample(candidates, min(self.options.starting_worlds.value, len(candidates)))
        for world_name in starting_worlds:
            self.multiworld.push_precollected(self.create_item(world_name))
        return starting_worlds

    def give_starting_tools(self) -> list[str]:
        if not self.options.starting_tools:
            return []
        for tool in STARTING_TOOLS:
            self.multiworld.push_precollected(self.create_item(tool))
        return STARTING_TOOLS

    def place_starting_accessories(self) -> None:
        for location_name, accessory in zip(self.get_starting_accessory_locations(), self.get_starting_accessories()):
            self.get_location(location_name).place_locked_item(self.create_item(accessory))

    def place_accessory_augments(self) -> None:
        for augment, location_name in zip(self.get_accessory_augments(), self.get_accessory_locations()):
            self.get_location(location_name).place_locked_item(self.create_item(augment))

    def place_level_up_stats(self) -> None:
        stats = list(VANILLA_LEVEL_UP_STATS.values())
        if self.options.level_stats == "shuffle":
            self.random.shuffle(stats)
        for level, stat in zip(VANILLA_LEVEL_UP_STATS, stats):
            self.get_location(f"Level {level:03} (Slot 1)").place_locked_item(self.create_item(stat))

    def build_base_item_counts(self) -> dict[str, int]:
        return {
            name: data.max_quantity
            for name, data in item_table.items()
            if any(group in POOL_ITEM_GROUPS for group in data.groups)
        }

    def apply_randomize_puppies(self, item_counts: dict[str, int]) -> None:
        if self.options.randomize_puppies:
            item_counts["Puppy"] = ceil(99 / self.options.puppy_value.value)
        else:
            item_counts["Puppy"] = 0

    def apply_extra_shared_abilities(self, item_counts: dict[str, int]) -> None:
        if self.options.extra_shared_abilities:
            item_counts["High Jump"] = 3
            item_counts["Progressive Glide"] = 4

    def apply_end_of_the_world_unlock(self, item_counts: dict[str, int]) -> None:
        if self.options.end_of_the_world_unlock != "item":
            item_counts["End of the World"] = 0

    def apply_exp_zero_in_pool(self, item_counts: dict[str, int]) -> None:
        if not self.options.exp_zero_in_pool:
            item_counts["EXP Zero"] = 0

    def apply_randomize_postcards(self, item_counts: dict[str, int]) -> None:
        postcard_mode = self.options.randomize_postcards.current_key
        if postcard_mode == "vanilla":
            item_counts["Postcard"] = 0
        elif postcard_mode == "chests":
            item_counts["Postcard"] = len(location_name_groups["Postcard"] & location_name_groups["Chest"])

    def apply_synthesis_materials(self, item_counts: dict[str, int]) -> None:
        item_counts["Mythril"] = self.options.mythril_in_pool.value
        item_counts["Orichalcum"] = self.options.orichalcum_in_pool.value

    def apply_raft_materials(self, item_counts: dict[str, int]) -> None:
        item_counts["Raft Materials"] = self.options.materials_in_pool.value

    def apply_lucky_emblems(self, item_counts: dict[str, int]) -> None:
        item_counts["Lucky Emblem"] = self.get_lucky_emblems_in_pool()

    def apply_final_rest_door_key(self, item_counts: dict[str, int]) -> None:
        if self.options.final_rest_door_key == "anywhere":
            item_counts["Final Door Key"] = 1
        else:
            item_counts["Final Door Key"] = 0

    def apply_randomize_emblem_pieces(self, item_counts: dict[str, int]) -> None:
        if not self.options.randomize_emblem_pieces:
            for emblem_piece in item_name_groups["Emblem Pieces"]:
                item_counts[emblem_piece] = 0

    def remove_items(self, item_counts: dict[str, int], names: list[str]) -> None:
        for name in names:
            if name in item_counts:
                item_counts[name] = 0

    def apply_augment_abilities_from_pool(self, item_counts: dict[str, int]) -> None:
        if self.options.augment_abilities_from_pool:
            self.remove_items(item_counts, self.get_accessory_augments())

    def apply_bundles(self, item_counts: dict[str, int]) -> None:
        if self.options.halloween_town_key_item_bundle:
            item_counts["Jack-In-The-Box"] = 0
        if self.options.slides_bundle:
            self.remove_items(item_counts, sorted(item_name_groups["Slides"] - {"Slide 1"}))
        if self.options.evidence_bundle:
            self.remove_items(item_counts, sorted(item_name_groups["Evidence"] - {"Footprints"}))

    def apply_stacking_world_items(self, item_counts: dict[str, int]) -> None:
        if not self.options.stacking_world_items:
            return
        for key_item, world_name in WORLD_KEY_ITEMS.items():
            if item_counts[key_item]:
                item_counts[key_item] = 0
                item_counts[world_name] += 1

    def apply_additional_slots(self, item_counts: dict[str, int]) -> None:
        item_counts["Item Slot Increase"] = self.options.additional_item_slots.value
        item_counts["Accessory Slot Increase"] = self.options.additional_accessory_slots.value

    def fill_item_pool(self, item_counts: dict[str, int]) -> None:
        item_pool = [self.create_item(name) for name, count in item_counts.items() for _ in range(count)]
        open_locations = len(self.multiworld.get_unfilled_locations(self.player))
        while len(item_pool) < open_locations:
            item_pool.append(self.create_item(self.get_filler_item_name()))
        self.multiworld.itempool += item_pool

    def get_lucky_emblems_in_pool(self) -> int:
        eotw_uses_emblems = self.options.end_of_the_world_unlock == "lucky_emblems"
        door_uses_emblems = self.options.final_rest_door_key == "lucky_emblems"
        if eotw_uses_emblems or door_uses_emblems:
            return self.options.lucky_emblems_in_pool.value
        return 0

    def get_lucky_emblems_required_for_end_of_the_world(self) -> int:
        if self.options.end_of_the_world_unlock == "lucky_emblems":
            return self.options.required_lucky_emblems_eotw.value
        return -1

    def get_lucky_emblems_required_for_final_rest_door(self) -> int:
        if self.options.final_rest_door_key == "lucky_emblems":
            return self.options.required_lucky_emblems_door.value
        return -1

    def get_level_locations(self) -> list[str]:
        stat_locations = [f"Level {level:03} (Slot 1)" for level in VANILLA_LEVEL_UP_STATS]
        return stat_locations + self.get_level_check_locations()

    def get_level_check_locations(self) -> list[str]:
        if self.level_check_locations is None:
            mode = self.options.level_check_locations.current_key
            if mode == "level_50":
                levels = self.random.sample(range(2, 51), 33)
            elif mode == "level_99":
                levels = self.random.sample(range(2, 100), 33)
            else:
                levels = []
            self.level_check_locations = [f"Level {level:03} (Slot 2)" for level in sorted(levels)]
        return self.level_check_locations

    def get_level_check_item_names(self) -> set[str]:
        sora_abilities = item_name_groups["Abilities"] - item_name_groups["Shared Abilities"]
        return sora_abilities | {"Item Slot Increase", "Accessory Slot Increase"}

    def fill_level_checks_with_stats_and_abilities(self) -> None:
        locations = [self.get_location(name) for name in self.get_level_check_locations()]
        allowed = self.get_level_check_item_names()
        eligible = [item for item in self.multiworld.itempool if item.player == self.player and item.name in allowed]
        self.random.shuffle(eligible)
        items = eligible[:len(locations)]
        if len(items) < len(locations):
            logging.warning(f"{self.player_name} only has {len(items)} stats and abilities for "
                            f"{len(locations)} level checks. The rest can hold any item.")
        placed = {id(item) for item in items}
        self.multiworld.itempool = [item for item in self.multiworld.itempool if id(item) not in placed]
        fill_restrictive(self.multiworld, self.multiworld.get_all_state(), locations, items,
                         single_player_placement=True, lock=True, allow_partial=True, name="KH1 Level Checks")

    def get_starting_accessory_locations(self) -> list[str]:
        if self.starting_accessory_locations is None:
            self.starting_accessory_locations = []
            if self.options.randomize_party_member_starting_accessories:
                candidates = list(get_locations_by_group("Accessory"))
                self.starting_accessory_locations = self.random.sample(candidates, 10)
        return self.starting_accessory_locations

    def get_starting_accessories(self) -> list[str]:
        if self.starting_accessories is None:
            self.starting_accessories = []
            if self.options.randomize_party_member_starting_accessories:
                self.starting_accessories = self.random.sample(list(get_items_by_group("Accessories")), 10)
        return self.starting_accessories

    def get_accessory_locations(self) -> list[str]:
        if self.accessory_locations is None:
            self.accessory_locations = []
            if self.options.accessory_augments:
                self.accessory_locations = list(get_locations_by_group("Augment"))
        return self.accessory_locations

    def get_accessory_augments(self) -> list[str]:
        if self.accessory_augments is None:
            self.accessory_augments = []
            if self.options.accessory_augments:
                candidates = list(get_items_by_group("Augments"))
                self.accessory_augments = self.random.sample(candidates, len(self.get_accessory_locations()))
        return self.accessory_augments

    def get_keyblade_stats(self) -> list[dict[str, int]]:
        keyblade_stats = [
            {stat: int(value) for stat, value in row.items() if stat != "keyblade"} for row in Data.keyblade_stats
        ]
        if self.options.bad_kingdom_key:
            kept, changed = keyblade_stats[:1], keyblade_stats[1:]
        else:
            kept, changed = [], keyblade_stats
        if self.options.keyblade_stats == "randomize":
            self.randomize_keyblade_stats(changed)
        elif self.options.keyblade_stats == "shuffle":
            self.random.shuffle(changed)
        return kept + changed

    def randomize_keyblade_stats(self, keyblade_stats: list[dict[str, int]]) -> None:
        ranges = {
            "STR": self.sorted_range(self.options.keyblade_min_str, self.options.keyblade_max_str),
            "CRR": self.sorted_range(self.options.keyblade_min_crit_rate, self.options.keyblade_max_crit_rate),
            "CRB": self.sorted_range(self.options.keyblade_min_crit_str, self.options.keyblade_max_crit_str),
            "REC": self.sorted_range(self.options.keyblade_min_recoil, self.options.keyblade_max_recoil),
            "MP": self.sorted_range(self.options.keyblade_min_mp, self.options.keyblade_max_mp),
        }
        for stats in keyblade_stats:
            for stat, (low, high) in ranges.items():
                stats[stat] = self.random.randint(low, high)

    def sorted_range(self, minimum_option, maximum_option) -> tuple[int, int]:
        minimum_option.value, maximum_option.value = sorted((minimum_option.value, maximum_option.value))
        return minimum_option.value, maximum_option.value

    def get_ap_costs(self) -> list[dict[str, str | int]]:
        if self.ap_costs is None:
            self.ap_costs = [
                {"Ability Name": row["ability"], "AP Cost": int(row["ap_cost"])} for row in Data.ability_ap_costs
            ]
            mode = self.options.randomize_ap_costs.current_key
            if mode == "shuffle":
                self.shuffle_ap_costs(self.ap_costs)
            elif mode == "randomize":
                self.randomize_ap_costs(self.ap_costs)
            elif mode == "distribute":
                self.distribute_ap_costs(self.ap_costs)
        return self.ap_costs

    def shuffle_ap_costs(self, ap_costs: list[dict[str, str | int]]) -> None:
        costs = [ap_cost["AP Cost"] for ap_cost in ap_costs]
        self.random.shuffle(costs)
        for ap_cost, cost in zip(ap_costs, costs):
            ap_cost["AP Cost"] = cost

    def randomize_ap_costs(self, ap_costs: list[dict[str, str | int]]) -> None:
        for ap_cost in ap_costs:
            ap_cost["AP Cost"] = self.random.randint(self.options.min_ap_cost.value, self.options.max_ap_cost.value)

    def distribute_ap_costs(self, ap_costs: list[dict[str, str | int]]) -> None:
        minimum = self.options.min_ap_cost.value
        maximum = self.options.max_ap_cost.value
        remaining = sum(ap_cost["AP Cost"] for ap_cost in ap_costs) - minimum * len(ap_costs)
        for ap_cost in ap_costs:
            ap_cost["AP Cost"] = minimum
        while remaining > 0:
            ap_cost = self.random.choice(ap_costs)
            if ap_cost["AP Cost"] < maximum:
                amount = self.random.randint(1, min(maximum - ap_cost["AP Cost"], remaining))
                ap_cost["AP Cost"] += amount
                remaining -= amount

    def get_mp_costs(self) -> list[int]:
        if self.mp_costs is None:
            mode = self.options.randomize_spell_mp_costs.current_key
            if mode == "shuffle":
                self.mp_costs = self.shuffled_mp_costs()
            elif mode == "randomize":
                self.mp_costs = self.randomized_mp_costs()
            else:
                self.mp_costs = list(VANILLA_SPELL_LEVEL_COSTS)
        return self.mp_costs

    def shuffled_mp_costs(self) -> list[int]:
        if self.options.individual_spell_level_costs:
            level_costs = list(VANILLA_SPELL_LEVEL_COSTS)
            self.random.shuffle(level_costs)
            return level_costs
        spell_costs = list(VANILLA_SPELL_COSTS)
        self.random.shuffle(spell_costs)
        return self.spread_spell_costs_to_levels(spell_costs)

    def randomized_mp_costs(self) -> list[int]:
        low, high = sorted((self.options.spell_mp_cost_min.value, self.options.spell_mp_cost_max.value))
        possible_costs = [cost for cost in POSSIBLE_SPELL_COSTS if low <= cost <= high]
        if self.options.individual_spell_level_costs:
            return [self.random.choice(possible_costs) for _ in VANILLA_SPELL_LEVEL_COSTS]
        spell_costs = [self.random.choice(possible_costs) for _ in VANILLA_SPELL_COSTS]
        return self.spread_spell_costs_to_levels(spell_costs)

    def spread_spell_costs_to_levels(self, spell_costs: list[int]) -> list[int]:
        level_costs = []
        for cost in spell_costs:
            level_costs += [cost] * 3
        return level_costs

    def get_spell_effectiveness(self) -> list[int]:
        if self.spell_effectiveness is None:
            self.spell_effectiveness = list(VANILLA_SPELL_EFFECTIVENESS)
            if self.options.scaling_spell_potency:
                for i, (effectiveness, cost, vanilla_cost) in enumerate(
                        zip(VANILLA_SPELL_EFFECTIVENESS, self.get_mp_costs(), VANILLA_SPELL_LEVEL_COSTS)):
                    self.spell_effectiveness[i] = max(int(effectiveness * cost / vanilla_cost + 0.5), 1)
        return self.spell_effectiveness

    def get_remote_location_ids(self) -> list[int]:
        remote_location_ids = []
        for location in self.multiworld.get_filled_locations(self.player):
            if location.name == "Final Ansem":
                continue
            location_data = location_table[location.name]
            if self.options.remote_items.current_key == "full":
                if "Accessory" not in location_data.groups and "Augment" not in location_data.groups:
                    remote_location_ids.append(location_data.code)
            elif location.item.player != self.player:
                remote_location_ids.append(location_data.code)
            elif "Synth" in location_data.groups and location.item.name not in item_name_groups["Items"]:
                remote_location_ids.append(location_data.code)
        return remote_location_ids

    def get_synthesis_item_name_byte_arrays(self) -> list[list[int]]:
        byte_arrays = []
        for location in self.multiworld.get_filled_locations(self.player):
            if location.name == "Final Ansem" or "Synth" not in location_table[location.name].groups:
                continue
            item_name = re.sub("[^A-Za-z0-9 ]+", "", location.item.name.replace("Progressive", "Prog"))[:14]
            byte_arrays.append([CHAR_TO_KH[character] for character in item_name])
        return byte_arrays

    def fill_slot_data(self) -> dict:
        return {
            "accessory_augments": bool(self.options.accessory_augments),
            "augment_abilities_from_pool": bool(self.options.augment_abilities_from_pool),
            "auto_attack": bool(self.options.auto_attack),
            "auto_save": bool(self.options.auto_save),
            "bad_kingdom_key": bool(self.options.bad_kingdom_key),
            "beep_hack": bool(self.options.beep_hack),
            "consistent_finishers": bool(self.options.consistent_finishers),
            "cups_standard": int(self.options.cups_standard.value),
            "cups_solo_time_trial": int(self.options.cups_solo_time_trial.value),
            "day_1_materials": int(self.options.day_1_materials.value),
            "day_2_materials": int(self.options.day_2_materials.value),
            "donald_death_link": bool(self.options.donald_death_link),
            "early_skip": bool(self.options.early_skip),
            "end_of_the_world_unlock": str(self.options.end_of_the_world_unlock.current_key),
            "exp_multiplier": int(self.options.exp_multiplier.value) / 16,
            "exp_zero_in_pool": bool(self.options.exp_zero_in_pool),
            "extra_shared_abilities": bool(self.options.extra_shared_abilities),
            "fast_camera": bool(self.options.fast_camera),
            "faster_animations": bool(self.options.faster_animations),
            "final_rest_door_key": str(self.options.final_rest_door_key.current_key),
            "four_by_three": bool(self.options.four_by_three),
            "goofy_death_link": bool(self.options.goofy_death_link),
            "halloween_town_key_item_bundle": bool(self.options.halloween_town_key_item_bundle),
            "slides_bundle": bool(self.options.slides_bundle),
            "evidence_bundle": bool(self.options.evidence_bundle),
            "skip_hundred_acre_wood_minigames": bool(self.options.skip_hundred_acre_wood_minigames),
            "individual_spell_level_costs": bool(self.options.individual_spell_level_costs),
            "interact_in_battle": bool(self.options.interact_in_battle),
            "keyblades_unlock_chests": bool(self.options.keyblades_unlock_chests),
            "level_check_items": str(self.options.level_check_items.current_key),
            "level_check_locations": str(self.options.level_check_locations.current_key),
            "level_stats": str(self.options.level_stats.current_key),
            "logic_difficulty": str(self.options.logic_difficulty.current_key),
            "materials_in_pool": int(self.options.materials_in_pool.value),
            "raft_finish": bool(self.options.raft_finish),
            "max_ap_cost": int(self.options.max_ap_cost.value),
            "min_ap_cost": int(self.options.min_ap_cost.value),
            "mythril_in_pool": int(self.options.mythril_in_pool.value),
            "mythril_price": int(self.options.mythril_price.value),
            "one_hp": bool(self.options.one_hp),
            "orichalcum_in_pool": int(self.options.orichalcum_in_pool.value),
            "orichalcum_price": int(self.options.orichalcum_price.value),
            "puppy_value": int(self.options.puppy_value.value),
            "randomize_ap_costs": str(self.options.randomize_ap_costs.current_key),
            "randomize_emblem_pieces": bool(self.options.exp_zero_in_pool),
            "randomize_party_member_starting_accessories": bool(self.options.randomize_party_member_starting_accessories),
            "randomize_postcards": str(self.options.randomize_postcards.current_key),
            "randomize_puppies": str(self.options.randomize_puppies.current_key),
            "randomize_spell_mp_costs": str(self.options.randomize_spell_mp_costs.current_key),
            "remote_items": str(self.options.remote_items.current_key),
            "remote_location_ids": self.get_remote_location_ids(),
            "required_lucky_emblems_door": self.get_lucky_emblems_required_for_final_rest_door(),
            "required_lucky_emblems_eotw": self.get_lucky_emblems_required_for_end_of_the_world(),
            "required_postcards": int(self.options.required_postcards.value),
            "required_puppies": int(self.options.required_puppies.value),
            "scaling_spell_potency": bool(self.options.scaling_spell_potency),
            "seed": self.multiworld.seed_name,
            "shorten_go_mode": bool(self.options.shorten_go_mode),
            "skip_summon_animations": bool(self.options.skip_summon_animations),
            "slot_name": self.multiworld.get_player_name(self.player),
            "additional_accessory_slots": int(self.options.additional_accessory_slots.value),
            "additional_item_slots": int(self.options.additional_item_slots.value),
            "spell_mp_cost_max": int(self.options.spell_mp_cost_max.value),
            "spell_mp_cost_min": int(self.options.spell_mp_cost_min.value),
            "spell_effectiveness": self.get_spell_effectiveness(),
            "spell_mp_costs": self.mp_costs,
            "stacking_world_items": bool(self.options.stacking_world_items),
            "starting_items": [item.code for item in self.multiworld.precollected_items[self.player]],
            "starting_tools": bool(self.options.starting_tools),
            "synthesis_item_name_byte_arrays": self.get_synthesis_item_name_byte_arrays(),
            "unlock_0_volume": bool(self.options.unlock_0_volume),
            "unskippable": bool(self.options.unskippable),
            "warp_anywhere": bool(self.options.warp_anywhere),
            "world_version": self.world_version,
        }
