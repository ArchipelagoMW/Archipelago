from math import ceil, floor
import random
from multiprocessing import Process
from Options import DeathLink, OptionError
import settings
import typing
from typing import Dict, Any, Optional, List
import warnings
from dataclasses import asdict

from .Hints import HintData, generate_hints
from .Items import BanjoTooieItem, ItemData, all_item_table, all_group_table, progressive_ability_breakdown, silo_table
from .Locations import BanjoTooieLocation, LocationData, all_location_table, MTLoc_Table, GMLoc_table, WWLoc_table, JRLoc_table, TLLoc_table, GILoc_table, HPLoc_table, CCLoc_table, MumboTokenGames_table, MumboTokenBoss_table, MumboTokenJinjo_table, SMLoc_table, JVLoc_table, IHWHLoc_table, IHPLLoc_table, IHPGLoc_table, IHCTLoc_table, IHWLLoc_table, IHQMLoc_table, CheatoRewardsLoc_table, JinjoRewardsLoc_table, HoneyBRewardsLoc_table
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
    version = "V4.4.2"
    web = BanjoTooieWeb()
    topology_present = True
    # item_name_to_id = {name: data.btid for name, data in all_item_table.items()}
    item_name_to_id = {}
    # TODO add implicit edges instead of this hack
    explicit_indirect_conditions: False

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
        "Dino": all_group_table["dino"],
        "Silos": all_group_table["Silos"],
        "Warp Pads": all_group_table["Warp Pads"],
    }

    location_name_groups = {}
    location_name_groups["Mayahem Temple"] = MTLoc_Table.keys()
    location_name_groups["Glitter Gulch Mine"] = GMLoc_table.keys()
    location_name_groups["Witchyworld"] = WWLoc_table.keys()
    location_name_groups["Jolly Roger's Lagoon"] = JRLoc_table.keys()
    location_name_groups["Terrydactyland"] = TLLoc_table.keys()
    location_name_groups["Grunty Industries"] = GILoc_table.keys()
    location_name_groups["Hailfire Peaks"] = HPLoc_table.keys()
    location_name_groups["Cloud Cuckooland"] = CCLoc_table.keys()
    location_name_groups["Isle O' Hags"] = SMLoc_table.keys() | JVLoc_table.keys() | IHWHLoc_table.keys() | IHPLLoc_table.keys() | IHPGLoc_table.keys() | IHCTLoc_table.keys() | IHWLLoc_table.keys() | IHQMLoc_table.keys()

    location_name_groups["Cheato Rewards"] = CheatoRewardsLoc_table.keys()
    location_name_groups["Jinjo Rewards"] = JinjoRewardsLoc_table.keys()
    location_name_groups["Honey B Rewards"] = HoneyBRewardsLoc_table.keys()

    location_name_groups["Jiggies"] = {c for c in all_location_table if all_location_table[c].group == "Jiggy"}
    location_name_groups["Jinjos"] = {c for c in all_location_table if all_location_table[c].group == "Jinjo"}
    location_name_groups["Empty Honeycombs"] = {c for c in all_location_table if all_location_table[c].group == "Honeycomb"}
    location_name_groups["Cheato Pages"] = {c for c in all_location_table if all_location_table[c].group == "Cheato Page"}
    location_name_groups["Notes"] = {c for c in all_location_table if all_location_table[c].group == "Note"}
    location_name_groups["Treble Clefs"] = {c for c in all_location_table if all_location_table[c].group == "Treble Clef"}
    location_name_groups["Doubloons"] = {c for c in JRLoc_table if JRLoc_table[c].group == "Doubloon"}
    location_name_groups["Signposts"] = {c for c in all_location_table if all_location_table[c].group == "Signpost"}
    location_name_groups["Jamjars Silos"] = {c for c in all_location_table if all_location_table[c].group == "Jamjars Silo"}
    location_name_groups["Glowbos"] = {c for c in all_location_table if all_location_table[c].group == "Glowbo"}
    location_name_groups["Train Switches"] = {c for c in all_location_table if all_location_table[c].group == "Train Switch"}
    location_name_groups["Stop 'n' Swop"] = {c for c in all_location_table if all_location_table[c].group == "Stop 'n' Swop"}
    location_name_groups["Nests"] = {c for c in all_location_table if all_location_table[c].group == "Nest"}
    location_name_groups["Warp Pads"] = {c for c in all_location_table if all_location_table[c].group == "Warp Pads"}
    location_name_groups["Warp Silos"] = {c for c in all_location_table if all_location_table[c].group == "Silos"}

    location_name_groups["Bosses"] = {
        locationName.JIGGYMT1,
        locationName.JIGGYGM1,
        locationName.JIGGYWW3,
        locationName.JIGGYJR7,
        locationName.JIGGYTD1,
        locationName.JIGGYTD4,
        locationName.JIGGYGI2,
        locationName.CHEATOGI3,
        locationName.JIGGYHP1,
        locationName.JIGGYCC1,
    }
    location_name_groups["Minigames"] = {
        locationName.JIGGYMT3,
        locationName.JIGGYGM2,
        locationName.JIGGYGM5,
        locationName.JIGGYWW1,
        locationName.JIGGYWW2,
        locationName.JIGGYWW4,
        locationName.JIGGYWW5,
        locationName.JIGGYJR1,
        locationName.JIGGYTD6,
        locationName.JIGGYGI9,
        locationName.JIGGYHP8,
        locationName.JIGGYCC3,
        locationName.JIGGYCC4,
        locationName.JIGGYCC5,
        locationName.JIGGYCC8,
        locationName.CHEATOGM1,
        locationName.CHEATOWW3,
        locationName.CHEATOCC2,
        locationName.CHEATOCC1,
        locationName.CHEATOCC3,
    }

    options_dataclass =  BanjoTooieOptions
    options: BanjoTooieOptions

    def __init__(self, world, player):
        self.kingjingalingjiggy = False
        self.starting_egg: int = 0
        self.starting_attack: int = 0

        self.hard_item_limit: int = 250
        self.traps_in_pool: int = 0
        self.jiggies_in_pool: int = 0
        self.notes_in_pool: int = 0
        self.doubloons_in_pool: int = 0


        self.slot_data = []
        self.preopened_silos = []
        self.randomize_worlds = {}
        self.randomize_order = {}
        self.worlds_randomized = False
        self.loading_zones = {}
        self.jamjars_siloname_costs = {}
        self.jamjars_silo_costs = {}
        self.hints: dict[int, HintData] = {}
        super(BanjoTooieWorld, self).__init__(world, player)

    def create_item(self, itemname: str) -> Item:
        item_classification = None

        if itemname == itemName.JIGGY_AS_FILLER:
            itemname = itemName.JIGGY
            if not hasattr(self.multiworld, "generation_is_fake"):
                item_classification = ItemClassification.filler
        elif itemname == itemName.JIGGY_AS_USEFUL:
            itemname = itemName.JIGGY
            if not hasattr(self.multiworld, "generation_is_fake"):
                item_classification = ItemClassification.useful
        elif itemname == itemName.NOTE_AS_FILLER:
            itemname = itemName.NOTE
            if not hasattr(self.multiworld, "generation_is_fake"):
                item_classification = ItemClassification.filler
        elif itemname == itemName.NOTE_AS_USEFUL:
            itemname = itemName.NOTE
            if not hasattr(self.multiworld, "generation_is_fake"):
                item_classification = ItemClassification.useful
        elif itemname == itemName.DOUBLOON_AS_FILLER:
            itemname = itemName.DOUBLOON
            if not hasattr(self.multiworld, "generation_is_fake"):
                item_classification = ItemClassification.filler

        banjoItem = all_item_table.get(itemname)
        if not banjoItem:
            raise Exception(f"{itemname} is not a valid item name for Banjo-Tooie")

        if item_classification is None:
            item_classification = self.get_classification(banjoItem)

        if item_classification == ItemClassification.trap:
            self.traps_in_pool += 1

        if itemname == itemName.JIGGY:
            self.jiggies_in_pool += 1
        if itemname == itemName.NOTE:
            self.notes_in_pool += 1
        if itemname == itemName.DOUBLOON:
            self.doubloons_in_pool += 1

        created_item = BanjoTooieItem(itemname, item_classification, banjoItem.btid, self.player)
        return created_item

    def get_classification(self, banjoItem: ItemData) -> ItemClassification:
        itemname = self.item_id_to_name[banjoItem.btid]

        if itemname == itemName.PAGES:
            if self.options.cheato_rewards:
                return ItemClassification.progression_skip_balancing
            else:
                return ItemClassification.filler

        if itemname == itemName.HONEY:
            if self.options.honeyb_rewards:
                return ItemClassification.progression_skip_balancing
            else:
                return ItemClassification.useful

        if banjoItem.type == "progress":
            return ItemClassification.progression
        if banjoItem.type == "progression_skip_balancing":
            return ItemClassification.progression_skip_balancing
        if banjoItem.type == "useful":
            return ItemClassification.useful
        if banjoItem.type == "filler":
            return ItemClassification.filler
        if banjoItem.type == "trap":
            return ItemClassification.trap

        raise Exception(f"{banjoItem.type} does not correspond to a valid item classification.")

    def create_event_item(self, name: str) -> Item:
        item_classification = ItemClassification.progression
        created_item = BanjoTooieItem(name, item_classification, None, self.player)
        return created_item

    def calculate_useful_filler(self, total, progression) -> (int, int):
        # We want to split non-progressive items into two halfs
        # half is useful, half is filler
        remainder = total - progression
        useful = ceil(remainder / 2)

        return (useful, remainder - useful)

    def get_jiggies_in_pool(self) -> List[Item]:
        itempool = []

        if self.options.jingaling_jiggy:
            # Below give the king a guarentee Jiggy if option is set
            self.get_location(locationName.JIGGYIH10).place_locked_item(self.create_item(itemName.JIGGY))
            self.kingjingalingjiggy = True

        progression_jiggies = max(self.randomize_worlds.values())
        if not self.options.open_hag1 and self.options.victory_condition in \
            (VictoryCondition.option_hag1,
                VictoryCondition.option_wonderwing_challenge,
                VictoryCondition.option_boss_hunt_and_hag1):
            progression_jiggies = max(progression_jiggies, 70)

        useful_jiggies, filler_jiggies = \
            self.calculate_useful_filler(all_item_table[itemName.JIGGY].qty, progression_jiggies)

        if self.kingjingalingjiggy:
            progression_jiggies -= 1
        if not self.options.randomize_jinjos:
            progression_jiggies -= 9

        # in case preplaced items are over the progression count
        if progression_jiggies < 0:
            useful_jiggies += progression_jiggies
            progression_jiggies = 0

        itempool += [
            self.create_item(itemName.JIGGY) for i in range(progression_jiggies)
        ]
        itempool += [
            self.create_item(itemName.JIGGY_AS_USEFUL) for i in range(useful_jiggies)
        ]
        if not self.options.replace_extra_jiggies:
            itempool += [
                self.create_item(itemName.JIGGY_AS_FILLER) for i in range(filler_jiggies)
            ]

        return itempool

    def get_notes_in_pool(self) -> List[Item]:
        if not self.options.randomize_notes:
            return []

        itempool = []

        progression_notes = ceil(max(self.jamjars_siloname_costs.values()) / 5)

        useful_notes, filler_notes = \
            self.calculate_useful_filler(int(900 / 5), progression_notes)

        taken_by_clefs = 4 * (self.options.extra_trebleclefs_count + all_item_table[itemName.TREBLE].qty)\
            + 2 * self.options.bass_clef_amount

        progression_notes -= taken_by_clefs

        # in case preplaced items are over the progression count
        if progression_notes < 0:
            useful_notes += progression_notes
            progression_notes = 0
        if useful_notes < 0:
            filler_notes += useful_notes
            useful_notes = 0
        if filler_notes < 0:
            warnings.warn("Number of notes that need to be inserted is somehow negative.")

        itempool += [
            self.create_item(itemName.NOTE) for i in range(progression_notes)
        ]
        itempool += [
            self.create_item(itemName.NOTE_AS_USEFUL) for i in range(useful_notes)
        ]
        if not self.options.replace_extra_notes:
            itempool += [
                self.create_item(itemName.NOTE_AS_FILLER) for i in range(filler_notes)
            ]

        return itempool

    def create_items(self) -> None:
        itempool = []

        # START OF ITEMS CUSTOM LOGIC

        if self.options.victory_condition == VictoryCondition.option_token_hunt:
            itempool += [self.create_item(itemName.MUMBOTOKEN) for i in range(15)]

        itempool += self.get_jiggies_in_pool()
        itempool += self.get_notes_in_pool()

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

        if name in all_group_table['Warp Pads'].keys() and not self.options.randomize_warp_pads:
            return None

        if name in all_group_table['Silos'].keys() and not self.options.randomize_silos:
            return None

        if name in all_group_table['Silos'].keys() and name in self.preopened_silos:
            return None

        if name == itemName.ROAR and not self.options.randomize_dino_roar:
            return None

        if item.btid == self.starting_egg:
            return None

        if item.btid == self.starting_attack:
            return None
        elif self.starting_attack != 0:   # Let's check if it's progressive starting move
            attack_name = self.item_id_to_name[self.starting_attack]
            if attack_name in progressive_ability_breakdown.keys() and \
                  name == progressive_ability_breakdown[attack_name][0]:
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
        self.validate_yaml_options()
        self.choose_starter_egg()
        self.choose_starter_attack()
        WorldRandomize(self)
        self.hand_preopened_silos()

    def validate_yaml_options(self) -> None:
        if self.options.randomize_worlds and self.options.randomize_bk_moves != RandomizeBKMoveList.option_none and self.options.logic_type == LogicType.option_intended:
            raise OptionError("Randomize Worlds and Randomize BK Moves is not compatible with Beginner Logic.")
        if (not self.options.randomize_notes and not self.options.randomize_signposts and not self.options.nestsanity) and self.options.randomize_bk_moves != RandomizeBKMoveList.option_none:
            if self.multiworld.players == 1:
                raise OptionError("Randomize Notes, signposts or nestsanity is required for Randomize BK Moves.")
        if not self.options.randomize_notes and (self.options.extra_trebleclefs_count != 0 and self.options.bass_clef_amount != 0):
            raise OptionError("Randomize Notes is required to add extra Treble Clefs or Bass Clefs")
        if self.options.progressive_beak_buster and (not self.options.randomize_bk_moves or not self.options.randomize_moves):
            raise OptionError("You cannot have progressive Beak Buster without randomizing moves and randomizing BK moves")
        if (self.options.egg_behaviour == EggsBehaviour.option_random_starting_egg or self.options.egg_behaviour == EggsBehaviour.option_simple_random_starting_egg) and (not self.options.randomize_bk_moves or not self.options.randomize_moves):
            raise OptionError("You cannot have Randomize Starting Egg without randomizing moves and randomizing BK moves")
        elif self.options.egg_behaviour == EggsBehaviour.option_progressive_eggs and not self.options.randomize_moves:
            raise OptionError("You cannot have progressive Eggs without randomizing moves")
        if self.options.progressive_shoes and not (self.options.randomize_bk_moves and self.options.randomize_moves and (self.options.randomize_signposts or self.options.nestsanity)):
            raise OptionError("You cannot have progressive Shoes without randomizing moves, randomizing BK moves and enabling either nestanity or randomize signpost")
        if self.options.progressive_water_training != ProgressiveWaterTraining.option_none and (self.options.randomize_bk_moves == RandomizeBKMoveList.option_none or not self.options.randomize_moves):
            raise OptionError("You cannot have progressive Water Training without randomizing moves and randomizing BK moves")
        if self.options.progressive_flight and (not self.options.randomize_bk_moves or not self.options.randomize_moves):
            raise OptionError("You cannot have progressive flight without randomizing moves and randomizing BK moves")
        if self.options.progressive_egg_aiming != ProgressiveEggAim.option_none and (not self.options.randomize_bk_moves or not self.options.randomize_moves):
            raise OptionError("You cannot have progressive egg aiming without randomizing moves and randomizing BK moves")
        if self.options.progressive_bash_attack and (not self.options.randomize_stop_n_swap or not self.options.randomize_moves):
            raise OptionError("You cannot have progressive bash attack without randomizing Stop N Swap and randomizing BK moves")
        if not self.options.randomize_moves and self.options.jamjars_silo_costs != JamjarsSiloCosts.option_vanilla:
            raise OptionError("You cannot change the silo costs without randomizing Jamjars' moves.")
        # if not self.options.randomize_moves and self.options.randomize_bk_moves != RandomizeBKMoveList.option_none and self.options.open_silos < 2:
        #     raise OptionError("If you enabled Randomized Worlds with BK Moves randomized, you must have at least 2 silos opened.")
        if not self.options.open_hag1 and self.options.victory_condition == VictoryCondition.option_wonderwing_challenge:
            self.options.open_hag1.value = True

    def choose_starter_egg(self) -> None:
        if self.options.egg_behaviour == EggsBehaviour.option_random_starting_egg or \
        self.options.egg_behaviour == EggsBehaviour.option_simple_random_starting_egg:
            eggs: list = []
            if self.options.egg_behaviour == EggsBehaviour.option_random_starting_egg:
                eggs = list([itemName.BEGGS, itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS])
            else:
                eggs = list([itemName.BEGGS, itemName.FEGGS, itemName.GEGGS, itemName.IEGGS])
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

    def choose_starter_attack(self) -> None:
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

    def hand_preopened_silos(self) -> None:
        for silo in self.preopened_silos:
            self.multiworld.push_precollected(self.create_item(silo))

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

        if not self.options.randomize_silos:
            self.prefill_silos()

        if not self.options.randomize_warp_pads:
            self.banjo_pre_fills("Warp Pads", None, True)

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
            self.get_location(locationName.JIGGYIH1).place_locked_item(self.create_item(itemName.JIGGY))
            self.get_location(locationName.JIGGYIH2).place_locked_item(self.create_item(itemName.JIGGY))
            self.get_location(locationName.JIGGYIH3).place_locked_item(self.create_item(itemName.JIGGY))
            self.get_location(locationName.JIGGYIH4).place_locked_item(self.create_item(itemName.JIGGY))
            self.get_location(locationName.JIGGYIH5).place_locked_item(self.create_item(itemName.JIGGY))
            self.get_location(locationName.JIGGYIH6).place_locked_item(self.create_item(itemName.JIGGY))
            self.get_location(locationName.JIGGYIH7).place_locked_item(self.create_item(itemName.JIGGY))
            self.get_location(locationName.JIGGYIH8).place_locked_item(self.create_item(itemName.JIGGY))
            self.get_location(locationName.JIGGYIH9).place_locked_item(self.create_item(itemName.JIGGY))

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

    def allow_jiggies_as_filler(self) -> bool:
        return self.options.replace_extra_jiggies and self.jiggies_in_pool < self.hard_item_limit

    def allow_notes_as_filler(self) -> bool:
        return self.options.replace_extra_notes and self.options.randomize_notes and self.notes_in_pool < self.hard_item_limit

    def allow_doubloons_as_filler(self) -> bool:
        return self.options.randomize_doubloons and self.doubloons_in_pool < self.hard_item_limit

    def get_filler_item_name(self) -> str:
        trap_weights = [
            (itemName.GNEST, self.options.golden_eggs_weight),
            (itemName.TTRAP, self.options.trip_trap_weight),
            (itemName.STRAP, self.options.slip_trap_weight),
            (itemName.TRTRAP, self.options.transform_trap_weight),
            (itemName.SQTRAP, self.options.squish_trap_weight),
            (itemName.TITRAP, self.options.tip_trap_weight),
        ]
        filler_weights = [
            (itemName.JIGGY_AS_FILLER, self.options.extra_jiggies_weight if self.allow_jiggies_as_filler() else 0),
            (itemName.NOTE_AS_FILLER, self.options.extra_notes_weight if self.allow_notes_as_filler() else 0),
            (itemName.DOUBLOON_AS_FILLER, self.options.extra_doubloons_weight if self.allow_doubloons_as_filler() else 0),
            (itemName.ENEST, self.options.egg_nests_weight * (2 if self.options.nestsanity else 1)),
            (itemName.FNEST, self.options.feather_nests_weight * (2 if self.options.nestsanity else 1)),
            # Intentionally leaving NONE as last;
            # because self.random.choices might always choose last if all weights are 0
            (itemName.NONE, self.options.big_o_pants_weight)
        ]

        if self.traps_in_pool < self.options.max_traps:
            weights = trap_weights + filler_weights
        else:
            weights = filler_weights

        names, actual_weights = zip(*weights)

        if sum(actual_weights) == 0:
            actual_weights = (*actual_weights[:-1], 1)

        return self.random.choices(names, actual_weights, k=1)[0]

    def prefill_silos(self):
        for name, data in silo_table.items():
            # A vanilla silo that's pre-opened does not give a check, since its item is in the starting inventory.
            if name not in self.preopened_silos:
                item = self.create_item(name)
                location = self.get_location(data.default_location)
                location.place_locked_item(item)

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
            "randomize_warp_pads",
            "randomize_silos",
            "hint_clarity",
            "dialog_character"
        )

        btoptions["player_name"] = self.multiworld.player_name[self.player]
        btoptions["seed"] = self.random.randint(12212, 9090763)

        btoptions["worlds"] = "true" if self.worlds_randomized else "false"
        btoptions["world_order"] = self.randomize_worlds
        btoptions["world_keys"] = self.randomize_order
        btoptions["loading_zones"] = self.loading_zones

        btoptions["starting_egg"] = int(self.starting_egg)
        btoptions["starting_attack"] = int(self.starting_attack)
        btoptions["preopened_silos"] = [self.item_name_to_id[name] for name in self.preopened_silos]

        btoptions["version"] = BanjoTooieWorld.version

        btoptions["jamjars_siloname_costs"] = self.jamjars_siloname_costs
        btoptions["jamjars_silo_costs"] = self.jamjars_silo_costs #table of silo costs
        btoptions["jamjars_silo_option"] = int(self.options.jamjars_silo_costs)
        btoptions["hints"] = {location: asdict(hint_data) for location, hint_data in self.hints.items()}
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
