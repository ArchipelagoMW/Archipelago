import os
import threading
import base64
from typing import ClassVar
from BaseClasses import MultiWorld, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule, add_item_rule
from .items import item_table, item_groups, create_item, create_world_items, arch_item_offset, \
    WORLD2_ACCESS_ITEM_ID, WORLD3_ACCESS_ITEM_ID, ITEM_CODE_GIL, ITEM_CODE_FUNGIBLE
from .locations import location_data, loc_id_start
from .options import ffvcd_options
from .regions import create_regions
from .rules import set_rules
from .ffvcd_arch.utilities.data import conductor
from .ffvcd_arch.utilities.data import collectible
from .client import FFVCDSNIClient
from .rom import LocalRom, get_base_rom_path, patch_rom, FFVCDDeltaPatch, USHASH
from collections import Counter
import shutil
import logging
import pkgutil
import settings
from Fill import fill_restrictive

logger = logging.getLogger("Final Fantasy V Career Day")

THIS_FILEPATH = os.path.dirname(__file__)

# lots of credit to others in the repository, such as pokemonrb, dkc3 and tloz

class FFVCDSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the FFV J(1.0) rom with RPGe patch applied"""
        description = "Final Fantasy V ROM File"
        copy_to = "Final Fantasy V (J).sfc"
        md5s = [USHASH]

    rom_file: RomFile = RomFile(RomFile.copy_to)

class FFVCDWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Final Fantasy V Career Day with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["cleartonic"]
    )
    theme = 'ice'
    tutorials = [setup_en]


class FFVCDWorld(World):
    """Final Fantasy V: Career Day"""

    game = "Final Fantasy V Career Day"
    
    options_dataclass = ffvcd_options
    options: ffvcd_options

    settings: ClassVar[FFVCDSettings]
    
    
    topology_present = False
    data_version = 1
    base_id = 776000
    
    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {location.name: location.address for location in location_data}

    item_name_groups = item_groups

    web = FFVCDWebWorld()
    set_rules = set_rules
    
    cond = None
    starting_crystals = None # passed to conductor later
    placed_crystals = []
    placed_abilities = []
    placed_magic = []

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)


    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)
        else:
            import Utils
            cls.rom_file = rom_file
            cls.source_rom_abs_path = os.path.abspath(Utils.user_path(rom_file))

    def generate_early(self):
        self.starting_items = Counter()
        self.world_lock = self.options.world_lock.value + 1
        
        if self.world_lock == 2:
            new_item = create_item("World 2 Access (Item)",  
                        ItemClassification.progression, 
                        None, 
                        self.player, ['World Access'])
            self.starting_items[new_item] = 1
            self.multiworld.push_precollected(new_item)
        if self.world_lock == 3:
            new_item = create_item("World 2 Access (Item)",  
                        ItemClassification.progression, 
                        None, 
                        self.player, ['World Access'])
            self.starting_items[new_item] = 1
            self.multiworld.push_precollected(new_item)
            new_item = create_item("World 3 Access (Item)",  
                        ItemClassification.progression, 
                        None, 
                        self.player, ['World Access'])
            self.starting_items[new_item] = 1
            self.multiworld.push_precollected(new_item)
            
    def create_item(self, name: str):
        item_data = item_table[name]
        return create_item(name, item_data.classification, item_data.id, self.player, item_data.groups)

    def get_filler_item_name(self):
        return self.random.choice([*item_groups[ITEM_CODE_FUNGIBLE], *item_groups[ITEM_CODE_GIL]])

    def create_items(self):
        
        # handle trapped chest items first, which are local only
        # this is to decide number of locations to place these items at
        # then this is passed to item creation 
        
        self.chosen_mib_locations = []        
        
        if self.options.trapped_chests:
            regions = self.multiworld.get_regions().region_cache[self.player]
            
            valid_regions = []
            for region_name, region in regions.items():
                if hasattr(region, "region_rank"):
                    rank = getattr(region, "region_rank")
                    if rank:
                        valid_regions.append(region)            
            LOC_TYPE_CHEST = 1 
            for rank in range(1, 11):
                regions_rank = [i for i in valid_regions if i.region_rank == rank]            
                locations_rank = [[i2 for i2 in i.locations] for i in regions_rank]
                locations_rank = [i for i2 in locations_rank for i in i2] # flatten
                locations_rank = [i for i in locations_rank if i.location_data.location_type == LOC_TYPE_CHEST]
    
                self.random.shuffle(locations_rank)
                chosen_locations_rank = self.random.sample(locations_rank, min(3, len(locations_rank)))
                for i in chosen_locations_rank:
                    i.mib_flag = True
                    self.chosen_mib_locations.append(i)
                    
        self.starting_crystals, self.placed_items, self.mib_items_to_place = create_world_items(self, trapped_chests_flag =\
                                                                  self.options.trapped_chests,\
                                                                  chosen_mib_locations = self.chosen_mib_locations)
        
        ITEM_CODE_ABILITIES = '2'
        ITEM_CODE_CRYSTALS = '3'
        ITEM_CODE_MAGIC = '8'

        for magic in [i for i in self.placed_items if ITEM_CODE_MAGIC in getattr(i, "groups")]: self.placed_magic.append(getattr(magic,"name"))
        for ability in [i for i in self.placed_items if ITEM_CODE_ABILITIES in getattr(i, "groups")]: self.placed_abilities.append(getattr(ability,"name"))
        for crystal in [i for i in self.placed_items if ITEM_CODE_CRYSTALS in getattr(i, "groups")]: self.placed_crystals.append(getattr(crystal,"name"))

        if "Trainer Crystal" not in self.starting_crystals:
            if "Catch Ability" in self.placed_abilities or "Trainer Crystal" in self.placed_crystals:
                add_rule(self.multiworld.get_location("Kelb - CornaJar at Kelb (CornaJar)", self.player),
                lambda state: state.has("Catch Ability", self.player, 1) or state.has("Trainer Crystal", self.player, 1))
            else:
                add_item_rule(self.multiworld.get_location("Kelb - CornaJar at Kelb (CornaJar)", self.player), \
                lambda item: not (item.classification & (ItemClassification.progression or ItemClassification.useful)) and item.player == self.player)

        add_rule(self.multiworld.get_location("Crescent Island - Power Song from Crescent Town (Power)", self.player),
        lambda state: state.has("Adamantite", self.player, 1) or state.has("World 2 Access (Item)", self.player, 1))

        add_rule(self.multiworld.get_location("Piano (Mua)", self.player), \
        lambda state: state.can_reach("Mua", "Region", self.player))

        add_rule(self.multiworld.get_location("Piano (Rugor)", self.player),
        lambda state: state.can_reach("Rugor", "Region", self.player))

        add_rule(self.multiworld.get_location("Crescent Island - Hero Song from Crescent Town (Hero)", self.player), \
        lambda state: state.can_reach("Mirage Village", "Region", self.player))

        add_rule(self.multiworld.get_location("Piano (Mirage)", self.player), \
        lambda state: state.can_reach("Mirage Village", "Region", self.player))
 
    def parse_options_for_conductor(self):
        # this sets up a config file from archipelago's options
        # for FFVCD's base randomizer to work with
        options_conductor = {}
        if self.options.job_palettes:
            options_conductor['job_palettes'] = True
        else:
            options_conductor['job_palettes'] = False
            
        if self.options.four_job:
            options_conductor['four_job'] = True
        else:
            options_conductor['four_job'] = False

           
        if self.options.remove_flashes:
            options_conductor['remove_flashes'] = True
        else:
            options_conductor['remove_flashes'] = False


        if self.options.trapped_chests:
            options_conductor['trapped_chests'] = True
        else:
            options_conductor['trapped_chests'] = False

        if self.options.piano_percent:
            options_conductor['piano_percent'] = True
        else:
            options_conductor['piano_percent'] = False

        options_conductor['source_rom_abs_path'] = self.source_rom_abs_path
        options_conductor['world_lock'] = self.world_lock
        options_conductor['player'] = self.player
        options_conductor['player_name'] = self.multiworld.player_name[self.player]
        options_conductor['all_player_names'] = self.multiworld.player_name
        options_conductor['starting_crystals'] = self.starting_crystals
        options_conductor['ability_settings'] = self.options.ability_settings
        options_conductor['character_names'] = {"Lenna": self.options.lenna_name.value,
            "Galuf": self.options.galuf_name.value,
            "Krile": self.options.krile_name.value,
            "Faris": self.options.faris_name.value,}

        self.options_conductor = options_conductor
        
        return options_conductor
                
    def pre_fill(self):
        if self.options.trapped_chests and self.options.trapped_chests_settings in [0,1]:
            state = self.multiworld.get_all_state(False)
            fill_restrictive(self.multiworld, state, self.chosen_mib_locations, self.mib_items_to_place,
                               single_player_placement=True, lock=True, allow_excluded=True)

    def create_regions(self):
        create_regions(self.multiworld, self.player)

    def generate_output(self, output_directory: str):
        locs = [i for i in self.multiworld.get_locations(self.player)]
        data = {}
        
        for loc in locs:
            if loc.address and loc.item:
                try:
                    lname = loc.item.name
                    data[hex(loc.address - loc_id_start).replace("0x","").upper()] = {'loc_name' : lname,
                                                                       'loc_player' : loc.item.player,
                                                                       'loc_progression' : loc.item.advancement,
                                                                       'loc_mib_flag' : loc.mib_flag,
                                                                       'loc_region_rank' : loc.parent_region.region_rank}
                except:
                    pass
            else:
                if not loc.is_event: #skip warning for event locations
                    print("No item for %s" % loc)

        options_conductor = self.parse_options_for_conductor()



        
        self.cond = conductor.Conductor(self.random, options_conductor, arch_data = data, \
                                        player = self.player, seed = self.multiworld.seed, placed_crystals = self.placed_crystals,\
                                        placed_abilities = self.placed_abilities, placed_magic = self.placed_magic)
        self.cond.randomize()

        # move 
        temp_patch_path = self.cond.save_patch(output_directory)
        self.filename_randomized = self.cond.patch_file(output_directory)

        rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.smc")

        ################
        # new system
        ################
        four_job = "" if self.options_conductor['four_job'] else 'no'
        basepatch_to_use = os.path.join('ffvcd_arch', 
                                        'process',
                                        'basepatch',
                                        "ffv_%sfjf_world%slock.bsdiff4" % (four_job,
                                                              self.options_conductor['world_lock'])
                                        )
        logger.debug("Copying %s -> %s" % (self.source_rom_abs_path, rompath))        
        shutil.copy(self.source_rom_abs_path, rompath)
        rom = LocalRom(rompath)
        rom.write_randomizer_asm_to_file(basepatch_to_use, temp_patch_path, rompath)
        patch_rom(self.multiworld, rom, self.player)
        self.rom_name = rom.name
        rom.write_to_file(rompath)


        patch = FFVCDDeltaPatch(os.path.splitext(rompath)[0]+FFVCDDeltaPatch.patch_file_ending, player=self.player,
                                player_name=self.multiworld.player_name[self.player], patched_path=rompath)
        
        patch.write()

        if os.path.exists(rompath):
            os.unlink(rompath)

        if os.path.exists(self.filename_randomized):
            os.unlink(self.filename_randomized)
            
        if os.path.exists(temp_patch_path):
            os.unlink(temp_patch_path)
        
        self.rom_name_available_event.set() # make sure threading continues and errors are collected
        logger.debug("Finished generate_output function")
        
    def fill_slot_data(self):
        slot_data = self.options.as_dict("four_job", "world_lock", "progression_checks", "trapped_chests")
        #this might look inefficient but due to order of operations this is the simplest way to pull starting ability currently
        slot_data['starting crystals'] = self.starting_crystals
        crystal_id_list = \
        {"Knight Crystal": "Guard",
        "Monk Crystal": "Kick",
        "Thief Crystal": "Escape",
        "Dragoon Crystal": "Jump",
        "Ninja Crystal": "Smoke",
        "Samurai Crystal": "SwdSlap",
        "Berserker Crystal": None,
        "Hunter Crystal": "Animals",
        "MysticKnight Crystal": "MgcSwrd Lv. 1",
        "WhiteMage Crystal": "White Lv. 1",
        "BlackMage Crystal": "Black Lv. 1",
        "TimeMage Crystal": "Time Lv. 1",
        "Summoner Crystal": "Summon Lv. 1",
        "BlueMage Crystal": "Blue",
        "RedMage Crystal": "Red Lv. 1",
        "Trainer Crystal": "Tame",
        "Chemist Crystal": "Mix",
        "Geomancer Crystal": "Terrain",
        "Bard Crystal": "Hide",
        "Dancer Crystal": "Flirt",
        "Mimic Crystal": "Mimic",
        "Freelancer Crystal": None,}
        ability_list = []
        for i in self.starting_crystals:
            ability_list.append(crystal_id_list[i])
        slot_data["starting abilities"] = ability_list
        return slot_data
      
    def modify_multidata(self, multidata: dict):
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
            
    def write_spoiler(self, spoiler_handle) -> None:
        spoiler_handle.write(self.cond.spoiler)