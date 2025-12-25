import logging
from collections import Counter
from math import ceil
import time

from Options import OptionError
import typing
from typing import Dict, Any, List
import warnings, settings
from dataclasses import asdict

from .Hints import HintData, generate_hints
from .Items import BanjoTooieItem, ItemData, all_item_table, all_group_table, progressive_ability_breakdown
from .Locations import LocationData, all_location_table, MTLoc_Table, GMLoc_table, WWLoc_table, \
    JRLoc_table, TLLoc_table, GILoc_table, HPLoc_table, CCLoc_table, MumboTokenGames_table, \
    MumboTokenBoss_table, MumboTokenJinjo_table, SMLoc_table, JVLoc_table, IHWHLoc_table, \
    IHPLLoc_table, IHPGLoc_table, IHCTLoc_table, IHWLLoc_table, IHQMLoc_table, \
    CheatoRewardsLoc_table, JinjoRewardsLoc_table, HoneyBRewardsLoc_table
from .Regions import create_regions, connect_regions
from .Options import BanjoTooieOptions, EggsBehaviour, JamjarsSiloCosts, LogicType, ProgressiveEggAim, \
    ProgressiveWaterTraining, RandomizeBKMoveList, VictoryCondition, bt_option_groups, WorldRequirements
from .Rules import BanjoTooieRules
from .Names import itemName, locationName, regionName
from .WorldOrder import randomize_world_progression
from BaseClasses import ItemClassification, Location, MultiWorld, Tutorial, Item
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, icon_paths, components, Type, launch_subprocess


def run_client():
    from .BTClient import main  # lazy import
    launch_subprocess(main)


components.append(Component("Banjo-Tooie Client", func=run_client, component_type=Type.CLIENT,
                            icon='Jinjo Icon'))
icon_paths['Jinjo Icon'] = "ap:worlds.banjo_tooie/assets/icon.png"

class BanjoTooieSettings(settings.Group):
    class RomPath(settings.OptionalUserFilePath):
        """File path of the Banjo-Tooie (USA) ROM."""

    class PatchPath(settings.OptionalUserFolderPath):
        """Folder path of where to save the patched ROM."""

    class ProgramPath(settings.OptionalUserFilePath):
        """
        File path of the program to automatically run.
        Leave blank to disable.
        """

    class ProgramArgs(str):
        """
        Arguments to pass to the automatically run program.
        Leave blank to disable.
        Set to "--lua=" to automatically use the correct path for the lua connector.
        """

    rom_path: RomPath | str = ""
    patch_path: PatchPath | str = ""
    program_path: ProgramPath | str = ""
    program_args: ProgramArgs | str = "--lua="


class BanjoTooieWeb(WebWorld):
    setup_en = Tutorial(
        "Setup Banjo-Tooie",
        """A guide to setting up Archipelago Banjo-Tooie on your computer.""",
        "English",
        "setup_en.md",
        "setup/en",
        ["Beebaleen"])
    setup_fr = Tutorial(
        "Setup Banjo-Tooie",
        """A guide to setting up Archipelago Banjo-Tooie on your computer.""",
        "French",
        "setup_fr.md",
        "setup/fr",
        ["g0goTBC"])

    tutorials = [setup_en, setup_fr]
    option_groups = bt_option_groups


class BanjoTooieWorld(World):
    """
    Banjo-Tooie is a single-player platform game in which the protagonists are controlled from a third-person perspective.
    Carrying over most of the mechanics and concepts established in its predecessor,
    the game features three-dimensional worlds consisting of various platforming challenges and puzzles, with a notable
    increased focus on puzzle-solving over the worlds of Banjo-Kazooie.
    """

    game = "Banjo-Tooie"
    options: BanjoTooieOptions
    settings: typing.ClassVar[BanjoTooieSettings]
    settings_key = "banjo_tooie_options"
    web = BanjoTooieWeb()
    topology_present = True
    item_name_to_id = {name: data.btid for name, data in all_item_table.items() if data.btid is not None}

    glitches_item_name = itemName.UT_GLITCHED
    ut_can_gen_without_yaml = True

    location_name_to_id = {name: data.btid for name, data in all_location_table.items() if data.btid is not None}
    location_name_to_group = {name: data.group for name, data in all_location_table.items() if data.group is not None}

    item_name_groups = {
        # "Jiggy": all_group_table["jiggy"],
        "Jinjo": set(all_group_table["jinjo"].keys()),
        "Moves": set(all_group_table["moves"].keys()),
        "Magic": set(all_group_table["magic"].keys()),
        "Stations": set(all_group_table["stations"].keys()),
        "StopnSwap": set(all_group_table["stopnswap"].keys()),
        "Access": set(all_group_table["levelaccess"].keys()),
        "Dino": set(all_group_table["dino"].keys()),
        "Silos": set(all_group_table["Silos"].keys()),
        "Warp Pads": set(all_group_table["Warp Pads"].keys()),
        "Cheats": set(all_group_table["cheats"].keys())
    }

    location_name_groups = {
        "Mayahem Temple": set(MTLoc_Table.keys()), "Glitter Gulch Mine": set(GMLoc_table.keys()),
        "Witchyworld": set(WWLoc_table.keys()), "Jolly Roger's Lagoon": set(JRLoc_table.keys()),
        "Terrydactyland": set(TLLoc_table.keys()), "Grunty Industries": set(GILoc_table.keys()),
        "Hailfire Peaks": set(HPLoc_table.keys()), "Cloud Cuckooland": set(CCLoc_table.keys()),
        "Isle O' Hags": set(SMLoc_table.keys()) | set(JVLoc_table.keys()) | set(IHWHLoc_table.keys()) | set(IHPLLoc_table.keys()) |
        set(IHPGLoc_table.keys()) | set(IHCTLoc_table.keys()) | set(IHWLLoc_table.keys()) | set(IHQMLoc_table.keys()),
        "Cheato Rewards": set(CheatoRewardsLoc_table.keys()),
        "Jinjo Rewards": set(JinjoRewardsLoc_table.keys()),
        "Honey B Rewards": set(HoneyBRewardsLoc_table.keys()),
        "Jiggies": {c for c in all_location_table if all_location_table[c].group == "Jiggy"},
        "Jinjos": {c for c in all_location_table if all_location_table[c].group == "Jinjo"},
        "Empty Honeycombs": {c for c in all_location_table if
                             all_location_table[c].group == "Honeycomb"},
        "Cheato Pages": {c for c in all_location_table if
                         all_location_table[c].group == "Cheato Page"},
        "Notes": {c for c in all_location_table if all_location_table[c].group == "Note"},
        "Treble Clefs": {c for c in all_location_table if
                         all_location_table[c].group == "Treble Clef"},
        "Doubloons": {c for c in JRLoc_table if JRLoc_table[c].group == "Doubloon"},
        "Signposts": {c for c in all_location_table if all_location_table[c].group == "Signpost"},
        "Jamjars Silos": {c for c in all_location_table if
                          all_location_table[c].group == "Jamjars Silo"},
        "Glowbos": {c for c in all_location_table if all_location_table[c].group == "Glowbo"},
        "Train Switches": {c for c in all_location_table if
                           all_location_table[c].group == "Train Switch"},
        "Stop 'n' Swop": {c for c in all_location_table if
                          all_location_table[c].group == "Stop 'n' Swop"},
        "Nests": {c for c in all_location_table if all_location_table[c].group == "Nest"},
        "Warp Pads": {c for c in all_location_table if all_location_table[c].group == "Warp Pads"},
        "Warp Silos": {c for c in all_location_table if all_location_table[c].group == "Silos"},
        "Ticket": {c for c in all_location_table if all_location_table[c].group == "Ticket"},
        "Green Relic": {c for c in all_location_table if
                        all_location_table[c].group == "Green Relic"}, "Bosses": {
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
        }, "Minigames": {
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
        }}

    options_dataclass = BanjoTooieOptions
    options: BanjoTooieOptions

    def __init__(self, world, player):
        self.starting_egg: int = 0
        self.starting_attack: int = 0

        self.hard_item_limit: int = 250
        self.traps_in_pool: int = 0
        self.jiggies_in_pool: int = 0
        self.notes_in_pool: int = 0
        self.doubloons_in_pool: int = 0

        self.slot_data = []
        self.preopened_silos = []
        self.world_requirements = {}
        self.world_order = {}
        self.loading_zones = {}
        self.jamjars_siloname_costs = {}
        self.jamjars_silo_costs = {}
        self.hints: dict[int, HintData] = {}
        super(BanjoTooieWorld, self).__init__(world, player)

    def create_item(self, name: str) -> Item:
        item_classification = None

        if name == itemName.JIGGY_AS_FILLER:
            name = itemName.JIGGY
            if not hasattr(self.multiworld, "generation_is_fake"):
                item_classification = ItemClassification.filler
        elif name == itemName.JIGGY_AS_USEFUL:
            name = itemName.JIGGY
            if not hasattr(self.multiworld, "generation_is_fake"):
                item_classification = ItemClassification.useful
        elif name == itemName.NOTE_AS_FILLER:
            name = itemName.NOTE
            if not hasattr(self.multiworld, "generation_is_fake"):
                item_classification = ItemClassification.filler
        elif name == itemName.NOTE_AS_USEFUL:
            name = itemName.NOTE
            if not hasattr(self.multiworld, "generation_is_fake"):
                item_classification = ItemClassification.useful
        elif name == itemName.DOUBLOON_AS_FILLER:
            name = itemName.DOUBLOON
            if not hasattr(self.multiworld, "generation_is_fake"):
                item_classification = ItemClassification.filler
        elif name == itemName.HEALTHUP and (
            self.options.logic_type.value
                == LogicType.option_easy_tricks or self.options.logic_type.value == LogicType.option_intended
        ):
            item_classification = ItemClassification.useful

        banjoItem = all_item_table.get(name)
        if not banjoItem:
            raise ValueError(f"{name} is not a valid item name for Banjo-Tooie")

        if item_classification is None:
            item_classification = self.get_classification(banjoItem)

        if item_classification == ItemClassification.trap:
            self.traps_in_pool += 1

        if name == itemName.JIGGY:
            self.jiggies_in_pool += 1
        if name == itemName.NOTE:
            self.notes_in_pool += 1
        if name == itemName.DOUBLOON:
            self.doubloons_in_pool += 1

        created_item = BanjoTooieItem(name, item_classification, banjoItem.btid, self.player)
        return created_item

    def get_classification(self, banjoItem: ItemData) -> ItemClassification:
        if banjoItem.btid is not None:
            itemname = self.item_id_to_name[banjoItem.btid]

            if itemname == itemName.PAGES:
                if self.options.cheato_rewards.value:
                    return ItemClassification.progression_deprioritized_skip_balancing
                else:
                    return ItemClassification.filler

            if itemname == itemName.HONEY:
                if self.options.honeyb_rewards.value:
                    return ItemClassification.progression_deprioritized_skip_balancing
                else:
                    return ItemClassification.useful

        if banjoItem.type not in (
            ItemClassification.progression,
            ItemClassification.progression_deprioritized_skip_balancing,
            ItemClassification.useful,
            ItemClassification.filler,
            ItemClassification.trap
        ):
            raise Exception(f"{banjoItem.type} does not correspond to a valid item classification.")

        return banjoItem.type

    def create_event_item(self, name: str) -> Item:
        item_classification = ItemClassification.progression
        created_item = BanjoTooieItem(name, item_classification, None, self.player)
        return created_item

    @staticmethod
    def calculate_useful_filler(total: int, progression: int) -> tuple[int, int]:
        # We want to split non-progressive items into two halfs
        # half is useful, half is filler
        remainder = total - progression
        useful = ceil(remainder / 2)

        return useful, remainder - useful

    def get_jiggies_in_pool(self) -> List[Item]:
        itempool = []

        if self.options.jingaling_jiggy.value:
            # Below give the king a guarentee Jiggy if option is set
            self.get_location(locationName.JIGGYIH10).place_locked_item(self.create_item(itemName.JIGGY))

        last_level_requirement = max(self.world_requirements.values())
        if not self.options.open_hag1.value and self.options.victory_condition.value == VictoryCondition.option_hag1:
            last_level_requirement = max(last_level_requirement, 70)

        # Buffer of 5 progression so that cryptic hints do not consider every jiggy as required,
        # and so that the spoiler log does not list the absolute worst jiggies as
        # part of the playthrough.
        progression_jiggies = min(last_level_requirement + 5, 90)

        # Buffer that is not considered in logic to make the generation faster while making the seed easier.
        useful_jiggies = ceil((90 - progression_jiggies - 5)/2)\
            if self.options.replace_extra_jiggies.value\
            else 90 - progression_jiggies

        # Some progression jiggies can be placed as locked items, so we don't add them to the pool.
        if self.options.jingaling_jiggy.value:
            progression_jiggies -= 1
        if not self.options.randomize_jinjos.value:
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
        return itempool

    def get_notes_in_pool(self) -> List[Item]:
        if not self.options.randomize_notes.value:
            return []

        itempool = []

        progression_notes = ceil(max(self.jamjars_siloname_costs.values()) / 5)

        useful_notes, filler_notes = \
            self.calculate_useful_filler(int(900 / 5), progression_notes)

        taken_by_clefs = 4 * (self.options.extra_trebleclefs_count.value + all_item_table[itemName.TREBLE].qty)\
            + 2 * self.options.bass_clef_amount.value

        progression_notes -= taken_by_clefs

        # in case preplaced items are over the progression count
        if progression_notes < 0:
            useful_notes += progression_notes
            progression_notes = 0
        if useful_notes < 0:
            filler_notes += useful_notes
            useful_notes = 0
        if filler_notes < 0:
            logging.warning("Number of notes that need to be inserted is somehow negative.")

        itempool += [
            self.create_item(itemName.NOTE) for i in range(progression_notes)
        ]
        itempool += [
            self.create_item(itemName.NOTE_AS_USEFUL) for i in range(useful_notes)
        ]
        if not self.options.replace_extra_notes.value:
            itempool += [
                self.create_item(itemName.NOTE_AS_FILLER) for i in range(filler_notes)
            ]

        return itempool

    def create_items(self) -> None:
        itempool = []

        # START OF ITEMS CUSTOM LOGIC

        if self.options.victory_condition.value == VictoryCondition.option_token_hunt:
            itempool += [self.create_item(itemName.MUMBOTOKEN) for i in range(self.options.tokens_in_pool.value)]

        itempool += self.get_jiggies_in_pool()
        itempool += self.get_notes_in_pool()

        count = all_item_table[itemName.TREBLE].qty if self.options.randomize_treble.value else 0
        count += self.options.extra_trebleclefs_count
        itempool += [self.create_item(itemName.TREBLE) for i in range(count)]

        count = self.options.bass_clef_amount.value
        itempool += [self.create_item(itemName.BASS) for i in range(count)]

        # END OF ITEMS CUSTOM LOGIC

        # Basic items that need no extra logic, if you need to customize quantity or logic, add them above this
        # and add the item to the handled_items in def item_filter.
        for name, item in all_item_table.items():
            item_name = self.item_filter(name, item)
            if item_name is not None:
                # We're still using the original item quantity.
                itempool += [self.create_item(item_name) for _ in range(item.qty)]

        # Add Filler items until all locations are filled
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        if len(itempool) > total_locations:
            warnings.warn(
                "Number of total available items exceeds the number of locations,\
                    likely there is a bug in the generation."
            )

        itempool += [self.create_filler() for _ in range(total_locations - len(itempool))]

        self.multiworld.itempool.extend(itempool)

    def item_filter(self, name: str, item: ItemData) -> str | None:
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
        if item.type in (ItemClassification.filler, ItemClassification.trap) and name != itemName.JNONE:
            return None

        if name == itemName.DOUBLOON and not self.options.randomize_doubloons.value:
            return None

        if name == itemName.PAGES and not self.options.randomize_cheato.value:  # Added later in Prefill
            return None

        if name == itemName.HONEY and not self.options.randomize_honeycombs.value:  # Added later in Prefill
            return None

        if name == itemName.HEALTHUP and not self.options.honeyb_rewards.value:
            return None

        if name in all_group_table['bk_moves'].keys()\
                and self.options.randomize_bk_moves.value == RandomizeBKMoveList.option_none:
            return None

        # talon trot and tall jump not in pool
        elif (name == itemName.TTROT or name == itemName.TJUMP)\
                and self.options.randomize_bk_moves.value == RandomizeBKMoveList.option_mcjiggy_special:
            return None

        if name in all_group_table['moves'].keys() and not self.options.randomize_bt_moves.value:
            return None

        if name in all_group_table['magic'].keys() and not self.options.randomize_glowbos.value:
            return None

        if name in all_group_table['jinjo'].keys() and not self.options.randomize_jinjos.value:
            return None

        if name == itemName.CHUFFY and not self.options.randomize_chuffy.value:
            return None

        if name in all_group_table['stations'].keys() and not self.options.randomize_stations.value:
            return None

        if name in all_group_table['levelaccess'].keys():
            return None

        if name in all_group_table['stopnswap'].keys() and not self.options.randomize_stop_n_swap.value:
            return None

        if name in all_group_table['Warp Pads'].keys() and not self.options.randomize_warp_pads.value:
            return None

        if name in all_group_table['Silos'].keys() and not self.options.randomize_silos.value:
            return None

        if name in all_group_table['cheats'].keys() and not self.options.cheato_rewards.value:
            return None

        if name in all_group_table['Silos'].keys() and name in self.preopened_silos:
            return None

        if name == itemName.ROAR and not self.options.randomize_dino_roar.value:
            return None

        if name == itemName.GRRELIC and not self.options.randomize_green_relics.value:
            return None

        if name == itemName.BTTICKET and not self.options.randomize_tickets.value:
            return None

        if name == itemName.BEANS and not self.options.randomize_beans.value:
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

        if self.options.progressive_beak_buster.value:
            if name in progressive_ability_breakdown[itemName.PBBUST]:
                return itemName.PBBUST

        if self.options.egg_behaviour.value == EggsBehaviour.option_progressive_eggs:
            if name in progressive_ability_breakdown[itemName.PEGGS]:
                return itemName.PEGGS

        if self.options.progressive_shoes.value:
            if name in progressive_ability_breakdown[itemName.PSHOES]:
                return itemName.PSHOES

        if self.options.progressive_water_training.value == ProgressiveWaterTraining.option_basic:
            if name in progressive_ability_breakdown[itemName.PSWIM]:
                return itemName.PSWIM
        elif self.options.progressive_water_training.value == ProgressiveWaterTraining.option_advanced:
            if name in progressive_ability_breakdown[itemName.PASWIM]:
                return itemName.PASWIM

        if self.options.progressive_bash_attack.value:
            if name in progressive_ability_breakdown[itemName.PBASH]:
                return itemName.PBASH

        if self.options.progressive_flight.value:
            if name in progressive_ability_breakdown[itemName.PFLIGHT]:
                return itemName.PFLIGHT

        if self.options.progressive_egg_aiming.value == ProgressiveEggAim.option_basic:
            if name in progressive_ability_breakdown[itemName.PEGGAIM]:
                return itemName.PEGGAIM
        elif self.options.progressive_egg_aiming.value == ProgressiveEggAim.option_advanced:
            if name in progressive_ability_breakdown[itemName.PAEGGAIM]:
                return itemName.PAEGGAIM

        # END OF PROGRESSIVE MOVES

        return name

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)
        self.pre_fill_me()

    def generate_early(self) -> None:
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Universal Tracker trickery
            slot_data = self.multiworld.re_gen_passthrough[self.game]

            slot_options: dict[str, Any] = slot_data.get("options", {})
            for key, value in slot_options.items():
                opt = getattr(self.options, key, None)
                if opt is not None:
                    setattr(self.options, key, opt.from_any(value))

            custom_bt_data = slot_data["custom_bt_data"]
            self.world_requirements = custom_bt_data["world_requirements"]
            self.world_order = custom_bt_data["world_order"]
            self.jamjars_siloname_costs = custom_bt_data["jamjars_siloname_costs"]
            self.loading_zones = custom_bt_data["loading_zones"]
        else:
            # Normal generation
            self.validate_yaml_options()
            self.choose_starter_egg()
            self.choose_starter_attack()
            randomize_world_progression(self)
            self.hand_preopened_silos()

    def validate_yaml_options(self) -> None:
        if self.options.randomize_worlds.value \
                and self.options.randomize_bk_moves.value != RandomizeBKMoveList.option_none\
                and self.options.logic_type.value == LogicType.option_intended:
            raise OptionError("Randomize Worlds and Randomize BK Moves is not compatible with Intended Logic.")
        if not self.options.randomize_notes.value \
                and not self.options.randomize_signposts.value and not self.options.nestsanity.value \
                and self.options.randomize_bk_moves.value != RandomizeBKMoveList.option_none:
            if self.multiworld.players == 1:
                raise OptionError("Randomize Notes, signposts or nestsanity is required for Randomize BK Moves.")
        if self.options.victory_condition.value == VictoryCondition.option_token_hunt:
            if self.options.token_hunt_length.value > self.options.tokens_in_pool.value:
                self.options.token_hunt_length.value = self.options.tokens_in_pool.value
            if self.options.tokens_in_pool.value > 15\
                    and not self.options.randomize_signposts.value\
                    and not self.options.nestsanity.value:
                raise OptionError(
                    "You cannot have more than 15 Mumbo Tokens without enabling Randomize Signposts or Nestanity."
                )
            if self.options.tokens_in_pool.value > 50 and not self.options.nestsanity.value:
                raise OptionError("You cannot have more than 50 Mumbo Tokens without enabling Nestanity.")
        if not self.options.randomize_notes.value\
                and self.options.extra_trebleclefs_count.value != 0\
                and self.options.bass_clef_amount.value != 0:
            raise OptionError("Randomize Notes is required to add extra Treble Clefs or Bass Clefs")
        if self.options.progressive_beak_buster.value\
                and (not self.options.randomize_bk_moves.value or not self.options.randomize_bt_moves.value):
            raise OptionError(
                "You cannot have progressive Beak Buster without randomizing moves and randomizing BK moves"
            )
        if (self.options.egg_behaviour.value == EggsBehaviour.option_random_starting_egg
                or self.options.egg_behaviour.value == EggsBehaviour.option_simple_random_starting_egg) \
                and (not self.options.randomize_bk_moves.value or not self.options.randomize_bt_moves.value):
            raise OptionError(
                "You cannot have Randomize Starting Egg without randomizing moves and randomizing BK moves"
            )
        elif self.options.egg_behaviour.value == EggsBehaviour.option_progressive_eggs\
                and not self.options.randomize_bt_moves.value:
            raise OptionError("You cannot have progressive Eggs without randomizing moves")
        if self.options.progressive_shoes.value\
                and not (
                    self.options.randomize_bk_moves.value
                    and self.options.randomize_bt_moves.value
                    and (self.options.randomize_signposts.value or self.options.nestsanity.value)
                ):
            raise OptionError("You cannot have progressive Shoes without randomizing moves, "
                              "randomizing BK moves and enabling either nestanity or randomize signpost")
        if self.options.progressive_water_training.value != ProgressiveWaterTraining.option_none \
                and (
                    self.options.randomize_bk_moves.value == RandomizeBKMoveList.option_none
                    or not self.options.randomize_bt_moves.value
                ):
            raise OptionError("You cannot have progressive Water Training\
                without randomizing moves and randomizing BK moves")
        if self.options.progressive_flight.value\
                and (not self.options.randomize_bk_moves.value or not self.options.randomize_bt_moves.value):
            raise OptionError("You cannot have progressive flight without randomizing moves and randomizing BK moves")
        if self.options.progressive_egg_aiming.value != ProgressiveEggAim.option_none\
                and (not self.options.randomize_bk_moves.value or not self.options.randomize_bt_moves.value):
            raise OptionError(
                "You cannot have progressive egg aiming without randomizing moves and randomizing BK moves"
            )
        if self.options.progressive_bash_attack.value\
                and (not self.options.randomize_stop_n_swap.value or not self.options.randomize_bt_moves.value):
            raise OptionError(
                "You cannot have progressive bash attack without randomizing Stop N Swap and randomizing BK moves"
                )
        if not self.options.randomize_bt_moves.value and self.options.jamjars_silo_costs.value != JamjarsSiloCosts.option_vanilla:
            raise OptionError("You cannot change the silo costs without randomizing Jamjars' moves.")
        if not self.options.open_hag1.value\
                and self.options.victory_condition.value == VictoryCondition.option_wonderwing_challenge:
            self.options.open_hag1.value = True
        if self.options.world_requirements.value != WorldRequirements.option_normal and not self.options.skip_puzzles.value:
            raise OptionError("Your world requirements needs to be set to normal if you are not going to skip puzzles.")

    def choose_starter_egg(self) -> None:
        if self.options.egg_behaviour.value == EggsBehaviour.option_random_starting_egg or \
                self.options.egg_behaviour.value == EggsBehaviour.option_simple_random_starting_egg:

            if self.options.egg_behaviour.value == EggsBehaviour.option_random_starting_egg:
                eggs = [itemName.BEGGS, itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS]
            else:
                eggs = [itemName.BEGGS, itemName.FEGGS, itemName.GEGGS, itemName.IEGGS]
            egg_name = self.random.choice(eggs)
            starting_egg = self.create_item(egg_name)
            self.multiworld.push_precollected(starting_egg)
            banjoItem = all_item_table[egg_name]
            self.starting_egg = banjoItem.btid
        else:
            starting_egg = self.create_item(itemName.BEGGS)
            self.multiworld.push_precollected(starting_egg)
            banjoItem = all_item_table[itemName.BEGGS]
            self.starting_egg = banjoItem.btid

    def choose_starter_attack(self) -> None:
        if self.options.randomize_bk_moves.value != RandomizeBKMoveList.option_none:
            if self.options.logic_type.value == LogicType.option_intended:
                if self.options.progressive_egg_aiming.value == ProgressiveEggAim.option_basic:
                    base_attacks = [itemName.PEGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT]
                elif self.options.progressive_egg_aiming.value == ProgressiveEggAim.option_advanced:
                    base_attacks = [itemName.PAEGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT]
                else:
                    base_attacks = [itemName.EGGSHOOT, itemName.EGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT]
            elif self.options.logic_type.value == LogicType.option_easy_tricks:
                if self.options.progressive_egg_aiming.value == ProgressiveEggAim.option_basic:
                    base_attacks = [itemName.PEGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT, itemName.WWING]
                elif self.options.progressive_egg_aiming.value == ProgressiveEggAim.option_advanced:
                    base_attacks = [itemName.PAEGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT, itemName.WWING]
                else:
                    base_attacks = [
                        itemName.EGGSHOOT,
                        itemName.EGGAIM,
                        itemName.BBARGE,
                        itemName.ROLL,
                        itemName.ARAT,
                        itemName.WWING
                    ]
            else:
                if self.options.progressive_egg_aiming.value == ProgressiveEggAim.option_basic:
                    base_attacks = [itemName.PEGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT, itemName.WWING]
                elif self.options.progressive_egg_aiming.value == ProgressiveEggAim.option_advanced:
                    base_attacks = [itemName.PAEGGAIM, itemName.BBARGE, itemName.ROLL, itemName.ARAT, itemName.WWING]
                else:
                    base_attacks = [
                        itemName.EGGSHOOT,
                        itemName.EGGAIM,
                        itemName.BBARGE,
                        itemName.ROLL,
                        itemName.ARAT,
                        itemName.WWING
                    ]
                base_attacks.append(itemName.PBASH if self.options.progressive_bash_attack.value else itemName.GRAT)
                base_attacks.append(itemName.PBBUST if self.options.progressive_beak_buster.value else itemName.BBUST)
            chosen_attack = self.random.choice(base_attacks)

            starting_attack = self.create_item(chosen_attack)
            self.multiworld.push_precollected(starting_attack)
            banjoItem = all_item_table.get(chosen_attack)
            self.starting_attack = banjoItem.btid

    def hand_preopened_silos(self) -> None:
        for silo in self.preopened_silos:
            self.multiworld.push_precollected(self.create_item(silo))

    def set_rules(self) -> None:
        rules = BanjoTooieRules(self)
        return rules.set_rules()

    def pre_fill_me(self) -> None:
        def prefill_locations_with_item(item_name: str, locations: list[str]) -> None:
            for location_name in locations:
                self.get_location(location_name).place_locked_item(self.create_item(item_name))

        if not self.options.randomize_honeycombs.value:
            self.banjo_pre_fills(itemName.HONEY, "Honeycomb", False)

        if not self.options.randomize_cheato.value:
            self.banjo_pre_fills(itemName.PAGES, "Cheato Page", False)

        if not self.options.randomize_doubloons.value:
            self.banjo_pre_fills(itemName.DOUBLOON, "Doubloon", False)

        if not self.options.randomize_bt_moves.value:
            self.banjo_pre_fills("Moves", None, True)

        if not self.options.randomize_dino_roar.value:
            self.banjo_pre_fills("Dino", None, True)

        if not self.options.randomize_glowbos.value:
            self.banjo_pre_fills("Magic", None, True)

        if not self.options.randomize_treble.value:
            self.banjo_pre_fills(itemName.TREBLE, "Treble Clef", False)

        if not self.options.randomize_stations.value:
            self.banjo_pre_fills("Stations", None, True)

        if not self.options.randomize_chuffy.value:
            self.banjo_pre_fills(itemName.CHUFFY, "Chuffy", False)

        if not self.options.randomize_notes.value:
            self.banjo_pre_fills(itemName.NOTE, "Note", False)

        if not self.options.randomize_stop_n_swap.value:
            self.banjo_pre_fills("StopnSwap", None, True)

        if not self.options.cheato_rewards.value:
            self.banjo_pre_fills("Cheats", None, True)

        if self.options.skip_puzzles.value:
            world_num = 1
            for world, amt in self.world_requirements.items():
                if world == regionName.GIO:
                    item = self.create_item(itemName.GIA)
                elif world == regionName.JR:
                    item = self.create_item(itemName.JRA)
                else:
                    item = self.create_item(world)
                self.get_location(f"World {world_num} Unlocked").place_locked_item(item)
                world_num += 1

        if self.options.victory_condition.value == VictoryCondition.option_minigame_hunt\
                or self.options.victory_condition.value == VictoryCondition.option_wonderwing_challenge:

            item = self.create_item(itemName.MUMBOTOKEN)
            for location_name in MumboTokenGames_table.keys():
                self.get_location(location_name).place_locked_item(item)

        if self.options.victory_condition.value == VictoryCondition.option_boss_hunt \
                or self.options.victory_condition.value == VictoryCondition.option_wonderwing_challenge \
                or self.options.victory_condition.value == VictoryCondition.option_boss_hunt_and_hag1:

            item = self.create_item(itemName.MUMBOTOKEN)
            for location_name in MumboTokenBoss_table.keys():
                self.get_location(location_name).place_locked_item(item)

        if self.options.victory_condition.value == VictoryCondition.option_jinjo_family_rescue\
                or self.options.victory_condition.value == VictoryCondition.option_wonderwing_challenge:
            item = self.create_item(itemName.MUMBOTOKEN)
            for location_name in MumboTokenJinjo_table.keys():
                self.get_location(location_name).place_locked_item(item)

        if not self.options.randomize_jinjos.value:
            prefill_locations_with_item(itemName.JIGGY, [
                locationName.JIGGYIH1,
                locationName.JIGGYIH2,
                locationName.JIGGYIH3,
                locationName.JIGGYIH4,
                locationName.JIGGYIH5,
                locationName.JIGGYIH6,
                locationName.JIGGYIH7,
                locationName.JIGGYIH8,
                locationName.JIGGYIH9
            ])
            prefill_locations_with_item(itemName.WJINJO, [
                locationName.JINJOJR5
            ])
            prefill_locations_with_item(itemName.OJINJO, [
                locationName.JINJOWW4,
                locationName.JINJOHP2
            ])
            prefill_locations_with_item(itemName.YJINJO, [
                locationName.JINJOWW3,
                locationName.JINJOHP4,
                locationName.JINJOHP3
            ])
            prefill_locations_with_item(itemName.BRJINJO, [
                locationName.JINJOGM1,
                locationName.JINJOJR2,
                locationName.JINJOTL2,
                locationName.JINJOTL5
            ])
            prefill_locations_with_item(itemName.GJINJO, [
                locationName.JINJOWW5,
                locationName.JINJOJR1,
                locationName.JINJOTL4,
                locationName.JINJOGI2,
                locationName.JINJOHP1
            ])
            prefill_locations_with_item(itemName.RJINJO, [
                locationName.JINJOMT2,
                locationName.JINJOMT3,
                locationName.JINJOMT5,
                locationName.JINJOJR3,
                locationName.JINJOJR4,
                locationName.JINJOWW2
            ])
            prefill_locations_with_item(itemName.BLJINJO, [
                locationName.JINJOGM3,
                locationName.JINJOTL1,
                locationName.JINJOHP5,
                locationName.JINJOCC2,
                locationName.JINJOIH1,
                locationName.JINJOIH4,
                locationName.JINJOIH5
            ])
            prefill_locations_with_item(itemName.PJINJO, [
                locationName.JINJOMT1,
                locationName.JINJOGM5,
                locationName.JINJOCC1,
                locationName.JINJOCC3,
                locationName.JINJOCC5,
                locationName.JINJOIH2,
                locationName.JINJOIH3,
                locationName.JINJOGI4
            ])
            prefill_locations_with_item(itemName.BKJINJO, [
                locationName.JINJOMT4,
                locationName.JINJOGM2,
                locationName.JINJOGM4,
                locationName.JINJOWW1,
                locationName.JINJOTL3,
                locationName.JINJOGI1,
                locationName.JINJOGI5,
                locationName.JINJOCC4,
                locationName.JINJOGI3
            ])

    def allow_jiggies_as_filler(self) -> bool:
        return self.options.replace_extra_jiggies.value and self.jiggies_in_pool < self.hard_item_limit

    def allow_notes_as_filler(self) -> bool:
        return self.options.replace_extra_notes.value\
            and self.options.randomize_notes.value\
            and self.notes_in_pool < self.hard_item_limit

    def allow_doubloons_as_filler(self) -> bool:
        return self.options.randomize_doubloons.value and self.doubloons_in_pool < self.hard_item_limit

    def get_filler_item_name(self) -> str:
        trap_weights = [
            (itemName.GNEST, self.options.golden_eggs_weight.value),
            (itemName.TTRAP, self.options.trip_trap_weight.value),
            (itemName.STRAP, self.options.slip_trap_weight.value),
            (itemName.TRTRAP, self.options.transform_trap_weight.value),
            (itemName.SQTRAP, self.options.squish_trap_weight.value),
            (itemName.TITRAP, self.options.tip_trap_weight.value),
        ]
        filler_weights = [
            (itemName.JIGGY_AS_FILLER, self.options.extra_jiggies_weight.value if self.allow_jiggies_as_filler() else 0),
            (itemName.NOTE_AS_FILLER, self.options.extra_notes_weight.value if self.allow_notes_as_filler() else 0),
            (itemName.DOUBLOON_AS_FILLER, self.options.extra_doubloons_weight
                if self.allow_doubloons_as_filler() else 0),
            (itemName.ENEST, self.options.egg_nests_weight.value * (2 if self.options.nestsanity.value else 1)),
            (itemName.FNEST, self.options.feather_nests_weight.value * (2 if self.options.nestsanity.value else 1)),
            (itemName.NONE, self.options.big_o_pants_weight.value)
        ]

        if self.traps_in_pool < self.options.max_traps.value:
            weights = trap_weights + filler_weights
        else:
            weights = filler_weights

        names, actual_weights = zip(*weights)

        if sum(actual_weights) == 0:
            actual_weights = (*actual_weights[:-1], 1)

        return self.random.choices(names, actual_weights, k=1)[0]

    def banjo_pre_fills(self, itemNameOrGroup: str, group: str | None, useGroup: bool) -> None:
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
    def stage_fill_hook(
        cls,
        multiworld: MultiWorld,
        progitempool: list[Item],
        usefulitempool: list[Item],
        filleritempool: list[Item],
        fill_locations: list[Location]
    ):
        # If there are a lot of items to fit in few locations, help out the generator by sorting the items into a more
        # easy to fill order. This reduces the chance of the fill algorithm getting stuck and having to swap items.
        # 0.75 is a heuristic threshold; default BT settings is about 82% of the pool being progression.
        if len(progitempool) / len(fill_locations) < 0.75:
            return

        bt_players = {world.player for world in multiworld.get_game_worlds(cls.game)}

        # Count how many copies of each item exist for each BT player.
        # Items with more copies are placed first, which helps AP's fill algorithm.
        item_counts: dict[int, Counter[str]] = {player: Counter() for player in bt_players}
        for item in progitempool:
            if item.player in bt_players:
                item_counts[item.player][item.name] += 1

        def sort_pool(item: Item) -> int:
            if item.player in item_counts:
                return item_counts[item.player][item.name]
            else:
                # If it's not an item belonging to a Banjo-Tooie player, keep its order the same.
                return 0

        progitempool.sort(key=sort_pool)

    @classmethod
    def stage_write_spoiler(cls, world, spoiler_handle):
        entrance_hags = {
            regionName.MT: regionName.MTE,
            regionName.GM: regionName.GGME,
            regionName.WW: regionName.WWE,
            regionName.JR: regionName.JRLE,
            regionName.TL: regionName.TDLE,
            regionName.GIO: regionName.GIE,
            regionName.HP: regionName.HFPE,
            regionName.CC: regionName.CCLE,
            regionName.CK: regionName.CKE,
            regionName.MTBOSS: regionName.MTTT,
            regionName.GMBOSS: regionName.CHUFFY,
            regionName.WWBOSS: regionName.WW,
            regionName.JRBOSS: regionName.JRLC,
            regionName.TLBOSS: regionName.TLTOP,
            regionName.GIBOSS: regionName.GI1,
            regionName.HPFBOSS: regionName.HP,
            regionName.HPIBOSS: regionName.HP,
            regionName.CCBOSS: regionName.CC,
        }
        bt_players = world.get_game_players(cls.game)
        spoiler_handle.write(f"\n\nBanjo-Tooie ({cls.world_version.as_simple_string()})")
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
            spoiler_handle.write("\n\tWorld Requirements:")
            for entrances, cost in currentWorld.world_requirements.items():
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
                spoiler_handle.write("\n\t\t{}: {}".format(
                    currentWorld.location_id_to_name[location_id],
                    hint_data.text
                ))

    def fill_slot_data(self) -> Dict[str, Any]:
        t0 = time.time()
        generate_hints(self)
        t1 = time.time()
        total = t1-t0
        if total >= 1:
            logging.info(f"Took {total:.4f} seconds in BanjoTooieWorld.generate_hints for player {self.player}, named {self.multiworld.player_name[self.player]}.")
        btoptions = {option_name: option.value for option_name, option in self.options.__dict__.items()}

        # plando_items not serialisable, so we can't include it in slot_data.
        btoptions.pop("plando_items")

        # Elements that are randomised outside the yaml and affects gameplay
        custom_bt_data: Dict[str, Any] = {
            "player_name": self.player_name,
            "seed": self.random.randint(12212, 9090763),
            "world_order": self.world_order,
            "world_requirements": self.world_requirements,
            "loading_zones": self.loading_zones,
            "preopened_silos_names": self.preopened_silos,
            "preopened_silos_ids": [self.item_name_to_id[name] for name in self.preopened_silos],
            "version": f"{self.world_version.as_simple_string()}",
            "jamjars_siloname_costs": self.jamjars_siloname_costs,
            "jamjars_silo_costs": self.jamjars_silo_costs,
            "hints": {location: asdict(hint_data) for location, hint_data in self.hints.items()}
        }
        slot_data = {
            "options": btoptions,
            "custom_bt_data": custom_bt_data,
        }
        return slot_data

    # for the universal tracker, doesn't get called in standard gen
    def interpret_slot_data(self, slot_data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return slot_data

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        # For hints, we choose to hint the level for which the collectible would count.
        # For example, Dippy Jiggy would hint to TDL.

        # For items in boss rooms, we hint the level that leads to the boss room, if boss rooms are randomised.
        # This has priority over the level entrance.

        def add_level_loading_zone_information(
                hint_information: Dict[int, str],
                locations: Dict[str, LocationData],
                level: str
                ):
            entrance_lookup = {
                regionName.MT: regionName.MTE,
                regionName.GM: regionName.GGME,
                regionName.WW: regionName.WWE,
                regionName.JR: regionName.JRLE,
                regionName.TL: regionName.TDLE,
                regionName.GIO: regionName.GIE,
                regionName.HP: regionName.HFPE,
                regionName.CC: regionName.CCLE,
                regionName.CK: regionName.CKE,
            }
            for data in locations.values():
                entrance_to_level = list(self.loading_zones.keys())[list(self.loading_zones.values()).index(level)]
                hint_information.update({data.btid: entrance_lookup[entrance_to_level]})

        hints = {}
        if self.options.randomize_world_entrance_loading_zones.value:
            add_level_loading_zone_information(hints, MTLoc_Table, regionName.MT)
            add_level_loading_zone_information(hints, GMLoc_table, regionName.GM)
            add_level_loading_zone_information(hints, WWLoc_table, regionName.WW)
            add_level_loading_zone_information(hints, JRLoc_table, regionName.JR)
            add_level_loading_zone_information(hints, TLLoc_table, regionName.TL)
            add_level_loading_zone_information(hints, GILoc_table, regionName.GIO)
            add_level_loading_zone_information(hints, HPLoc_table, regionName.HP)
            add_level_loading_zone_information(hints, CCLoc_table, regionName.CC)

        if self.options.randomize_boss_loading_zones.value:
            boss_entrance_lookup = {
                regionName.MTBOSS: regionName.MTTT,
                regionName.GMBOSS: regionName.CHUFFY,
                regionName.WWBOSS: regionName.WW,
                regionName.JRBOSS: regionName.JRLC,
                regionName.TLBOSS: regionName.TLTOP,
                regionName.GIBOSS: regionName.GI1,
                regionName.HPFBOSS: regionName.HP,
                regionName.HPIBOSS: regionName.HP,
                regionName.CCBOSS: regionName.CC,
            }
            for boss_region_name in boss_entrance_lookup.keys():
                for location in self.get_region(boss_region_name).locations:
                    entrance_name = list(self.loading_zones.keys())[
                        list(self.loading_zones.values()).index(boss_region_name)
                    ]
                    hints.update({location.address: boss_entrance_lookup[entrance_name]})

        hint_data.update({self.player: hints})
