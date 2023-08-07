import typing
import math

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .Items import SA2BItem, ItemData, item_table, upgrades_table, emeralds_table, junk_table, trap_table, item_groups
from .Locations import SA2BLocation, all_locations, setup_locations
from .Options import sa2b_options
from .Regions import create_regions, shuffleable_regions, connect_regions, LevelGate, gate_0_whitelist_regions, \
    gate_0_blacklist_regions
from .Rules import set_rules
from .Names import ItemName, LocationName
from worlds.AutoWorld import WebWorld, World
from .GateBosses import get_gate_bosses, get_boss_rush_bosses, get_boss_name
from .Missions import get_mission_table, get_mission_count_table, get_first_and_last_cannons_core_missions
import Patch


class SA2BWeb(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Sonic Adventure 2: Battle randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["RaspberrySpaceJam", "PoryGone", "Entiss"]
    )
    
    tutorials = [setup_en]


def check_for_impossible_shuffle(shuffled_levels: typing.List[int], gate_0_range: int, multiworld: MultiWorld):
    blacklist_level_count = 0

    for i in range(gate_0_range):
        if shuffled_levels[i] in gate_0_blacklist_regions:
            blacklist_level_count += 1

    if blacklist_level_count == gate_0_range:
        index_to_swap = multiworld.random.randint(0, gate_0_range)
        for i in range(len(shuffled_levels)):
            if shuffled_levels[i] in gate_0_whitelist_regions:
                shuffled_levels[i], shuffled_levels[index_to_swap] = shuffled_levels[index_to_swap], shuffled_levels[i]
                break


class SA2BWorld(World):
    """
    Sonic Adventure 2 Battle is an action platforming game. Play as Sonic, Tails, Knuckles, Shadow, Rouge, and Eggman across 31 stages and prevent the destruction of the earth.
    """
    game: str = "Sonic Adventure 2 Battle"
    option_definitions = sa2b_options
    topology_present = False
    data_version = 6

    item_name_groups = item_groups
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    location_table: typing.Dict[str, int]

    music_map: typing.Dict[int, int]
    voice_map: typing.Dict[int, int]
    mission_map: typing.Dict[int, int]
    mission_count_map: typing.Dict[int, int]
    emblems_for_cannons_core: int
    region_emblem_map: typing.Dict[int, int]
    gate_costs: typing.Dict[int, int]
    gate_bosses: typing.Dict[int, int]
    boss_rush_map: typing.Dict[int, int]
    web = SA2BWeb()

    def _get_slot_data(self):
        return {
            "ModVersion": 202,
            "Goal": self.multiworld.goal[self.player].value,
            "MusicMap": self.music_map,
            "VoiceMap": self.voice_map,
            "MissionMap": self.mission_map,
            "MissionCountMap": self.mission_count_map,
            "MusicShuffle": self.multiworld.music_shuffle[self.player].value,
            "Narrator": self.multiworld.narrator[self.player].value,
            "MinigameTrapDifficulty": self.multiworld.minigame_trap_difficulty[self.player].value,
            "RingLoss": self.multiworld.ring_loss[self.player].value,
            "RingLink": self.multiworld.ring_link[self.player].value,
            "RequiredRank": self.multiworld.required_rank[self.player].value,
            "ChaoKeys": self.multiworld.keysanity[self.player].value,
            "Whistlesanity": self.multiworld.whistlesanity[self.player].value,
            "GoldBeetles": self.multiworld.beetlesanity[self.player].value,
            "OmochaoChecks": self.multiworld.omosanity[self.player].value,
            "AnimalChecks": self.multiworld.animalsanity[self.player].value,
            "KartRaceChecks": self.multiworld.kart_race_checks[self.player].value,
            "ChaoRaceChecks": self.multiworld.chao_race_checks[self.player].value,
            "ChaoGardenDifficulty": self.multiworld.chao_garden_difficulty[self.player].value,
            "DeathLink": self.multiworld.death_link[self.player].value,
            "EmblemPercentageForCannonsCore": self.multiworld.emblem_percentage_for_cannons_core[self.player].value,
            "RequiredCannonsCoreMissions": self.multiworld.required_cannons_core_missions[self.player].value,
            "NumberOfLevelGates": self.multiworld.number_of_level_gates[self.player].value,
            "LevelGateDistribution": self.multiworld.level_gate_distribution[self.player].value,
            "EmblemsForCannonsCore": self.emblems_for_cannons_core,
            "RegionEmblemMap": self.region_emblem_map,
            "GateCosts": self.gate_costs,
            "GateBosses": self.gate_bosses,
            "BossRushMap": self.boss_rush_map,
        }

    def _create_items(self, name: str):
        data = item_table[name]
        return [self.create_item(name) for _ in range(data.quantity)]

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        slot_data["MusicMap"] = self.music_map
        for option_name in sa2b_options:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data

    def get_levels_per_gate(self) -> list:
        levels_per_gate = list()
        max_gate_index = self.multiworld.number_of_level_gates[self.player]
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

        if self.multiworld.level_gate_distribution[self.player] == 0 or self.multiworld.level_gate_distribution[self.player] == 2:
            early_distribution = self.multiworld.level_gate_distribution[self.player] == 0
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
        if self.multiworld.goal[self.player].value == 3:
            # Turn off everything else for Grand Prix goal
            self.multiworld.number_of_level_gates[self.player].value = 0
            self.multiworld.emblem_percentage_for_cannons_core[self.player].value = 0
            self.multiworld.junk_fill_percentage[self.player].value = 100
            self.multiworld.trap_fill_percentage[self.player].value = 100
            self.multiworld.omochao_trap_weight[self.player].value = 0
            self.multiworld.timestop_trap_weight[self.player].value = 0
            self.multiworld.confusion_trap_weight[self.player].value = 0
            self.multiworld.tiny_trap_weight[self.player].value = 0
            self.multiworld.gravity_trap_weight[self.player].value = 0
            self.multiworld.ice_trap_weight[self.player].value = 0
            self.multiworld.slow_trap_weight[self.player].value = 0

            valid_trap_weights = self.multiworld.exposition_trap_weight[self.player].value + \
                                 self.multiworld.cutscene_trap_weight[self.player].value + \
                                 self.multiworld.pong_trap_weight[self.player].value

            if valid_trap_weights == 0:
                self.multiworld.exposition_trap_weight[self.player].value = 4
                self.multiworld.cutscene_trap_weight[self.player].value = 4
                self.multiworld.pong_trap_weight[self.player].value = 4

            if self.multiworld.kart_race_checks[self.player].value == 0:
                self.multiworld.kart_race_checks[self.player].value = 2

            self.gate_bosses = {}
            self.boss_rush_map = {}
        else:
            self.gate_bosses   = get_gate_bosses(self.multiworld, self.player)
            self.boss_rush_map = get_boss_rush_bosses(self.multiworld, self.player)

    def create_regions(self):
        self.mission_map       = get_mission_table(self.multiworld, self.player)
        self.mission_count_map = get_mission_count_table(self.multiworld, self.player)

        self.location_table = setup_locations(self.multiworld, self.player, self.mission_map, self.mission_count_map)
        create_regions(self.multiworld, self.player, self.location_table)

        # Not Generate Basic
        if self.multiworld.goal[self.player].value in [0, 2, 4, 5, 6]:
            self.multiworld.get_location(LocationName.finalhazard, self.player).place_locked_item(self.create_item(ItemName.maria))
        elif self.multiworld.goal[self.player].value == 1:
            self.multiworld.get_location(LocationName.green_hill, self.player).place_locked_item(self.create_item(ItemName.maria))
        elif self.multiworld.goal[self.player].value == 3:
            self.multiworld.get_location(LocationName.grand_prix, self.player).place_locked_item(self.create_item(ItemName.maria))

        itempool: typing.List[SA2BItem] = []

        # First Missions
        total_required_locations = len(self.location_table)
        total_required_locations -= 1; # Locked Victory Location

        if self.multiworld.goal[self.player].value != 3:
            # Fill item pool with all required items
            for item in {**upgrades_table}:
                itempool += [self.create_item(item, False, self.multiworld.goal[self.player].value)]

            if self.multiworld.goal[self.player].value in [1, 2, 6]:
                # Some flavor of Chaos Emerald Hunt
                for item in {**emeralds_table}:
                    itempool += self._create_items(item)

        # Cap at player-specified Emblem count
        raw_emblem_count = total_required_locations - len(itempool)
        total_emblem_count = min(raw_emblem_count, self.multiworld.max_emblem_cap[self.player].value)
        extra_junk_count = raw_emblem_count - total_emblem_count

        self.emblems_for_cannons_core = math.floor(
            total_emblem_count * (self.multiworld.emblem_percentage_for_cannons_core[self.player].value / 100.0))

        gate_cost_mult = 1.0
        if self.multiworld.level_gate_costs[self.player].value == 0:
            gate_cost_mult = 0.6
        elif self.multiworld.level_gate_costs[self.player].value == 1:
            gate_cost_mult = 0.8

        shuffled_region_list = list(range(30))
        emblem_requirement_list = list()
        self.multiworld.random.shuffle(shuffled_region_list)
        levels_per_gate = self.get_levels_per_gate()

        check_for_impossible_shuffle(shuffled_region_list, math.ceil(levels_per_gate[0]), self.multiworld)
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
                if current_gate > self.multiworld.number_of_level_gates[self.player].value:
                    current_gate = self.multiworld.number_of_level_gates[self.player].value
                else:
                    current_gate_emblems = max(
                        math.floor(total_emblem_count * math.pow(total_levels_added / 30.0, 2.0) * gate_cost_mult), current_gate)
                    gates.append(LevelGate(current_gate_emblems))
                    self.gate_costs[current_gate] = current_gate_emblems
                levels_added_to_gate = 0

        self.region_emblem_map = dict(zip(shuffled_region_list, emblem_requirement_list))

        first_cannons_core_mission, final_cannons_core_mission = get_first_and_last_cannons_core_missions(self.mission_map, self.mission_count_map)

        connect_regions(self.multiworld, self.player, gates, self.emblems_for_cannons_core, self.gate_bosses, self.boss_rush_map, first_cannons_core_mission, final_cannons_core_mission)

        max_required_emblems = max(max(emblem_requirement_list), self.emblems_for_cannons_core)
        itempool += [self.create_item(ItemName.emblem) for _ in range(max_required_emblems)]

        non_required_emblems = (total_emblem_count - max_required_emblems)
        junk_count = math.floor(non_required_emblems * (self.multiworld.junk_fill_percentage[self.player].value / 100.0))
        itempool += [self.create_item(ItemName.emblem, True) for _ in range(non_required_emblems - junk_count)]

        # Carve Traps out of junk_count
        trap_weights = []
        trap_weights += ([ItemName.omochao_trap] * self.multiworld.omochao_trap_weight[self.player].value)
        trap_weights += ([ItemName.timestop_trap] * self.multiworld.timestop_trap_weight[self.player].value)
        trap_weights += ([ItemName.confuse_trap] * self.multiworld.confusion_trap_weight[self.player].value)
        trap_weights += ([ItemName.tiny_trap] * self.multiworld.tiny_trap_weight[self.player].value)
        trap_weights += ([ItemName.gravity_trap] * self.multiworld.gravity_trap_weight[self.player].value)
        trap_weights += ([ItemName.exposition_trap] * self.multiworld.exposition_trap_weight[self.player].value)
        #trap_weights += ([ItemName.darkness_trap] * self.multiworld.darkness_trap_weight[self.player].value)
        trap_weights += ([ItemName.ice_trap] * self.multiworld.ice_trap_weight[self.player].value)
        trap_weights += ([ItemName.slow_trap] * self.multiworld.slow_trap_weight[self.player].value)
        trap_weights += ([ItemName.cutscene_trap] * self.multiworld.cutscene_trap_weight[self.player].value)
        trap_weights += ([ItemName.pong_trap] * self.multiworld.pong_trap_weight[self.player].value)

        junk_count += extra_junk_count
        trap_count = 0 if (len(trap_weights) == 0) else math.ceil(junk_count * (self.multiworld.trap_fill_percentage[self.player].value / 100.0))
        junk_count -= trap_count

        junk_pool = []
        junk_keys = list(junk_table.keys())
        for i in range(junk_count):
            junk_item = self.multiworld.random.choice(junk_keys)
            junk_pool.append(self.create_item(junk_item))

        itempool += junk_pool

        trap_pool = []
        for i in range(trap_count):
            trap_item = self.multiworld.random.choice(trap_weights)
            trap_pool.append(self.create_item(trap_item))

        itempool += trap_pool

        self.multiworld.itempool += itempool

        # Music Shuffle
        if self.multiworld.music_shuffle[self.player] == "levels":
            musiclist_o = list(range(0, 47))
            musiclist_s = musiclist_o.copy()
            self.multiworld.random.shuffle(musiclist_s)
            musiclist_o.extend(range(47, 78))
            musiclist_s.extend(range(47, 78))

            if self.multiworld.sadx_music[self.player].value == 1:
                musiclist_s = [x+100 for x in musiclist_s]
            elif self.multiworld.sadx_music[self.player].value == 2:
                for i in range(len(musiclist_s)):
                    if self.multiworld.random.randint(0,1):
                        musiclist_s[i] += 100

            self.music_map = dict(zip(musiclist_o, musiclist_s))
        elif self.multiworld.music_shuffle[self.player] == "full":
            musiclist_o = list(range(0, 78))
            musiclist_s = musiclist_o.copy()
            self.multiworld.random.shuffle(musiclist_s)

            if self.multiworld.sadx_music[self.player].value == 1:
                musiclist_s = [x+100 for x in musiclist_s]
            elif self.multiworld.sadx_music[self.player].value == 2:
                for i in range(len(musiclist_s)):
                    if self.multiworld.random.randint(0,1):
                        musiclist_s[i] += 100

            self.music_map = dict(zip(musiclist_o, musiclist_s))
        elif self.multiworld.music_shuffle[self.player] == "singularity":
            musiclist_o = list(range(0, 78))
            musiclist_s = [self.multiworld.random.choice(musiclist_o)] * len(musiclist_o)

            if self.multiworld.sadx_music[self.player].value == 1:
                musiclist_s = [x+100 for x in musiclist_s]
            elif self.multiworld.sadx_music[self.player].value == 2:
                if self.multiworld.random.randint(0,1):
                    musiclist_s = [x+100 for x in musiclist_s]

            self.music_map = dict(zip(musiclist_o, musiclist_s))
        else:
            musiclist_o = list(range(0, 78))
            musiclist_s = musiclist_o.copy()

            if self.multiworld.sadx_music[self.player].value == 1:
                musiclist_s = [x+100 for x in musiclist_s]
            elif self.multiworld.sadx_music[self.player].value == 2:
                for i in range(len(musiclist_s)):
                    if self.multiworld.random.randint(0,1):
                        musiclist_s[i] += 100

            self.music_map = dict(zip(musiclist_o, musiclist_s))

        # Voice Shuffle
        if self.multiworld.voice_shuffle[self.player] == "shuffled":
            voicelist_o = list(range(0, 2623))
            voicelist_s = voicelist_o.copy()
            self.multiworld.random.shuffle(voicelist_s)

            self.voice_map = dict(zip(voicelist_o, voicelist_s))
        elif self.multiworld.voice_shuffle[self.player] == "rude":
            voicelist_o = list(range(0, 2623))
            voicelist_s = voicelist_o.copy()
            self.multiworld.random.shuffle(voicelist_s)

            for i in range(len(voicelist_s)):
                if self.multiworld.random.randint(1,100) > 80:
                    voicelist_s[i] = 17

            self.voice_map = dict(zip(voicelist_o, voicelist_s))
        elif self.multiworld.voice_shuffle[self.player] == "chao":
            voicelist_o = list(range(0, 2623))
            voicelist_s = voicelist_o.copy()
            self.multiworld.random.shuffle(voicelist_s)

            for i in range(len(voicelist_s)):
                voicelist_s[i] = self.multiworld.random.choice(range(2586, 2608))

            self.voice_map = dict(zip(voicelist_o, voicelist_s))
        elif self.multiworld.voice_shuffle[self.player] == "singularity":
            voicelist_o = list(range(0, 2623))
            voicelist_s = [self.multiworld.random.choice(voicelist_o)] * len(voicelist_o)

            self.voice_map = dict(zip(voicelist_o, voicelist_s))
        else:
            voicelist_o = list(range(0, 2623))
            voicelist_s = voicelist_o.copy()

            self.voice_map = dict(zip(voicelist_o, voicelist_s))


    def create_item(self, name: str, force_non_progression=False, goal=0) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif name == ItemName.emblem or \
             name in emeralds_table.keys() or \
             (name == ItemName.knuckles_shovel_claws and goal in [4, 5]):
            classification = ItemClassification.progression_skip_balancing
        elif data.progression:
            classification = ItemClassification.progression
        elif data.trap:
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.filler

        created_item = SA2BItem(name, classification, data.code, self.player)

        return created_item

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(list(junk_table.keys()))

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.gate_bosses, self.boss_rush_map, self.mission_map, self.mission_count_map)

    def write_spoiler(self, spoiler_handle: typing.TextIO):
        if self.multiworld.number_of_level_gates[self.player].value > 0 or self.multiworld.goal[self.player].value in [4, 5, 6]:
            spoiler_handle.write("\n")
            header_text = "Sonic Adventure 2 Bosses for {}:\n"
            header_text = header_text.format(self.multiworld.player_name[self.player])
            spoiler_handle.write(header_text)

            if self.multiworld.number_of_level_gates[self.player].value > 0:
                for x in range(len(self.gate_bosses.values())):
                    text = "Gate {0} Boss: {1}\n"
                    text = text.format((x + 1), get_boss_name(self.gate_bosses[x + 1]))
                    spoiler_handle.writelines(text)
                spoiler_handle.write("\n")

            if self.multiworld.goal[self.player].value in [4, 5, 6]:
                for x in range(len(self.boss_rush_map.values())):
                    text = "Boss Rush Boss {0}: {1}\n"
                    text = text.format((x + 1), get_boss_name(self.boss_rush_map[x]))
                    spoiler_handle.writelines(text)
                spoiler_handle.write("\n")

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        gate_names = [
            LocationName.gate_0_region,
            LocationName.gate_1_region,
            LocationName.gate_2_region,
            LocationName.gate_3_region,
            LocationName.gate_4_region,
            LocationName.gate_5_region,
        ]
        no_hint_region_names = [
            LocationName.cannon_core_region,
            LocationName.chao_garden_beginner_region,
            LocationName.chao_garden_intermediate_region,
            LocationName.chao_garden_expert_region,
        ]
        er_hint_data = {}
        for i in range(self.multiworld.number_of_level_gates[self.player].value + 1):
            gate_name = gate_names[i]
            gate_region = self.multiworld.get_region(gate_name, self.player)
            if not gate_region:
                continue
            for exit in gate_region.exits:
                if exit.connected_region.name in gate_names or exit.connected_region.name in no_hint_region_names:
                    continue
                level_region = exit.connected_region
                for location in level_region.locations:
                    er_hint_data[location.address] = gate_name

        hint_data[self.player] = er_hint_data

    @classmethod
    def stage_fill_hook(cls, world, progitempool, usefulitempool, filleritempool, fill_locations):
        if world.get_game_players("Sonic Adventure 2 Battle"):
            progitempool.sort(
                key=lambda item: 0 if (item.name != 'Emblem') else 1)
