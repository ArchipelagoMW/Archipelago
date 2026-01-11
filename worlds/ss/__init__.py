import os
import zipfile
import json
from base64 import b64encode
from copy import deepcopy
from collections.abc import Mapping
from dataclasses import fields
from typing import Any, ClassVar

import yaml

from BaseClasses import MultiWorld, Region, Tutorial, LocationProgressType, ItemClassification as IC
from Options import Toggle, OptionError
from worlds.AutoWorld import WebWorld, World
from worlds.Files import APPlayerContainer, AutoPatchRegister
from worlds.generic.Rules import add_item_rule
from worlds.LauncherComponents import (
    Component,
    SuffixIdentifier,
    Type,
    components,
    launch_subprocess,
    icon_paths,
)

from .Constants import *

from .Items import ITEM_TABLE, SSItem
from .Locations import LOCATION_TABLE, SSLocation, SSLocFlag
from .Options import SSOptions
from .Rules import set_rules
from .Names import HASH_NAMES
from .Entrances import AP_ENTRANCE_TABLE
from .Utils import restricted_safe_dump

from .rando.DungeonRando import DungeonRando
from .rando.EntranceRando import EntranceRando
from .rando.ItemPlacement import handle_itempool, item_classification
from .rando.HintPlacement import Hints
from .rando.MiscRando import shuffle_batreaux_counts

from .logic.LogicParser import parse_expression
from .logic.Logic import ALL_REQUIREMENTS

AP_VERSION = [0, 6, 2]
WORLD_VERSION = [0, 5, 3]
RANDO_VERSION = [0, 5, 3]


def run_client() -> None:
    """
    Launch the Skyward Sword client.
    """
    print("Running SS Client")
    from .SSClient import main

    launch_subprocess(main, name="SSClient")


components.append(
    Component(
        "Skyward Sword Client",
        func=run_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apssr"),
        icon="Skyward Sword"
    )
)
icon_paths["Skyward Sword"] = "ap:worlds.ss/assets/icon.png"


class SSWeb(WebWorld):
    """
    This class handles the web interface.

    The web interface includes the setup guide and the options page for generating YAMLs.
    """
    tutorials = [Tutorial(
        "Skyward Sword Setup Guide",
        "A guide to setting up SSR for Archipelago on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["bcats"]
    )]
    theme = "ice"
    rich_text_options_doc = True


class SSContainer(APPlayerContainer):
    """
    This class defines the container file for Skyward Sword.
    """

    game: str = "Skyward Sword"
    patch_file_ending: str = ".apssr"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if "data" in kwargs:
            self.data = kwargs["data"]
            del kwargs["data"]

        super().__init__(*args, **kwargs)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        """
        Write the contents of the container file.
        """
        super().write_contents(opened_zipfile)

        # Record the data for the game under the key `plando` using the adjusted safe_dump method that supports counters
        opened_zipfile.writestr("plando", b64encode(bytes(restricted_safe_dump(self.data, sort_keys=False), "utf-8")))

class SSWorld(World):
    """
    What if that's Zelda down there, and she's sending me a signal? It's a sign!
    It says, `Save me, Groose. You're my only hope!`
    The more I think about it, the more sure I get! It's Zelda down there, and I gotta go rescue her!

    Anyhow, don't think about trying to go down there before me. I'm her hero, remember?

    Ugh. I don't even know why I'm talking to you. Looking at you just makes me feel sad again.
    """

    options_dataclass = SSOptions
    options: SSOptions
       
    game: ClassVar[str] = "Skyward Sword"
    topology_present: bool = True
    web = SSWeb()
    required_client_version: tuple[int, int, int] = (0, 5, 1)
    origin_region_name: str = "" # This is set later
    explicit_indirect_conditions = False 
    
    item_name_to_id: ClassVar[dict[str, int]] = {
        name: SSItem.get_apid(data.code)
        for name, data in ITEM_TABLE.items()
        if data.code is not None
    }
    location_name_to_id: ClassVar[dict[str, int]] = {
        name: SSLocation.get_apid(data.code)
        for name, data in LOCATION_TABLE.items()
        if data.code is not None
    }

    create_items = handle_itempool
    set_rules = set_rules

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.progress_locations: set[str] = set()
        self.nonprogress_locations: set[str] = set()

        self.dungeons = DungeonRando(self)
        self.entrances = EntranceRando(self)

    def determine_progress_and_nonprogress_locations(self) -> tuple[set[str], set[str]]:
        """
        Determine which locations are progress or nonprogress based on player's options.

        :return: A tuple of a set of progress locations and a set of nonprogress locations.
        """

        progress_locations: set[str] = set()
        nonprogress_locations: set[str] = set()

        def add_flag(option: Toggle, flag: SSLocFlag) -> SSLocFlag:
            return flag if option else SSLocFlag.ALWAYS

        # Keep these always enabled
        enabled_flags = SSLocFlag.ALWAYS
        enabled_flags |= SSLocFlag.TADTONE
        enabled_flags |= SSLocFlag.BEEDLE

        # AP Progression Groups
        enabled_flags |= add_flag(self.options.progression_goddess_chests, SSLocFlag.GODDESS)
        enabled_flags |= add_flag(self.options.progression_minigames, SSLocFlag.MINIGME)
        enabled_flags |= add_flag(self.options.progression_crystals, SSLocFlag.CRYSTAL)
        enabled_flags |= add_flag(self.options.progression_scrapper, SSLocFlag.SCRAPPR)

        # Other flags
        enabled_flags |= add_flag(self.options.rupeesanity, SSLocFlag.RUPEE)
        enabled_flags |= add_flag(self.options.treasuresanity_in_silent_realms, SSLocFlag.TRIAL)

        # Empty Unrequired Dungeons
        if self.options.empty_unrequired_dungeons:
            enabled_flags |= (
                SSLocFlag.D_SV
                if "Skyview" in self.dungeons.required_dungeons
                else SSLocFlag.ALWAYS
            )
            enabled_flags |= (
                SSLocFlag.D_ET
                if "Earth Temple" in self.dungeons.required_dungeons
                else SSLocFlag.ALWAYS
            )
            enabled_flags |= (
                SSLocFlag.D_LMF
                if "Lanayru Mining Facility" in self.dungeons.required_dungeons
                else SSLocFlag.ALWAYS
            )
            enabled_flags |= (
                SSLocFlag.D_AC
                if "Ancient Cistern" in self.dungeons.required_dungeons
                else SSLocFlag.ALWAYS
            )
            enabled_flags |= (
                SSLocFlag.D_SSH
                if "Sandship" in self.dungeons.required_dungeons
                else SSLocFlag.ALWAYS
            )
            enabled_flags |= (
                SSLocFlag.D_FS
                if "Fire Sanctuary" in self.dungeons.required_dungeons
                else SSLocFlag.ALWAYS
            )
            if self.options.triforce_required and self.options.triforce_shuffle != "anywhere":
                enabled_flags |= SSLocFlag.D_SK
        else:
            enabled_flags |= (
                SSLocFlag.D_SV
                | SSLocFlag.D_ET
                | SSLocFlag.D_LMF
                | SSLocFlag.D_AC
                | SSLocFlag.D_SSH
                | SSLocFlag.D_FS
                | SSLocFlag.D_SK
            )

        for loc, data in LOCATION_TABLE.items():
            if data.flags & SSLocFlag.BTREAUX:
                if loc == "Batreaux's House - Chest":
                    bat_rew = "Batreaux's House - Third Reward"
                elif loc == "Batreaux's House - Seventh Reward":
                    bat_rew = "Batreaux's House - Sixth Reward"
                else:
                    bat_rew = loc
                if BATREAUX_LOCATIONS.index(bat_rew) < self.options.progression_batreaux.value:
                    progress_locations.add(loc)
                else:
                    nonprogress_locations.add(loc)
            elif data.flags & enabled_flags == data.flags:
                progress_locations.add(loc)
            else:
                nonprogress_locations.add(loc)

        for loc in self.options.exclude_locations.value:
            if loc in progress_locations:
                progress_locations.remove(loc)
                nonprogress_locations.add(loc)
            elif loc in nonprogress_locations:
                pass
            else:
                raise OptionError(
                    f"Unknown location in option `excluded locations`: {loc}"
                )

        return progress_locations, nonprogress_locations
    
    @staticmethod
    def _get_classification_name(classification: IC) -> str:
        """
        Return a string representation of the item's highest-order classification.
        :param classification: The item's classification.
        :return: A string representation of the item's highest classification. The order of classification is
        progression > trap > useful > filler.
        """

        if IC.progression in classification:
            return "progression"
        elif IC.trap in classification:
            return "trap"
        elif IC.useful in classification:
            return "useful"
        else:
            return "filler"

    def generate_early(self) -> None:
        """
        Run before any other steps of the multiworld, but after options.
        """

        # Shuffle required dungeons and entrances according to options
        self.dungeons.randomize_required_dungeons()
        self.entrances.randomize_dungeon_entrances(self.dungeons.required_dungeons)
        self.entrances.randomize_trial_gates()

        self.entrances.randomize_starting_statues()
        self.entrances.randomize_starting_entrance()
        self.origin_region_name = self.entrances.starting_entrance["apregion"]

        # Determine progress and nonprogress locations
        self.progress_locations, self.nonprogress_locations = (
            self.determine_progress_and_nonprogress_locations()
        )

        self.batreaux_rewards = shuffle_batreaux_counts(self)
        self.batreaux_requirements = {}

    def create_regions(self) -> None:
        """
        Create and connect regions.
        """

        for reg_name, data in ALL_REQUIREMENTS.items():
            region = Region(reg_name, self.player, self.multiworld)
            for short_loc_name, rule in data["locations"].items():
                full_loc_name = f"{data["hint_region"]} - {short_loc_name}"
                og_full_loc_name = deepcopy(full_loc_name)
                if LOCATION_TABLE[full_loc_name].flags & SSLocFlag.BTREAUX:
                    # Remove location from progress or nonprogress locations
                    if full_loc_name in self.progress_locations:
                        self.progress_locations.remove(full_loc_name)
                        bat_loc_progress = True
                    elif full_loc_name in self.nonprogress_locations:
                        self.nonprogress_locations.remove(full_loc_name)
                        bat_loc_progress = False
                    else:
                        raise Exception(
                            f"Batreaux location not found in progress "
                            f"locations nor nonprogress locations: {full_loc_name}"
                        )

                    if short_loc_name == "Chest":
                        crystal_count = self.batreaux_rewards["Third Reward"]
                        short_loc_name = f"{str(crystal_count)} Crystals Chest"
                        full_loc_name = f"{data["hint_region"]} - {str(crystal_count)} Crystals Chest"
                        self.batreaux_requirements[short_loc_name] = f"{str(crystal_count)} Gratitude Crystals"
                    elif short_loc_name == "Seventh Reward":
                        crystal_count = self.batreaux_rewards["Sixth Reward"]
                        short_loc_name = f"{str(crystal_count)} Crystals Second Reward"
                        full_loc_name = f"{data["hint_region"]} - {str(crystal_count)} Crystals Second Reward"
                        self.batreaux_requirements[short_loc_name] = f"{str(crystal_count)} Gratitude Crystals"
                    else:
                        crystal_count = self.batreaux_rewards[short_loc_name]
                        short_loc_name = f"{str(crystal_count)} Crystals"
                        full_loc_name = f"{data["hint_region"]} - {str(crystal_count)} Crystals"
                        self.batreaux_requirements[short_loc_name] = f"{str(crystal_count)} Gratitude Crystals"

                    # Add new location back into progress or nonprogress locations
                    if bat_loc_progress:
                        self.progress_locations.add(full_loc_name)
                    else:
                        self.nonprogress_locations.add(full_loc_name)

                    # Create a batreaux reward location
                    location = SSLocation(self.player, full_loc_name, region, LOCATION_TABLE[og_full_loc_name], ogname=og_full_loc_name)
                else:
                    # Create a normal location
                    location = SSLocation(self.player, full_loc_name, region, LOCATION_TABLE[full_loc_name])
                if full_loc_name in self.nonprogress_locations:
                    location.progress_type = LocationProgressType.EXCLUDED
                region.locations.append(location)
            self.multiworld.regions.append(region)

        self.connected_regions = set()
        self.connected_entrances = set()

        self.connect_regions(self.origin_region_name)

        # These are checks to make sure all locations were made
        # Batreaux rewards are handled differently, so skip those

        for loc in LOCATION_TABLE.keys():
            if LOCATION_TABLE[loc].region == "Batreaux's House":
                continue
            assert self.get_location(loc), f"Location found in location table, but not in requirements: {loc}"

        for loc in self.multiworld.get_locations(self.player):
            if loc.parent_region.name == "Batreaux's House":
                continue
            assert LOCATION_TABLE[loc.name], f"Location found in requirements, but not in location table: {loc}"

    def connect_regions(self, region_name) -> None:
        """
        This function connects all regions starting from the origin region and going out.
        This function is to be called **once** outside of this function, with the region_name
        parameter as the origin region. This is a recursive function that will automatically
        connect all regions outside of the origin region.

        :param region_name: The region to connect.
        """
        appended_regions = []

        if region_name not in self.connected_regions:
            for exit_short_name, rule in ALL_REQUIREMENTS[region_name]["exits"].items():
                exit_full_name = f"{region_name} - {exit_short_name}"
                if exit_full_name in self.connected_entrances:
                    continue
                entrance = [ent for ent in AP_ENTRANCE_TABLE if ent.exit_name == exit_full_name].pop()
                entrance_region = entrance.entrance_region
                entrance_full_name = entrance.entrance_name
                region = self.get_region(region_name)

                if entrance.group == 10:
                    if exit_full_name == "Sky - Emerald Pillar":
                        prov = "Faron Province"
                    elif exit_full_name == "Sky - Ruby Pillar":
                        prov = "Eldin Province"
                    elif exit_full_name == "Sky - Amber Pillar":
                        prov = "Lanayru Province"
                    statue = self.entrances.starting_statues[prov][1]
                    entrance_region = statue["apregion"]
                    entrance_full_name = None

                if entrance.group == 2:
                    dungeon_entrance = exit_short_name.lower().replace(" ", "_")
                    dungeon = [dun for dun, conn in self.entrances.dungeon_connections.items() if conn == dungeon_entrance].pop()
                    entrance_region = DUNGEON_INITIAL_REGIONS[dungeon]
                    entrance_full_name = None

                if entrance.group == 4 or entrance.group == 6:
                    dungeon = ALL_REQUIREMENTS[region_name]["hint_region"]
                    dungeon_entrance = self.entrances.dungeon_connections[dungeon]
                    entrance_region = DUNGEON_ENTRANCE_REGIONS[dungeon_entrance]
                    entrance_full_name = None

                if entrance.group == 3:
                    if region_name.endswith(" Silent Realm"):
                        # exiting silent realm
                        trial = region_name
                        trial_gate = self.entrances.trial_connections[trial]
                        entrance_region = TRIAL_GATE_REGIONS[trial_gate]
                        entrance_full_name = f"{entrance_region} - {trial_gate}"
                    else:
                        # entering silent realm
                        trial_gate = exit_short_name.lower().replace(" ", "_")
                        trial = [trl for trl, conn in self.entrances.trial_connections.items() if conn == trial_gate].pop()
                        entrance_region = trial
                        entrance_full_name = f"{trial} - Trial Gate"

                # Add exits- with logic if overworld or req dungeon, no logic if unreq dungeon
                if (
                    (
                        ALL_REQUIREMENTS[region_name]["hint_region"] in self.dungeons.banned_dungeons
                        or ALL_REQUIREMENTS[entrance_region]["hint_region"] in self.dungeons.banned_dungeons
                        or (
                            (
                                ALL_REQUIREMENTS[region_name]["hint_region"] == "Sky Keep"
                                or ALL_REQUIREMENTS[entrance_region]["hint_region"] == "Sky Keep"
                            )
                            and not self.dungeons.sky_keep_required
                        )
                    )
                    and self.options.empty_unrequired_dungeons
                ):
                    region.add_exits(
                        {entrance_region: exit_full_name},
                        {entrance_region: lambda state: True}
                    )
                else:
                    region.add_exits(
                        {entrance_region: exit_full_name},
                        {entrance_region: eval(f"lambda state, player=self.player: {parse_expression(rule)}")}
                    )

                # if entrance_full_name is None:
                #     # One way entrance
                #     self.connected_entrances.add(exit_full_name)
                # else:
                #     # Two way entrance
                #     self.connected_entrances.update({exit_full_name, entrance_full_name})

                # Treat all exits as one way now

                self.connected_entrances.add(exit_full_name)
                appended_regions.append(entrance_region)

            self.connected_regions.add(region_name)

            for reg in deepcopy(appended_regions):
                if reg in self.connected_regions:
                    continue
                self.connect_regions(reg)

    def create_item(self, name: str) -> SSItem:
        """
        Create an item for the Skyward Sword world for this player.

        :param name: The name of the item.
        :raises KeyError: If an invalid item name is provided.
        """

        if name in ITEM_TABLE:
            return SSItem(
                name, self.player, ITEM_TABLE[name], item_classification(self, name)
            )
        raise KeyError(f"Invalid item name: {name}")
    
 #   def post_fill(self):


    def region_to_hint_region(self, region: Region) -> str:
        """
        Returns the hint region for a region object.

        :param region: The region object.
        :return: A string of the hint region.
        """

        return ALL_REQUIREMENTS[region.name]["hint_region"]

    def generate_output(self, output_directory: str) -> None:
        """
        Create the output .apssr file that is used to randomize the ISO.

        :param output_directory: The output directory for the .apssr file.
        """
                # Fill hint data
        self.hints = Hints(self)
        self.hints.handle_hints()

        # spheres = self.multiworld.get_spheres()
        # locs = {}
        # for i, sphere in enumerate(spheres):
        #     locs[i] = sorted([(loc.name, loc.item.name) for loc in sphere], key=lambda loc: loc[0])
        # with open("./worlds/ss/Playthrough.json", "w") as f:
        #     json.dump(locs, f, indent=2)
        
        multiworld = self.multiworld
        player = self.player
        player_hash = self.random.sample(HASH_NAMES, 3)
        mw_player_names = [
            self.multiworld.get_player_name(i + 1)
            for i in range(self.multiworld.players)
        ]

        # seed_name on web adds an additional 'W', making the seed 21 characters long.
        if 'W' in multiworld.seed_name:
            ap_seed = multiworld.seed_name[1:]
        else:
            ap_seed = multiworld.seed_name

        # Output seed name and slot number to seed RNG in randomizer client.
        output_data = {
            "AP Version": list(AP_VERSION),
            "World Version": list(WORLD_VERSION),
            "Hash": f"AP P{player} " + " ".join(player_hash),
            "AP Seed": ap_seed,
            "Rando Seed": self.random.randint(
                0, 2**32 - 1
            ),
            "Slot": player,
            "Name": self.player_name,
            "All Players": mw_player_names,
            "Options": {},
            "Excluded Locations": set(),
            "Starting Items": self.starting_items,
            "Required Dungeons": self.dungeons.required_dungeons,
            "Locations": {},
            "Batreaux Rewards": self.batreaux_rewards,
            "Hints": self.hints.placed_hints,
            "Log Hints": self.hints.placed_hints_log,
            "SoT Location": self.hints.handle_impa_sot_hint(),
            "Dungeon Entrances": {},
            "Trial Entrances": {},
            "Starting Statues": self.entrances.starting_statues,
            "Starting Entrance": self.entrances.starting_entrance,
        }

        # Output options to file.
        for field in fields(self.options):
            if field.name =="plando_items":
                continue # Skip adding plando_items to patchfile 
            output_data["Options"][field.name.replace("_", "-")] = getattr(
                self.options, field.name
            ).value

        # Excluded locations, and account for batreaux checks
        for loc in self.nonprogress_locations:
            if self.get_location(loc).ogname:
                output_data["Excluded Locations"].add(self.get_location(loc).ogname)
            else:
                output_data["Excluded Locations"].add(loc)

        # Unused options in AP must be filled for the patcher
        output_data["Options"]["limit-start-entrance"] = 0
        output_data["Options"]["cube-sots"] = 0
        output_data["Options"]["precise-item"] = 1

        # Output which item has been placed at each location.
        locations = sorted(
            multiworld.get_locations(player),
            key=lambda loc: loc.code if loc.code is not None else 10000,
        )
        for location in locations:
            if location.name != "Hylia's Realm - Defeat Demise":
                if location.item:
                    item_info = {
                        "player": location.item.player,
                        "name": location.item.name,
                        "game": location.item.game,
                        "classification": SSWorld._get_classification_name(location.item.classification),
                    }
                else:
                    print(
                        f"No item in location: {location.name}. Defaulting to red rupee."
                    )
                    item_info = {
                        "player": location.item.player,
                        "name": "Red Rupee",
                        "game": "Skyward Sword",
                        "classification": "filler",
                    }
                if location.ogname:
                    output_data["Locations"][location.ogname] = item_info
                else:
                    output_data["Locations"][location.name] = item_info

        # Fix entrances
        dunconn = {}
        trlconn = {}
        for dun, ent in self.entrances.dungeon_connections.items():
            rando_friendly_entrance_name_list = []
            for w in ent.split("_"):
                if w not in ["in", "on"]:
                    w = w[0].upper() + w[1:]
                rando_friendly_entrance_name_list.append(w)
            rando_friendly_entrance_name = " ".join(rando_friendly_entrance_name_list)
            dunconn[rando_friendly_entrance_name] = dun
        for dun in sorted(dunconn.keys(), key=lambda i: DUNGEON_ENTRANCE_LIST.index(i)):
            output_data["Dungeon Entrances"][dun] = dunconn[dun]
        for trl, gate in self.entrances.trial_connections.items():
            rando_friendly_gate_name_list = []
            for w in gate.split("_"):
                if w not in ["in", "on"]:
                    w = w[0].upper() + w[1:]
                rando_friendly_gate_name_list.append(w)
            rando_friendly_gate_name = " ".join(rando_friendly_gate_name_list)
            trlconn[rando_friendly_gate_name] = trl
        for trl in sorted(trlconn.keys(), key=lambda i: TRIAL_GATE_LIST.index(i)):
            output_data["Trial Entrances"][trl] = trlconn[trl]

        # Output the plando details to file.
        apssr = SSContainer(
            path=os.path.join(
                output_directory, f"{multiworld.get_out_file_name_base(player)}{SSContainer.patch_file_ending}"
            ),
            player=player,
            player_name=self.player_name,
            data=output_data,
        )
        apssr.write()

    def fill_slot_data(self) -> Mapping[str, Any]:
        """
        Return the `slot_data` field that will be in the `Connected` network package.

        This is a way the generator can give custom data to the client.
        The client will receive this as JSON in the `Connected` response.

        :return: A dictionary to be sent to the client when it connects to the server.
        """
        slot_data = {
            "required_dungeon_count": self.options.required_dungeon_count.value,
            "triforce_required": self.options.triforce_required.value,
            "triforce_shuffle": self.options.triforce_shuffle.value,
            "got_sword_requirement": self.options.got_sword_requirement.value,
            "got_dungeon_requirement": self.options.got_dungeon_requirement.value,
            "imp2_skip": self.options.imp2_skip.value,
            "skip_horde": self.options.skip_horde.value,
            "skip_g3": self.options.skip_g3.value,
            "skip_demise": self.options.skip_demise.value,
            "got_start": self.options.got_start.value,
            "open_thunderhead": self.options.open_thunderhead.value,
            "open_et": self.options.open_et.value,
            "open_lmf": self.options.open_lmf.value,
            "open_lake_floria": self.options.open_lake_floria.value,
            "empty_unrequired_dungeons": self.options.empty_unrequired_dungeons.value,
            "map_mode": self.options.map_mode.value,
            "small_key_mode": self.options.small_key_mode.value,
            "boss_key_mode": self.options.boss_key_mode.value,
            "fs_lava_flow": self.options.fs_lava_flow.value,
            "shuffle_trial_objects": self.options.shuffle_trial_objects.value,
            "treasuresanity_in_silent_realms": self.options.treasuresanity_in_silent_realms.value,
            "trial_treasure_amount": self.options.trial_treasure_amount.value,
            "randomize_entrances": self.options.randomize_entrances.value,
            "randomize_trials": self.options.randomize_trials.value,
            "random_start_entrance": self.options.random_start_entrance.value,
            "limit_start_entrance": 0, # self.options.limit_start_entrance.value,
            "random_start_statues": self.options.random_start_statues.value,
            "shopsanity": self.options.shopsanity.value,
            "rupoor_mode": self.options.rupoor_mode.value,
            "rupeesanity": self.options.rupeesanity.value,
            "tadtonesanity": self.options.tadtonesanity.value,
            "gondo_upgrades": self.options.gondo_upgrades.value,
            "sword_dungeon_reward": self.options.sword_dungeon_reward.value,
            "batreaux_counts": self.options.batreaux_counts.value,
            "randomize_boss_key_puzzles": self.options.randomize_boss_key_puzzles.value,
            "random_puzzles": self.options.random_puzzles.value,
            "peatrice_conversations": self.options.peatrice_conversations.value,
            "demise_count": self.options.demise_count.value,
            "dowsing_after_whitesword": self.options.dowsing_after_whitesword.value,
            "full_wallet_upgrades": self.options.full_wallet_upgrades.value,
            "ammo_availability": self.options.ammo_availability.value,
            "upgraded_skyward_strike": self.options.upgraded_skyward_strike.value,
            "fast_air_meter": self.options.fast_air_meter.value,
            "enable_heart_drops": self.options.enable_heart_drops.value,
            "damage_multiplier": self.options.damage_multiplier.value,
            "starting_sword": self.options.starting_sword.value,
            "starting_tablet_count": self.options.starting_tablet_count.value,
            "starting_crystal_packs": self.options.starting_crystal_packs.value,
            "starting_bottles": self.options.starting_bottles.value,
            "starting_heart_containers": self.options.starting_heart_containers.value,
            "starting_heart_pieces": self.options.starting_heart_pieces.value,
            "starting_tadtones": self.options.starting_tadtones.value,
            "random_starting_item": self.options.random_starting_item.value,
            "start_with_hylian_shield": self.options.start_with_hylian_shield.value,
            "full_starting_wallet": self.options.full_starting_wallet.value,
            "max_starting_bugs": self.options.max_starting_bugs.value,
            "max_starting_treasures": self.options.max_starting_treasures.value,
            "ap_hint_distribution": self.options.hint_distribution.value,
            "song_hints": self.options.song_hints.value,
            "chest_dowsing": self.options.chest_dowsing.value,
            "dungeon_dowsing": self.options.dungeon_dowsing.value,
            "impa_sot_hint": self.options.impa_sot_hint.value,
            "cube_sots": 0, #self.options.cube_sots.value,
            "precise_item": 1, #self.options.precise_item.value,
            "starting_items": self.options.starting_items.value,
            "death_link": self.options.death_link.value,
            "locations_for_hint": getattr(getattr(self, "hints", None), "locations_for_hint", []),
            "excluded_locations": self.nonprogress_locations,
            "required_dungeons": self.dungeons.required_dungeons,
        }

        return slot_data

