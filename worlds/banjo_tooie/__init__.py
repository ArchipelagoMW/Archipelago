from math import ceil, floor
import random
from multiprocessing import Process
from Options import DeathLink
import settings
import typing
from typing import Dict, Any
from .Items import BanjoTooieItem, all_item_table, all_group_table
from .Locations import BanjoTooieLocation, LocationData, all_location_table, MTLoc_Table, GMLoc_table, WWLoc_table, JRLoc_table, TLLoc_table, GILoc_table, HPLoc_table, CCLoc_table, MumboTokenGames_table, MumboTokenBoss_table, MumboTokenJinjo_table
from .Regions import create_regions, connect_regions
from .Options import BanjoTooieOptions, EggsBehaviour, JamjarsSiloCosts, LogicType, ProgressiveEggAim, ProgressiveWaterTraining, RandomizeBKMoveList, TowerOfTragedy, VictoryCondition
from .Rules import BanjoTooieRules
from .Names import itemName, locationName, regionName
from .WorldOrder import WorldRandomize

#from Utils import get_options
from BaseClasses import ItemClassification, Tutorial, Item, Region, MultiWorld
#from Fill import fill_restrictive
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch_subprocess


def run_client():
    from worlds.banjo_tooie.BTClient import main  # lazy import
    launch_subprocess(main)

components.append(Component("Banjo-Tooie Client", func=run_client, component_type=Type.CLIENT))

#NOTE! For Backward Compatability, don't use type str|None. multi types not allowed on older Pythons
class BanjoTooieWeb(WebWorld):
    setup_en = Tutorial("Setup Banjo-Tooie",
        """A guide to setting up Archipelago Banjo-Tooie on your computer.""",
        "English",
        "setup_en.md",
        "setup/en",
        ["Beebaleen"])

    setup_fr = Tutorial("Setup Banjo-Tooie",
        """A guide to setting up Archipelago Banjo-Tooie on your computer.""",
        "French",
        "setup_fr.md",
        "setup/fr",
        ["g0goTBC"])

    tutorials = [setup_en, setup_fr]


class BanjoTooieWorld(World):
    """
    Banjo-Tooie is a single-player platform game in which the protagonists are controlled from a third-person perspective.
    Carrying over most of the mechanics and concepts established in its predecessor,
    the game features three-dimensional worlds consisting of various platforming challenges and puzzles, with a notable
    increased focus on puzzle-solving over the worlds of Banjo-Kazooie.
    """

    game: str = "Banjo-Tooie"
    web = BanjoTooieWeb()
    topology_present = True
    # item_name_to_id = {name: data.btid for name, data in all_item_table.items()}
    item_name_to_id = {}

    for name, data in all_item_table.items():
        if data.btid is None:  # Skip Victory Item
            continue
        item_name_to_id[name] = data.btid

    location_name_to_id = {name: data.btid for name, data in all_location_table.items()}
    location_name_to_group = {name: data.group for name, data in all_location_table.items()}

    item_name_groups = {
        # "Jiggy": all_group_table["jiggy"],
        "Jinjo": all_group_table["jinjo"],
        "Moves": all_group_table["moves"],
        "Magic": all_group_table["magic"],
        "Stations": all_group_table["stations"],
        "StopnSwap": all_group_table["stopnswap"],
        "Access": all_group_table["levelaccess"],
        "Dino": all_group_table["dino"]
    }

    options_dataclass =  BanjoTooieOptions
    options: BanjoTooieOptions

    def __init__(self, world, player):
        self.version = "V4.1"
        self.kingjingalingjiggy = False
        self.starting_egg: int = 0
        self.starting_attack: int = 0
        self.jiggy_counter: int = 0
        self.doubloon_counter: int = 0
        self.notecounter: int = 0
        self.slot_data = []
        self.randomize_worlds = {}
        self.randomize_order = {}
        self.worlds_randomized = False
        self.single_silo = ""
        self.loading_zones = {}
        self.jamjars_siloname_costs = {}
        self.jamjars_silo_costs = {}
        super(BanjoTooieWorld, self).__init__(world, player)

    def item_code(self, itemname: str) -> int:
        return all_item_table[itemname].btid

    def create_item(self, itemname: str) -> Item:
        banjoItem = all_item_table.get(itemname)
        if not banjoItem:
            raise Exception(f"{itemname} is not a valid item name for Banjo-Tooie")
        if banjoItem.type == "progress":
            if banjoItem.btid == self.item_code(itemName.JIGGY):
                if not hasattr(self.multiworld, "generation_is_fake"):
                    maxJiggy = max(self.randomize_worlds.values())
                    if not self.options.open_hag1:
                        maxJiggy = max(maxJiggy, 70)

                    extraJiggys = (90 - maxJiggy)/2
                    if self.jiggy_counter > (maxJiggy+extraJiggys):
                        item_classification = ItemClassification.filler
                    elif self.jiggy_counter > maxJiggy:
                        item_classification = ItemClassification.useful
                    else:
                        item_classification = ItemClassification.progression
                    self.jiggy_counter += 1
                else:
                    item_classification = ItemClassification.progression
            elif banjoItem.btid == self.item_code(itemName.NOTE) and self.options.randomize_notes:
                if not hasattr(self.multiworld, "generation_is_fake"):
                    total_clefs = 20 * (self.options.extra_trebleclefs_count + 9) + 10 * self.options.bass_clef_amount
                    progression_five_packs = int(max(0, max(self.jamjars_siloname_costs.values())-total_clefs)/5)
                    useful_five_packs = floor((900-total_clefs-progression_five_packs*5)/5/2)
                    # filler_five_packs = ceil((900-total_clefs-progression_five_packs*5)/5/2)
                    if self.notecounter <= progression_five_packs:
                        item_classification = ItemClassification.progression
                    elif self.notecounter > progression_five_packs and self.notecounter <= progression_five_packs + useful_five_packs:
                        item_classification = ItemClassification.useful
                    else:
                        item_classification = ItemClassification.filler
                    self.notecounter += 1
                else:
                    item_classification = ItemClassification.progression
            else:
                item_classification = ItemClassification.progression
        if banjoItem.type == "progression_skip_balancing": #Mumbo Tokens
            item_classification = ItemClassification.progression_skip_balancing
        if banjoItem.type == "useful":
            if banjoItem.btid == self.item_code(itemName.PAGES): # Cheato pages
                if self.options.cheato_rewards:
                    item_classification = ItemClassification.progression
                else:
                    item_classification = ItemClassification.filler
            elif banjoItem.btid == self.item_code(itemName.HONEY) and self.options.honeyb_rewards: #Honeycombs
                item_classification = ItemClassification.progression
            else:
                item_classification = ItemClassification.useful

        if banjoItem.type == "filler":
            item_classification = ItemClassification.filler

        if banjoItem.type == "trap":
            item_classification = ItemClassification.trap

        if banjoItem.type == "victory":
            victory_item = BanjoTooieItem("Kick Around", ItemClassification.filler, None, self.player)
            return victory_item

        created_item = BanjoTooieItem(self.item_id_to_name[banjoItem.btid], item_classification, banjoItem.btid, self.player)
        return created_item

    def create_event_item(self, name: str) -> Item:
        item_classification = ItemClassification.progression
        created_item = BanjoTooieItem(name, item_classification, None, self.player)
        return created_item

    def create_items(self) -> None:
        itempool = []
        ############## START OF TRAP / BIG O PANTS COUNTER #######################################
        trap_big_pants_counter = 0
        removed_enests = 0
        removed_fnests = 0
        if self.options.cheato_rewards and not self.options.randomize_bk_moves:
            for i in range(5):
                trap_big_pants_counter += 1
        if self.options.honeyb_rewards and not self.options.randomize_bk_moves: #10 if both options are on
            for i in range(5):
                trap_big_pants_counter += 1
        if self.options.randomize_bk_moves == RandomizeBKMoveList.option_mcjiggy_special: # 2 moves won't be added to the pool
            for i in range(2):
                trap_big_pants_counter += 1
        if not self.options.randomize_bk_moves: # No moves added, fills for the Jiggy Chunks, Dino Kids
            for i in range(6):
                trap_big_pants_counter += 1
        if self.options.bass_clef_amount > 0:
            for i in range(self.options.bass_clef_amount): #adds an additional big-o-pants for each bass clef
                trap_big_pants_counter += 1
        if self.options.extra_trebleclefs_count > 0:
            for i in range(self.options.extra_trebleclefs_count*3): #adds an additional big-o-pants for each bass clef
                if self.options.victory_condition == VictoryCondition.option_token_hunt and \
                (((self.options.bass_clef_amount * 2) + (self.options.extra_trebleclefs_count * 4)) >= 130) and \
                i == (self.options.extra_trebleclefs_count*3 - 15):
                    break
                trap_big_pants_counter += 1
        if self.options.traps and self.options.nestsanity:
            total_nests = all_item_table[itemName.ENEST].qty + all_item_table[itemName.FNEST].qty

            removed_nests = int(total_nests * self.options.traps_nests_ratio / 100)
            removed_enests = int(all_item_table[itemName.ENEST].qty * self.options.traps_nests_ratio / 100)
            removed_fnests = removed_nests - removed_enests

            trap_big_pants_counter += removed_nests + all_item_table[itemName.GNEST].qty
        elif self.options.nestsanity: # nestsanity with no traps, remove gnests
            trap_big_pants_counter += all_item_table[itemName.GNEST].qty

        if self.options.traps:
            trap_list = self.random.choices(["gnests", "ttrap", "strap", "trtrap", "sqtrap"], weights = [
                self.options.golden_eggs_weight if self.options.nestsanity else 0,
                self.options.trip_trap_weight,
                self.options.slip_trap_weight,
                self.options.transform_trap_weight,
                self.options.squish_trap_weight,
            ], k = trap_big_pants_counter)

        ############## END OF TRAP / BIG O PANTS COUNTER #######################################
        for name,id in all_item_table.items():
            item = self.create_item(name)
            if self.item_filter(item):
                if item.code == self.item_code(itemName.JIGGY) and self.kingjingalingjiggy:
                    for i in range(id.qty - 1): #note the -1 in the count here. King Took one already.
                        if not self.options.randomize_jinjos and self.jiggy_counter > 81:
                            break
                        else:
                            itempool += [self.create_item(name)]
                else:
                    # Mumbo Token Hunt Item Amt
                    if item.code == self.item_code(itemName.MUMBOTOKEN) and self.options.victory_condition == VictoryCondition.option_token_hunt:
                        for i in range(15):
                            itempool += [self.create_item(name)]
                    # EO Mumbo Token Hunt Item Amt

                    #if none in pool
                    elif item.code == self.item_code(itemName.NONE):
                       for i in range(trap_big_pants_counter):
                            itempool += [self.create_item(name)]
                    elif item.code == self.item_code(itemName.TTRAP):
                        for i in range(trap_list.count("ttrap")):
                            itempool += [self.create_item(name)]
                    elif item.code == self.item_code(itemName.STRAP):
                        for i in range(trap_list.count("strap")):
                            itempool += [self.create_item(name)]
                    elif item.code == self.item_code(itemName.TRTRAP):
                        for i in range(trap_list.count("trtrap")):
                            itempool += [self.create_item(name)]
                    elif item.code == self.item_code(itemName.SQTRAP):
                        for i in range(trap_list.count("sqtrap")):
                            itempool += [self.create_item(name)]
                    elif item.code == self.item_code(itemName.GNEST):
                        for i in range(trap_list.count("gnests")):
                            itempool += [self.create_item(name)]
                    #end of none qty logic

                    #nests removal for nestsanity and nest traps
                    elif item.code == self.item_code(itemName.ENEST):
                        for i in range(all_item_table[item.name].qty - removed_enests):
                            itempool += [self.create_item(name)]
                    elif item.code == self.item_code(itemName.FNEST):
                        for i in range(all_item_table[item.name].qty - removed_fnests):
                            itempool += [self.create_item(name)]
                    #end of nest removal for nest traps

                    #notes - extra other notes
                    elif item.code == self.item_code(itemName.NOTE):
                        count = id.qty
                        count -= ((self.options.bass_clef_amount*2) + (self.options.extra_trebleclefs_count*4))
                        for i in range(count):
                            if self.options.victory_condition == VictoryCondition.option_token_hunt:
                                if (count - self.notecounter) < 15 and count >= 15:
                                    break #sub in for Mumbo Tokens up to 15
                            itempool += [self.create_item(name)]

                    #treble - extra trebles
                    elif item.code == self.item_code(itemName.TREBLE) and self.options.extra_trebleclefs_count > 0: #add more Trebles
                        count = id.qty
                        count += self.options.extra_trebleclefs_count
                        for i in range(count):
                            itempool += [self.create_item(name)]
                    #bass clef - extra bass clef
                    elif item.code == self.item_code(itemName.BASS) and self.options.bass_clef_amount > 0: #add Bass clefs
                        count = id.qty
                        count += self.options.bass_clef_amount
                        for i in range(count):
                            itempool += [self.create_item(name)]
                    else:
                        for i in range(id.qty):
                            if not self.options.randomize_jinjos and self.jiggy_counter > 81 and item.code == self.item_code(itemName.JIGGY):
                                break
                            else:
                                itempool += [self.create_item(name)]
            elif item.code == self.item_code(itemName.PBASH) and item.code == self.starting_attack and self.options.progressive_bash_attack: #we only need 1 more Progressive Bash Attack
                itempool += [self.create_item(name)] #only creates 1 progressive bash attack
            elif self.check_starting_progressive(item) > 0:
                for i in range(self.check_starting_progressive(item)):
                    itempool += [item]
        self.multiworld.itempool.extend(itempool)

    def item_filter(self, item: Item) -> Item:
        if(item.code == self.item_code(itemName.JIGGY) and not self.kingjingalingjiggy and self.options.jingaling_jiggy):
            #Below give the king a guarentee Jiggy if option is set
            self.get_location(self.location_id_to_name[1230685]).place_locked_item(item)
            self.kingjingalingjiggy = True
            return True #doesn't need to be in the Pool.

        if item.code == 0: #Events
            return False

        if(item.code == self.item_code(itemName.DOUBLOON) and not self.options.randomize_doubloons) :
            return False

        if(item.code == self.item_code(itemName.PAGES) and not self.options.randomize_cheato) : # Added later in Prefill
            return False

        if(item.code == self.item_code(itemName.HONEY) and not self.options.randomize_honeycombs) : # Added later in Prefill
            return False

        if(item.code in range(self.item_code(itemName.GGRAB), self.item_code(itemName.AMAZEOGAZE) + 1) and not self.options.randomize_moves) : #range you need to add +1 to the end.
            return False

        if(item.code in range(self.item_code(itemName.HUMBAMT), self.item_code(itemName.HUMBAIH) + 1) and not self.options.randomize_glowbos) : #range you need to add +1 to the end.
            return False

        if(item.code in range(self.item_code(itemName.MUMBOMT), self.item_code(itemName.MUMBOIH) + 1) and not self.options.randomize_glowbos) : #range you need to add +1 to the end.
            return False

        if(item.code in range(self.item_code(itemName.WJINJO), self.item_code(itemName.BKJINJO) + 1) and not self.options.randomize_jinjos) :#range you need to add +1 to the end.
            return False

        if(item.code == self.item_code(itemName.TREBLE) and not self.options.randomize_treble):
            return False

        if item.code == self.item_code(itemName.CHUFFY) and not self.options.randomize_chuffy:
            return False

        if item.code in range(self.item_code(itemName.TRAINSWGI), self.item_code(itemName.TRAINSWWW) + 1) and not self.options.randomize_stations:
            return False

        if item.code == self.item_code(itemName.NOTE) and not self.options.randomize_notes: #Notes
            return False

        if item.code == self.item_code(itemName.MUMBOTOKEN) and self.options.victory_condition != VictoryCondition.option_token_hunt: #Mumbo Tokens for Mini Game and Boss Hunt and Jinjo Fam
            return False

        # if item.code == self.item_code(itemName.IKEY) and self.options.warp_traps == 0:
        #     return False

        # from itemName.MTA to itemName.CKA inclusive
        if item.code in range(self.item_code(itemName.MTA), self.item_code(itemName.CKA) + 1):
            return False

        #from itemName.IKEY to itemName.PMEGG inclusive
        if item.code in range(self.item_code(itemName.IKEY), self.item_code(itemName.PMEGG) + 1) and not self.options.randomize_stop_n_swap:
            return False

        #from itemName.DIVE, to itemName.BBOMB inclusive
        if item.code in range(self.item_code(itemName.DIVE), self.item_code(itemName.BBOMB) + 1) and self.options.randomize_bk_moves == RandomizeBKMoveList.option_none:
            return False
        elif (item.code == self.item_code(itemName.TTROT) or item.code == self.item_code(itemName.TJUMP)) and self.options.randomize_bk_moves == RandomizeBKMoveList.option_mcjiggy_special: # talon trot and tall jump not in pool
            return False

        if item.code == self.item_code(itemName.GNEST) and\
            (not self.options.nestsanity or not self.options.traps): #Golden egg nests
            return False
        if item.code == self.item_code(itemName.ENEST) and not self.options.nestsanity: #egg nests
            return False
        if item.code == self.item_code(itemName.FNEST) and not self.options.nestsanity: #Feather nests
            return False

        # if item.code == self.item_code(itemName.NONE) and self.options.cheato_rewards == False and self.options.honeyb_rewards == False:
        #     return False
        if item.code == self.item_code(itemName.NONE) and self.options.randomize_bk_moves == RandomizeBKMoveList.option_all \
            and (self.options.bass_clef_amount == 0 and self.options.extra_trebleclefs_count == 0):
            return False
        if item.code == self.item_code(itemName.NONE) and self.options.traps:
            return False

        if (item.code == self.item_code(itemName.TTRAP) or item.code == self.item_code(itemName.STRAP) or \
            item.code == self.item_code(itemName.TRTRAP) or item.code == self.item_code(itemName.SQTRAP)) and not self.options.traps:
            return False

        if self.options.progressive_beak_buster and (item.code == self.item_code(itemName.BBUST) or item.code == self.item_code(itemName.BDRILL)):
            return False

        if item.code == self.item_code(itemName.PBBUST) and not self.options.progressive_beak_buster:
            return False

        if item.code == self.item_code(itemName.PFLIGHT) and not self.options.progressive_flight:
            return False

        if item.code == self.item_code(itemName.PEGGAIM) and self.options.progressive_egg_aiming != ProgressiveEggAim.option_basic:
            return False

        if item.code == self.item_code(itemName.PAEGGAIM) and self.options.progressive_egg_aiming != ProgressiveEggAim.option_advanced:
            return False

        if item.code == self.item_code(itemName.PASWIM) and self.options.progressive_water_training != ProgressiveWaterTraining.option_advanced:
            return False

        if self.options.egg_behaviour != EggsBehaviour.option_random_starting_egg and item.code == self.item_code(itemName.BEGGS): #remove blue eggs in pool
            return False
        if self.options.egg_behaviour == EggsBehaviour.option_progressive_eggs and (item.code == self.item_code(itemName.FEGGS) or\
            item.code == self.item_code(itemName.GEGGS) or item.code == self.item_code(itemName.IEGGS) or item.code == self.item_code(itemName.CEGGS)):
            return False
        if item.code == self.item_code(itemName.PEGGS) and self.options.egg_behaviour != EggsBehaviour.option_progressive_eggs:
            return False
        if self.options.egg_behaviour == EggsBehaviour.option_random_starting_egg and item.code == self.starting_egg: #Already has this egg in inventory
            return False

        if self.options.progressive_shoes and (item.code == self.item_code(itemName.SSTRIDE) or item.code == self.item_code(itemName.TTRAIN) \
            or item.code == self.item_code(itemName.SPRINGB) or item.code == self.item_code(itemName.CLAWBTS)):
            return False
        if item.code == self.item_code(itemName.PSHOES) and not self.options.progressive_shoes:
            return False

        if self.options.progressive_water_training != ProgressiveWaterTraining.option_none and (item.code == self.item_code(itemName.DIVE) or item.code == self.item_code(itemName.DAIR) \
            or item.code == self.item_code(itemName.FSWIM)):
            return False
        if self.options.progressive_water_training == ProgressiveWaterTraining.option_advanced and (item.code == self.item_code(itemName.AUQAIM) or item.code == self.item_code(itemName.TTORP)):
            return False
        if item.code == self.item_code(itemName.PSWIM) and self.options.progressive_water_training != ProgressiveWaterTraining.option_basic:
            return False

        if self.options.progressive_flight and (item.code == self.item_code(itemName.FPAD) or item.code == self.item_code(itemName.BBOMB) or item.code == self.item_code(itemName.AIREAIM)):
            return False

        if self.options.progressive_egg_aiming != ProgressiveEggAim.option_none and (item.code == self.item_code(itemName.EGGAIM) or item.code == self.item_code(itemName.EGGSHOOT)):
            return False
        if self.options.progressive_egg_aiming == ProgressiveEggAim.option_advanced and (item.code == self.item_code(itemName.AMAZEOGAZE) or item.code == self.item_code(itemName.BBLASTER)):
            return False

        if self.options.progressive_bash_attack and (item.code == self.item_code(itemName.BBASH) or item.code == self.item_code(itemName.GRAT)):
            return False
        if item.code == self.item_code(itemName.PBASH) and not self.options.progressive_bash_attack:
            return False

        if item.code == self.item_code(itemName.ROAR) and not self.options.randomize_dino_roar:
            return False

        if self.options.randomize_bk_moves != RandomizeBKMoveList.option_none and item.code == self.starting_attack: #Already has this attack in inventory
            return False

        return True

    def check_starting_progressive(self, item: Item) -> int:
        if item.code == self.starting_attack and (item.code in range(1230828, 1230833) or item.code in range(1230782, 1230786)):
            return all_item_table[item.name].qty - 1
        return 0

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)
        self.pre_fill_me()

    def generate_early(self) -> None:
        if self.options.randomize_worlds and self.options.randomize_bk_moves != RandomizeBKMoveList.option_none and self.options.logic_type == LogicType.option_intended:
            raise ValueError("Randomize Worlds and Randomize BK Moves is not compatible with Beginner Logic.")
        if not self.options.randomize_notes and self.options.randomize_worlds and self.options.randomize_bk_moves != RandomizeBKMoveList.option_none:
            if self.multiworld.players == 1:
                raise ValueError("Randomize Notes is required for Randomize BK Moves and Randomize Worlds enabled.")
        if not self.options.randomize_notes and (self.options.extra_trebleclefs_count != 0 and self.options.bass_clef_amount != 0):
            raise ValueError("Randomize Notes is required to add extra Treble Clefs or Bass Clefs")
        if self.options.progressive_beak_buster and (not self.options.randomize_bk_moves or not self.options.randomize_moves):
            raise ValueError("You cannot have progressive Beak Buster without randomizing moves and randomizing BK moves")
        if self.options.egg_behaviour == EggsBehaviour.option_random_starting_egg and (not self.options.randomize_bk_moves or not self.options.randomize_moves):
            raise ValueError("You cannot have Randomize Starting Egg without randomizing moves and randomizing BK moves")
        elif self.options.egg_behaviour == EggsBehaviour.option_progressive_eggs and not self.options.randomize_moves:
            raise ValueError("You cannot have progressive Eggs without randomizing moves")
        if self.options.progressive_shoes and (not self.options.randomize_bk_moves or not self.options.randomize_moves):
            raise ValueError("You cannot have progressive Shoes without randomizing moves and randomizing BK moves")
        if self.options.progressive_water_training != ProgressiveWaterTraining.option_none and (self.options.randomize_bk_moves == RandomizeBKMoveList.option_none or not self.options.randomize_moves):
            raise ValueError("You cannot have progressive Water Training without randomizing moves and randomizing BK moves")
        if self.options.progressive_flight and (not self.options.randomize_bk_moves or not self.options.randomize_moves):
            raise ValueError("You cannot have progressive flight without randomizing moves and randomizing BK moves")
        if self.options.progressive_egg_aiming != ProgressiveEggAim.option_none and (not self.options.randomize_bk_moves or not self.options.randomize_moves):
            raise ValueError("You cannot have progressive egg aiming without randomizing moves and randomizing BK moves")
        if self.options.progressive_bash_attack and (not self.options.randomize_stop_n_swap or not self.options.randomize_moves):
            raise ValueError("You cannot have progressive bash attack without randomizing Stop N Swap and randomizing BK moves")
        if not self.options.randomize_moves and self.options.jamjars_silo_costs != JamjarsSiloCosts.option_vanilla:
            raise ValueError("You cannot change the silo costs without randomizing Jamjars' moves.")
        if not self.options.open_hag1 and self.options.victory_condition == VictoryCondition.option_wonderwing_challenge:
            self.options.open_hag1 = True


        if self.options.egg_behaviour == EggsBehaviour.option_random_starting_egg:
            eggs = list([itemName.BEGGS, itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS])
            self.random.shuffle(eggs)
            starting_egg = self.create_item(eggs[0])
            self.multiworld.push_precollected(starting_egg)
            banjoItem = all_item_table.get(eggs[0])
            self.starting_egg = banjoItem.btid
        else:
            starting_egg = self.create_item(itemName.BEGGS)
            self.multiworld.push_precollected(starting_egg)
            banjoItem = all_item_table.get(itemName.BEGGS)
            self.starting_egg = banjoItem.btid

        if self.options.randomize_bk_moves != RandomizeBKMoveList.option_none:
            chosen_attack: str
            base_attacks: list
            if self.options.logic_type == LogicType.option_intended:
                if self.options.progressive_egg_aiming == ProgressiveEggAim.option_basic:
                    base_attacks = [itemName.PEGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT]
                elif self.options.progressive_egg_aiming == ProgressiveEggAim.option_advanced:
                    base_attacks = [itemName.PAEGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT]
                else:
                    base_attacks = [itemName.EGGSHOOT, itemName.EGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT]
            if self.options.logic_type == LogicType.option_easy_tricks:
                if self.options.progressive_egg_aiming == ProgressiveEggAim.option_basic:
                    base_attacks = [itemName.PEGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT, itemName.WWING]
                elif self.options.progressive_egg_aiming == ProgressiveEggAim.option_advanced:
                    base_attacks = [itemName.PAEGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT, itemName.WWING]
                else:
                    base_attacks = [itemName.EGGSHOOT, itemName.EGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT, itemName.WWING]
            else:
                if self.options.progressive_egg_aiming == ProgressiveEggAim.option_basic:
                    base_attacks = [itemName.PEGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT, itemName.WWING]
                elif self.options.progressive_egg_aiming == ProgressiveEggAim.option_advanced:
                    base_attacks = [itemName.PAEGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT, itemName.WWING]
                else:
                    base_attacks = [itemName.EGGSHOOT, itemName.EGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT, itemName.WWING]
                base_attacks.append(itemName.PBASH if self.options.progressive_bash_attack else itemName.GRAT)
                base_attacks.append(itemName.PBBUST if self.options.progressive_beak_buster else itemName.BBUST)
            chosen_attack = self.random.choice(base_attacks)

            starting_attack = self.create_item(chosen_attack)
            self.multiworld.push_precollected(starting_attack)
            banjoItem = all_item_table.get(chosen_attack)
            self.starting_attack = banjoItem.btid
        WorldRandomize(self)

    def set_rules(self) -> None:
        rules = Rules.BanjoTooieRules(self)
        return rules.set_rules()

    def pre_fill_me(self) -> None:
        if not self.options.randomize_honeycombs:
            self.banjo_pre_fills(itemName.HONEY, "Honeycomb", False)

        if not self.options.randomize_cheato:
            self.banjo_pre_fills(itemName.PAGES, "Cheato Page", False)

        if not self.options.randomize_doubloons:
            self.banjo_pre_fills(itemName.DOUBLOON, "Doubloon", False)

        if not self.options.randomize_moves:
            self.banjo_pre_fills("Moves", None, True)

        if not self.options.randomize_dino_roar:
            self.banjo_pre_fills("Dino", None, True)

        if not self.options.randomize_glowbos:
            self.banjo_pre_fills("Magic", None, True)

        if not self.options.randomize_treble:
            self.banjo_pre_fills(itemName.TREBLE, "Treble Clef", False)

        if not self.options.randomize_stations:
            self.banjo_pre_fills("Stations", None, True)

        if not self.options.randomize_chuffy:
            self.banjo_pre_fills(itemName.CHUFFY, "Chuffy", False)

        if not self.options.randomize_notes:
            self.banjo_pre_fills(itemName.NOTE, "Note", False)

        if not self.options.randomize_stop_n_swap:
            self.banjo_pre_fills("StopnSwap", None, True)

        if not self.worlds_randomized and self.options.skip_puzzles:
            self.banjo_pre_fills("Access", None, True)
        elif self.worlds_randomized:
            world_num = 1
            for world, amt in self.randomize_worlds.items():
                if world == regionName.GIO:
                    item = self.create_item(itemName.GIA)
                elif world == regionName.JR:
                    item = self.create_item(itemName.JRA)
                else:
                    item = self.create_item(world)
                self.get_location("World "+ str(world_num) +" Unlocked").place_locked_item(item)
                world_num += 1
        else:
            world_num = 1
            for world, amt in self.randomize_worlds.items():
                item = self.create_item(itemName.NONE)
                self.get_location("World "+ str(world_num) +" Unlocked").place_locked_item(item)
                world_num += 1

        if self.options.victory_condition == VictoryCondition.option_minigame_hunt\
            or self.options.victory_condition == VictoryCondition.option_wonderwing_challenge:

            item = self.create_item(itemName.MUMBOTOKEN)
            for location_name in MumboTokenGames_table.keys():
                self.get_location(location_name).place_locked_item(item)

        if self.options.victory_condition == VictoryCondition.option_boss_hunt\
            or self.options.victory_condition == VictoryCondition.option_wonderwing_challenge:

            item = self.create_item(itemName.MUMBOTOKEN)
            for location_name in MumboTokenBoss_table.keys():
                self.get_location(location_name).place_locked_item(item)

        if self.options.victory_condition == VictoryCondition.option_jinjo_family_rescue\
            or self.options.victory_condition == VictoryCondition.option_wonderwing_challenge:
            item = self.create_item(itemName.MUMBOTOKEN)
            for location_name in MumboTokenJinjo_table.keys():
                self.get_location(location_name).place_locked_item(item)

        elif not self.options.randomize_jinjos:
            item = self.create_item(itemName.JIGGY)
            self.get_location(locationName.JIGGYIH1).place_locked_item(item)
            self.get_location(locationName.JIGGYIH2).place_locked_item(item)
            self.get_location(locationName.JIGGYIH3).place_locked_item(item)
            self.get_location(locationName.JIGGYIH4).place_locked_item(item)
            self.get_location(locationName.JIGGYIH5).place_locked_item(item)
            self.get_location(locationName.JIGGYIH6).place_locked_item(item)
            self.get_location(locationName.JIGGYIH7).place_locked_item(item)
            self.get_location(locationName.JIGGYIH8).place_locked_item(item)
            self.get_location(locationName.JIGGYIH9).place_locked_item(item)

        if not self.options.randomize_jinjos:
            item = self.create_item(itemName.WJINJO)
            self.get_location(locationName.JINJOJR5).place_locked_item(item)

            item = self.create_item(itemName.OJINJO)
            self.get_location(locationName.JINJOWW4).place_locked_item(item)
            self.get_location(locationName.JINJOHP2).place_locked_item(item)

            item = self.create_item(itemName.YJINJO)
            self.get_location(locationName.JINJOWW3).place_locked_item(item)
            self.get_location(locationName.JINJOHP4).place_locked_item(item)
            self.get_location(locationName.JINJOHP3).place_locked_item(item)

            item = self.create_item(itemName.BRJINJO)
            self.get_location(locationName.JINJOGM1).place_locked_item(item)
            self.get_location(locationName.JINJOJR2).place_locked_item(item)
            self.get_location(locationName.JINJOTL2).place_locked_item(item)
            self.get_location(locationName.JINJOTL5).place_locked_item(item)

            item = self.create_item(itemName.GJINJO)
            self.get_location(locationName.JINJOWW5).place_locked_item(item)
            self.get_location(locationName.JINJOJR1).place_locked_item(item)
            self.get_location(locationName.JINJOTL4).place_locked_item(item)
            self.get_location(locationName.JINJOGI2).place_locked_item(item)
            self.get_location(locationName.JINJOHP1).place_locked_item(item)

            item = self.create_item(itemName.RJINJO)
            self.get_location(locationName.JINJOMT2).place_locked_item(item)
            self.get_location(locationName.JINJOMT3).place_locked_item(item)
            self.get_location(locationName.JINJOMT5).place_locked_item(item)
            self.get_location(locationName.JINJOJR3).place_locked_item(item)
            self.get_location(locationName.JINJOJR4).place_locked_item(item)
            self.get_location(locationName.JINJOWW2).place_locked_item(item)

            item = self.create_item(itemName.BLJINJO)
            self.get_location(locationName.JINJOGM3).place_locked_item(item)
            self.get_location(locationName.JINJOTL1).place_locked_item(item)
            self.get_location(locationName.JINJOHP5).place_locked_item(item)
            self.get_location(locationName.JINJOCC2).place_locked_item(item)
            self.get_location(locationName.JINJOIH1).place_locked_item(item)
            self.get_location(locationName.JINJOIH4).place_locked_item(item)
            self.get_location(locationName.JINJOIH5).place_locked_item(item)

            item = self.create_item(itemName.PJINJO)
            self.get_location(locationName.JINJOMT1).place_locked_item(item)
            self.get_location(locationName.JINJOGM5).place_locked_item(item)
            self.get_location(locationName.JINJOCC1).place_locked_item(item)
            self.get_location(locationName.JINJOCC3).place_locked_item(item)
            self.get_location(locationName.JINJOCC5).place_locked_item(item)
            self.get_location(locationName.JINJOIH2).place_locked_item(item)
            self.get_location(locationName.JINJOIH3).place_locked_item(item)
            self.get_location(locationName.JINJOGI4).place_locked_item(item)

            item = self.create_item(itemName.BKJINJO)
            self.get_location(locationName.JINJOMT4).place_locked_item(item)
            self.get_location(locationName.JINJOGM2).place_locked_item(item)
            self.get_location(locationName.JINJOGM4).place_locked_item(item)
            self.get_location(locationName.JINJOWW1).place_locked_item(item)
            self.get_location(locationName.JINJOTL3).place_locked_item(item)
            self.get_location(locationName.JINJOGI1).place_locked_item(item)
            self.get_location(locationName.JINJOGI5).place_locked_item(item)
            self.get_location(locationName.JINJOCC4).place_locked_item(item)
            self.get_location(locationName.JINJOGI3).place_locked_item(item)

    def get_filler_item_name(self) -> str:
        return itemName.NONE

    def banjo_pre_fills(self, itemNameOrGroup: str, group: str, useGroup: bool ) -> None:
        if useGroup:
            for group_name, item_info in self.item_name_groups.items():
                if group_name == itemNameOrGroup:
                    for name in item_info:
                        item = self.create_item(name)
                        banjoItem = all_item_table.get(name)
                        # self.multiworld.get_location(banjoItem.defualt_location, self.player).place_locked_item(item)
                        location = self.get_location(banjoItem.default_location)
                        location.place_locked_item(item)
        else:
            for name, id in self.location_name_to_id.items():
                item = self.create_item(itemNameOrGroup)
                if self.location_name_to_group[name] == group:
                    # self.multiworld.get_location(name, self.player).place_locked_item(item)
                    location = self.get_location(name)
                    location.place_locked_item(item)

    @classmethod
    def stage_write_spoiler(cls, world, spoiler_handle):
        entrance_hags = {
            regionName.MT: regionName.IOHWH,
            regionName.GM: regionName.IOHPL,
            regionName.WW: regionName.IOHPG,
            regionName.JR: regionName.IOHCT + " (Jolly Rogers Lagoon Entrance)",
            regionName.TL: regionName.IOHWL + " (Terrydactyland Entrance)",
            regionName.GIO: regionName.IOHQM + " (Grunty Industries Entrance)",
            regionName.HP: regionName.IOHCT_HFP_ENTRANCE,
            regionName.CC: regionName.IOHWL + " (Cloud Cuckooland Entrance)",
            regionName.CK: regionName.IOHQM + " (Caudron Keep Entrance)"
        }
        bt_players = world.get_game_players(cls.game)
        # spoiler_handle.write('\n\nBanjo-Tooie')
        for player in bt_players:
            name = world.get_player_name(player)
            spoiler_handle.write(f"\n\nBanjo-Tooie ({name}):")
            spoiler_handle.write("\n\tVersion: " + world.worlds[player].version)
            spoiler_handle.write("\n\tLoading Zones:")
            for starting_zone, actual_world in world.worlds[player].loading_zones.items():
                    if actual_world == regionName.JR:
                        spoiler_handle.write(f"\n\t\t{entrance_hags[starting_zone]} -> Jolly Roger's Lagoon")
                    elif actual_world == regionName.GIO:
                        spoiler_handle.write(f"\n\t\t{entrance_hags[starting_zone]} -> Grunty Industries")
                    else:
                        spoiler_handle.write(f"\n\t\t{entrance_hags[starting_zone]} -> {actual_world}")
            spoiler_handle.write("\n\tWorld Costs:")
            for entrances, cost in world.worlds[player].randomize_worlds.items():
                    if entrances == regionName.JR:
                        spoiler_handle.write(f"\n\t\tJolly Roger's Lagoon: {cost}")
                    elif entrances == regionName.GIO:
                        spoiler_handle.write(f"\n\t\tGrunty Industries: {cost}")
                    else:
                        spoiler_handle.write(f"\n\t\t{entrances}: {cost}")
            spoiler_handle.write("\n\tBanjo-Tooie Open Overworld Silos:\n")
            spoiler_handle.write("\t\t"+world.worlds[player].single_silo)
            spoiler_handle.write("\n\tJamjars' Silo Costs:")
            for silo, cost in world.worlds[player].jamjars_siloname_costs.items():
                    spoiler_handle.write(f"\n\t\t{silo}: {cost}")


    def fill_slot_data(self) -> Dict[str, Any]:
        btoptions = self.options.as_dict(
            "death_link", #deathlink, now int
            "logic_type", #good and matches
            "victory_condition", #goal_type and matches
            "minigame_hunt_length", #good and matches
            "boss_hunt_length", #good and matches
            "jinjo_family_rescue_length", #good and matches
            "token_hunt_length", #good and matches
            "randomize_moves", #moves, now int
            "randomize_bk_moves", #bk_moves and matches
            "egg_behaviour", #good and matches
            "progressive_beak_buster", #good, now int
            "progressive_shoes", #good, now int
            "progressive_water_training", #good and matches
            "progressive_flight", #good, now int
            "progressive_egg_aiming", #good and matches
            "progressive_bash_attack", #good, now int
            "randomize_notes", #notes, now int
            "randomize_treble", #trebleclef, now int
            "randomize_jinjos", #jinjo, now int
            "randomize_doubloons", #doubloons, now int
            "randomize_cheato", #pages, now int
            "cheato_rewards", #matches, now int
            "randomize_honeycombs", #honeycomb, now int
            "honeyb_rewards", #matches, now int
            "randomize_glowbos", #magic, now int
            "randomize_stop_n_swap", #mystery, now int
            "randomize_dino_roar", #roar, now int
            "nestsanity", #matches, now int
            "randomize_stations", #stations, now int
            "randomize_chuffy", #chuffy, now int
            "skip_puzzles", #matches, now int
            "open_hag1", #matches, now int
            "backdoors", #matches, now int
            "open_silos", #silo_option and matches
            "speed_up_minigames", #minigames, now int
            "tower_of_tragedy", #skip_tot, now int
            "skip_klungo", #matches, now int
            "dialog_character") #matches and matches

        btoptions["player_name"] = self.multiworld.player_name[self.player]
        btoptions["seed"] = self.random.randint(12212, 9090763)

        btoptions["worlds"] = "true" if self.worlds_randomized else "false"
        btoptions["world_order"] = self.randomize_worlds
        btoptions["world_keys"] = self.randomize_order
        btoptions["loading_zones"] = self.loading_zones

        btoptions["starting_egg"] = int(self.starting_egg)
        btoptions["starting_attack"] = int(self.starting_attack)
        btoptions["first_silo"] = self.single_silo

        btoptions["version"] = self.version
        
        btoptions["jamjars_siloname_costs"] = self.jamjars_siloname_costs
        btoptions["jamjars_silo_costs"] = self.jamjars_silo_costs #table of silo costs
        btoptions["jamjars_silo_option"] = int(self.options.jamjars_silo_costs)
        return btoptions

    # for the universal tracker, doesn't get called in standard gen
    @staticmethod
    def interpret_slot_data(slot_data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        return slot_data

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        # For hints, we choose to hint the level for which the collectible would count.
        # For example, Dippy Jiggy would hint to TDL.

        def add_loading_zone_information(hint_information: Dict[int, str], locations: Dict[str, LocationData], entrance: str):
            for data in locations.values():
                hint_information.update({data.btid: entrance})

        #used for Lua/C++ client reasons
        def get_entrance(level: str):
            level = list(self.loading_zones.keys())[list(self.loading_zones.values()).index(level)]
            if level == regionName.JR:
                return "Jolly Roger's Lagoon"
            elif level == regionName.GIO:
                return "Grunty Industries"
            else:
                return level

        if not self.options.randomize_world_loading_zone:
            return

        hints = {}

        add_loading_zone_information(hints, MTLoc_Table, get_entrance(regionName.MT))
        add_loading_zone_information(hints, GMLoc_table, get_entrance(regionName.GM))
        add_loading_zone_information(hints, WWLoc_table, get_entrance(regionName.WW))
        add_loading_zone_information(hints, JRLoc_table, get_entrance(regionName.JR))
        add_loading_zone_information(hints, TLLoc_table, get_entrance(regionName.TL))
        add_loading_zone_information(hints, GILoc_table, get_entrance(regionName.GIO))
        add_loading_zone_information(hints, HPLoc_table, get_entrance(regionName.HP))
        add_loading_zone_information(hints, CCLoc_table, get_entrance(regionName.CC))

        hint_data.update({self.player: hints})
