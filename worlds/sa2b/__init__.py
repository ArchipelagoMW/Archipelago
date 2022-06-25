import typing
import math

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .Items import SA2BItem, ItemData, item_table, upgrades_table, junk_table, trap_table
from .Locations import SA2BLocation, all_locations, setup_locations
from .Options import sa2b_options
from .Regions import create_regions, shuffleable_regions, connect_regions, LevelGate, gate_0_whitelist_regions, \
    gate_0_blacklist_regions
from .Rules import set_rules
from .Names import ItemName, LocationName
from ..AutoWorld import WebWorld, World
from .GateBosses import get_gate_bosses, get_boss_name
import Patch


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
    data_version = 2

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    location_table: typing.Dict[str, int]

    music_map: typing.Dict[int, int]
    emblems_for_cannons_core: int
    region_emblem_map: typing.Dict[int, int]
    gate_costs: typing.Dict[int, int]
    gate_bosses: typing.Dict[int, int]
    web = SA2BWeb()

    def _get_slot_data(self):
        return {
            "ModVersion": 101,
            "MusicMap": self.music_map,
            "MusicShuffle": self.world.music_shuffle[self.player].value,
            "RequiredRank": self.world.required_rank[self.player].value,
            "ChaoRaceChecks": self.world.chao_race_checks[self.player].value,
            "ChaoGardenDifficulty": self.world.chao_garden_difficulty[self.player].value,
            "DeathLink": self.world.death_link[self.player].value,
            "IncludeMissions": self.world.include_missions[self.player].value,
            "EmblemPercentageForCannonsCore": self.world.emblem_percentage_for_cannons_core[self.player].value,
            "NumberOfLevelGates": self.world.number_of_level_gates[self.player].value,
            "LevelGateDistribution": self.world.level_gate_distribution[self.player].value,
            "EmblemsForCannonsCore": self.emblems_for_cannons_core,
            "RegionEmblemMap": self.region_emblem_map,
            "GateCosts": self.gate_costs,
            "GateBosses": self.gate_bosses,
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

    def generate_early(self):
        self.gate_bosses = get_gate_bosses(self.world, self.player)

    def generate_basic(self):
        self.world.get_location(LocationName.biolizard, self.player).place_locked_item(self.create_item(ItemName.maria))

        itempool: typing.List[SA2BItem] = []

        # First Missions
        total_required_locations = len(self.location_table)
        total_required_locations -= 1; # Locked Victory Location

        # Fill item pool with all required items
        for item in {**upgrades_table}:
            itempool += self._create_items(item)

        # Cap at 180 Emblems
        raw_emblem_count = total_required_locations - len(itempool)
        total_emblem_count = min(raw_emblem_count, 180)
        extra_junk_count = raw_emblem_count - total_emblem_count

        self.emblems_for_cannons_core = math.floor(
            total_emblem_count * (self.world.emblem_percentage_for_cannons_core[self.player].value / 100.0))

        gate_cost_mult = 1.0
        if self.world.level_gate_costs[self.player].value == 0:
            gate_cost_mult = 0.6
        elif self.world.level_gate_costs[self.player].value == 1:
            gate_cost_mult = 0.8

        shuffled_region_list = list(range(30))
        emblem_requirement_list = list()
        self.world.random.shuffle(shuffled_region_list)
        levels_per_gate = self.get_levels_per_gate()

        check_for_impossible_shuffle(shuffled_region_list, math.ceil(levels_per_gate[0]), self.world)
        levels_added_to_gate = 0
        total_levels_added = 0
        current_gate = 0
        current_gate_emblems = 0
        self.gate_costs = dict()
        self.gate_costs[0] = 0
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
                        math.floor(total_emblem_count * math.pow(total_levels_added / 30.0, 2.0) * gate_cost_mult), current_gate)
                    gates.append(LevelGate(current_gate_emblems))
                    self.gate_costs[current_gate] = current_gate_emblems
                levels_added_to_gate = 0

        self.region_emblem_map = dict(zip(shuffled_region_list, emblem_requirement_list))

        connect_regions(self.world, self.player, gates, self.emblems_for_cannons_core, self.gate_bosses)

        max_required_emblems = max(max(emblem_requirement_list), self.emblems_for_cannons_core)
        itempool += [self.create_item(ItemName.emblem)] * max_required_emblems

        non_required_emblems = (total_emblem_count - max_required_emblems)
        junk_count = math.floor(non_required_emblems * (self.world.junk_fill_percentage[self.player].value / 100.0))
        itempool += [self.create_item(ItemName.emblem, True)] * (non_required_emblems - junk_count)

        # Carve Traps out of junk_count
        trap_weights = []
        trap_weights += ([ItemName.omochao_trap] * self.world.omochao_trap_weight[self.player].value)
        trap_weights += ([ItemName.timestop_trap] * self.world.timestop_trap_weight[self.player].value)
        trap_weights += ([ItemName.confuse_trap] * self.world.confusion_trap_weight[self.player].value)
        trap_weights += ([ItemName.tiny_trap] * self.world.tiny_trap_weight[self.player].value)

        junk_count += extra_junk_count
        trap_count = 0 if (len(trap_weights) == 0) else math.ceil(junk_count * (self.world.trap_fill_percentage[self.player].value / 100.0))
        junk_count -= trap_count

        junk_pool = []
        junk_keys = list(junk_table.keys())
        for i in range(junk_count):
            junk_item = self.world.random.choice(junk_keys)
            junk_pool += [self.create_item(junk_item)]

        itempool += junk_pool

        trap_pool = []
        for i in range(trap_count):
            trap_item = self.world.random.choice(trap_weights)
            trap_pool += [self.create_item(trap_item)]

        itempool += trap_pool

        self.world.itempool += itempool

        # Music Shuffle
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
        self.location_table = setup_locations(self.world, self.player)
        create_regions(self.world, self.player, self.location_table)

    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif name == ItemName.emblem:
            classification = ItemClassification.progression_skip_balancing
        elif data.progression:
            classification = ItemClassification.progression
        elif data.trap:
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.filler

        created_item = SA2BItem(name, classification, data.code, self.player)

        return created_item

    def set_rules(self):
        set_rules(self.world, self.player, self.gate_bosses)

    def write_spoiler(self, spoiler_handle: typing.TextIO):
        spoiler_handle.write("\n")
        header_text = "Sonic Adventure 2 Bosses for {}:\n"
        header_text = header_text.format(self.world.player_name[self.player])
        spoiler_handle.write(header_text)
        for x in range(len(self.gate_bosses.values())):
            text = "Gate {0} Boss: {1}\n"
            text = text.format((x + 1), get_boss_name(self.gate_bosses[x + 1]))
            spoiler_handle.writelines(text)

    @classmethod
    def stage_fill_hook(cls, world, progitempool, nonexcludeditempool, localrestitempool, nonlocalrestitempool,
                        restitempool, fill_locations):
        if world.get_game_players("Sonic Adventure 2 Battle"):
            progitempool.sort(
                key=lambda item: 0 if (item.name != 'Emblem') else 1)
