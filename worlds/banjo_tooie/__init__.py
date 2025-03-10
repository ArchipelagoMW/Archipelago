from math import ceil, floor
import random
from multiprocessing import Process
from Options import DeathLink
import settings
import typing
from typing import Dict, Any, Optional
import warnings

from .Hints import HintData, generate_hints
from .Items import BanjoTooieItem, ItemData, all_item_table, all_group_table, progressive_ability_breakdown
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
    from .BTClient import main  # lazy import
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
    version = "V4.2"
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
        self.hints: dict[int, HintData] = {}
        super(BanjoTooieWorld, self).__init__(world, player)

    def create_item(self, itemname: str) -> Item:
        banjoItem = all_item_table.get(itemname)
        if not banjoItem:
            raise Exception(f"{itemname} is not a valid item name for Banjo-Tooie")
        if banjoItem.type == "progress":
            if itemname == itemName.JIGGY:
                if not hasattr(self.multiworld, "generation_is_fake"):
                    maxJiggy = max(self.randomize_worlds.values())
                    if not self.options.open_hag1 and self.options.victory_condition in \
                        (VictoryCondition.option_hag1,
                         VictoryCondition.option_wonderwing_challenge,
                         VictoryCondition.option_boss_hunt_and_hag1):
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
            elif itemname == itemName.NOTE and self.options.randomize_notes:
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
            if itemname == itemName.PAGES: # Cheato pages
                if self.options.cheato_rewards:
                    item_classification = ItemClassification.progression
                else:
                    item_classification = ItemClassification.filler
            elif itemname == itemName.HONEY and self.options.honeyb_rewards: #Honeycombs
                item_classification = ItemClassification.progression
            else:
                item_classification = ItemClassification.useful

        if banjoItem.type == "filler":
            item_classification = ItemClassification.filler

        if banjoItem.type == "trap":
            item_classification = ItemClassification.trap

        created_item = BanjoTooieItem(self.item_id_to_name[banjoItem.btid], item_classification, banjoItem.btid, self.player)
        return created_item

    def create_event_item(self, name: str) -> Item:
        item_classification = ItemClassification.progression
        created_item = BanjoTooieItem(name, item_classification, None, self.player)
        return created_item

    def create_items(self) -> None:
        itempool = []

        # START OF ITEMS CUSTOM LOGIC

        if self.options.nestsanity:
            removed_enests = 0
            removed_fnests = 0

            if self.options.traps and self.options.traps_nests_ratio > 0:
                total_nests = all_item_table[itemName.ENEST].qty + all_item_table[itemName.FNEST].qty

                removed_nests = int(total_nests * self.options.traps_nests_ratio / 100)
                removed_enests = int(all_item_table[itemName.ENEST].qty * self.options.traps_nests_ratio / 100)
                removed_fnests = removed_nests - removed_enests

            itempool += [self.create_item(itemName.ENEST) for i in range(all_item_table[itemName.ENEST].qty - removed_enests)]
            itempool += [self.create_item(itemName.FNEST) for i in range(all_item_table[itemName.FNEST].qty - removed_fnests)]

        if self.options.victory_condition == VictoryCondition.option_token_hunt:
            itempool += [self.create_item(itemName.MUMBOTOKEN) for i in range(15)]

        if self.options.jingaling_jiggy:
            # Below give the king a guarentee Jiggy if option is set
            self.get_location(locationName.JIGGYIH10).place_locked_item(self.create_item(itemName.JIGGY))
            self.kingjingalingjiggy = True

        for i in range(all_item_table[itemName.JIGGY].qty - self.kingjingalingjiggy):
            # Jinjos need their jiggies
            if not self.options.randomize_jinjos and self.jiggy_counter > 81:
                break
            itempool += [self.create_item(itemName.JIGGY)]

        if self.options.randomize_notes:
            count = all_item_table[itemName.NOTE].qty
            count -= self.options.bass_clef_amount * 2 + self.options.extra_trebleclefs_count * 4
            itempool += [self.create_item(itemName.NOTE) for i in range(count)]

        count = all_item_table[itemName.TREBLE].qty if self.options.randomize_treble else 0
        count += self.options.extra_trebleclefs_count
        itempool += [self.create_item(itemName.TREBLE) for i in range(count)]

        count = self.options.bass_clef_amount
        itempool += [self.create_item(itemName.BASS) for i in range(count)]

        # END OF ITEMS CUSTOM LOGIC

        # Basic items that need no extra logic, if you need to customize quantity or logic, add them above this
        # and add the item to the handled_items in def item_filter.
        for name, item in all_item_table.items():
            item_name = self.item_filter(name, item)
            if not item_name is None:
                # We're still using the original item quantity.
                itempool += [self.create_item(item_name) for _ in range(item.qty)]

        # Add Filler items until all locations are filled
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        if len(itempool) > total_locations:
            warnings.warn("Number of total available items exceeds the number of locations, likely there is a bug in the generation.")

        itempool += [self.create_filler() for _ in range(total_locations - len(itempool))]

        self.multiworld.itempool.extend(itempool)


    def item_filter(self, name: str, item: ItemData) -> Optional[ItemData]:
        handled_items = [
            itemName.JIGGY,
            itemName.NOTE,
            itemName.TREBLE,
            itemName.BASS,
            itemName.MUMBOTOKEN,
        ]

        if name in handled_items:
            return None

        # While JNONE is filler, it's funny enough to warrant always keeping
        if item.type in ['filler', 'trap'] and name != itemName.JNONE:
            return None

        if name == itemName.DOUBLOON and not self.options.randomize_doubloons:
            return None

        if name == itemName.PAGES and not self.options.randomize_cheato: # Added later in Prefill
            return None

        if name == itemName.HONEY and not self.options.randomize_honeycombs: # Added later in Prefill
            return None

        if name in all_group_table['bk_moves'].keys() and self.options.randomize_bk_moves == RandomizeBKMoveList.option_none:
            return None
        elif (name == itemName.TTROT or name == itemName.TJUMP) and self.options.randomize_bk_moves == RandomizeBKMoveList.option_mcjiggy_special: # talon trot and tall jump not in pool
            return None

        if name in all_group_table['moves'].keys() and not self.options.randomize_moves:
            return None

        if name in all_group_table['magic'].keys() and not self.options.randomize_glowbos:
            return None

        if name in all_group_table['jinjo'].keys() and not self.options.randomize_jinjos:
            return None

        if name == itemName.CHUFFY and not self.options.randomize_chuffy:
            return None

        if name in all_group_table['stations'].keys() and not self.options.randomize_stations:
            return None

        if name in all_group_table['levelaccess'].keys():
            return None

        if name in all_group_table['stopnswap'].keys() and not self.options.randomize_stop_n_swap:
            return None

        if name == itemName.ROAR and not self.options.randomize_dino_roar:
            return None

        if item.btid == self.starting_egg:
            return None

        if item.btid == self.starting_attack:
            return None

        # START OF PROGRESSIVE MOVES

        # We add a progressive ability when we go through the individual items
        if name in progressive_ability_breakdown.keys():
            return None

        if self.options.progressive_beak_buster:
            if name in progressive_ability_breakdown[itemName.PBBUST]:
                return itemName.PBBUST

        if self.options.egg_behaviour == EggsBehaviour.option_progressive_eggs:
            if name in progressive_ability_breakdown[itemName.PEGGS]:
                return itemName.PEGGS

        if self.options.progressive_shoes:
            if name in progressive_ability_breakdown[itemName.PSHOES]:
                return itemName.PSHOES

        if self.options.progressive_water_training == ProgressiveWaterTraining.option_basic:
            if name in progressive_ability_breakdown[itemName.PSWIM]:
                return itemName.PSWIM
        elif self.options.progressive_water_training == ProgressiveWaterTraining.option_advanced:
            if name in progressive_ability_breakdown[itemName.PASWIM]:
                return itemName.PASWIM

        if self.options.progressive_bash_attack:
            if name in progressive_ability_breakdown[itemName.PBASH]:
                return itemName.PBASH

        if self.options.progressive_flight:
            if name in progressive_ability_breakdown[itemName.PFLIGHT]:
                return itemName.PFLIGHT

        if self.options.progressive_egg_aiming == ProgressiveEggAim.option_basic:
            if name in progressive_ability_breakdown[itemName.PEGGAIM]:
                return itemName.PEGGAIM
        elif self.options.progressive_egg_aiming == ProgressiveEggAim.option_advanced:
            if name in progressive_ability_breakdown[itemName.PAEGGAIM]:
                return itemName.PAEGGAIM

        # END OF PROGRESSIVE MOVES

        return name

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)
        self.pre_fill_me()

    def generate_early(self) -> None:
        if self.options.randomize_worlds and self.options.randomize_bk_moves != RandomizeBKMoveList.option_none and self.options.logic_type == LogicType.option_intended:
            raise ValueError("Randomize Worlds and Randomize BK Moves is not compatible with Beginner Logic.")
        if (not self.options.randomize_notes and not self.options.randomize_signposts and not self.options.nestsanity) and self.options.randomize_bk_moves != RandomizeBKMoveList.option_none:
            if self.multiworld.players == 1:
                raise ValueError("Randomize Notes, signposts or nestsanity is required for Randomize BK Moves.")
        if not self.options.randomize_notes and (self.options.extra_trebleclefs_count != 0 and self.options.bass_clef_amount != 0):
            raise ValueError("Randomize Notes is required to add extra Treble Clefs or Bass Clefs")
        if self.options.progressive_beak_buster and (not self.options.randomize_bk_moves or not self.options.randomize_moves):
            raise ValueError("You cannot have progressive Beak Buster without randomizing moves and randomizing BK moves")
        if self.options.egg_behaviour == EggsBehaviour.option_random_starting_egg and (not self.options.randomize_bk_moves or not self.options.randomize_moves):
            raise ValueError("You cannot have Randomize Starting Egg without randomizing moves and randomizing BK moves")
        elif self.options.egg_behaviour == EggsBehaviour.option_progressive_eggs and not self.options.randomize_moves:
            raise ValueError("You cannot have progressive Eggs without randomizing moves")
        if self.options.progressive_shoes and not (self.options.randomize_bk_moves and self.options.randomize_moves and (self.options.randomize_signposts or self.options.nestsanity)):
            raise ValueError("You cannot have progressive Shoes without randomizing moves, randomizing BK moves and enabling either nestanity or randomize signpost")
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
            self.options.open_hag1.value = True


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
            elif self.options.logic_type == LogicType.option_easy_tricks:
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
            or self.options.victory_condition == VictoryCondition.option_wonderwing_challenge\
            or self.options.victory_condition == VictoryCondition.option_boss_hunt_and_hag1:

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
        if self.options.traps:
            return self.random.choices([itemName.GNEST, itemName.TTRAP, itemName.STRAP, itemName.TRTRAP, itemName.SQTRAP, itemName.TITRAP], weights = [
                self.options.golden_eggs_weight if self.options.nestsanity else 0,
                self.options.trip_trap_weight,
                self.options.slip_trap_weight,
                self.options.transform_trap_weight,
                self.options.squish_trap_weight,
                self.options.tip_trap_weight,
            ], k = 1)[0]
        elif self.options.nestsanity:
            return self.random.choices([itemName.ENEST, itemName.FNEST], weights = [
                all_item_table[itemName.ENEST].qty,
                all_item_table[itemName.FNEST].qty,
            ])[0]
        else:
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
        spoiler_handle.write('\n\nBanjo-Tooie ({})'.format(BanjoTooieWorld.version))
        for player in bt_players:
            currentWorld: BanjoTooieWorld = world.worlds[player]
            name = world.get_player_name(player)
            spoiler_handle.write(f"\n\n{name}:")
            spoiler_handle.write('\n\tLoading Zones:')
            for starting_zone, actual_world in currentWorld.loading_zones.items():
                    if actual_world == regionName.JR:
                        spoiler_handle.write(f"\n\t\t{entrance_hags[starting_zone]} -> Jolly Roger's Lagoon")
                    elif actual_world == regionName.GIO:
                        spoiler_handle.write(f"\n\t\t{entrance_hags[starting_zone]} -> Grunty Industries")
                    else:
                        spoiler_handle.write(f"\n\t\t{entrance_hags[starting_zone]} -> {actual_world}")
            spoiler_handle.write("\n\tWorld Costs:")
            for entrances, cost in currentWorld.randomize_worlds.items():
                    if entrances == regionName.JR:
                        spoiler_handle.write(f"\n\t\tJolly Roger's Lagoon: {cost}")
                    elif entrances == regionName.GIO:
                        spoiler_handle.write(f"\n\t\tGrunty Industries: {cost}")
                    else:
                        spoiler_handle.write(f"\n\t\t{entrances}: {cost}")
            spoiler_handle.write("\n\tBanjo-Tooie Open Overworld Silos:\n")
            spoiler_handle.write("\t\t" + currentWorld.single_silo)
            spoiler_handle.write("\n\tJamjars' Silo Costs:")
            for silo, cost in currentWorld.jamjars_siloname_costs.items():
                    spoiler_handle.write(f"\n\t\t{silo}: {cost}")
            spoiler_handle.write('\n\tHints:')
            for location_id, hint_data in currentWorld.hints.items():
                    spoiler_handle.write("\n\t\t{}: {}".format(currentWorld.location_id_to_name[location_id], hint_data.text))


    def fill_slot_data(self) -> Dict[str, Any]:
        generate_hints(self)
        btoptions = self.options.as_dict(
            "death_link",
            "logic_type",
            "victory_condition",
            "minigame_hunt_length",
            "boss_hunt_length",
            "jinjo_family_rescue_length",
            "token_hunt_length",
            "randomize_moves",
            "randomize_bk_moves",
            "egg_behaviour",
            "progressive_beak_buster",
            "progressive_shoes",
            "progressive_water_training",
            "progressive_flight",
            "progressive_egg_aiming",
            "progressive_bash_attack",
            "randomize_notes",
            "randomize_treble",
            "randomize_jinjos",
            "randomize_doubloons",
            "randomize_cheato",
            "cheato_rewards",
            "randomize_honeycombs",
            "honeyb_rewards",
            "randomize_glowbos",
            "randomize_stop_n_swap",
            "randomize_dino_roar",
            "nestsanity",
            "randomize_stations",
            "randomize_chuffy",
            "skip_puzzles",
            "open_hag1",
            "backdoors",
            "open_silos",
            "speed_up_minigames",
            "tower_of_tragedy",
            "skip_klungo",
            "easy_canary",
            "extra_cheats",
            "randomize_signposts",
            "signpost_hints",
            "signpost_move_hints",
            "dialog_character")

        btoptions["player_name"] = self.multiworld.player_name[self.player]
        btoptions["seed"] = self.random.randint(12212, 9090763)

        btoptions["worlds"] = "true" if self.worlds_randomized else "false"
        btoptions["world_order"] = self.randomize_worlds
        btoptions["world_keys"] = self.randomize_order
        btoptions["loading_zones"] = self.loading_zones

        btoptions["starting_egg"] = int(self.starting_egg)
        btoptions["starting_attack"] = int(self.starting_attack)
        btoptions["first_silo"] = self.single_silo

        btoptions["version"] = BanjoTooieWorld.version

        btoptions["jamjars_siloname_costs"] = self.jamjars_siloname_costs
        btoptions["jamjars_silo_costs"] = self.jamjars_silo_costs #table of silo costs
        btoptions["jamjars_silo_option"] = int(self.options.jamjars_silo_costs)
        btoptions["hints"] = {location: hint_data._asdict() for location, hint_data in self.hints.items()}
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
