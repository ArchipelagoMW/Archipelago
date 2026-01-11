from typing import List, Dict, Any, ClassVar

from BaseClasses import Region, Tutorial, MultiWorld, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Items import BombTSAItem, item_data_table, item_table, pommy_shop_genes, item_filler, item_filler_weight, trap_filler, trap_filler_weight, planet_coord_list, elemental_stones
from .Locations import *
from .Options import BombTSAOptions, bomberman_tsa_option_groups
from .Regions import region_data_table
from .Rules import *
from .Rom import MD5Hash, BombTSAProcedurePatch, write_tokens
from .Rom import get_base_rom_path as get_base_rom_path
from .Client import BombTSAClient



import Utils
import dataclasses
import typing
import random
import os
import pkgutil
import Patch
import settings
import logging
import copy

logger = logging.getLogger("Bomberman TSA")

#from .gamemaps import POMMY_SHOP_GENES, SHOP_PART_LOCS

class BombTSASettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Bomberman The Second Attack US rom"""
        copy_to = "BombermanTSA.z64"
        description = "Bomberman The Second Attack (US) ROM File"
        md5s = [MD5Hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)

class BombTSAWebWorld(WebWorld):
    theme = "partyTime"
    
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Bomberman The Second Attack.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["Happyhappyism"]
    )
    
    tutorials = [setup_en]
    option_groups = bomberman_tsa_option_groups

class BombTSAWorld(World):
    """The greatest game of all time."""

    game = "Bomberman The Second Attack"
    data_version = 1
    web = BombTSAWebWorld()
    options: BombTSAOptions
    options_dataclass = BombTSAOptions
    settings: ClassVar[BombTSASettings]
    topology_present = False
    settings_key = "bombermantsa_settings"
    location_name_to_id = location_table
    location_name_to_id.update(shop_location_table)
    location_name_to_id.update(pommy_location_table)
    location_name_to_id.update(powerup_location_table)
    item_name_to_id = item_table

    startbomb = 0
    pommy_shop_hint_map = {}

    def __init__(self, world: MultiWorld, player: int):
        #self.included_stages = create_stage_list(self.options.stage_total.value)
        super().__init__(world, player)

    def create_item(self, name: str) -> BombTSAItem:
        return BombTSAItem(name, item_data_table[name].type, item_data_table[name].code, self.player)
    
    def create_item_no_progression(self, name:str) -> BombTSAItem:
        if item_data_table[name].type == ItemClassification.progression:
            return BombTSAItem(name, ItemClassification.useful, item_data_table[name].code, self.player)
        else:
            return BombTSAItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[BombTSAItem] = []
        
        for name, item in item_data_table.items():
            if item.code and item.can_create(self):# and (name in self.included_stages):
                for x in range(item.num_exist):
                    if name[0:5] == "Pommy" and self.options.pommysanity == False:
                        item_pool.append(self.create_item_no_progression(name))
                    else:
                        item_pool.append(self.create_item(name))
        
        # Starting Element Stone
        # valid_startingstones = ["Fire Stone","Ice Stone","Wind Stone","Earth Stone","Lightning Stone","Light Stone","Dark Stone"]
        valid_startingstones = elemental_stones.copy()
        self.startbomb = self.options.start_element.value
        if self.startbomb == 7:
            self.startbomb = self.random.randint(0,6)
        #logger.warning(f"Starting Element Stone choice index: {self.startbomb}")
        #logger.warning(f"Starting Stones: {valid_startingstones}")
        self.multiworld.push_precollected(self.create_item(valid_startingstones.pop(self.startbomb)))
        #logger.warning(f"Starting Stones: {valid_startingstones}")
        for element in valid_startingstones:
            item_pool.append(self.create_item(element))

        # Starting Planets
        #planet_items = ["Aquanet Coordinates","Horizon Coordinates","Starlight Coordinates",
                        #"Neverland Coordinates","Epikyur Coordinates","Thantos Coordinates"]
        planet_items = planet_coord_list.copy()
        planet_count = (self.options.start_planet.value - 1 )
        if planet_count:
            self.random.shuffle(planet_items)
            for x in range(planet_count):
                self.multiworld.push_precollected(self.create_item(planet_items.pop(0)))
        for planet in planet_items:
            item_pool.append(self.create_item(planet))

        if self.options.pommyshop == 0:
            for gene in pommy_shop_genes:
                item_pool.append(self.create_item(gene))

        if self.options.noah_open.value == 2:
            item_pool.append(self.create_item("Noah Coordinates"))
            
        if self.options.include_warkeys or self.options.noah_open == 1:
            for x in range(3):
                item_pool.append(self.create_item("Warship key"))

        junk = len(self.multiworld.get_unfilled_locations(self.player)) - len(item_pool)
        item_pool += [self.create_item(self.get_filler_item_name()) for _ in range(junk)]
        
        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        #self.included_stages = self.create_stage_list(self.options.stage_total.value)
        #logger.warning(f"{shop_location_table}")
        shop_gene_list_raw = list(shop_loc_list.keys())
        self.random.shuffle(shop_gene_list_raw)
        shop_gene_list = {}
        for i in range(len(pommy_shop_genes)):
            
            shop_loc_name = shop_gene_list_raw.pop(0)
            shop_gene_list[shop_loc_name] = shop_loc_list[shop_loc_name]
        #logger.warning(f"{shop_gene_list}")
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            
            #if region_name in self.included_stages or region_name in fixed_regions:
            region = self.get_region(region_name)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.can_create(self) and location_data.base_loc
            }, BombTSALocation)

            if self.options.shopsanity or self.options.pommyshop:
                if self.options.shopsanity:
                    region.add_locations({
                    location_name: location_data.address for location_name, location_data in location_data_table.items()
                    if location_data.region == region_name and location_data.loc_type == "Shop" # and (region_name in self.included_stages or region_name in fixed_regions)
                    }, BombTSALocation)
                else:
                    #logger.warning(f"{shop_gene_list}")
                    region.add_locations({
                    location_name: shop_address for location_name, shop_address in shop_gene_list.items()
                    if location_data_table[location_name].region == region_name
                    }, BombTSALocation)

                
            if self.options.pommysanity:
                region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.loc_type == "Gene"# and (region_name in self.included_stages or region_name in fixed_regions)
                }, BombTSALocation)
            
            if self.options.powersanity:
                region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.loc_type == "Powerup" # and (region_name in self.included_stages or region_name in fixed_regions)
                }, BombTSALocation)
            region.add_exits(region_data_table[region_name].connecting_regions)


        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self):
                continue
            
            locked_item = self.create_item(location_data_table[location_name].locked_item)
            self.get_location(location_name).place_locked_item(locked_item)
        
        # Place Pommy Genes in Shop Parts
        if self.options.pommyshop:
            genes = pommy_shop_genes
            self.random.shuffle(genes)
            parts = list(shop_gene_list.keys())
            self.random.shuffle(parts)
            for gene in genes:
                #self.pommy_shop_hint_map[gene] = parts[0]
                logger.warning(f"{parts}")
                shop_part = parts.pop(0)
                logger.warning(f"{shop_part}")
                self.get_location(shop_part).place_locked_item(self.create_item(gene))


    def get_filler_item_name(self) -> str:
        filler_items = item_filler
        filler_weights = item_filler_weight
        if self.options.include_traps:
            filler_items.extend(trap_filler)
            filler_weights.extend(trap_filler_weight)
        junk_item = self.random.choices(item_filler,item_filler_weight)[0]
        return junk_item
        # filler_items = ["200 Coins","Heart","Gold Heart"]
        # filler_weights = [0.4,0.8,0.2]
        # if self.options.include_traps:
        #     filler_items.extend(["Stun Trap","Panic Bomb Trap","Fire Trap","Reverse Trap"])
        #     filler_weights.extend([0.3,0.4,0.3,0.4])
        # junk_item = self.random.choices(filler_items,filler_weights)[0]
        # return junk_item

    def set_rules(self) -> None:
        player = self.player
        region_rules = get_region_rules(player)

        for entrance_name, rule in region_rules.items():
            entrance = self.multiworld.get_entrance(entrance_name, player)
            entrance.access_rule = rule

        # Noah Access
        noah_entrance = self.multiworld.get_entrance("Menu -> Noah", player)
        
        match self.options.noah_open.value:
            case 0:
                noah_entrance.access_rule = lambda state: ((sum(
                        (state.can_reach_location("Alcatraz Generator", player),
                        state.can_reach_location("Aquanet Generator", player),
                        state.can_reach_location("Horizon Generator", player),
                        state.can_reach_location("Starlight Generator", player),
                        state.can_reach_location("Neverland Generator", player),
                        state.can_reach_location("Epikyur Generator", player),
                        state.can_reach_location("Thantos Generator", player),)
                        ) >= self.options.planet_required.value))
            case 1:
                lambda state: state.has("Warship Key", player, 3)
            case 2:
                noah_entrance.access_rule = lambda state: state.has("Noah Coordinates", player)

        location_rules = get_location_rules(player)

        for location in self.multiworld.get_locations(player):
            name = location.name
            #if name in location_rules and location_data_table[name].can_create(self.multiworld, player):
            if name in location_rules:
                location.access_rule = location_rules[name]

        # Completion condition.
        match self.options.game_goal.value:
            case 0: # Final Boss
                self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
            case 1: # Generators
                self.multiworld.completion_condition[self.player] = lambda state: sum(
                    (state.can_reach_location("Alcatraz Generator", player),
                    state.can_reach_location("Aquanet Generator", player),
                    state.can_reach_location("Horizon Generator", player),
                    state.can_reach_location("Starlight Generator", player),
                    state.can_reach_location("Neverland Generator", player),
                    state.can_reach_location("Epikyur Generator", player),
                    state.can_reach_location("Thantos Generator", player),)
                    ) >= self.options.planet_required.value
            case 2:
                    self.multiworld.completion_condition[self.player] = lambda state: (
                    state.has("Fire Stone",player) and state.has("Ice Stone",player) and state.has("Wind Stone",player) and state.has("Earth Stone",player)
                    and state.has("Lightning Stone",player) and state.has("Dark Stone",player) and state.has("Light Stone",player) )

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "DeathLink": self.options.death_link.value
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
        
        patch = BombTSAProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        #patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "tsabasepatch.bsdiff4"))
        #procedure = [("apply_bsdiff4", ["base_patch.bsdiff4"]), ("apply_tokens", ["token_data.bin"])]
        procedure = [("apply_tokens", ["token_data.bin"])]
        patch.procedure = procedure
        write_tokens(self, patch, self.startbomb)
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))
        