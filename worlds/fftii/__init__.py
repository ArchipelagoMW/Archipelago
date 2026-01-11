import json
import logging
import os

import Utils
import settings
import typing

from typing import Dict, Any, TextIO
from BaseClasses import MultiWorld, ItemClassification, Tutorial, Item, Region, Entrance
from Utils import version_tuple

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule

from .Items import item_table
from .Locations import all_locations, FinalFantasyTacticsIILocation
from .Logic import create_logic_rule, create_logic_rule_for_list, LogicObject, PoachLogicObject
from .Options import FinalFantasyTacticsIIOptions, fftii_option_groups
from .Rom import FinalFantasyTacticsIIProcedurePatch
from .Client import FinalFantasyTacticsIvaliceIslandClient

from .data.items import zodiac_stone_names, world_map_pass_names, job_names, shop_levels, \
    special_character_names, ramza_job_levels, rare_item_names, shop_item_names, \
    gil_item_names_weighted, earned_job_names, filler_item_names, jp_item_names_weighted
from .data.locations import all_regions, world_map_regions, story_battle_locations, character_recruit_locations, \
    sidequest_battle_locations, job_unlock_locations, rare_battle_locations, default_murond_fights, \
    shop_unlock_locations, monster_location_names, story_zodiac_stone_locations, sidequest_zodiac_stone_locations, \
    ramza_job_unlock_locations, location_sort_list_names, locations_with_text, linked_reward_names, \
    altima_only_story_zodiac_stone_locations, location_groups
from .data.logic.FFTLocation import LocationNames
from .data.logic.Monsters import monster_locations_lookup, monster_family_lookup, monster_families
from .data.logic.regions.Fovoham import fovoham_regions
from .data.logic.regions.Gallione import gallione_regions
from .data.logic.regions.Jobs import jobs_regions
from .data.logic.regions.Lesalia import lesalia_regions
from .data.logic.regions.Limberry import limberry_regions
from .data.logic.regions.Lionel import lionel_regions
from .data.logic.regions.Murond import murond_regions
from .data.logic.regions.Zeltennia import zeltennia_regions
from .data.text import create_text_for_own_item, create_text_for_offworld_item


class FinalFantasyTacticsIISettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Final Fantasy Tactics ISO"""
        description = "Final Fantasy Tactics ISO File"
        copy_to = "Final Fantasy Tactics (USA).bin"
        md5s = ["b156ba386436d20fd5ed8d37bab6b624"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = False


class FinalFantasyTacticsIIWeb(WebWorld):
    theme = "ocean"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Final Fantasy Tactics for Archipelago on your computer.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Rosalie"]
    )

    tutorials = [setup]

    rich_text_options_doc = True
    option_groups = fftii_option_groups


class FinalFantasyTacticsIvaliceIslandWorld(World):
    """
    An open world mod for Final Fantasy Tactics for Archipelago.
    Find all the Zodiac Stones and make your way to Murond Death City to confront Altima!
    """
    settings: typing.ClassVar[FinalFantasyTacticsIISettings]
    game = "Final Fantasy Tactics Ivalice Island"
    options_dataclass = FinalFantasyTacticsIIOptions
    options: FinalFantasyTacticsIIOptions

    base_id = 0
    web = FinalFantasyTacticsIIWeb()

    item_name_to_id = {item: item_data.id for item, item_data in item_table.items()}
    location_name_to_id = {location.name: location.id for location in all_locations}
    item_name_groups = {
        "Zodiac Stones": zodiac_stone_names,
        "Characters": special_character_names,
        "Jobs": job_names
    }

    location_name_groups = location_groups

    filler_items: list[str] | None
    included_locations: list[str]
    murond_fights: list[str]
    starting_pass: str
    zodiac_stones_required: int
    zodiac_stones_in_pool: int

    version = "0.1.0"
    debug = False
    topology_present = debug

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.filler_items = None
        self.included_locations = list()
        self.murond_fights = list()
        self.starting_pass = "Gallione Pass"
        self.zodiac_stones_required = 0

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        logging.info(f"Final Fantasy Tactics Ivalice Island APWorld v{cls.version} used for generation.")

    @classmethod
    def stage_write_spoiler_header(cls, _multiworld: MultiWorld, spoiler_handle: TextIO):
        spoiler_handle.write(f"\nFinal Fantasy Tactics Ivalice Island APWorld version: v{cls.version}\n")

    def create_item(self, name: str) -> "FinalFantasyTacticsIIItem":
        return FinalFantasyTacticsIIItem(name, item_table[name].classification, self.item_name_to_id[name], self.player)

    def create_event(self, name: str) -> "FinalFantasyTacticsIIItem":
        return FinalFantasyTacticsIIItem(name, ItemClassification.progression, None, self.player)

    def generate_early(self) -> None:
        # Story battles are always in
        included_locations: list[LocationNames] = []
        included_locations.extend(story_battle_locations)

        # Character recruitment locations are always in if not tied to a sidequest
        if self.options.sidequest_battles:
            character_recruitments = character_recruit_locations
        else:
            character_recruitments = [
                character for character in character_recruit_locations if character not in sidequest_battle_locations
            ]
        included_locations.extend(character_recruitments)

        # Shop unlocks are always in
        included_locations.extend(shop_unlock_locations)

        # Ramza form unlocks are always in
        included_locations.extend(ramza_job_unlock_locations)

        # Optional locations
        if self.options.sidequest_battles:
            included_locations.extend(sidequest_battle_locations)
        if self.options.job_unlocks:
            included_locations.extend(job_unlock_locations)
        if self.options.rare_battles:
            included_locations.extend(rare_battle_locations)


        if self.options.final_battles == self.options.final_battles.option_vanilla:
            self.murond_fights.extend([fight.value for fight in default_murond_fights])

        self.included_locations = [location.value for location in included_locations]

        if self.options.poach_locations:
            self.included_locations.extend(monster_location_names)

        # Make Zodiac Stones local if option is set

        if self.options.zodiac_stone_locations == self.options.zodiac_stone_locations.option_anywhere_local:
            self.options.local_items.value |= set(zodiac_stone_names)

        self.zodiac_stones_required = self.options.zodiac_stones_required.value
        self.zodiac_stones_in_pool = self.options.zodiac_stones_in_pool.value
        # Determine number of zodiac stones based on options
        if self.options.zodiac_stone_locations == self.options.zodiac_stone_locations.option_vanilla_stones:
            max_stones = len(story_zodiac_stone_locations)
            if self.options.final_battles == self.options.final_battles.option_altima_only:
                max_stones += len(altima_only_story_zodiac_stone_locations)
            if self.options.sidequest_battles:
                max_stones += len(sidequest_zodiac_stone_locations)
            self.zodiac_stones_required = min(self.zodiac_stones_required, max_stones)
            self.zodiac_stones_in_pool = min(self.zodiac_stones_in_pool, max_stones)
        if self.zodiac_stones_in_pool < self.zodiac_stones_required:
            self.zodiac_stones_in_pool = self.zodiac_stones_required

        early_items_dict = {}
        if self.options.early_pass:
            early_pass = self.random.choice(["Fovoham Pass", "Lesalia Pass", "Murond Pass"])
            early_items_dict.update({early_pass: 1})
        if self.options.chemist_placement == self.options.chemist_placement.option_early:
            early_items_dict["Chemist"] = 1
        self.multiworld.early_items[self.player].update(early_items_dict)

        if self.options.chemist_placement == self.options.chemist_placement.option_starting:
            self.options.start_inventory_from_pool.value.update({"Chemist": 1})
            #self.push_precollected(self.create_item("Chemist"))

        if self.options.starting_shop_level > 0:
            shop_level = self.options.starting_shop_level.value
            self.options.start_inventory_from_pool.value.update({"Progressive Shop Level": shop_level})
            #for i in range(shop_level):
            #    self.push_precollected(self.create_item("Progressive Shop Level"))

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        for region_data in all_regions:
            region = Region(region_data.name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Will be adjusted for different starting regions.
        starting_region = self.get_region("Gariland")
        menu.connect(starting_region)
        self.options.start_inventory.value[self.starting_pass] = 1

        # Debug lists
        gallione_locations = []
        fovoham_locations = []
        lesalia_locations = []
        lionel_locations = []
        zeltennia_locations = []
        limberry_locations = []
        murond_locations = []

        # Define connections
        locations_to_add = []
        for origin_region_data in all_regions:
            origin_region = self.get_region(origin_region_data.name)
            for connection in origin_region_data.connections:
                connecting_region = self.get_region(connection.destination.name)
                logic_object = LogicObject(self.player, self.options, 0, self.zodiac_stones_required)
                if self.debug:
                    print(f"Connection: {origin_region.name} to {connecting_region.name}")
                logic_object.requirements = create_logic_rule_for_list(
                    connection.requirements,
                    self.options,
                    self.debug)
                connection_name = f"{origin_region.name} to {connecting_region.name}"
                new_entrance = Entrance(self.player, connection_name, origin_region)
                new_entrance.access_rule = logic_object.logic_rule
                origin_region.exits.append(new_entrance)
                new_entrance.connect(connecting_region)
            for location in origin_region_data.locations:
                if origin_region_data in gallione_regions:
                    gallione_locations.append(location)
                if origin_region_data in fovoham_regions:
                    fovoham_locations.append(location)
                if origin_region_data in lesalia_regions:
                    lesalia_locations.append(location)
                if origin_region_data in lionel_regions:
                    lionel_locations.append(location)
                if origin_region_data in zeltennia_regions:
                    zeltennia_locations.append(location)
                if origin_region_data in limberry_regions:
                    limberry_locations.append(location)
                if origin_region_data in murond_regions:
                    murond_locations.append(location)
                if not location.check_enabled(self.options):
                    if self.debug:
                        print(f"Excluding {location}")
                    continue
                new_location = FinalFantasyTacticsIILocation(
                    self.player,
                    location.name,
                    self.location_name_to_id[location.name],
                    origin_region
                )
                locations_to_add.append(new_location)
        locations_to_add.sort(key=lambda loc: location_sort_list_names.index(loc.name))
        for location in locations_to_add:
            location.parent_region.locations.append(location)
        for region in jobs_regions:
            menu.connect(self.get_region(region.name))

        poach_region = Region("Poaching", self.player, self.multiworld)
        self.multiworld.regions.append(poach_region)
        menu.connect(poach_region)
        if self.options.poach_locations:
            for poach_location in monster_location_names:
                new_location = FinalFantasyTacticsIILocation(
                    self.player, poach_location, self.location_name_to_id[poach_location], poach_region
                )
                poach_region.locations.append(new_location)

        victory_location = self.get_location(LocationNames.AIRSHIPS_2_STORY.value)
        victory_location.place_locked_item(self.create_item("Farlem"))

        # Debug print list and number of locations for analysis purposes
        if self.debug:
            all_region_locations = {
                "Gallione": gallione_locations,
                "Fovoham": fovoham_locations,
                "Lesalia": lesalia_locations,
                "Lionel": lionel_locations,
                "Zeltennia": zeltennia_locations,
                "Limberry": limberry_locations,
                "Murond": murond_locations
            }
            with open("fftlocations.txt", "w") as file:
                for key, value in all_region_locations.items():
                    locations = [location.name for location in value if location.name in self.included_locations]
                    file.write(f"{key} Locations ({len(locations)}):\n")
                    for location in locations:
                        file.write(f"{location}\n")
                    file.write("\n")

        #for fight in self.murond_fights:
        #    self.get_location(fight).place_locked_item(self.create_item(self.random.choice(rare_item_names)))

        if self.debug:
            from Utils import visualize_regions
            visualize_regions(self.get_region("Menu"), f"fftdiagram{self.player}.puml")

    def create_items(self):

        # Get all world map passes we don't start with
        world_map_passes = [item for item in world_map_pass_names if item != self.starting_pass]
        self.push_precollected(self.create_item(self.starting_pass))

        # Squire is always unlocked
        self.options.start_inventory.value["Squire"] = 1
        self.push_precollected(self.create_item("Squire"))

        # If we don't have jobs in the pool, we "start" with them all
        if not self.options.job_unlocks:
            for job_name in earned_job_names:
                self.options.start_inventory.value[job_name] = 1
                self.push_precollected(self.create_item(job_name))

        # Pick Zodiac Stones to place ingame
        zodiac_stones_in_game = self.random.sample(zodiac_stone_names, k=self.zodiac_stones_in_pool)

        # Handle major items
        major_items = [
           *world_map_passes, *shop_levels, *special_character_names, *ramza_job_levels
        ]

        # Place Zodiac Stones if stones are in vanilla spots. Otherwise, add them to itempool.
        if self.options.zodiac_stone_locations == self.options.zodiac_stone_locations.option_vanilla_stones:
            stone_locations = [location.value for location in story_zodiac_stone_locations]
            if self.options.sidequest_battles:
                stone_locations.extend([location.value for location in sidequest_zodiac_stone_locations])
            if self.options.final_battles == self.options.final_battles.option_altima_only:
                stone_locations.extend([location.value for location in altima_only_story_zodiac_stone_locations])
            stone_locations_pruned = self.random.sample(stone_locations, k=self.zodiac_stones_in_pool)
            self.random.shuffle(stone_locations)
            for stone in zodiac_stones_in_game:
                self.get_location(stone_locations_pruned.pop()).place_locked_item(self.create_item(stone))
        else:
            major_items.extend(zodiac_stones_in_game)

        # Add jobs if they're items
        if self.options.job_unlocks:
            major_items.extend(earned_job_names)

        # Get unfilled location count.
        world_locations = self.multiworld.get_unfilled_locations(self.player)
        location_count = len(world_locations)

        # Get filler item count and determine filler pool
        filler_item_count = location_count - len(major_items)
        filler_items = self.determine_filler_item_pool(filler_item_count)

        # Create items
        itempool = [*major_items, *filler_items]
        for item in map(self.create_item, itempool):
            self.multiworld.itempool.append(item)

    def determine_filler_item_pool(self, filler_item_count: int) -> list[str]:

        filler_lists = []
        normal_weight = self.options.normal_item_weight.value
        rare_weight = self.options.rare_item_weight.value
        gil_weight = self.options.bonus_gil_item_weight.value
        jp_weight = self.options.jp_boon_item_weight.value

        # Shortcut if everything's the same weight (or if someone gets funny and sets them all to zero)
        if normal_weight == rare_weight == gil_weight == jp_weight:
            filler_lists = [shop_item_names, rare_item_names, gil_item_names_weighted, jp_item_names_weighted]
        else:
            # One instance of a list per weight value
            for i in range(normal_weight):
                filler_lists.append(shop_item_names)
            for i in range(rare_weight):
                filler_lists.append(rare_item_names)
            for i in range(gil_weight):
                filler_lists.append(gil_item_names_weighted)
            for i in range(jp_weight):
                filler_lists.append(jp_item_names_weighted)
        all_filler = []
        for filler_list in filler_lists:
            all_filler.extend(filler_list)
        filler_set = set(all_filler)
        self.filler_items = sorted(list(filler_set))

        return_list = []
        # For every itempool slot, just pull a random item from each pool in order based on weight
        # Could change this if we want the weights to be random and not static
        for i in range(filler_item_count):
            chosen_list = filler_lists[i % len(filler_lists)]
            chosen_item = self.random.choice(chosen_list)
            return_list.append(chosen_item)
        return return_list

    def set_rules(self):
        # Locations that aren't real don't get rules set, of course
        for location in all_locations:
            if location.name not in self.included_locations:
                continue

            ap_location = self.get_location(location.name)
            if location.name in monster_location_names:
                # Poach locations rules
                monster_object = monster_locations_lookup[location.name[6:]]
                monster_family_name = monster_family_lookup[monster_object.monster_name]
                monster_family = [
                    monster_locations_lookup[monster_name.value] for monster_name in
                    monster_families[monster_family_name]
                ]
                poach_logic_object = PoachLogicObject(self.player, self.options)
                poach_logic_object.requirements = monster_object.compiled_requirements
                breed_logic_object = PoachLogicObject(self.player, self.options)
                breed_logic_object.requirements = []
                for monster in monster_family:
                    breed_logic_object.requirements.extend(monster.compiled_requirements)
                add_rule(
                    ap_location,
                    lambda state,
                           poach_object=poach_logic_object,
                           breed_object=breed_logic_object: poach_object.poach_logic_rule(state) or
                                  (breed_object.poach_logic_rule(state) and state.has("Mediator", self.player)))
            else:
                # Regular location rules
                logic_object = LogicObject(self.player, self.options, location.battle_level, self.zodiac_stones_required)
                if self.debug:
                    print(f"\n{location.name} requirements (Battle level {location.battle_level}):")
                logic_object.requirements = create_logic_rule_for_list(
                    location.requirements, self.options, self.debug)
                add_rule(ap_location, logic_object.logic_rule)

        # Victory condition
        add_rule(
            self.get_location(LocationNames.AIRSHIPS_2_STORY.value),
            lambda state: state.has_group("Zodiac Stones", self.player, self.zodiac_stones_required)
                          and state.can_reach_region("Murond Death City", self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Farlem", self.player)

    def pre_fill(self) -> None:
        pass

    def generate_basic(self):
        pass

    def generate_output(self, output_directory: str) -> None:
        patch_dict: dict[str, Any] = dict()
        # Hash of the MW seed to associate with save file
        patch_dict["SeedHash"] = self.multiworld.seed % 0x7FFF
        patch_dict["APJobs"] = self.options.job_unlocks.value
        patch_dict["RareBattles"] = self.options.rare_battles.value
        patch_dict["Sidequests"] = self.options.sidequest_battles.value
        patch_dict["FinalBattles"] = self.options.final_battles.value
        patch_dict["RequiredStones"] = self.zodiac_stones_required
        patch_dict["EXPMultiplier"] = self.options.exp_gain_multiplier.value
        patch_dict["JPMultiplier"] = self.options.jp_gain_multiplier.value
        patch_dict["LocationDict"] = self.create_location_dict()

        rom_name_text = f'FFTII{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:9}'
        rom_name_text = rom_name_text[:20]
        rom_name = bytearray(rom_name_text, 'utf-8')
        rom_name.extend([0] * (20 - len(rom_name)))
        patch_dict["RomName"] = f'FFTII{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:9}'

        patch_dict["OutputFile"] = f'{self.multiworld.get_out_file_name_base(self.player)}'

        patch = FinalFantasyTacticsIIProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("patch_file.json", json.dumps(patch_dict).encode("UTF-8"))
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)

    def create_location_dict(self):
        locations = self.get_locations()
        location_dict = dict()
        for location in locations:
            if location.name not in locations_with_text:
                continue
            item_locations = [location.name]
            if location.name in linked_reward_names.keys():
                for linked_location in linked_reward_names[location.name]:
                    item_locations.append(linked_location)
            item_strings = []
            is_any_progression: bool = False
            for location_name in item_locations:
                ap_location = self.get_location(location_name)
                item = ap_location.item
                if item.classification & ItemClassification.progression:
                    is_any_progression = True
                    classification = ItemClassification.progression
                elif item.classification & ItemClassification.useful:
                    classification = ItemClassification.useful
                elif item.classification & ItemClassification.trap:
                    classification = ItemClassification.trap
                else:
                    classification = ItemClassification.filler
                player = item.player
                if player == self.player:
                    text = create_text_for_own_item(item.name, classification)
                else:
                    other_game = self.multiworld.game[player]
                    is_fft = other_game == "Final Fantasy Tactics Ivalice Island"
                    text = create_text_for_offworld_item(self.multiworld.player_name[player],
                                                         item.name,
                                                         classification,
                                                         is_fft)
                item_strings.append(text)
            if len(item_strings) > 1:
                if len(item_strings) == 2:
                    item_strings[-1] = " and " + item_strings[-1]
                else:
                    for index, string in enumerate(item_strings[0:-1]):
                        item_strings[index] = string + ", "
                    item_strings[-1] = "and " + item_strings[-1]
            terminator = "!" if is_any_progression else "."
            final_item_string = f"{self.player_name}'s party found " + "".join(item_strings) + terminator
            location_dict[location.name] = final_item_string
        return location_dict

    def modify_multidata(self, multidata: dict):
        import base64
        rom_name_text = f'FFTII{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:9}'
        rom_name_text = rom_name_text[:20]
        rom_name = bytearray(rom_name_text, 'utf-8')
        rom_name.extend([0] * (20 - len(rom_name)))
        new_name = base64.b64encode(bytes(rom_name)).decode()
        multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def get_filler_item_name(self) -> str:
        if self.filler_items is None:
            self.filler_items = ["Potion"]
        return self.random.choice(self.filler_items)

    def fill_slot_data(self) -> Dict[str, Any]:
        return_dict = self.options.as_dict(
            "bonus_gil_item_size",
            "jp_boon_size",
            "sidequest_battles",
            "rare_battles",
            "final_battles",
            "poach_locations",
            "job_unlocks",
            "logical_difficulty"
        )
        return_dict["zodiac_stones_required"] = self.zodiac_stones_required
        return return_dict


class FinalFantasyTacticsIIItem(Item):
    game = "Final Fantasy Tactics Ivalice Island"
