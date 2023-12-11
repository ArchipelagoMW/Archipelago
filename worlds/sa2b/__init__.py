import typing
import math
import logging

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .Items import SA2BItem, ItemData, item_table, upgrades_table, emeralds_table, junk_table, trap_table, item_groups, \
                   eggs_table, fruits_table, seeds_table, hats_table, animals_table, chaos_drives_table
from .Locations import SA2BLocation, all_locations, setup_locations, chao_animal_event_location_table, black_market_location_table
from .Options import sa2b_options
from .Regions import create_regions, shuffleable_regions, connect_regions, LevelGate, gate_0_whitelist_regions, \
    gate_0_blacklist_regions
from .Rules import set_rules
from .Names import ItemName, LocationName
from .AestheticData import chao_name_conversion, sample_chao_names, totally_real_item_names, \
                           all_exits, all_destinations, multi_rooms, single_rooms, room_to_exits_map, exit_to_room_map, valid_kindergarten_exits
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
    data_version = 7

    item_name_groups = item_groups
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    location_table: typing.Dict[str, int]

    mission_map: typing.Dict[int, int]
    mission_count_map: typing.Dict[int, int]
    emblems_for_cannons_core: int
    region_emblem_map: typing.Dict[int, int]
    gate_costs: typing.Dict[int, int]
    gate_bosses: typing.Dict[int, int]
    boss_rush_map: typing.Dict[int, int]
    black_market_costs: typing.Dict[int, int]

    web = SA2BWeb()

    def fill_slot_data(self) -> dict:
        return {
            "ModVersion": 203,
            "Goal": self.options.goal.value,
            "MusicMap": self.generate_music_data(),
            "VoiceMap": self.generate_voice_data(),
            "DefaultEggMap": self.generate_chao_egg_data(),
            "DefaultChaoNameMap": self.generate_chao_name_data(),
            "MissionMap": self.mission_map,
            "MissionCountMap": self.mission_count_map,
            "MusicShuffle": self.options.music_shuffle.value,
            "Narrator": self.options.narrator.value,
            "MinigameTrapDifficulty": self.options.minigame_trap_difficulty.value,
            "RingLoss": self.options.ring_loss.value,
            "RingLink": self.options.ring_link.value,
            "RequiredRank": self.options.required_rank.value,
            "ChaoKeys": self.options.keysanity.value,
            "Whistlesanity": self.options.whistlesanity.value,
            "GoldBeetles": self.options.beetlesanity.value,
            "OmochaoChecks": self.options.omosanity.value,
            "AnimalChecks": self.options.animalsanity.value,
            "KartRaceChecks": self.options.kart_race_checks.value,
            "ChaoStadiumChecks": self.options.chao_stadium_checks.value,
            "ChaoRaceDifficulty": self.options.chao_race_difficulty.value,
            "ChaoKarateDifficulty": self.options.chao_karate_difficulty.value,
            "ChaoStats": self.options.chao_stats.value,
            "ChaoStatsFrequency": self.options.chao_stats_frequency.value,
            "ChaoStatsStamina": self.options.chao_stats_stamina.value,
            "ChaoStatsHidden": self.options.chao_stats_hidden.value,
            "ChaoAnimalParts": self.options.chao_animal_parts.value,
            "ChaoKindergarten": self.options.chao_kindergarten.value,
            "BlackMarketSlots": self.options.black_market_slots.value,
            "BlackMarketData": self.generate_black_market_data(),
            "BlackMarketUnlockCosts": self.black_market_costs,
            "BlackMarketUnlockSetting": self.options.black_market_unlock_costs.value,
            "ChaoERLayout": self.generate_er_layout(),
            "DeathLink": self.options.death_link.value,
            "EmblemPercentageForCannonsCore": self.options.emblem_percentage_for_cannons_core.value,
            "RequiredCannonsCoreMissions": self.options.required_cannons_core_missions.value,
            "NumberOfLevelGates": self.options.number_of_level_gates.value,
            "LevelGateDistribution": self.options.level_gate_distribution.value,
            "EmblemsForCannonsCore": self.emblems_for_cannons_core,
            "RegionEmblemMap": self.region_emblem_map,
            "GateCosts": self.gate_costs,
            "GateBosses": self.gate_bosses,
            "BossRushMap": self.boss_rush_map,
            "PlayerNum": self.player,
        }

    def generate_early(self):
        if self.options.goal.value == 3:
            # Turn off everything else for Grand Prix goal
            self.options.number_of_level_gates.value = 0
            self.options.emblem_percentage_for_cannons_core.value = 0

            self.options.chao_race_difficulty.value = 0
            self.options.chao_karate_difficulty.value = 0
            self.options.chao_stats.value = 0
            self.options.chao_animal_parts.value = 0
            self.options.chao_kindergarten.value = 0
            self.options.black_market_slots.value = 0

            self.options.junk_fill_percentage.value = 100
            self.options.trap_fill_percentage.value = 100
            self.options.omochao_trap_weight.value = 0
            self.options.timestop_trap_weight.value = 0
            self.options.confusion_trap_weight.value = 0
            self.options.tiny_trap_weight.value = 0
            self.options.gravity_trap_weight.value = 0
            self.options.ice_trap_weight.value = 0
            self.options.slow_trap_weight.value = 0
            self.options.cutscene_trap_weight.value = 0

            valid_trap_weights = self.options.exposition_trap_weight.value + \
                                 self.options.reverse_trap_weight.value + \
                                 self.options.pong_trap_weight.value

            if valid_trap_weights == 0:
                self.options.exposition_trap_weight.value = 4
                self.options.reverse_trap_weight.value = 4
                self.options.pong_trap_weight.value = 4

            if self.options.kart_race_checks.value == 0:
                self.options.kart_race_checks.value = 2

            self.gate_bosses = {}
            self.boss_rush_map = {}
        else:
            self.gate_bosses   = get_gate_bosses(self.multiworld, self)
            self.boss_rush_map = get_boss_rush_bosses(self.multiworld, self)

    def create_regions(self):
        self.mission_map       = get_mission_table(self.multiworld, self, self.player)
        self.mission_count_map = get_mission_count_table(self.multiworld, self, self.player)

        self.location_table = setup_locations(self, self.player, self.mission_map, self.mission_count_map)
        create_regions(self.multiworld, self, self.player, self.location_table)

        # Not Generate Basic
        self.black_market_costs = dict()

        if self.options.goal.value in [0, 2, 4, 5, 6]:
            self.multiworld.get_location(LocationName.finalhazard, self.player).place_locked_item(self.create_item(ItemName.maria))
        elif self.options.goal.value == 1:
            self.multiworld.get_location(LocationName.green_hill, self.player).place_locked_item(self.create_item(ItemName.maria))
        elif self.options.goal.value == 3:
            self.multiworld.get_location(LocationName.grand_prix, self.player).place_locked_item(self.create_item(ItemName.maria))
        elif self.options.goal.value == 7:
            self.multiworld.get_location(LocationName.chaos_chao, self.player).place_locked_item(self.create_item(ItemName.maria))

            for animal_name in chao_animal_event_location_table.keys():
                animal_region = self.multiworld.get_region(animal_name, self.player)
                animal_event_location = SA2BLocation(self.player, animal_name, None, animal_region)
                animal_region.locations.append(animal_event_location)
                animal_event_item = SA2BItem(animal_name, ItemClassification.progression, None, self.player)
                self.multiworld.get_location(animal_name, self.player).place_locked_item(animal_event_item)

        itempool: typing.List[SA2BItem] = []

        # First Missions
        total_required_locations = len(self.location_table)
        total_required_locations -= 1; # Locked Victory Location

        if self.options.goal.value != 3:
            # Fill item pool with all required items
            for item in {**upgrades_table}:
                itempool += [self.create_item(item, False, self.options.goal.value)]

            if self.options.goal.value in [1, 2, 6]:
                # Some flavor of Chaos Emerald Hunt
                for item in {**emeralds_table}:
                    itempool.append(self.create_item(item))

            # Black Market
            itempool += [self.create_item(ItemName.market_token) for _ in range(self.options.black_market_slots.value)]

            black_market_unlock_mult = 1.0
            if self.options.black_market_unlock_costs.value == 0:
                black_market_unlock_mult = 0.5
            elif self.options.black_market_unlock_costs.value == 1:
                black_market_unlock_mult = 0.75

            for i in range(self.options.black_market_slots.value):
                self.black_market_costs[i] = math.floor((i + 1) * black_market_unlock_mult)

        # Cap at player-specified Emblem count
        raw_emblem_count = total_required_locations - len(itempool)
        total_emblem_count = min(raw_emblem_count, self.options.max_emblem_cap.value)
        extra_junk_count = raw_emblem_count - total_emblem_count

        self.emblems_for_cannons_core = math.floor(
            total_emblem_count * (self.options.emblem_percentage_for_cannons_core.value / 100.0))

        gate_cost_mult = 1.0
        if self.options.level_gate_costs.value == 0:
            gate_cost_mult = 0.6
        elif self.options.level_gate_costs.value == 1:
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
                if current_gate > self.options.number_of_level_gates.value:
                    current_gate = self.options.number_of_level_gates.value
                else:
                    current_gate_emblems = max(
                        math.floor(total_emblem_count * math.pow(total_levels_added / 30.0, 2.0) * gate_cost_mult), current_gate)
                    gates.append(LevelGate(current_gate_emblems))
                    self.gate_costs[current_gate] = current_gate_emblems
                levels_added_to_gate = 0

        self.region_emblem_map = dict(zip(shuffled_region_list, emblem_requirement_list))

        first_cannons_core_mission, final_cannons_core_mission = get_first_and_last_cannons_core_missions(self.mission_map, self.mission_count_map)

        connect_regions(self.multiworld, self, self.player, gates, self.emblems_for_cannons_core, self.gate_bosses, self.boss_rush_map, first_cannons_core_mission, final_cannons_core_mission)

        max_required_emblems = max(max(emblem_requirement_list), self.emblems_for_cannons_core)
        itempool += [self.create_item(ItemName.emblem) for _ in range(max_required_emblems)]

        non_required_emblems = (total_emblem_count - max_required_emblems)
        junk_count = math.floor(non_required_emblems * (self.options.junk_fill_percentage.value / 100.0))
        itempool += [self.create_item(ItemName.emblem, True) for _ in range(non_required_emblems - junk_count)]

        # Carve Traps out of junk_count
        trap_weights = []
        trap_weights += ([ItemName.omochao_trap] * self.options.omochao_trap_weight.value)
        trap_weights += ([ItemName.timestop_trap] * self.options.timestop_trap_weight.value)
        trap_weights += ([ItemName.confuse_trap] * self.options.confusion_trap_weight.value)
        trap_weights += ([ItemName.tiny_trap] * self.options.tiny_trap_weight.value)
        trap_weights += ([ItemName.gravity_trap] * self.options.gravity_trap_weight.value)
        trap_weights += ([ItemName.exposition_trap] * self.options.exposition_trap_weight.value)
        #trap_weights += ([ItemName.darkness_trap] * self.options.darkness_trap_weight.value)
        trap_weights += ([ItemName.ice_trap] * self.options.ice_trap_weight.value)
        trap_weights += ([ItemName.slow_trap] * self.options.slow_trap_weight.value)
        trap_weights += ([ItemName.cutscene_trap] * self.options.cutscene_trap_weight.value)
        trap_weights += ([ItemName.reverse_trap] * self.options.reverse_trap_weight.value)
        trap_weights += ([ItemName.pong_trap] * self.options.pong_trap_weight.value)

        junk_count += extra_junk_count
        trap_count = 0 if (len(trap_weights) == 0) else math.ceil(junk_count * (self.options.trap_fill_percentage.value / 100.0))
        junk_count -= trap_count

        chao_active = self.any_chao_locations_active()
        junk_pool = []
        junk_keys = list(junk_table.keys())

        # Chao Junk
        if chao_active:
            junk_keys += list(chaos_drives_table.keys())
        eggs_keys = list(eggs_table.keys())
        fruits_keys = list(fruits_table.keys())
        seeds_keys = list(seeds_table.keys())
        hats_keys = list(hats_table.keys())
        eggs_count = 0
        seeds_count = 0
        hats_count = 0

        for i in range(junk_count):
            junk_type = self.random.randint(0, len(junk_keys) + 3)

            if chao_active and junk_type == len(junk_keys) + 0 and eggs_count < 20:
                junk_item = self.multiworld.random.choice(eggs_keys)
                junk_pool.append(self.create_item(junk_item))
                eggs_count += 1
            elif chao_active and junk_type == len(junk_keys) + 1:
                junk_item = self.multiworld.random.choice(fruits_keys)
                junk_pool.append(self.create_item(junk_item))
            elif chao_active and junk_type == len(junk_keys) + 2 and seeds_count < 12:
                junk_item = self.multiworld.random.choice(seeds_keys)
                junk_pool.append(self.create_item(junk_item))
                seeds_count += 1
            elif chao_active and junk_type == len(junk_keys) + 3 and hats_count < 20:
                junk_item = self.multiworld.random.choice(hats_keys)
                junk_pool.append(self.create_item(junk_item))
                hats_count += 1
            else:
                junk_item = self.multiworld.random.choice(junk_keys)
                junk_pool.append(self.create_item(junk_item))

        itempool += junk_pool

        trap_pool = []
        for i in range(trap_count):
            trap_item = self.multiworld.random.choice(trap_weights)
            trap_pool.append(self.create_item(trap_item))

        itempool += trap_pool

        self.multiworld.itempool += itempool



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
        junk_keys = list(junk_table.keys())

        # Chao Junk
        if self.any_chao_locations_active():
            junk_keys += list(chaos_drives_table.keys())

        return self.multiworld.random.choice(junk_keys)

    def set_rules(self):
        set_rules(self.multiworld, self, self.player, self.gate_bosses, self.boss_rush_map, self.mission_map, self.mission_count_map, self.black_market_costs)

    def write_spoiler(self, spoiler_handle: typing.TextIO):
        if self.options.number_of_level_gates.value > 0 or self.options.goal.value in [4, 5, 6]:
            spoiler_handle.write("\n")
            header_text = "Sonic Adventure 2 Bosses for {}:\n"
            header_text = header_text.format(self.multiworld.player_name[self.player])
            spoiler_handle.write(header_text)

            if self.options.number_of_level_gates.value > 0:
                for x in range(len(self.gate_bosses.values())):
                    text = "Gate {0} Boss: {1}\n"
                    text = text.format((x + 1), get_boss_name(self.gate_bosses[x + 1]))
                    spoiler_handle.writelines(text)
                spoiler_handle.write("\n")

            if self.options.goal.value in [4, 5, 6]:
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
            LocationName.chao_race_beginner_region,
            LocationName.chao_race_intermediate_region,
            LocationName.chao_race_expert_region,
            LocationName.chao_karate_beginner_region,
            LocationName.chao_karate_intermediate_region,
            LocationName.chao_karate_expert_region,
            LocationName.chao_karate_super_region,
            LocationName.kart_race_beginner_region,
            LocationName.kart_race_standard_region,
            LocationName.kart_race_expert_region,
            LocationName.chao_kindergarten_region,
            LocationName.black_market_region,
        ]
        er_hint_data = {}
        for i in range(self.options.number_of_level_gates.value + 1):
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

        for i in range(self.options.black_market_slots.value):
            location = self.multiworld.get_location(LocationName.chao_black_market_base + str(i + 1), self.player)
            er_hint_data[location.address] = str(self.black_market_costs[i]) + " " + str(ItemName.market_token)


        hint_data[self.player] = er_hint_data

    @classmethod
    def stage_fill_hook(cls, multiworld: MultiWorld, progitempool, usefulitempool, filleritempool, fill_locations):
        if multiworld.get_game_players("Sonic Adventure 2 Battle"):
            progitempool.sort(
                key=lambda item: 0 if (item.name != 'Emblem') else 1)

    def get_levels_per_gate(self) -> list:
        levels_per_gate = list()
        max_gate_index = self.options.number_of_level_gates
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

        if self.options.level_gate_distribution == 0 or self.options.level_gate_distribution == 2:
            early_distribution = self.options.level_gate_distribution == 0
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

    def any_chao_locations_active(self) -> bool:
        if self.options.chao_race_difficulty.value > 0 or \
           self.options.chao_karate_difficulty.value > 0 or \
           self.options.chao_stats.value > 0 or \
           self.options.chao_animal_parts or \
           self.options.chao_kindergarten or \
           self.options.black_market_slots.value > 0:
            return True;

        return False

    def generate_music_data(self) -> typing.Dict[int, int]:
        if self.options.music_shuffle == "levels":
            musiclist_o = list(range(0, 47))
            musiclist_s = musiclist_o.copy()
            self.random.shuffle(musiclist_s)
            musiclist_o.extend(range(47, 78))
            musiclist_s.extend(range(47, 78))

            if self.options.sadx_music.value == 1:
                musiclist_s = [x+100 for x in musiclist_s]
            elif self.options.sadx_music.value == 2:
                for i in range(len(musiclist_s)):
                    if self.random.randint(0,1):
                        musiclist_s[i] += 100

            return dict(zip(musiclist_o, musiclist_s))
        elif self.options.music_shuffle == "full":
            musiclist_o = list(range(0, 78))
            musiclist_s = musiclist_o.copy()
            self.random.shuffle(musiclist_s)

            if self.options.sadx_music.value == 1:
                musiclist_s = [x+100 for x in musiclist_s]
            elif self.options.sadx_music.value == 2:
                for i in range(len(musiclist_s)):
                    if self.random.randint(0,1):
                        musiclist_s[i] += 100

            return dict(zip(musiclist_o, musiclist_s))
        elif self.options.music_shuffle == "singularity":
            musiclist_o = list(range(0, 78))
            musiclist_s = [self.random.choice(musiclist_o)] * len(musiclist_o)

            if self.options.sadx_music.value == 1:
                musiclist_s = [x+100 for x in musiclist_s]
            elif self.options.sadx_music.value == 2:
                if self.random.randint(0,1):
                    musiclist_s = [x+100 for x in musiclist_s]

            return dict(zip(musiclist_o, musiclist_s))
        else:
            musiclist_o = list(range(0, 78))
            musiclist_s = musiclist_o.copy()

            if self.options.sadx_music.value == 1:
                musiclist_s = [x+100 for x in musiclist_s]
            elif self.options.sadx_music.value == 2:
                for i in range(len(musiclist_s)):
                    if self.random.randint(0,1):
                        musiclist_s[i] += 100

            return dict(zip(musiclist_o, musiclist_s))

    def generate_voice_data(self) -> typing.Dict[int, int]:
        if self.options.voice_shuffle == "shuffled":
            voicelist_o = list(range(0, 2623))
            voicelist_s = voicelist_o.copy()
            self.random.shuffle(voicelist_s)

            return dict(zip(voicelist_o, voicelist_s))
        elif self.options.voice_shuffle == "rude":
            voicelist_o = list(range(0, 2623))
            voicelist_s = voicelist_o.copy()
            self.random.shuffle(voicelist_s)

            for i in range(len(voicelist_s)):
                if self.random.randint(1,100) > 80:
                    voicelist_s[i] = 17

            return dict(zip(voicelist_o, voicelist_s))
        elif self.options.voice_shuffle == "chao":
            voicelist_o = list(range(0, 2623))
            voicelist_s = voicelist_o.copy()
            self.random.shuffle(voicelist_s)

            for i in range(len(voicelist_s)):
                voicelist_s[i] = self.random.choice(range(2586, 2608))

            return dict(zip(voicelist_o, voicelist_s))
        elif self.options.voice_shuffle == "singularity":
            voicelist_o = list(range(0, 2623))
            voicelist_s = [self.random.choice(voicelist_o)] * len(voicelist_o)

            return dict(zip(voicelist_o, voicelist_s))
        else:
            voicelist_o = list(range(0, 2623))
            voicelist_s = voicelist_o.copy()

            return dict(zip(voicelist_o, voicelist_s))

    def generate_chao_egg_data(self) -> typing.Dict[int, int]:
        if self.options.shuffle_starting_chao_eggs:
            egglist_o = list(range(0, 4))
            egglist_s = self.random.sample(range(0,54), 4)

            return dict(zip(egglist_o, egglist_s))
        else:
            # Indicate these are not shuffled
            egglist_o = [0, 1, 2, 3]
            egglist_s = [255, 255, 255, 255]

            return dict(zip(egglist_o, egglist_s))

    def generate_chao_name_data(self) -> typing.Dict[int, int]:
        number_of_names = 30
        name_list_o = list(range(number_of_names * 7))
        name_list_s = []

        name_list_base = []
        name_list_copy = list(self.multiworld.player_name.values())
        name_list_copy.remove(self.multiworld.player_name[self.player])

        if len(name_list_copy) >= number_of_names:
            name_list_base = self.random.sample(name_list_copy, number_of_names)
        else:
            name_list_base = name_list_copy
            self.random.shuffle(name_list_base)

            name_list_base += self.random.sample(sample_chao_names, number_of_names - len(name_list_base))

        for name in name_list_base:
            for char_idx in range(7):
                if char_idx < len(name):
                    name_list_s.append(chao_name_conversion[name[char_idx]])
                else:
                    name_list_s.append(0x00)

        return dict(zip(name_list_o, name_list_s))

    def generate_black_market_data(self) -> typing.Dict[int, int]:
        if self.options.black_market_slots.value == 0:
            return {}

        ring_costs = [50, 75, 100]

        market_data = {}
        item_names = []
        player_names = []
        progression_flags = []
        totally_real_item_names_copy = totally_real_item_names.copy()
        location_names = [(LocationName.chao_black_market_base + str(i)) for i in range(1, self.options.black_market_slots.value + 1)]
        locations = [self.multiworld.get_location(location_name, self.player) for location_name in location_names]
        for location in locations:
            if location.item.classification & ItemClassification.trap:
                item_name = self.random.choice(totally_real_item_names_copy)
                totally_real_item_names_copy.remove(item_name)
                item_names.append(item_name)
            else:
                item_names.append(location.item.name)
            player_names.append(self.multiworld.player_name[location.item.player])

            if location.item.classification & ItemClassification.progression or location.item.classification & ItemClassification.trap:
                progression_flags.append(2)
            elif location.item.classification & ItemClassification.useful:
                progression_flags.append(1)
            else:
                progression_flags.append(0)

        for item_idx in range(self.options.black_market_slots.value):
            for chr_idx in range(len(item_names[item_idx][:26])):
                market_data[(item_idx * 46) + chr_idx] = ord(item_names[item_idx][chr_idx])
            for chr_idx in range(len(player_names[item_idx][:16])):
                market_data[(item_idx * 46) + 26 + chr_idx] = ord(player_names[item_idx][chr_idx])

            market_data[(item_idx * 46) + 42] = ring_costs[progression_flags[item_idx]] * self.options.black_market_price_multiplier.value

        return market_data

    def generate_er_layout(self) -> typing.Dict[int, int]:
        if not self.options.chao_entrance_randomization:
            return {}

        er_layout = {}

        start_exit = self.random.randint(0, 3)
        accessible_rooms = []

        multi_rooms_copy      = multi_rooms.copy()
        single_rooms_copy     = single_rooms.copy()
        all_exits_copy        = all_exits.copy()
        all_destinations_copy = all_destinations.copy()

        multi_rooms_copy.remove(0x07)
        accessible_rooms.append(0x07)

        # Place Kindergarten somewhere sane
        exit_choice = self.random.choice(valid_kindergarten_exits)
        exit_room = exit_to_room_map[exit_choice]
        all_exits_copy.remove(exit_choice)
        multi_rooms_copy.remove(exit_room)

        destination = 0x06
        single_rooms_copy.remove(destination)
        all_destinations_copy.remove(destination)

        er_layout[exit_choice] = destination

        reverse_exit = self.random.choice(room_to_exits_map[destination])

        er_layout[reverse_exit] = exit_to_room_map[exit_choice]

        all_exits_copy.remove(reverse_exit)
        all_destinations_copy.remove(exit_room)

        # Connect multi-exit rooms
        loop_guard = 0
        while len(multi_rooms_copy) > 0:
            loop_guard += 1
            if loop_guard > 2000:
                logging.warning(f"Failed to generate Chao Entrance Randomization for player: {self.multiworld.player_name[self.player]}")
                return {}

            exit_room = self.random.choice(accessible_rooms)
            possible_exits = [exit for exit in room_to_exits_map[exit_room] if exit in all_exits_copy]
            if len(possible_exits) == 0:
                continue
            exit_choice = self.random.choice(possible_exits)
            all_exits_copy.remove(exit_choice)

            destination = self.random.choice(multi_rooms_copy)
            multi_rooms_copy.remove(destination)
            all_destinations_copy.remove(destination)
            accessible_rooms.append(destination)

            er_layout[exit_choice] = destination

            reverse_exit = self.random.choice(room_to_exits_map[destination])

            er_layout[reverse_exit] = exit_room

            all_exits_copy.remove(reverse_exit)
            all_destinations_copy.remove(exit_room)

        # Connect dead-end rooms
        loop_guard = 0
        while len(single_rooms_copy) > 0:
            loop_guard += 1
            if loop_guard > 2000:
                logging.warning(f"Failed to generate Chao Entrance Randomization for player: {self.multiworld.player_name[self.player]}")
                return {}

            exit_room = self.random.choice(accessible_rooms)
            possible_exits = [exit for exit in room_to_exits_map[exit_room] if exit in all_exits_copy]
            if len(possible_exits) == 0:
                continue
            exit_choice = self.random.choice(possible_exits)
            all_exits_copy.remove(exit_choice)

            destination = self.random.choice(single_rooms_copy)
            single_rooms_copy.remove(destination)
            all_destinations_copy.remove(destination)

            er_layout[exit_choice] = destination

            reverse_exit = self.random.choice(room_to_exits_map[destination])

            er_layout[reverse_exit] = exit_room

            all_exits_copy.remove(reverse_exit)
            all_destinations_copy.remove(exit_room)

        # Connect remaining exits
        loop_guard = 0
        while len(all_exits_copy) > 0:
            loop_guard += 1
            if loop_guard > 2000:
                logging.warning(f"Failed to generate Chao Entrance Randomization for player: {self.multiworld.player_name[self.player]}")
                return {}

            exit_room = self.random.choice(all_destinations_copy)
            possible_exits = [exit for exit in room_to_exits_map[exit_room] if exit in all_exits_copy]
            if len(possible_exits) == 0:
                continue
            exit_choice = self.random.choice(possible_exits)
            all_exits_copy.remove(exit_choice)
            all_destinations_copy.remove(exit_room)

            destination = self.random.choice(all_destinations_copy)
            all_destinations_copy.remove(destination)

            er_layout[exit_choice] = destination

            possible_reverse_exits = [exit for exit in room_to_exits_map[destination] if exit in all_exits_copy]
            reverse_exit = self.random.choice(possible_reverse_exits)

            er_layout[reverse_exit] = exit_room

            all_exits_copy.remove(reverse_exit)

        return er_layout
