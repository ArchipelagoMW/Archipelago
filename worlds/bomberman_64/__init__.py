from typing import List, Dict, Any, ClassVar

from BaseClasses import Region, Tutorial, MultiWorld, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Items import Bomb64Item, item_data_table, item_table
from .Locations import Bomb64Location, location_data_table, location_table, locked_locations, normal_only_location_data, normal_location_table#, hard_only_location_data, hard_location_table
from .Options import Bomb64Options
from .Regions import region_data_table
from .Rules import *
from .Rom import MD5Hash, Bomb64ProcedurePatch, write_tokens
from .Rom import get_base_rom_path as get_base_rom_path
from .Client import Bomb64Client

import Utils
import dataclasses
import typing
import random
import os
import pkgutil
import Patch
import settings

COLOR_PATCHES = [
    "BomberWhite.bsdiff4",
    "BomberBlack.bsdiff4",
    "BomberRed.bsdiff4",
    "BomberBlue.bsdiff4",
]

class Bomb64Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Bomberman 64 US rom"""
        copy_to = "Bomberman64.z64"
        description = "Bomberman Tournament (US) ROM File"
        md5s = [MD5Hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)

class Bomb64WebWorld(WebWorld):
    theme = "partyTime"
    
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Bomb64.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["Happyhappyism"]
    )
    
    tutorials = [setup_en]


class Bomb64World(World):
    """
    In Bomberman 64, hop between four different elemental worlds (each with its own set of baddies) before going after the main nasty who threatens Planet Bomber. The multi-player Battle mode offers even more explosive action!
    """

    game = "Bomberman 64"
    data_version = 1
    web = Bomb64WebWorld()
    options: Bomb64Options
    options_dataclass = Bomb64Options
    settings: ClassVar[Bomb64Settings]
    topology_present = False
    settings_key = "bomberman64_settings"
    location_name_to_id = location_table
    location_name_to_id.update(normal_location_table)
    #location_name_to_id.update(hard_location_table)
    item_name_to_id = item_table
    

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

    def create_item(self, name: str) -> Bomb64Item:
        return Bomb64Item(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[Bomb64Item] = []
        for name, item in item_data_table.items():
            if item.code and item.can_create(self):
                for x in range(item.num_exist):
                    item_pool.append(self.create_item(name))

        if self.options.max_cards.value < self.options.gold_cards.value:
            gold_total = self.options.gold_cards.value
        else:
            gold_total = self.options.max_cards.value
        for x in range(gold_total):
            item_pool.append(self.create_item("Gold Card"))

        # Check for open stages
        if self.options.open_stages:
            self.multiworld.push_precollected(self.create_item("Green Key"))
            self.multiworld.push_precollected(self.create_item("Green Key"))
            self.multiworld.push_precollected(self.create_item("Blue Key"))
            self.multiworld.push_precollected(self.create_item("Blue Key"))
            self.multiworld.push_precollected(self.create_item("Red Key"))
            self.multiworld.push_precollected(self.create_item("Red Key"))
            self.multiworld.push_precollected(self.create_item("White Key"))
            self.multiworld.push_precollected(self.create_item("White Key"))
        else:
            item_pool.append(self.create_item("Green Key"))
            item_pool.append(self.create_item("Green Key"))
            item_pool.append(self.create_item("Blue Key"))
            item_pool.append(self.create_item("Blue Key"))
            item_pool.append(self.create_item("Red Key"))
            item_pool.append(self.create_item("Red Key"))
            item_pool.append(self.create_item("White Key"))
            item_pool.append(self.create_item("White Key"))


        junk = len(self.multiworld.get_unfilled_locations(self.player)) - len(item_pool)
        item_pool += [self.create_item(self.get_filler_item_name()) for _ in range(junk)]
        
        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Create regions.
        #rainbow_regions = ["Beyond the Clouds","Vs Spellmaker","Doom Castle","The Final Battle"]
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            #if self.options.palace_on:
            self.multiworld.regions.append(region)
            #elif region_name not in rainbow_regions:
            #    self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.get_region(region_name)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.can_create(self)
            }, Bomb64Location)
            region.add_exits(region_data_table[region_name].connecting_regions)

            if self.options.difficulty.value == 0: # Normal mode
                region.add_locations({
                location_name: location_data.address for location_name, location_data in normal_only_location_data.items()
                if location_data.region == region_name and location_data.can_create(self)
                }, Bomb64Location)
            #else:
            #    region.add_locations({
            #    location_name: location_data.address for location_name, location_data in hard_only_location_data.items()
            #    if location_data.region == region_name and location_data.can_create(self)
            #    }, Bomb64Location)

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self):
                continue
            
            locked_item = self.create_item(location_data_table[location_name].locked_item)
            self.get_location(location_name).place_locked_item(locked_item)
        
        if self.options.game_goal.value == 2:
            self.get_location("Winged Guardian Clear").place_locked_item(self.create_item("Boss Medal"))
            self.get_location("Sewer Savage Clear").place_locked_item(self.create_item("Boss Medal"))
            self.get_location("Hot Avenger Clear").place_locked_item(self.create_item("Boss Medal"))
            self.get_location("Cold Killer Clear").place_locked_item(self.create_item("Boss Medal"))

        if not self.options.palace_on:
            from .Locations import palace_excludes 
            for loc_name in palace_excludes:
                self.get_location(loc_name).place_locked_item(self.create_item(self.get_filler_item_name()))

    def get_filler_item_name(self) -> str:
        filler_items = ["Extra Life","5 Gems","Heart","Fast Virus","Sticky Virus","Slow Virus","Bombless Virus","Restless Virus","Death Virus"]
        filler_weights = [0.5, 0.7,0.8, 0.5,0.001,0.4,0.3,0.02,0.05]
        junk_item = random.choices(filler_items,filler_weights)[0]
        return junk_item

    def set_rules(self) -> None:
        player = self.player
        region_rules = get_region_rules(player, (self.options.gold_cards.value))
        #if self.options.palace_on:
        #palace_rules = get_palace_region_rules(player, )
        #region_rules.update(palace_rules)
        # Set Altier rules
        #black_fort_entrance = self.multiworld.get_entrance("Black Fortress -> Vs Altair", player)
        #black_fort_entrance.access_rule =  
        #palace_entrance = self.multiworld.get_entrance(, player)
        #black_fort_entrance.access_rule =  


        for entrance_name, rule in region_rules.items():
            entrance = self.multiworld.get_entrance(entrance_name, player)
            entrance.access_rule = rule
        
        location_rules = get_location_rules(player)
        if self.options.difficulty:
            extra_location_rules = get_hardmode_rules(player)
        else:
            extra_location_rules = get_normalmode_rules(player)

        for location in self.multiworld.get_locations(player):
            name = location.name
            #if name in location_rules and location_data_table[name].can_create(self.multiworld, player):
            if name in location_rules:
                location.access_rule = location_rules[name]
            elif name in extra_location_rules:
                location.access_rule = extra_location_rules[name]

                
        # Completion condition.
        if self.options.game_goal.value == 0: # Altier
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Omnicube", self.player)
        if self.options.game_goal.value == 1: # Gold Cards
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Gold Card", self.player, self.options.gold_cards.value)
        if self.options.game_goal.value == 2: # Bosses
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Boss Medal", self.player, 4)

    def fill_slot_data(self) -> Dict[str, Any]:
        goals = ["altier","goldcards","mainbosses"]
        difficulty = ["normal","hard"]
        return {
            "gold_cards": self.options.gold_cards.value,
            "game_goal": goals[self.options.game_goal.value],
            "difficulty": difficulty[self.options.difficulty.value],
            "DeathLink": self.options.death_link.value,
            "palace": self.options.palace_on.value,

        }
    
    def generate_output(self, output_directory: str):
        outfilepname = f"_P{self.player}"
        outfilepname += f"_{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '_')}"
        self.rom_name_text = f'B64{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0'
        self.romName = bytearray(self.rom_name_text, "utf8")[:0x20]
        self.romName.extend([0] * (0x20 - len(self.romName)))
        self.rom_name = self.romName
        self.playerName = bytearray(self.multiworld.player_name[self.player], "utf8")[:0x20]
        self.playerName.extend([0] * (0x20 - len(self.playerName)))
        
        patch = Bomb64ProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "Stage.bsdiff4"))
        procedure = [("apply_bsdiff4", ["base_patch.bsdiff4"]), ]
        if self.options.color.value > 0:
            patch.write_file("color.bsdiff4", pkgutil.get_data(__name__, COLOR_PATCHES[self.options.color.value]))
            procedure.append(("apply_bsdiff4", ["color.bsdiff4"]))
        procedure.append(("apply_tokens", ["token_data.bin"]))
        #procedure = [("apply_tokens", ["token_data.bin"])]
        patch.procedure = procedure
        write_tokens(self, patch)
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))
