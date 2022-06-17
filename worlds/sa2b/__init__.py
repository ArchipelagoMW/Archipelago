import typing
import math

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .Items import SA2BItem, ItemData, item_table, upgrades_table
from .Locations import SA2BLocation, all_locations, setup_locations
from .Options import sa2b_options
from .Regions import create_regions, shuffleable_regions, connect_regions, LevelGate, gate_0_whitelist_regions, \
    gate_0_blacklist_regions
from .Rules import set_rules
from .Names import ItemName, LocationName
from ..AutoWorld import WebWorld, World


class SA2BWeb(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Sonic Adventure 2: Battle randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["RaspberrySpaceJam", "PoryGone"]
    )
    
    tutorials = [setup_en]


def check_for_impossible_shuffle(shuffled_levels: typing.List[int], gate_0_range: int, world: MultiWorld):
    blacklist_level_count = 0

    for i in range(gate_0_range):
        if shuffled_levels[i] in gate_0_blacklist_regions:
            blacklist_level_count += 1

    if blacklist_level_count == gate_0_range:
        index_to_swap = world.random.randint(0, gate_0_range)
        for i in range(len(shuffled_levels)):
            if shuffled_levels[i] in gate_0_whitelist_regions:
                shuffled_levels[i], shuffled_levels[index_to_swap] = shuffled_levels[index_to_swap], shuffled_levels[i]
                break


class SA2BWorld(World):
    """
    Sonic Adventure 2 Battle is an action platforming game. Play as Sonic, Tails, Knuckles, Shadow, Rogue, and Eggman across 31 stages and prevent the destruction of the earth.
    """
    game: str = "Sonic Adventure 2 Battle"
    options = sa2b_options
    topology_present = False
    data_version = 1

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    music_map: typing.Dict[int, int]
    emblems_for_cannons_core: int
    region_emblem_map: typing.Dict[int, int]
    web = SA2BWeb()

    def _get_slot_data(self):
        return {
            "ModVersion": 100,
            "MusicMap": self.music_map,
            "MusicShuffle": self.world.music_shuffle[self.player].value,
            "DeathLink": self.world.death_link[self.player].value,
            "IncludeMissions": self.world.include_missions[self.player].value,
            "EmblemPercentageForCannonsCore": self.world.emblem_percentage_for_cannons_core[self.player].value,
            "NumberOfLevelGates": self.world.number_of_level_gates[self.player].value,
            "LevelGateDistribution": self.world.level_gate_distribution[self.player].value,
            "EmblemsForCannonsCore": self.emblems_for_cannons_core,
            "RegionEmblemMap": self.region_emblem_map,
        }

    def _create_items(self, name: str):
        data = item_table[name]
        return [self.create_item(name)] * data.quantity

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        slot_data["MusicMap"] = self.music_map
        for option_name in sa2b_options:
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data

    def get_levels_per_gate(self) -> list:
        levels_per_gate = list()
        max_gate_index = self.world.number_of_level_gates[self.player]
        average_level_count = 30 / (max_gate_index + 1)
        levels_added = 0

        for i in range(max_gate_index + 1):
            levels_per_gate.append(average_level_count)
            levels_added += average_level_count
        additional_count_iterator = 0
        while levels_added < 30:
            levels_per_gate[additional_count_iterator] += 1
            levels_added += 1
            additional_count_iterator += 1 if additional_count_iterator < max_gate_index else -max_gate_index

        if self.world.level_gate_distribution[self.player] == 0 or self.world.level_gate_distribution[self.player] == 2:
            early_distribution = self.world.level_gate_distribution[self.player] == 0
            levels_to_distribute = 5
            gate_index_offset = 0
            while levels_to_distribute > 0:
                if levels_per_gate[0 + gate_index_offset] == 1 or \
                        levels_per_gate[max_gate_index - gate_index_offset] == 1:
                    break
                if early_distribution:
                    levels_per_gate[0 + gate_index_offset] += 1
                    levels_per_gate[max_gate_index - gate_index_offset] -= 1
                else:
                    levels_per_gate[0 + gate_index_offset] -= 1
                    levels_per_gate[max_gate_index - gate_index_offset] += 1
                gate_index_offset += 1
                if gate_index_offset > math.floor(max_gate_index / 2):
                    gate_index_offset = 0
                levels_to_distribute -= 1

        return levels_per_gate

    def generate_basic(self):
        self.world.get_location(LocationName.biolizard, self.player).place_locked_item(self.create_item(ItemName.maria))

        itempool: typing.List[SA2BItem] = []

        # First Missions
        total_required_locations = 31

        # Mission Locations
        total_required_locations *= self.world.include_missions[self.player].value

        # Upgrades
        total_required_locations += 28

        # Fill item pool with all required items
        for item in {**upgrades_table}:
            itempool += self._create_items(item)

        total_emblem_count = total_required_locations - len(itempool)

        # itempool += [self.create_item(ItemName.emblem)] * total_emblem_count

        self.emblems_for_cannons_core = math.floor(
            total_emblem_count * (self.world.emblem_percentage_for_cannons_core[self.player].value / 100.0))

        shuffled_region_list = list(range(30))
        emblem_requirement_list = list()
        self.world.random.shuffle(shuffled_region_list)
        levels_per_gate = self.get_levels_per_gate()

        check_for_impossible_shuffle(shuffled_region_list, math.ceil(levels_per_gate[0]), self.world)
        levels_added_to_gate = 0
        total_levels_added = 0
        current_gate = 0
        current_gate_emblems = 0
        gates = list()
        gates.append(LevelGate(0))
        for i in range(30):
            gates[current_gate].gate_levels.append(shuffled_region_list[i])
            emblem_requirement_list.append(current_gate_emblems)
            levels_added_to_gate += 1
            total_levels_added += 1
            if levels_added_to_gate >= levels_per_gate[current_gate]:
                current_gate += 1
                if current_gate > self.world.number_of_level_gates[self.player].value:
                    current_gate = self.world.number_of_level_gates[self.player].value
                else:
                    current_gate_emblems = max(
                        math.floor(total_emblem_count * math.pow(total_levels_added / 30.0, 2.0)), current_gate)
                    gates.append(LevelGate(current_gate_emblems))
                levels_added_to_gate = 0

        self.region_emblem_map = dict(zip(shuffled_region_list, emblem_requirement_list))

        connect_regions(self.world, self.player, gates, self.emblems_for_cannons_core)

        max_required_emblems = max(max(emblem_requirement_list), self.emblems_for_cannons_core)
        itempool += [self.create_item(ItemName.emblem)] * max_required_emblems
        itempool += [self.create_item(ItemName.emblem, True)] * (total_emblem_count - max_required_emblems)

        self.world.itempool += itempool

        if self.world.music_shuffle[self.player] == "levels":
            musiclist_o = list(range(0, 47))
            musiclist_s = musiclist_o.copy()
            self.world.random.shuffle(musiclist_s)
            self.music_map = dict(zip(musiclist_o, musiclist_s))
        elif self.world.music_shuffle[self.player] == "full":
            musiclist_o = list(range(0, 78))
            musiclist_s = musiclist_o.copy()
            self.world.random.shuffle(musiclist_s)
            self.music_map = dict(zip(musiclist_o, musiclist_s))
        else:
            self.music_map = dict()

    def create_regions(self):
        location_table = setup_locations(self.world, self.player)
        create_regions(self.world, self.player, location_table)

    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if name == ItemName.emblem:
            classification = ItemClassification.progression_skip_balancing
        elif force_non_progression:
            classification = ItemClassification.filler
        elif data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        created_item = SA2BItem(name, classification, data.code, self.player)

        return created_item

    def set_rules(self):
        set_rules(self.world, self.player)

    @classmethod
    def stage_fill_hook(cls, world, progitempool, nonexcludeditempool, localrestitempool, nonlocalrestitempool,
                        restitempool, fill_locations):
        if world.get_game_players("Sonic Adventure 2 Battle"):
            progitempool.sort(
                key=lambda item: 0 if (item.name != 'Emblem') else 1)
