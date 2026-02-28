"""File specifically used for the cases of archipelago generation."""

import os
import typing
import math
import threading
import time
import json
import zipfile
import codecs
from io import BytesIO
import pkgutil
import shutil
import sys
import tempfile
from typing import Any, TypedDict

baseclasses_loaded = False
try:
    # DO NOT DO IMPORTS FOR AP BEFORE THIS OR IN THIS BLOCK
    # THIS BLOCK JUST DETERMINES IF AP IS INSTALLED
    import BaseClasses

    baseclasses_loaded = True
except ImportError:
    pass
if baseclasses_loaded:

    def display_error_box(title: str, text: str) -> bool | None:
        """Display an error message box."""
        from tkinter import Tk, messagebox

        root = Tk()
        root.withdraw()
        ret = messagebox.showerror(title, text)
        root.update()

    def copy_dependencies(zip_path, file):
        """Copy a ZIP file from the package to a temporary directory, extracts its contents.

        Ensures the temporary directory exists.
        Args:
            zip_path (str): The relative path to the ZIP file within the package.
        Behavior:
            - Creates a temporary directory if it does not exist.
            - Reads the ZIP file from the package using `pkgutil.get_data`.
            - Writes the ZIP file to the temporary directory if it does not already exist.
            - Extracts the contents of the ZIP file into the temporary directory.
        Prints:
            - A message if the ZIP file could not be read.
            - A message when the ZIP file is successfully copied.
            - A message when the ZIP file is successfully extracted.
        """
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        zip_dest = os.path.join(temp_dir, file)
        try:
            # Load the ZIP file from the package
            zip_data = pkgutil.get_data(__name__, zip_path)
            # Check if the zip already exists in the destination
            if not os.path.exists(zip_dest):
                if zip_data is None:
                    print(f"Failed to read {zip_path}")
                else:
                    # Write the ZIP file to the destination
                    with open(zip_dest, "wb") as f:
                        f.write(zip_data)
                    print(f"Copied {zip_path} to {zip_dest}")

                    # Extract the ZIP file
                    with zipfile.ZipFile(zip_dest, "r") as zip_ref:
                        zip_ref.extractall(temp_dir)
                    print(f"Extracted {zip_dest} into {temp_dir}")

        except PermissionError:
            display_error_box("Permission Error", "Unable to install Dependencies to AP, please try to install AP as an admin.")
            raise PermissionError("Permission Error: Unable to install Dependencies to AP, please try to install AP as an admin.")

        # Add the temporary directory to sys.path
        if temp_dir not in sys.path:
            sys.path.insert(0, temp_dir)

    platform_type = sys.platform
    python_version = f"{sys.version_info.major}{sys.version_info.minor}"
    baseclasses_path = os.path.dirname(os.path.dirname(BaseClasses.__file__))
    if not baseclasses_path.endswith("lib"):
        baseclasses_path = os.path.join(baseclasses_path, "lib")
    # Remove ANY PIL folders from the baseclasses_path
    # Or Pyxdelta or pillow folders
    try:
        for folder in os.listdir(baseclasses_path):
            if folder.startswith("PIL") or folder.startswith("pyxdelta") or folder.startswith("pillow"):
                folder_path = os.path.join(baseclasses_path, folder)
                if os.path.isdir(folder_path):
                    shutil.rmtree(folder_path)
                elif os.path.isfile(folder_path):
                    os.remove(folder_path)
            # Also if its windows.zip or linux.zip, remove it
            if folder.startswith("windows.zip") or folder.startswith("linux.zip"):
                os.remove(os.path.join(baseclasses_path, folder))
    except Exception as e:
        pass

    if platform_type == "win32":
        zip_path = "vendor/windows.zip"  # Path inside the package
        copy_dependencies(zip_path, "windows.zip")
    elif platform_type == "linux":
        # Try version-specific zip first, fall back to generic
        version_zip = f"vendor/linux_{python_version}.zip"
        generic_zip = "vendor/linux.zip"
        try:
            copy_dependencies(version_zip, f"linux_{python_version}.zip")
        except (FileNotFoundError, KeyError):
            try:
                copy_dependencies(generic_zip, "linux.zip")
            except (FileNotFoundError, KeyError):
                raise Exception(f"Could not find vendor dependencies for Linux Python {python_version}")
    else:
        raise Exception(f"Unsupported platform: {platform_type}")

    # Add paths for APWorld context - use __file__ to get the correct base path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    sys.path.append("worlds/dk64/")
    sys.path.append("worlds/dk64/archipelago/")
    sys.path.append("custom_worlds/dk64.apworld/dk64/")
    sys.path.append("custom_worlds/dk64.apworld/dk64/archipelago/")
    from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification, CollectionState
    from BaseClasses import Location, LocationProgressType
    from entrance_rando import randomize_entrances, EntranceRandomizationError, disconnect_entrance_for_randomization
    import settings
    import logging

    import randomizer.ItemPool as DK64RItemPool

    from randomizer.Enums.Items import Items as DK64RItems
    from archipelago.Goals import GOAL_MAPPING, QUANTITY_GOALS, calculate_quantity, pp_wincon
    from archipelago.Items import DK64Item, full_item_table, setup_items
    from archipelago.Options import DK64Options, Goal, SwitchSanity, SelectStartingKong, dk64_option_groups, LoadingZoneRando
    from archipelago.Regions import all_locations, create_regions, connect_regions, connect_exit_level_and_deathwarp, connect_glitch_transitions
    from archipelago.Rules import set_rules
    from archipelago.client.common import check_version
    from worlds.AutoWorld import WebWorld, World, AutoLogicRegister
    from worlds.Files import APPlayerContainer
    from archipelago.Logic import LogicVarHolder, logic_item_name_to_id
    from randomizer.Spoiler import Spoiler
    from randomizer.Settings import Settings
    from randomizer.ShuffleWarps import LinkWarps
    from randomizer.Patching.ApplyRandomizer import patching_response
    from version import version
    from randomizer.Patching.EnemyRando import randomize_enemies_0
    from randomizer.Fill import ShuffleItems, Generate_Spoiler, IdentifyMajorItems
    from randomizer.CompileHints import compileMicrohints
    from archipelago.Hints import CompileArchipelagoHints
    from randomizer.Enums.Types import Types, BarrierItems
    from randomizer.Enums.Enemies import Enemies
    from randomizer.Enums.Kongs import Kongs
    from randomizer.Enums.Levels import Levels
    from randomizer.Enums.Maps import Maps
    from randomizer.Enums.Minigames import Minigames
    from randomizer.Enums.Locations import Locations as DK64RLocations
    from randomizer.Enums.Settings import (
        Enemies,
        GlitchesSelected,
        Items,
        LevelRandomization,
        Kongs,
        MicrohintsEnabled,
        ShuffleLoadingZones,
        TricksSelected,
        SlamRequirement,
    )
    from randomizer.Enums.Switches import Switches
    from randomizer.Enums.SwitchTypes import SwitchType
    from randomizer.Enums.EnemySubtypes import EnemySubtype
    from randomizer.Lists import Item as DK64RItem
    from randomizer.Lists.Location import ShopLocationReference
    from randomizer.Lists.ShufflableExit import ShufflableExits
    from randomizer.Lists.Switches import SwitchInfo
    from randomizer.Lists.EnemyTypes import EnemyLoc, EnemyMetaData
    from worlds.LauncherComponents import Component, SuffixIdentifier, components, Type, icon_paths
    import randomizer.ShuffleExits as ShuffleExits
    from archipelago.FillSettings import fillsettings
    from archipelago.Prices import generate_prices
    from Utils import open_filename
    import shutil
    import zlib

    boss_map_names = {
        Maps.JapesBoss: "Army Dillo 1",
        Maps.AztecBoss: "Dogadon 1",
        Maps.FactoryBoss: "Mad Jack",
        Maps.GalleonBoss: "Pufftoss",
        Maps.FungiBoss: "Dogadon 2",
        Maps.CavesBoss: "Army Dillo 2",
        Maps.CastleBoss: "King Kut Out",
        Maps.KroolDonkeyPhase: "DK Phase",
        Maps.KroolDiddyPhase: "Diddy Phase",
        Maps.KroolLankyPhase: "Lanky Phase",
        Maps.KroolTinyPhase: "Tiny Phase",
        Maps.KroolChunkyPhase: "Chunky Phase",
    }

    def crc32_of_file(file_path):
        """Compute CRC32 checksum of a file."""
        crc_value = 0
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                crc_value = zlib.crc32(chunk, crc_value)
        return f"{crc_value & 0xFFFFFFFF:08X}"  # Convert to 8-character hex

    def launch_client():
        """Launch the DK64 client."""
        from archipelago.DK64Client import launch
        from worlds.LauncherComponents import launch as launch_component

        launch_component(launch, name="DK64 Client")

    components.append(Component("DK64 Client", func=launch_client, component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".chunky"), icon="dk64"))
    icon_paths["dk64"] = f"ap:{__name__}/base-hack/assets/DKTV/logo3.png"

    class DK64Container(APPlayerContainer):
        """This class defines the container file for DK64."""

        game: str = "Donkey Kong 64"
        patch_file_ending: str = ".chunky"

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Initialize the DK64 container."""
            if "data" in kwargs:
                self.data = kwargs["data"]
                del kwargs["data"]

            super().__init__(*args, **kwargs)

        def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
            """Write the contents of the container file."""
            super().write_contents(opened_zipfile)

            # Write the patch data for the game
            if "patch_data" in self.data:
                opened_zipfile.writestr("patch_data", self.data["patch_data"])

    class DK64CollectionState(metaclass=AutoLogicRegister):
        """Logic Mixin to handle some awkward situations when the CollectionState is copied."""

        def init_mixin(self, parent: MultiWorld):
            """Reset the logic holder in all DK64 worlds. This is called on every CollectionState init."""
            dk64_ids = parent.get_game_players(DK64World.game) + parent.get_game_groups(DK64World.game)
            self.dk64_logic_holder = {}
            for player in dk64_ids:
                if hasattr(parent.worlds[player], "spoiler"):
                    self.dk64_logic_holder[player] = LogicVarHolder(parent.worlds[player].spoiler, player)  # If we don't reset here, we double-collect the starting inventory

        def copy_mixin(self, ret) -> CollectionState:
            """Update the current logic holder in all DK64 worlds with the current CollectionState. This is called after the CollectionState init inside the copy() method, so this essentially undoes the above method."""
            dk64_ids = ret.multiworld.get_game_players(DK64World.game) + ret.multiworld.get_game_groups(DK64World.game)
            for player in dk64_ids:
                if player in ret.dk64_logic_holder.keys():
                    ret.dk64_logic_holder[player].UpdateFromArchipelagoItems(ret)  # If we don't update here, every copy wipes the logic holder's knowledge
                else:
                    if hasattr(ret.multiworld.worlds[player], "spoiler"):
                        print("Hey")
            return ret

    class DK64Settings(settings.Group):
        """Settings for the DK64 randomizer."""

        class ReleaseVersion(str):
            """Choose the release version of the DK64 randomizer to use.

            By setting it to master (Default) you will always pull the latest stable version.
            By setting it to dev you will pull the latest development version.
            If you want a specific version, you can set it to a AP version number eg: v1.0.45
            """

        class EnableMinimalLogic(settings.Bool):
            """Enable minimal logic for DK64.

            If disabled, any player YAML with minimal logic enabled will be forced to use glitchless logic instead.
            This allows hosts to disable the minimal logic option if they don't want it on their server.
            """

        release_branch: ReleaseVersion = ReleaseVersion("master")
        enable_minimal_logic_dk64: EnableMinimalLogic | bool = False

    class DK64Web(WebWorld):
        """WebWorld for DK64."""

        theme = "jungle"

        setup_en = Tutorial("Multiworld Setup Guide", "A guide to setting up the Donkey Kong 64 randomizer connected to an Archipelago Multiworld.", "English", "setup_en.md", "setup/en", ["PoryGone"])

        tutorials = [setup_en]
        option_groups = dk64_option_groups

    class LZRSeedGroup(TypedDict):
        """Type definition for Loading Zone Randomizer seed groups."""

        shuffle_helm_level_order: bool  # whether helm level order is shuffled
        enable_chaos_blockers: bool  # whether chaos blockers are enabled (disabled if any player has it off)
        randomize_blocker_required_amounts: bool  # whether to randomize B. Lockers
        blocker_max: int  # maximum B. Locker value
        maximize_helm_blocker: bool  # whether to maximize Helm B. Locker (enabled if any player has it on)
        level_blockers: typing.Dict[str, int]  # manual B. Locker values (if not randomized)
        generated_blockers: typing.Optional[typing.List[int]]  # actual blocker values after generation (shared across group)
        logic_type: int  # logic type: 1=glitchless, 0=advanced_glitchless, 2=glitched
        tricks_selected: typing.Set[str]  # intersection of tricks enabled by all players
        glitches_selected: typing.Set[str]  # intersection of glitches enabled by all players

    class DK64World(World):
        """Donkey Kong 64 is a 3D collectathon platforming game.

        Play as the whole DK Crew and rescue the Golden Banana hoard from King K. Rool.
        """

        game: str = "Donkey Kong 64"
        options_dataclass = DK64Options
        options: DK64Options
        topology_present = False
        settings: typing.ClassVar[DK64Settings]
        seed_groups: typing.ClassVar[dict[str, LZRSeedGroup]] = {}

        item_name_to_id = {name: data.code for name, data in full_item_table.items()}
        location_name_to_id = all_locations

        def blueprint_item_group() -> str:
            """Item group for blueprints."""
            res = set()
            for name, _ in full_item_table.items():
                if "Blueprint" in name:
                    res.add(name)
            return res

        def gun_item_group() -> str:
            """Item group for guns."""
            res = set()
            gun_items = ["Coconut", "Peanut", "Grape", "Feather", "Pineapple"]
            for item in gun_items:
                if item in full_item_table:
                    res.add(item)
            return res

        def inst_item_group() -> str:
            """Item group for instruments."""
            res = set()
            inst_items = ["Bongos", "Guitar", "Trombone", "Saxophone", "Triangle"]
            for item in inst_items:
                if item in full_item_table:
                    res.add(item)
            return res

        def shared_item_group() -> str:
            """Item group for Training Moves."""
            res = set()
            training_items = ["Vines", "Diving", "Oranges", "Barrels", "Climbing", "progression Slam", "Fairy Camera", "Shockwave"]
            for item in training_items:
                if item in full_item_table:
                    res.add(item)
            return res

        def barrels_item_group() -> str:
            """Item group for Barrels."""
            res = set()
            barrels_items = ["Strong Kong", "Rocketbarrel Boost", "Orangstand Sprint", "Mini Monkey", "Hunky Chunky"]
            for item in barrels_items:
                if item in full_item_table:
                    res.add(item)
            return res

        def active_item_group() -> str:
            """Item group for Active Moves."""
            res = set()
            active_items = ["Gorilla Grab", "Chimpy Charge", "Pony Tail Twirl", "Orangstand", "Primate Punch"]
            for item in active_items:
                if item in full_item_table:
                    res.add(item)
            return res

        def pad_item_group() -> str:
            """Item group for Pads."""
            res = set()
            pad_items = ["Baboon Blast", "Simian Spring", "Baboon Balloon", "Monkeyport", "Gorilla Gone"]
            for item in pad_items:
                if item in full_item_table:
                    res.add(item)
            return res

        def dk_item_group() -> str:
            """Item group for DK Moves."""
            res = set()
            dk_items = ["Coconut", "Bongos", "Gorilla Grab", "Strong Kong", "Baboon Blast"]
            for item in dk_items:
                if item in full_item_table:
                    res.add(item)
            return res

        def diddy_item_group() -> str:
            """Item group for Diddy Moves."""
            res = set()
            diddy_items = ["Peanut", "Guitar", "Chimpy Charge", "Rocketbarrel Boost", "Simian Spring"]
            for item in diddy_items:
                if item in full_item_table:
                    res.add(item)
            return res

        def lanky_item_group() -> str:
            """Item group for Lanky Moves."""
            res = set()
            lanky_items = ["Grape", "Trombone", "Orangstand", "Orangstand Spring", "Baboon Balloon"]
            for item in lanky_items:
                if item in full_item_table:
                    res.add(item)
            return res

        def tiny_item_group() -> str:
            """Item group for Tiny Moves."""
            res = set()
            tiny_items = ["Feather", "Saxophone", "Pony Tail Twirl", "Mini Monkey", "Monkeyport"]
            for item in tiny_items:
                if item in full_item_table:
                    res.add(item)
            return res

        def chunky_item_group() -> str:
            """Item group for Chunky Moves."""
            res = set()
            chunky_items = ["Pineapple", "Triangle", "Primate Punch", "Hunky Chunky", "Triangle"]
            for item in chunky_items:
                if item in full_item_table:
                    res.add(item)
            return res

        def key_item_group() -> str:
            """Item group for Keys."""
            res = set()
            key_items = ["Key 1", "Key 2", "Key 3", "Key 4", "Key 5", "Key 6", "Key 7", "Key 8"]
            for item in key_items:
                if item in full_item_table:
                    res.add(item)
            return res

        def kong_item_group() -> str:
            """Item group for Kongs."""
            res = set()
            kong_items = ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"]
            for item in kong_items:
                if item in full_item_table:
                    res.add(item)
            return res

        def company_coin_item_group() -> str:
            """Item group for Company Coins."""
            res = set()
            coin_items = ["Nintendo Coin", "Rareware Coin"]
            for item in coin_items:
                if item in full_item_table:
                    res.add(item)
            return res

        def dk_name() -> str:
            """Add Kong to end of Kongs."""
            res = set()
            if "Donkey" in full_item_table:
                res.add("Donkey")
            return res

        def diddy_name() -> str:
            """Add Kong to end of Kongs."""
            res = set()
            if "Diddy" in full_item_table:
                res.add("Diddy")
            return res

        def lanky_name() -> str:
            """Add Kong to end of Kongs."""
            res = set()
            if "Lanky" in full_item_table:
                res.add("Lanky")
            return res

        def tiny_name() -> str:
            """Add Kong to end of Kongs."""
            res = set()
            if "Tiny" in full_item_table:
                res.add("Tiny")
            return res

        def chunky_name() -> str:
            """Add Kong to end of Kongs."""
            res = set()
            if "Chunky" in full_item_table:
                res.add("Chunky")
            return res

        def isles_locations() -> str:
            """Location group for Isles locations."""
            res = set()
            for location_name in all_locations.keys():
                if location_name.startswith("Isles"):
                    res.add(location_name)
            # Add specific Banana Fairy related locations
            if "The Banana Fairy's Gift" in all_locations:
                res.add("The Banana Fairy's Gift")
            if "Returning the Banana Fairies" in all_locations:
                res.add("Returning the Banana Fairies")
            return res

        def japes_locations() -> str:
            """Location group for Japes locations."""
            res = set()
            for location_name in all_locations.keys():
                if location_name.startswith("Japes"):
                    res.add(location_name)
            return res

        def aztec_locations() -> str:
            """Location group for Aztec locations."""
            res = set()
            for location_name in all_locations.keys():
                if location_name.startswith("Aztec"):
                    res.add(location_name)
            return res

        def factory_locations() -> str:
            """Location group for Factory locations."""
            res = set()
            for location_name in all_locations.keys():
                if location_name.startswith("Factory") or location_name.startswith("DK Arcade"):
                    res.add(location_name)
            return res

        def galleon_locations() -> str:
            """Location group for Galleon locations."""
            res = set()
            for location_name in all_locations.keys():
                if location_name.startswith("Galleon") or location_name.startswith("Treasure Chest"):
                    res.add(location_name)
            return res

        def forest_locations() -> str:
            """Location group for Forest locations."""
            res = set()
            for location_name in all_locations.keys():
                if location_name.startswith("Forest"):
                    res.add(location_name)
            return res

        def caves_locations() -> str:
            """Location group for Caves locations."""
            res = set()
            for location_name in all_locations.keys():
                if location_name.startswith("Caves"):
                    res.add(location_name)
            return res

        def castle_locations() -> str:
            """Location group for Castle locations."""
            res = set()
            for location_name in all_locations.keys():
                if location_name.startswith("Castle"):
                    res.add(location_name)
            return res

        def helm_locations() -> str:
            """Location group for Helm locations."""
            res = set()
            # Locations to exclude from Helm group
            excluded_locations = {
                "Helm Donkey Barrel 1",
                "Helm Donkey Barrel 2",
                "Helm Diddy Barrel 1",
                "Helm Diddy Barrel 2",
                "Helm Lanky Barrel 1",
                "Helm Lanky Barrel 2",
                "Helm Tiny Barrel 1",
                "Helm Tiny Barrel 2",
                "Helm Chunky Barrel 1",
                "Helm Chunky Barrel 2",
            }
            for location_name in all_locations.keys():
                if location_name.startswith("Helm") and location_name not in excluded_locations:
                    res.add(location_name)
                if location_name == "The End of Helm":
                    res.add(location_name)
            return res

        def medal_locations() -> str:
            """Location group for Medal locations."""
            res = set()
            for location_name in all_locations.keys():
                if "Medal" in location_name:
                    res.add(location_name)
            return res

        def boss_locations() -> str:
            """Location group for Boss locations."""
            res = set()
            for location_name in all_locations.keys():
                if "Boss Defeated" in location_name:
                    res.add(location_name)
            return res

        item_name_groups = {
            "Blueprints": blueprint_item_group(),
            "Guns": gun_item_group(),
            "Instruments": inst_item_group(),
            "Shared Moves": shared_item_group(),
            "Transformation Barrels": barrels_item_group(),
            "Active Moves": active_item_group(),
            "Pad Moves": pad_item_group(),
            "DK Moves": dk_item_group(),
            "Diddy Moves": diddy_item_group(),
            "Lanky Moves": lanky_item_group(),
            "Tiny Moves": tiny_item_group(),
            "Chunky Moves": chunky_item_group(),
            "Donkey Kong": dk_name(),
            "Diddy Kong": diddy_name(),
            "Lanky Kong": lanky_name(),
            "Tiny Kong": tiny_name(),
            "Chunky Kong": chunky_name(),
            "Keys": key_item_group(),
            "Kongs": kong_item_group(),
            "Company Coins": company_coin_item_group(),
        }

        location_name_groups = {
            "DK Isles": isles_locations(),
            "Jungle Japes": japes_locations(),
            "Angry Aztec": aztec_locations(),
            "Frantic Factory": factory_locations(),
            "Gloomy Galleon": galleon_locations(),
            "Fungi Forest": forest_locations(),
            "Crystal Caves": caves_locations(),
            "Creepy Castle": castle_locations(),
            "Hideout Helm": helm_locations(),
            "Banana Medals": medal_locations(),
            "Bosses": boss_locations(),
        }

        # with open("donklocations.txt", "w") as f:
        #     print(location_name_to_id, file=f)

        # with open("donkitems.txt", "w") as f:
        #     print(item_name_to_id, file=f)

        web = DK64Web()

        def __init__(self, multiworld: MultiWorld, player: int):
            """Initialize the DK64 world."""
            self.rom_name_available_event = threading.Event()
            self.hint_data_available = threading.Event()
            self.hint_compilation_complete = threading.Event()
            super().__init__(multiworld, player)
            self.ap_version = json.loads(pkgutil.get_data(__name__, "archipelago.json").decode("utf-8"))["world_version"]
            self.entrance_connections: dict[str, str] = {}

        @classmethod
        def stage_assert_generate(cls, multiworld: MultiWorld):
            """Assert the stage and generate the world."""
            # Check if dk64.z64 exists, if it doesn't prompt the user to provide it
            # ANd then we will copy it to the root directory
            crc_values = ["D44B4FC6"]
            rom_file = "dk64.z64"
            if not os.path.exists(rom_file):
                print("Please provide a DK64 ROM file.")
                file = open_filename("Select DK64 ROM", (("N64 ROM", (".z64", ".n64")),))
                if not file:
                    raise FileNotFoundError("No ROM file selected.")
                crc = crc32_of_file(file)
                print(f"CRC32: {crc}")
                if crc not in crc_values:
                    print("Invalid DK64 ROM file, please make sure your ROM is big endian.")
                    raise FileNotFoundError("Invalid DK64 ROM file, please make sure your ROM is a vanilla DK64 file in big endian.")
                # Copy the file to the root directory
                try:
                    shutil.copy(file, rom_file)
                except Exception as e:
                    raise FileNotFoundError(f"Failed to copy ROM file, this may be a permissions issue: {e}")
            else:
                crc = crc32_of_file(rom_file)
                print(f"CRC32: {crc}")
                if crc not in crc_values:
                    print("Invalid DK64 ROM file, please make sure your ROM is big endian.")
                    raise FileNotFoundError("Invalid DK64 ROM file, please make sure your ROM is a vanilla DK64 file in big endian.")
            check_version()

        def generate_early(self):
            """Generate the world."""
            # Check host setting for minimal logic and force glitchless if disabled
            if not self.settings.enable_minimal_logic_dk64:
                dk64_worlds_for_minimal_check: tuple[DK64World] = self.multiworld.get_game_worlds("Donkey Kong 64")
                affected_players = []
                for world in dk64_worlds_for_minimal_check:
                    if world.options.logic_type.value == 4:  # 4 = minimal logic
                        affected_players.append(world.player_name)
                        world.options.logic_type.value = 1  # Force to glitchless

                if affected_players:
                    import logging

                    logging.warning(
                        f"DK64: Minimal logic is DISABLED in host.yaml. "
                        f"The following player(s) have tried to sneak Minimal Logic in: {', '.join(affected_players)}. As such, they have been forced to use glitchless logic."
                    )

            # Handle seed group synchronization for custom LZR seed groups
            # We need to process ALL DK64 worlds to build/update seed groups before any player applies settings
            dk64_worlds: tuple[DK64World] = self.multiworld.get_game_worlds("Donkey Kong 64")
            for world in dk64_worlds:
                if world.options.loading_zone_rando.value not in [0, LoadingZoneRando.option_no]:
                    # Only process custom seed group strings, not standard numeric option values
                    if isinstance(world.options.loading_zone_rando.value, str):
                        group = world.options.loading_zone_rando.value
                        # if this is the first world in the group, set the rules equal to its rules
                        if group not in self.seed_groups:
                            helm_value = bool(world.options.shuffle_helm_level_order.value)
                            self.seed_groups[group] = LZRSeedGroup(
                                shuffle_helm_level_order=helm_value,
                                enable_chaos_blockers=bool(world.options.enable_chaos_blockers.value),
                                randomize_blocker_required_amounts=bool(world.options.randomize_blocker_required_amounts.value),
                                blocker_max=int(world.options.blocker_max.value),
                                maximize_helm_blocker=bool(world.options.maximize_level8_blocker.value),
                                level_blockers={
                                    "level_1": int(world.options.level_blockers.value.get("level_1", 0)),
                                    "level_2": int(world.options.level_blockers.value.get("level_2", 0)),
                                    "level_3": int(world.options.level_blockers.value.get("level_3", 0)),
                                    "level_4": int(world.options.level_blockers.value.get("level_4", 0)),
                                    "level_5": int(world.options.level_blockers.value.get("level_5", 0)),
                                    "level_6": int(world.options.level_blockers.value.get("level_6", 0)),
                                    "level_7": int(world.options.level_blockers.value.get("level_7", 0)),
                                    "level_8": int(world.options.level_blockers.value.get("level_8", 64)),
                                },
                                generated_blockers=None,  # will be filled after first player generates
                                logic_type=int(world.options.logic_type.value),
                                tricks_selected=set(world.options.tricks_selected.value),
                                glitches_selected=set(world.options.glitches_selected.value),
                            )
                        else:
                            # Group already exists - update with more permissive/restrictive rules
                            # shuffle_helm_level_order: if any player has it enabled, enable it for the group
                            if world.options.shuffle_helm_level_order.value:
                                self.seed_groups[group]["shuffle_helm_level_order"] = True

                            # chaos_blockers: if any player has it disabled, disable it for the group
                            if not world.options.enable_chaos_blockers.value:
                                self.seed_groups[group]["enable_chaos_blockers"] = False

                            # randomize_blockers: if any player has it disabled, disable it for the group
                            if not world.options.randomize_blocker_required_amounts.value:
                                self.seed_groups[group]["randomize_blocker_required_amounts"] = False

                            # blocker_max: use the lowest value in the group
                            self.seed_groups[group]["blocker_max"] = min(self.seed_groups[group]["blocker_max"], int(world.options.blocker_max.value))

                            # maximize_helm_blocker: if any player has it enabled, enable it for the group
                            if world.options.maximize_level8_blocker.value:
                                self.seed_groups[group]["maximize_helm_blocker"] = True

                            # level blockers: use the lowest value in the group for each
                            for level_num in range(1, 9):
                                blocker_key = f"level_{level_num}"
                                option_key = "level_blockers"
                                self.seed_groups[group][option_key][blocker_key] = min(self.seed_groups[group][option_key][blocker_key], int(getattr(world.options, option_key)[blocker_key]))

                            # logic_type: use most restrictive (glitchless=1 > advanced_glitchless=0 > glitched=2)
                            # Priority order: glitchless (1) is most restrictive, then advanced_glitchless (0), then glitched (2)
                            current_logic = self.seed_groups[group]["logic_type"]
                            new_logic = int(world.options.logic_type.value)

                            # If current is glitched (2) and new is anything else, use new (more restrictive)
                            if current_logic == 2 and new_logic != 2:
                                self.seed_groups[group]["logic_type"] = new_logic
                            # If current is advanced_glitchless (0) and new is glitchless (1), use glitchless
                            elif current_logic == 0 and new_logic == 1:
                                self.seed_groups[group]["logic_type"] = 1
                            # If current is glitchless (1), keep it (most restrictive)
                            # If new is glitched (2), keep current (more restrictive)

                            # tricks_selected: intersection of all players' tricks (only tricks ALL players have)
                            self.seed_groups[group]["tricks_selected"] = self.seed_groups[group]["tricks_selected"].intersection(set(world.options.tricks_selected.value))

                            # glitches_selected: intersection of all players' glitches (only glitches ALL players have)
                            self.seed_groups[group]["glitches_selected"] = self.seed_groups[group]["glitches_selected"].intersection(set(world.options.glitches_selected.value))

            # Apply seed group settings and create group random if using a custom seed group BEFORE fillsettings
            self.group_random = None
            self.original_random = None
            if self.options.loading_zone_rando.value not in [0, LoadingZoneRando.option_no]:
                # Only apply seed group settings for custom string values, not standard numeric options
                if isinstance(self.options.loading_zone_rando.value, str):
                    group = self.options.loading_zone_rando.value
                    if group in self.seed_groups:
                        # Override player's options with seed group settings
                        self.options.shuffle_helm_level_order.value = int(self.seed_groups[group]["shuffle_helm_level_order"])
                        self.options.enable_chaos_blockers.value = int(self.seed_groups[group]["enable_chaos_blockers"])
                        self.options.randomize_blocker_required_amounts.value = int(self.seed_groups[group]["randomize_blocker_required_amounts"])
                        self.options.blocker_max.value = self.seed_groups[group]["blocker_max"]
                        self.options.maximize_level8_blocker.value = int(self.seed_groups[group]["maximize_helm_blocker"])
                        self.options.level_blockers.value = self.seed_groups[group]["level_blockers"]

                        # Create group random for LZR seed synchronization and replace self.random
                        combined_seed = f"{self.multiworld.seed}_{group}"
                        from hashlib import sha256

                        seed_hash = int(sha256(combined_seed.encode()).hexdigest()[:16], 16)
                        from random import Random

                        self.group_random = Random(seed_hash)
                        self.original_random = self.random
                        self.random = self.group_random

            # Use the fillsettings function to configure all settings
            settings = fillsettings(self.options, self.multiworld, self.random)
            # Enable entrance randomization if the option is set (any value other than no/off/false/0)
            if self.options.loading_zone_rando.value not in [0, LoadingZoneRando.option_no]:
                settings.level_randomization = LevelRandomization.loadingzone
                settings.shuffle_loading_zones = ShuffleLoadingZones.all
            else:
                settings.level_randomization = LevelRandomization.level_order_complex
                settings.shuffle_loading_zones = ShuffleLoadingZones.levels
            self.spoiler = Spoiler(settings)
            # Undo any changes to this location's name, until we find a better way to prevent this from confusing the tracker and the AP code that is responsible for sending out items
            self.spoiler.LocationList[DK64RLocations.FactoryDonkeyDKArcade].name = "Factory Donkey DK Arcade Round 1"
            self.spoiler.settings.shuffled_location_types.append(Types.ArchipelagoItem)

            Generate_Spoiler(self.spoiler)

            # Store/retrieve blocker values for seed group synchronization
            if self.options.loading_zone_rando.value not in [0, LoadingZoneRando.option_no]:
                if self.options.loading_zone_rando.value not in LoadingZoneRando.options.values():
                    group = self.options.loading_zone_rando.value
                    if group in self.seed_groups:
                        # If this is the first player to generate, store the blocker values
                        if self.seed_groups[group]["generated_blockers"] is None:
                            blocker_values = [
                                self.spoiler.settings.blocker_0,
                                self.spoiler.settings.blocker_1,
                                self.spoiler.settings.blocker_2,
                                self.spoiler.settings.blocker_3,
                                self.spoiler.settings.blocker_4,
                                self.spoiler.settings.blocker_5,
                                self.spoiler.settings.blocker_6,
                                self.spoiler.settings.blocker_7,
                            ]
                            self.seed_groups[group]["generated_blockers"] = blocker_values
                        else:
                            # Use the stored blocker values from the first player
                            blocker_values = self.seed_groups[group]["generated_blockers"]
                            self.spoiler.settings.blocker_0 = blocker_values[0]
                            self.spoiler.settings.blocker_1 = blocker_values[1]
                            self.spoiler.settings.blocker_2 = blocker_values[2]
                            self.spoiler.settings.blocker_3 = blocker_values[3]
                            self.spoiler.settings.blocker_4 = blocker_values[4]
                            self.spoiler.settings.blocker_5 = blocker_values[5]
                            self.spoiler.settings.blocker_6 = blocker_values[6]
                            self.spoiler.settings.blocker_7 = blocker_values[7]

                            # randomize_blockers: if any player has it disabled, disable it for the group
                            if not world.options.randomize_blocker_required_amounts.value:
                                self.seed_groups[group]["randomize_blocker_required_amounts"] = False

                            # blocker_max: use the lowest value in the group
                            self.seed_groups[group]["blocker_max"] = min(self.seed_groups[group]["blocker_max"], int(world.options.blocker_max.value))

                            # maximize_helm_blocker: if any player has it enabled, enable it for the group
                            if world.options.maximize_level8_blocker.value:
                                self.seed_groups[group]["maximize_helm_blocker"] = True

                            # level blockers: use the lowest value in the group for each
                            for level_num in range(1, 9):
                                blocker_key = f"level_{level_num}"
                                option_key = "level_blockers"
                                self.seed_groups[group][option_key][blocker_key] = min(self.seed_groups[group][option_key][blocker_key], int(getattr(world.options, option_key)[blocker_key]))

            # Apply seed group settings and create group random if using a custom seed group BEFORE fillsettings
            self.group_random = None
            self.original_random = None
            if self.options.loading_zone_rando.value not in [0, LoadingZoneRando.option_no]:
                if self.options.loading_zone_rando.value not in LoadingZoneRando.options.values():
                    group = self.options.loading_zone_rando.value
                    if group in self.seed_groups:
                        # Override player's options with seed group settings
                        self.options.shuffle_helm_level_order.value = int(self.seed_groups[group]["shuffle_helm_level_order"])
                        self.options.enable_chaos_blockers.value = int(self.seed_groups[group]["enable_chaos_blockers"])
                        self.options.randomize_blocker_required_amounts.value = int(self.seed_groups[group]["randomize_blocker_required_amounts"])
                        self.options.blocker_max.value = self.seed_groups[group]["blocker_max"]
                        self.options.maximize_level8_blocker.value = int(self.seed_groups[group]["maximize_helm_blocker"])
                        self.options.level_blockers.value = self.seed_groups[group]["level_blockers"]

                        # Apply synchronized logic and glitch settings
                        self.options.logic_type.value = self.seed_groups[group]["logic_type"]
                        self.options.tricks_selected.value = list(self.seed_groups[group]["tricks_selected"])
                        self.options.glitches_selected.value = list(self.seed_groups[group]["glitches_selected"])

                        # Create group random for LZR seed synchronization and replace self.random
                        from random import Random

                        self.group_random = Random(group)
                        self.original_random = self.random
                        self.random = self.group_random

            # Use the fillsettings function to configure all settings
            settings = fillsettings(self.options, self.multiworld, self.random)
            # Enable entrance randomization if the option is set (any value other than no/off/false/0)
            if self.options.loading_zone_rando.value not in [0, LoadingZoneRando.option_no]:
                settings.level_randomization = LevelRandomization.loadingzone
                settings.shuffle_loading_zones = ShuffleLoadingZones.all
            else:
                settings.level_randomization = LevelRandomization.level_order_complex
                settings.shuffle_loading_zones = ShuffleLoadingZones.levels
            self.spoiler = Spoiler(settings)
            # Undo any changes to this location's name, until we find a better way to prevent this from confusing the tracker and the AP code that is responsible for sending out items
            self.spoiler.LocationList[DK64RLocations.FactoryDonkeyDKArcade].name = "Factory Donkey DK Arcade Round 1"
            self.spoiler.settings.shuffled_location_types.append(Types.ArchipelagoItem)

            Generate_Spoiler(self.spoiler)

            # Store/retrieve blocker values for seed group synchronization
            if self.options.loading_zone_rando.value not in [0, LoadingZoneRando.option_no]:
                if self.options.loading_zone_rando.value not in LoadingZoneRando.options.values():
                    group = self.options.loading_zone_rando.value
                    if group in self.seed_groups:
                        # If this is the first player to generate, store the blocker values
                        if self.seed_groups[group]["generated_blockers"] is None:
                            blocker_values = [
                                self.spoiler.settings.blocker_0,
                                self.spoiler.settings.blocker_1,
                                self.spoiler.settings.blocker_2,
                                self.spoiler.settings.blocker_3,
                                self.spoiler.settings.blocker_4,
                                self.spoiler.settings.blocker_5,
                                self.spoiler.settings.blocker_6,
                                self.spoiler.settings.blocker_7,
                            ]
                            self.seed_groups[group]["generated_blockers"] = blocker_values
                        else:
                            # Use the stored blocker values from the first player
                            blocker_values = self.seed_groups[group]["generated_blockers"]
                            self.spoiler.settings.blocker_0 = blocker_values[0]
                            self.spoiler.settings.blocker_1 = blocker_values[1]
                            self.spoiler.settings.blocker_2 = blocker_values[2]
                            self.spoiler.settings.blocker_3 = blocker_values[3]
                            self.spoiler.settings.blocker_4 = blocker_values[4]
                            self.spoiler.settings.blocker_5 = blocker_values[5]
                            self.spoiler.settings.blocker_6 = blocker_values[6]
                            self.spoiler.settings.blocker_7 = blocker_values[7]

            if self.options.enable_shared_shops.value:
                from randomizer.Lists.Location import SharedShopLocations

                all_shared_shops = list(SharedShopLocations)
                self.random.shuffle(all_shared_shops)
                self.spoiler.settings.selected_shared_shops = set(all_shared_shops[:10])
            else:
                self.spoiler.settings.selected_shared_shops = set()

            # Generate custom shop prices for Archipelago
            generate_prices(self.spoiler, self.options, self.random)

            # Handle Loading Zones - this will handle LO and (someday?) LZR appropriately
            if self.spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.none:
                if self.spoiler.settings.level_randomization != LevelRandomization.loadingzone:
                    # UT should not reshuffle the level order, but should update the exits
                    if not hasattr(self.multiworld, "generation_is_fake"):
                        ShuffleExits.ExitShuffle(self.spoiler, skip_verification=True)
                    self.spoiler.UpdateExits()
                # else: LZR shuffling happens in connect_entrances()

            # Repopulate any spoiler-related stuff at this point from slot data
            if hasattr(self.multiworld, "generation_is_fake"):
                if hasattr(self.multiworld, "re_gen_passthrough"):
                    if "Donkey Kong 64" in self.multiworld.re_gen_passthrough:
                        passthrough = self.multiworld.re_gen_passthrough["Donkey Kong 64"]
                        if passthrough["EnemyData"]:
                            for location, data in passthrough["EnemyData"].items():
                                self.spoiler.enemy_location_list[DK64RLocations[location]] = EnemyLoc(Maps[data["map"]], Enemies[data["enemy"]], 0, [], False)
                        if passthrough["MinigameData"]:
                            for loc, minigame in passthrough["MinigameData"].items():
                                self.spoiler.shuffled_barrel_data[DK64RLocations[loc]].minigame = Minigames[minigame]
                        if passthrough["JunkedLocations"]:
                            for loc in passthrough["JunkedLocations"]:
                                del self.location_name_to_id[loc]
                        if passthrough.get("ShopPrices"):
                            # Restore shop prices from slot data (shop locations only)
                            restored_prices = {}
                            for location_name, price in passthrough["ShopPrices"].items():
                                # Convert location name string back to enum
                                try:
                                    location_id = DK64RLocations[location_name]
                                    restored_prices[location_id] = price
                                except (KeyError, AttributeError):
                                    print(f"Warning: Could not restore price for location {location_name}")
                            self.spoiler.settings.prices = restored_prices

            # Handle hint preparation by initiating some variables
            self.hint_data = {
                "kong": [],
                "key": [],
                "woth": [],
                "major": [],
                "deep": [],
            }
            # Initialize hint location mapping and dynamic hints storage
            self.hint_location_mapping = {}
            self.dynamic_hints = {}  # Store dynamic hints for CreateHints functionality
            self.foreignMicroHints = {}

            # Handle locations that start empty due to being junk
            self.junked_locations = []

        def create_regions(self) -> None:
            """Create the regions."""
            create_regions(self.multiworld, self.player, self.spoiler, self.options)

            def exclude_locations(location_names: typing.List[str]):
                for location_name in location_names:
                    try:
                        self.multiworld.get_location(location_name, self.player).progress_type = LocationProgressType.EXCLUDED
                    except KeyError:
                        continue  # Location not in multiworld

            maximum_snide = self.options.maximum_snide.value
            excluded_locations = []

            # Add blueprint turn-in locations above the maximum_snide threshold
            for blueprint_count in range(maximum_snide + 1, 41):
                location_name = f"Turning In {blueprint_count} Blueprints"
                if location_name in all_locations:
                    excluded_locations.append(location_name)

            # Exclude the locations using Archipelago's exclude_locations mechanism
            if excluded_locations:
                exclude_locations(excluded_locations)

        def create_items(self) -> None:
            """Create the items."""
            itempool: typing.List[DK64Item] = setup_items(self)
            self.multiworld.itempool += itempool

        def get_filler_item_name(self) -> str:
            """Get the filler item name."""
            return DK64RItem.ItemList[DK64RItems.JunkMelon].name

        def set_rules(self):
            """Set the rules."""
            set_rules(self.multiworld, self.player)

        def generate_basic(self):
            """Generate the basic world."""
            self.multiworld.get_location("Banana Hoard", self.player).place_locked_item(DK64Item("Banana Hoard", ItemClassification.progression_skip_balancing, 0xD64060, self.player))  # TEMP?

        def connect_entrances(self) -> None:
            """Randomize and connect entrances if LZR is on."""
            LinkWarps(self.spoiler)  # I am very skeptical that this works at all - must be resolved if we want to do more than Isles warps preactivated
            connect_regions(self, self.spoiler.settings)

            if (
                self.options.loading_zone_rando.value not in [0, LoadingZoneRando.option_no]
                and self.spoiler.settings.level_randomization == LevelRandomization.loadingzone
                and not hasattr(self.multiworld, "generation_is_fake")
            ):
                # Reset shuffle state for all exits to ensure clean state between players
                # This prevents state contamination when multiple DK64 players have different helm shuffle settings
                for exit in ShufflableExits.values():
                    exit.toBeShuffled = False
                    exit.shuffled = False
                    exit.shuffledId = None

                ap_entrance_to_transition = {}
                for transition_enum, shufflable_exit in ShufflableExits.items():
                    # TODO: Make this configurable with DLZR
                    if shufflable_exit.back.reverse is None:
                        continue
                    ap_entrance_to_transition[shufflable_exit.name] = transition_enum

                # Store entrance connections for ROM patching
                def store_entrance_connections(state, exits, entrances):
                    """Store entrance randomization results in the spoiler."""
                    for source_exit, target_entrance in zip(exits, entrances):
                        exit_name = source_exit.name
                        source_transition = ap_entrance_to_transition.get(exit_name)
                        if not source_transition:
                            continue

                        target_transition = ap_entrance_to_transition.get(target_entrance.name)
                        if not target_transition:
                            continue

                        target_reverse = ShufflableExits[target_transition].back.reverse
                        if target_reverse is None:
                            continue

                        ShufflableExits[source_transition].shuffledId = target_reverse
                        ShufflableExits[source_transition].shuffled = True

                # Store initial entrance/exit state before randomization attempts
                initial_entrance_states = {}
                for region in self.multiworld.get_regions(self.player):
                    for entrance in region.entrances:
                        if not entrance.parent_region:  # This is an ER target
                            initial_entrance_states[entrance] = entrance.connected_region

                initial_exit_states = {}
                for region in self.multiworld.get_regions(self.player):
                    for exit in region.exits:
                        if not exit.connected_region:  # This is a randomizable exit
                            initial_exit_states[exit] = (region, exit.parent_region)

                # Retry entrance randomization if it fails (similar to Crystalis implementation)
                DK64_MAX_ER_ATTEMPTS = 20
                for attempt in range(DK64_MAX_ER_ATTEMPTS):
                    try:
                        self.er_placement_state = randomize_entrances(self, True, {0: [0]}, on_connect=store_entrance_connections)
                        break
                    except EntranceRandomizationError as error:
                        if attempt >= DK64_MAX_ER_ATTEMPTS - 1:
                            raise EntranceRandomizationError(f"DK64: failed entrance randomization after {DK64_MAX_ER_ATTEMPTS} " f"attempts. Final error:\n\n{error}")
                        logging.warning(f"DK64: Entrance randomization attempt {attempt + 1} failed, retrying...")

                        # Restore entrance/exit state for retry
                        # First, disconnect all exits that were connected during failed attempt
                        for region in self.multiworld.get_regions(self.player):
                            for exit in list(region.exits):
                                if exit.connected_region and exit in initial_exit_states:
                                    exit.connected_region = None

                        # Restore ER targets to their original regions
                        for entrance, original_region in initial_entrance_states.items():
                            # Remove entrance from wherever it ended up
                            if entrance.connected_region:
                                if entrance in entrance.connected_region.entrances:
                                    entrance.connected_region.entrances.remove(entrance)
                            # Restore to original region
                            entrance.connected_region = original_region
                            if entrance not in original_region.entrances:
                                original_region.entrances.append(entrance)

                # Handle exit level and deathwarp
                connect_exit_level_and_deathwarp(self, self.er_placement_state)

                # Handle glitch transitions
                connect_glitch_transitions(self, self.er_placement_state)

                # After randomization, update the spoiler's exit data
                self.spoiler.UpdateExits()

                # Restore original random if we replaced it with group random
                if self.original_random:
                    self.random = self.original_random

        def get_archipelago_item_type_by_classification(self, item_classification: ItemClassification) -> DK64RItems:
            """Get the appropriate DK64R Archipelago item type based on the ItemClassification."""
            if item_classification in [ItemClassification.progression, ItemClassification.progression_skip_balancing]:
                return DK64RItems.ArchipelagoItem
            elif item_classification == ItemClassification.useful:
                return DK64RItems.SpecialArchipelagoItem
            elif item_classification == ItemClassification.trap:
                return DK64RItems.TrapArchipelagoItem
            elif item_classification == ItemClassification.filler:
                return DK64RItems.ArchipelagoItem.FoolsArchipelagoItem
            else:
                return DK64RItems.ArchipelagoItem

        def generate_output(self, output_directory: str):
            """Generate the output."""
            try:
                spoiler = self.spoiler
                spoiler.settings.archipelago = True
                spoiler.settings.random = self.random
                spoiler.settings.player_name = self.multiworld.get_player_name(self.player)
                spoiler.first_move_item = None  # Not relevant with Fast Start always enabled
                spoiler.pregiven_items = []
                # Initialize dictionary to store Archipelago location to item name mappings for textbox display
                spoiler.archipelago_locations = {}
                for item in self.multiworld.precollected_items[self.player]:
                    dk64_item = logic_item_name_to_id[item.name]
                    # Only moves can be pushed to the pregiven_items list
                    if DK64RItem.ItemList[dk64_item].type in [Types.Shop, Types.Shockwave, Types.TrainingBarrel, Types.Climbing, Types.Cranky, Types.Funky, Types.Candy, Types.Snide]:
                        spoiler.pregiven_items.append(dk64_item)
                local_trap_count = 0
                ap_item_is_major_item = False
                ap_major_item_type = None  # Track which archipelago item type to add to major items
                self.junked_locations = []
                # Read through all item assignments in this AP world and find their DK64 equivalents so we can update our world state for patching purposes
                for ap_location in self.multiworld.get_locations(self.player):
                    # We never need to place Collectibles or Events in our world state
                    if "Collectible" in ap_location.name or "Event" in ap_location.name or "Token" in ap_location.name:
                        continue
                    # Find the corresponding DK64 Locations enum
                    dk64_location_id = None
                    for dk64_loc_id, dk64_loc in spoiler.LocationList.items():
                        if dk64_loc.name == ap_location.name:
                            dk64_location_id = dk64_loc_id
                            break
                    if dk64_location_id is not None and ap_location.item is not None:
                        ap_item = ap_location.item
                        # Any item that isn't for this player is placed as an AP item, regardless of whether or not it could be a DK64 item
                        if ap_item.player != self.player:
                            # Store the Archipelago item name for textbox display (items from other players)
                            player_name = self.multiworld.get_player_name(ap_item.player)
                            spoiler.archipelago_locations[dk64_location_id] = f"{ap_item.name} ({player_name})"
                            archipelago_item_type = self.get_archipelago_item_type_by_classification(ap_item.classification)
                            spoiler.LocationList[dk64_location_id].PlaceItem(spoiler, archipelago_item_type)
                            # If Jetpac has an progression AP item, we should hint is as if it were a major item
                            if dk64_location_id == DK64RLocations.RarewareCoin and ap_item.advancement:
                                ap_item_is_major_item = True
                                ap_major_item_type = archipelago_item_type
                        # Collectibles don't get placed in the LocationList
                        elif "Collectible" in ap_item.name or "Boss Defeated" == ap_item.name or "Bonus Completed" in ap_item.name:
                            continue
                        else:
                            dk64_item = logic_item_name_to_id[ap_item.name]
                            if dk64_item is not None:
                                if dk64_item in [
                                    DK64RItems.IceTrapBubble,
                                    DK64RItems.IceTrapReverse,
                                    DK64RItems.IceTrapSlow,
                                    DK64RItems.IceTrapDisableA,
                                    DK64RItems.IceTrapDisableB,
                                    DK64RItems.IceTrapDisableCU,
                                    DK64RItems.IceTrapDisableZ,
                                    DK64RItems.IceTrapGetOutGB,
                                    DK64RItems.IceTrapDryGB,
                                    DK64RItems.IceTrapFlipGB,
                                    DK64RItems.IceTrapIceFloorGB,
                                    DK64RItems.IceTrapPaperGB,
                                    DK64RItems.IceTrapSlipGB,
                                    DK64RItems.IceTrapAnimalGB,
                                    DK64RItems.IceTrapRockfallGB,
                                    DK64RItems.IceTrapDisableTagGB,
                                ]:
                                    local_trap_count += 1

                                dk64_location = spoiler.LocationList[dk64_location_id]
                                # Most of these item restrictions should be handled by item rules, so this is a failsafe.
                                # Junk items can't be placed in shops, bosses, or arenas. Fortunately this is junk, so we can just patch a NoItem there instead.
                                # Shops are allowed to get Junk items placed by AP in order to artificially slightly reduce the number of checks in shops.
                                if DK64RItem.ItemList[dk64_item].type == Types.JunkItem and (dk64_location.type in [Types.Key, Types.Crown]):
                                    dk64_item = DK64RItems.NoItem
                                    self.junked_locations.append(ap_location.name)
                                # Blueprints can't be on fairies for technical reasons. Instead we'll patch it in as an AP item and have AP handle it.
                                if dk64_item in DK64RItemPool.Blueprints() and dk64_location.type == Types.Fairy:
                                    # Store the item name for textbox display since this becomes an Archipelago item
                                    spoiler.archipelago_locations[dk64_location_id] = ap_item.name
                                    dk64_item = self.get_archipelago_item_type_by_classification(ap_item.classification)
                                # Track explicit "No Item" placements
                                elif ap_item.name == "No Item":
                                    self.junked_locations.append(ap_location.name)
                                spoiler.LocationList[dk64_location_id].PlaceItem(spoiler, dk64_item)
                            else:
                                print(f"Item {ap_item.name} not found in DK64 item table.")
                    elif dk64_location_id is not None:
                        spoiler.LocationList[dk64_location_id].PlaceItem(spoiler, DK64RItems.NoItem)
                    else:
                        print(f"Location {ap_location.name} not found in DK64 location table.")

                spoiler.settings.ice_trap_count = local_trap_count
                ShuffleItems(spoiler)

                spoiler.UpdateLocations(spoiler.LocationList)
                self.updateBossKongs(spoiler)
                compileMicrohints(spoiler)
                # Could add a hints on/off setting?
                microhints_enabled = self.options.shopkeeper_hints.value or self.options.microhints.value > 0
                hints_enabled = self.options.hint_style > 0

                if hints_enabled or microhints_enabled:
                    self.hint_data_available.wait()

                if hints_enabled:
                    CompileArchipelagoHints(self, self.hint_data)
                    # Signal that hint compilation is complete
                    self.hint_compilation_complete.set()
                else:
                    # If hints are not enabled, immediately set the event
                    self.hint_compilation_complete.set()

                if microhints_enabled:
                    # Finalize microhints
                    if self.options.shopkeeper_hints.value:
                        shopkeepers = [DK64RItems.Candy, DK64RItems.Cranky, DK64RItems.Funky, DK64RItems.Snide]
                    else:
                        shopkeepers = []
                    # Define helm_prog_items only when microhints is "some" or "all"
                    if self.options.microhints.value in [1, 2]:  # some or all
                        helm_prog_items = [DK64RItems.BaboonBlast, DK64RItems.BaboonBalloon, DK64RItems.Monkeyport, DK64RItems.GorillaGrab, DK64RItems.ChimpyCharge, DK64RItems.GorillaGone]
                    else:
                        helm_prog_items = []
                    # Define instruments only when microhints is "all"
                    if self.options.microhints.value == 2:  # all
                        instruments = [DK64RItems.Bongos, DK64RItems.Guitar, DK64RItems.Trombone, DK64RItems.Saxophone, DK64RItems.Triangle]
                    else:
                        instruments = []
                    hinted_slams = []
                    if DK64RItems.ProgressiveSlam in self.foreignMicroHints.keys() and DK64RItem.ItemList[DK64RItems.ProgressiveSlam].name in self.spoiler.microhints.keys():
                        # Break down the slam hint to retrieve raw data
                        text1 = "Ladies and Gentlemen! It appears that one fighter has come unequipped to properly handle this reptilian beast. Perhaps they should have looked in "
                        local_hinted_slams = self.spoiler.microhints[DK64RItem.ItemList[DK64RItems.ProgressiveSlam].name].replace(text1.upper(), "")
                        local_hinted_slams = local_hinted_slams.replace(" for the elusive slam.".upper(), "")
                        hinted_slams = local_hinted_slams.split(" or ".upper())
                    for hintedItem in self.foreignMicroHints.keys():
                        text = ""
                        if hintedItem in helm_prog_items and self.options.microhints.value in [1, 2]:
                            text = f"\x07{self.foreignMicroHints[hintedItem][0][0]}\x07 would be better off looking in \x07{self.foreignMicroHints[hintedItem][0][1]}\x07 for this.".upper()
                        elif hintedItem in instruments and self.options.microhints.value == 2:
                            text = f"\x07{self.foreignMicroHints[hintedItem][0][0]}\x07 would be better off looking in \x07{self.foreignMicroHints[hintedItem][0][1]}\x07 for this.".upper()
                        elif hintedItem == DK64RItems.ProgressiveSlam:
                            for slam in self.foreignMicroHints[DK64RItems.ProgressiveSlam]:
                                hinted_slams.append(f"\x07{slam[0]}: {slam[1]}\x07")
                            slam_text = " or ".join(hinted_slams)
                            text = f"Ladies and Gentlemen! It appears that one fighter has come unequipped to properly handle this reptilian beast. Perhaps they should have looked in {slam_text} for the elusive slam.".upper()
                        elif self.options.shopkeeper_hints.value and hintedItem in shopkeepers:
                            text = f"{hintedItem.name} has gone on a space mission to \x07{self.foreignMicroHints[hintedItem][0][0]}'s\x07 \x0d{self.foreignMicroHints[hintedItem][0][1]}\x0d.".upper()

                        # Only create microhint if we have text to display
                        if text:
                            for letter in text:
                                if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
                                    text = text.replace(letter, " ")
                            self.spoiler.microhints[DK64RItem.ItemList[hintedItem].name] = text

                spoiler.majorItems = IdentifyMajorItems(spoiler)
                if ap_item_is_major_item and ap_major_item_type is not None:
                    spoiler.majorItems.append(ap_major_item_type)

                # Generate patch with cumulative prices (what players see in-game)
                patch_data, _ = patching_response(spoiler)
                lanky = self.update_seed_results(patch_data, spoiler, self.player)

                output_data = {
                    "patch_data": lanky,
                    "player": self.player,
                    "player_name": self.player_name,
                    "version": self.ap_version,
                    "seed": self.multiworld.seed_name,
                }

                # Output the patch details to file using the container
                dk64_container = DK64Container(
                    path=os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}{DK64Container.patch_file_ending}"),
                    player=self.player,
                    player_name=self.player_name,
                    data=output_data,
                )
                dk64_container.write()

                # Clear the path_data out of memory to flush memory usage
                del patch_data
            except Exception:
                raise
            finally:
                self.rom_name_available_event.set()  # make sure threading continues and errors are collected

        @classmethod
        def stage_generate_output(cls, multiworld: MultiWorld, output_directory: str):
            """Prepare hint data."""
            # Microhint stuff
            microHintItemNames = {
                "Progressive Slam": DK64RItems.ProgressiveSlam,
                "Bongos": DK64RItems.Bongos,
                "Guitar": DK64RItems.Guitar,
                "Trombone": DK64RItems.Trombone,
                "Saxophone": DK64RItems.Saxophone,
                "Triangle": DK64RItems.Triangle,
                "Baboon Blast": DK64RItems.BaboonBlast,
                "Baboon Balloon": DK64RItems.BaboonBalloon,
                "Monkeyport": DK64RItems.Monkeyport,
                "Gorilla Grab": DK64RItems.GorillaGrab,
                "Chimpy Charge": DK64RItems.ChimpyCharge,
                "Gorilla Gone": DK64RItems.GorillaGone,
                "Candy": DK64RItems.Candy,
                "Cranky": DK64RItems.Cranky,
                "Funky": DK64RItems.Funky,
                "Snide": DK64RItems.Snide,
            }
            shopkeepers = [DK64RItems.Candy, DK64RItems.Cranky, DK64RItems.Funky, DK64RItems.Snide]
            helm_prog_items = [DK64RItems.BaboonBlast, DK64RItems.BaboonBalloon, DK64RItems.Monkeyport, DK64RItems.GorillaGrab, DK64RItems.ChimpyCharge, DK64RItems.GorillaGone]
            instruments = [DK64RItems.Bongos, DK64RItems.Guitar, DK64RItems.Trombone, DK64RItems.Saxophone, DK64RItems.Triangle]
            microhint_categories = {
                MicrohintsEnabled.off: shopkeepers.copy(),
                MicrohintsEnabled.base: helm_prog_items.copy() + [DK64RItems.ProgressiveSlam] + shopkeepers.copy(),
                MicrohintsEnabled.all: helm_prog_items.copy() + instruments.copy() + shopkeepers.copy() + [DK64RItems.ProgressiveSlam],
            }

            # Hint stuff
            try:
                # Get players that have hints enabled.
                players = {
                    autoworld.player
                    for autoworld in multiworld.get_game_worlds("Donkey Kong 64")
                    if autoworld.options.hint_style > 0 or autoworld.options.shopkeeper_hints or autoworld.options.microhints > 0
                }
                if not players:
                    # Bail if every player has hints off
                    return
                # Locations that could get a "deep locations" hint:
                deep_location_names = [
                    "Returning the Banana Fairies",
                    "Aztec Tiny Beetle Race",
                    "Factory Donkey DK Arcade Round 1",
                    "Forest Donkey Baboon Blast",
                    "Forest Diddy Owl Race",
                    "Forest Lanky Rabbit Race",
                    "Caves Donkey Baboon Blast",
                    "Caves Lanky Beetle Race",
                    "Castle Donkey Minecart",
                    "Forest Donkey Mushroom Cannons",
                    "Isles Battle Arena 2 (Fungi Lobby: Gorilla Gone Box)",
                    "Isles Diddy Summit Barrel",
                    "Helm Battle Arena (Top of Blast-o-Matic)",
                    "Helm Donkey Medal",
                    "Helm Chunky Medal",
                    "Helm Tiny Medal",
                    "Helm Lanky Medal",
                    "Helm Diddy Medal",
                    "Helm Fairy (Key 8 Room (1))",
                    "Helm Fairy (Key 8 Room (2))",
                    "Galleon Diddy Mechfish",
                    "Jetpac",
                    "Galleon Chunky Cannon Game",
                    "Galleon Tiny Medal",
                    "Factory Chunky Toy Monster",
                    "Caves Dirt: Giant Kosha",
                    "Castle Lanky Tower",
                    "Japes Boss Defeated",
                    "Aztec Boss Defeated",
                    "Factory Boss Defeated",
                    "Galleon Boss Defeated",
                    "Forest Boss Defeated",
                    "Caves Boss Defeated",
                    "Castle Boss Defeated",
                ]

                # Look through every location in the multiworld and find all the DK64 items that are progression
                for loc in [location for location in multiworld.get_locations() if not location.is_event]:
                    player = loc.item.player
                    autoworld = multiworld.worlds[player]
                    locworld = multiworld.worlds[loc.player]

                    is_donk_item = player in players
                    is_donk_location = loc.player in players

                    microhints_enabled = is_donk_item and autoworld.options.microhints > 0
                    shopkeepers_enabled = is_donk_item and autoworld.options.shopkeeper_hints

                    # Skip locations that aren't related to DK64 or are clearly unimportant to us
                    if not (is_donk_location and loc.name in deep_location_names) and not (is_donk_item and autoworld.isMajorItem(loc.item)):
                        continue

                    is_microhintable = is_donk_item and loc.item.name in microHintItemNames and microHintItemNames[loc.item.name] in microhint_categories[autoworld.spoiler.settings.microhints_enabled]

                    # Gather information on microhints
                    if (microhints_enabled or shopkeepers_enabled) and is_microhintable:
                        if player != loc.player:
                            if microHintItemNames[loc.item.name] in autoworld.foreignMicroHints.keys():
                                autoworld.foreignMicroHints[microHintItemNames[loc.item.name]].append((multiworld.get_player_name(loc.player), loc.name[:80]))
                            else:
                                autoworld.foreignMicroHints[microHintItemNames[loc.item.name]] = [(multiworld.get_player_name(loc.player), loc.name[:80])]

                    # Bail if hints are disabled at this point
                    if (is_donk_item and autoworld.options.hint_style == 0) and not is_donk_location:
                        continue

                    # From here, no need to hint shopkeepers, since their microhints are basically free
                    if is_donk_item and loc.item.name in ("Candy", "Cranky", "Funky", "Snide"):
                        continue

                    # Prioritize hinting Kongs
                    if is_donk_item and loc.item.name in ("Donkey", "Diddy", "Lanky", "Tiny", "Chunky"):
                        autoworld.hint_data["kong"].append(loc)
                        continue

                    # Prioritize hinting Keys
                    if is_donk_item and loc.item.name in ("Key 1", "Key 2", "Key 4", "Key 5"):
                        autoworld.hint_data["key"].append(loc)
                        continue

                    # Hint locations that are nasty to reach
                    if is_donk_location and loc.name in deep_location_names:
                        locworld.hint_data["deep"].append(loc)
                        continue

                    # For the rest of the locations, do WOTH hints.
                    if is_donk_item and autoworld.isMajorItem(loc.item) and (not autoworld.spoiler.settings.key_8_helm or loc.name != "The End of Helm"):
                        autoworld.hint_data["major"].append(loc)
                        # Skip item at location and see if game is still beatable
                        state = CollectionState(multiworld)
                        state.locations_checked.add(loc)
                        # VERY SLOW! User needs to explicitly enable this option.
                        if autoworld.options.hint_style == 2 and not multiworld.can_beat_game(state):
                            autoworld.hint_data["woth"].append(loc)

            except Exception as e:
                raise e
            finally:
                for autoworld in multiworld.get_game_worlds("Donkey Kong 64"):
                    autoworld.hint_data_available.set()

        def update_seed_results(self, patch, spoiler, player_id):
            """Update the seed results."""
            timestamp = time.time()
            hash = spoiler.settings.seed_hash
            spoiler_log = {}
            spoiler_log["Generated Time"] = timestamp
            spoiler_log["Settings"] = {}
            spoiler_log["Cosmetics"] = {}
            # Zip all the data into a single file.
            zip_data = BytesIO()
            with zipfile.ZipFile(zip_data, "w") as zip_file:
                # Write each variable to the zip file
                zip_file.writestr("patch", patch)
                zip_file.writestr("hash", str(hash))
                zip_file.writestr("spoiler_log", str(json.dumps(spoiler_log)))
                zip_file.writestr("generated_time", str(timestamp))
                zip_file.writestr("version", version)
                zip_file.writestr("seed_number", self.multiworld.get_out_file_name_base(self.player))
                zip_file.writestr("seed_id", self.multiworld.get_out_file_name_base(self.player))
            zip_data.seek(0)
            # Convert the zip to a string of base64 data
            zip_conv = codecs.encode(zip_data.getvalue(), "base64").decode()

            return zip_conv

        def modify_multidata(self, multidata: dict):
            """Modify the multidata."""
            pass

        def get_smaller_shops_data(self) -> dict:
            """Get information about which shops appear with smaller shops enabled."""
            if not (self.options.smaller_shops.value and Types.Shop in self.spoiler.settings.shuffled_location_types):
                return {}

            # Build set of vendor/level combinations that have shared shops
            shared_shop_vendors = set()
            if self.options.enable_shared_shops.value:
                available_shared_shops = getattr(self.spoiler.settings, "selected_shared_shops", set())
                for location_id in available_shared_shops:
                    if location_id in self.spoiler.LocationList:
                        location = self.spoiler.LocationList[location_id]
                        if location.type == Types.Shop and location.kong == Kongs.any:
                            shared_shop_vendors.add((location.level, location.vendor))

            smaller_shops_data = {}
            for level_enum, vendor_data in ShopLocationReference.items():
                level_name = level_enum.name

                for vendor_enum, location_list in vendor_data.items():
                    vendor_name = vendor_enum.name

                    # Kong names in order: DK, Diddy, Lanky, Tiny, Chunky, then Shared
                    kong_names = ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky", "Shared"]

                    for i, location_id in enumerate(location_list):
                        location_obj = self.spoiler.LocationList[location_id]

                        # Create key like "IslesCrankyDonkey"
                        if i < 5:  # Kong-specific locations
                            key = f"{level_name}{vendor_name}{kong_names[i]}"

                            # Kong shops are inaccessible if:
                            # 1. Blocked by smaller_shops setting, OR
                            # 2. A shared shop exists at this vendor/level
                            is_accessible = not location_obj.smallerShopsInaccessible and (level_enum, vendor_enum) not in shared_shop_vendors
                        else:  # Shared shop location
                            key = f"{level_name}{vendor_name}Shared"

                            # Shared shops are accessible if:
                            # 1. Not blocked by smaller_shops setting, AND
                            # 2. This vendor/level has a shared shop enabled
                            is_accessible = not location_obj.smallerShopsInaccessible and (level_enum, vendor_enum) in shared_shop_vendors

                        smaller_shops_data[key] = 1 if is_accessible else 0

            return smaller_shops_data

        def fill_slot_data(self) -> dict:
            """Fill the slot data."""
            # If hints are enabled, wait for hint compilation to complete
            if hasattr(self, "options") and self.options.hint_style > 0:
                self.hint_compilation_complete.wait()
            hint_mapping = getattr(self, "hint_location_mapping", {})
            dynamic_hints = getattr(self, "dynamic_hints", {})

            slot_data = {
                "Goal": self.options.goal.value,
                "win_condition_item": self.spoiler.settings.win_condition_item.value,
                "helm_hurry": self.spoiler.settings.helm_hurry,
                "ClimbingShuffle": self.options.climbing_shuffle.value,
                "PlayerNum": self.player,
                "death_link": self.options.death_link.value,
                "ring_link": self.options.ring_link.value,
                "tag_link": self.options.tag_link.value,
                "trap_link": self.options.trap_link.value,
                "receive_notifications": self.options.receive_notifications.value,
                "LevelOrder": ", ".join([level.name for order, level in self.spoiler.settings.level_order.items()]),
                "StartingKongs": ", ".join([kong.name for kong in self.spoiler.settings.starting_kong_list]),
                "ForestTime": self.spoiler.settings.fungi_time_internal.name,
                "GalleonWater": self.spoiler.settings.galleon_water_internal.name,
                "MedalCBRequirement": self.spoiler.settings.medal_cb_req,
                "MedalCBRequirementLevel": ", ".join(
                    [
                        f"{level}: {req}"
                        for level, req in zip(["JungleJapes", "AngryAztec", "FranticFactory", "GloomyGalleon", "FungiForest", "CrystalCaves", "CreepyCastle"], self.spoiler.settings.medal_cb_req_level)
                    ]
                ),
                "BLockerValues": ", ".join(
                    [
                        f"{['Japes', 'Aztec', 'Factory', 'Galleon', 'Forest', 'Caves', 'Castle', 'Helm'][i]}: {count} {barrier_type.name}"
                        for i, (barrier_type, count) in enumerate(zip(self.spoiler.settings.BLockerEntryItems, self.spoiler.settings.BLockerEntryCount))
                    ]
                ),
                "RemovedBarriers": ", ".join([barrier.name for barrier in self.spoiler.settings.remove_barriers_selected]),
                "FairyRequirement": self.spoiler.settings.rareware_gb_fairies,
                "MermaidPearls": self.spoiler.settings.mermaid_gb_pearls,
                "JetpacReq": self.spoiler.settings.medal_requirement,
                "BossBananas": ", ".join([str(cost) for cost in self.spoiler.settings.BossBananas]),
                "BossMaps": ", ".join(map.name for map in self.spoiler.settings.boss_maps),
                "BossKongs": ", ".join(kong.name for kong in self.spoiler.settings.boss_kongs),
                "LankyFreeingKong": self.spoiler.settings.lanky_freeing_kong,
                "HelmOrder": ", ".join([str(room) for room in self.spoiler.settings.helm_order]),
                "OpenLobbies": self.spoiler.settings.open_lobbies,
                "KroolInBossPool": self.spoiler.settings.krool_in_boss_pool,
                "SwitchSanity": (
                    {
                        switch.name: {
                            "kong": data.kong.name if hasattr(data.kong, "name") else Kongs(data.kong).name,
                            "type": data.switch_type.name if hasattr(data.switch_type, "name") else SwitchType(data.switch_type).name,
                        }
                        for switch, data in self.spoiler.settings.switchsanity_data.items()
                    }
                    if hasattr(self.spoiler.settings, "switchsanity_data") and self.spoiler.settings.switchsanity_data
                    else {}
                ),
                "LogicType": self.spoiler.settings.logic_type.name,
                "TricksSelected": ", ".join([trick.name for trick in self.spoiler.settings.tricks_selected]),
                "GlitchesSelected": ", ".join([glitch.name for glitch in self.spoiler.settings.glitches_selected]),
                "StartingKeyList": ", ".join([key.name for key in self.spoiler.settings.starting_key_list]),
                "ProgressiveSwitchStrength": self.spoiler.settings.alter_switch_allocation,
                "SlamLevels": (
                    ", ".join(
                        [
                            f"{['JungleJapes', 'AngryAztec', 'FranticFactory', 'GloomyGalleon', 'FungiForest', 'CrystalCaves', 'CreepyCastle', 'HideoutHelm'][i]}: {slam_req.name}"
                            for i, slam_req in enumerate(self.spoiler.settings.switch_allocation)
                        ]
                    )
                    if self.spoiler.settings.alter_switch_allocation
                    else ""
                ),
                "Junk": self.junked_locations,
                "HintsInPool": self.options.hints_in_item_pool.value,
                "BouldersInPool": self.options.boulders_in_pool.value,
                "Dropsanity": self.options.dropsanity.value,
                "Version": self.ap_version,
                "EnemyData": (
                    {
                        location_id.name: {"map": enemy_loc.map.name, "enemy": enemy_loc.enemy.name}
                        for location_id, enemy_loc in self.spoiler.enemy_location_list.items()
                        if EnemyMetaData[enemy_loc.enemy].e_type == EnemySubtype.GroundBeefy
                    }
                    if self.options.dropsanity.value
                    else {}
                ),
                "Shopkeepers": self.options.shopowners_in_pool.value,
                "HalfMedals": self.options.half_medals_in_pool.value,
                "MinigameData": ({location_id.name: minigame_data.minigame.name for location_id, minigame_data in self.spoiler.shuffled_barrel_data.items()}),
                "Autocomplete": self.options.auto_complete_bonus_barrels.value,
                "HelmBarrelCount": self.options.helm_room_bonus_count.value,
                "CrownDoorItem": self.spoiler.settings.crown_door_item.name,
                "CrownDoorItemCount": self.spoiler.settings.crown_door_item_count,
                "CoinDoorItem": self.spoiler.settings.coin_door_item.name,
                "CoinDoorItemCount": self.spoiler.settings.coin_door_item_count,
                "SmallerShopsData": self.get_smaller_shops_data(),
                "ShopPrices": (
                    {
                        (location_id.name if hasattr(location_id, "name") else str(location_id)): price
                        for location_id, price in self.spoiler.settings.prices.items()
                        if location_id in self.spoiler.LocationList and self.spoiler.LocationList[location_id].type == Types.Shop
                    }
                    if hasattr(self.spoiler.settings, "prices")
                    else {}
                ),
                "HintLocationMapping": hint_mapping,
                "hints": {str(location): hint_data for location, hint_data in dynamic_hints.items()},
                "EntranceRando": (
                    {source_exit: target_entrance for source_exit, target_entrance in self.er_placement_state.pairings}
                    if self.spoiler.settings.level_randomization == LevelRandomization.loadingzone and self.spoiler.shuffled_exit_data
                    else {}
                ),
            }
            return slot_data

        def write_spoiler(self, spoiler_handle: typing.TextIO):
            """Write the spoiler."""
            spoiler_handle.write("\n")
            spoiler_handle.write("Additional Settings info for player: " + self.player_name)
            spoiler_handle.write("\n")
            spoiler_handle.write(f"Goal: {pp_wincon(self.spoiler.settings.win_condition_item, self.spoiler.settings.win_condition_count)}")
            spoiler_handle.write("\n")
            spoiler_handle.write("Level Order: " + ", ".join([level.name for order, level in self.spoiler.settings.level_order.items()]))
            spoiler_handle.write("\n")
            human_boss_order = []
            for i in range(len(self.spoiler.settings.boss_maps)):
                human_boss_order.append(boss_map_names[self.spoiler.settings.boss_maps[i]])
            spoiler_handle.write("Boss Order: " + ", ".join(human_boss_order))
            spoiler_handle.write("\n")
            spoiler_handle.write("Starting Kongs: " + ", ".join([kong.name for kong in self.spoiler.settings.starting_kong_list]))
            spoiler_handle.write("\n")
            spoiler_handle.write("Helm Order: " + ", ".join([Kongs(room).name for room in self.spoiler.settings.helm_order]))
            spoiler_handle.write("\n")
            spoiler_handle.write("K. Rool Order: " + ", ".join([phase.name for phase in self.spoiler.settings.krool_order]))
            spoiler_handle.write("\n")
            spoiler_handle.write("Forest Time: " + self.spoiler.settings.fungi_time_internal.name)
            spoiler_handle.write("\n")
            spoiler_handle.write("Galleon Water: " + self.spoiler.settings.galleon_water_internal.name)
            spoiler_handle.write("\n")
            spoiler_handle.write("CBs for Medal: " + str(self.spoiler.settings.medal_cb_req))
            spoiler_handle.write("\n")
            # Include both barrier type and count for B. Lockers
            blocker_requirements = []
            for i, (barrier_type, count) in enumerate(zip(self.spoiler.settings.BLockerEntryItems, self.spoiler.settings.BLockerEntryCount)):
                level_names = ["Japes", "Aztec", "Factory", "Galleon", "Forest", "Caves", "Castle", "Helm"]
                blocker_requirements.append(f"{level_names[i]}: {count} {barrier_type.name}")
            spoiler_handle.write("B. Locker Requirements: " + ", ".join(blocker_requirements))
            spoiler_handle.write("\n")
            spoiler_handle.write("Removed Barriers: " + ", ".join([barrier.name for barrier in self.spoiler.settings.remove_barriers_selected]))
            spoiler_handle.write("\n")
            if (
                hasattr(self.spoiler.settings, "switchsanity_enabled")
                and self.spoiler.settings.switchsanity_enabled
                and hasattr(self.spoiler.settings, "switchsanity_data")
                and self.spoiler.settings.switchsanity_data
            ):
                spoiler_handle.write("Switchsanity Settings: \n")
                for switch, data in self.spoiler.settings.switchsanity_data.items():
                    kong_name = data.kong.name if hasattr(data.kong, "name") else Kongs(data.kong).name
                    switch_type_name = data.switch_type.name if hasattr(data.switch_type, "name") else SwitchType(data.switch_type).name
                    spoiler_handle.write(f"  - {switch.name}: {kong_name} with {switch_type_name}\n")
            if not self.spoiler.settings.bonus_barrel_auto_complete and self.spoiler.settings.minigames_list_selected:
                spoiler_handle.write("Shuffled Bonus Barrels: \n")
                for loc, minigame in self.spoiler.shuffled_barrel_data.items():
                    spoiler_handle.write(f" - {loc.name}: {minigame.minigame.name}\n")
            spoiler_handle.write("Generated Time: " + time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()) + " GMT")
            spoiler_handle.write("\n")
            spoiler_handle.write("Randomizer Version: " + self.spoiler.settings.version)
            spoiler_handle.write("\n")
            spoiler_handle.write("APWorld Version: " + self.ap_version)
            spoiler_handle.write("\n")

            # Write entrance randomization data if LZR is enabled
            if self.spoiler.settings.level_randomization == LevelRandomization.loadingzone and self.spoiler.shuffled_exit_data:
                from randomizer.Lists.ShufflableExit import ShufflableExits

                spoiler_handle.write("\n")
                spoiler_handle.write("=== Entrance Randomization (Loading Zone Randomizer) ===\n")
                # Sort by transition name for readability
                sorted_exits = sorted(self.spoiler.shuffled_exit_data.items(), key=lambda x: x[0].name)
                for transition_enum, shuffled_back in sorted_exits:
                    source_exit = ShufflableExits[transition_enum]
                    # Find the ShufflableExit that contains this TransitionBack to get the full descriptive name
                    dest_exit_name = shuffled_back.name  # Fallback to short name
                    for other_transition, other_exit in ShufflableExits.items():
                        if other_exit.back == shuffled_back:
                            dest_exit_name = other_exit.name
                            break
                    spoiler_handle.write(f"{source_exit.name} -> {dest_exit_name}\n")
                spoiler_handle.write("\n")

            # Write shop prices
            spoiler_handle.write("\n")
            spoiler_handle.write("=== Shop Prices ===\n")

            # Get price shopprices name
            price_shopprices_names = {0: "Free", 1: "Easy", 2: "Medium", 3: "Hard"}
            shopprices_name = price_shopprices_names.get(self.options.shop_prices.value, "Unknown")
            spoiler_handle.write(f"Price Difficulty: {shopprices_name}\n")
            spoiler_handle.write("\n")

            # Progressive moves
            from randomizer.Enums.Items import Items as DK64RItems

            progressive_moves = {
                DK64RItems.ProgressiveSlam: "Progressive Slam",
                DK64RItems.ProgressiveAmmoBelt: "Progressive Ammo Belt",
                DK64RItems.ProgressiveInstrumentUpgrade: "Progressive Instrument Upgrade",
            }

            spoiler_handle.write("Progressive Move Prices:\n")
            for item_id, item_name in progressive_moves.items():
                if item_id in self.spoiler.settings.prices:
                    prices = self.spoiler.settings.prices[item_id]
                    if isinstance(prices, list):
                        price_str = ", ".join([str(p) for p in prices])
                        spoiler_handle.write(f"  {item_name}: [{price_str}]\n")

            spoiler_handle.write("\n")
            spoiler_handle.write("Shop Location Prices:\n")

            # Organize shop locations by vendor and level
            from randomizer.Enums.Locations import Locations as DK64RLocations

            shop_prices_by_location = []
            for location_id, location in self.spoiler.LocationList.items():
                if location.type == Types.Shop and location_id in self.spoiler.settings.prices:
                    price = self.spoiler.settings.prices[location_id]
                    shop_prices_by_location.append((location.name, price))

            # Sort alphabetically by location name
            shop_prices_by_location.sort(key=lambda x: x[0])

            for location_name, price in shop_prices_by_location:
                spoiler_handle.write(f"  {location_name}: {price} coins\n")

            spoiler_handle.write("\n")

        def create_item(self, name: str, force_non_progression=False) -> Item:
            """Create an item."""
            data = full_item_table[name]

            if force_non_progression:
                classification = ItemClassification.filler
            elif data.progression:
                classification = ItemClassification.progression
            elif hasattr(self.multiworld, "generation_is_fake"):
                # UT needs to classify things as progression or it won't track them
                classification = ItemClassification.progression
            else:
                classification = ItemClassification.filler

            created_item = DK64Item(name, classification, data.code, self.player)

            return created_item

        def isMajorItem(self, item: DK64Item):
            """Determine whether a DK64Item is a Major Item."""
            # Events, colored bananas, tokens
            if "," in item.name or "Boss Defeated" in item.name or "Bonus Completed" in item.name:
                return False
            # Not progression
            if item.classification != ItemClassification.progression and item.classification != ItemClassification.progression_skip_balancing:
                return False
            # Golden bananas and blueprints
            if item.name == "Golden Banana" or "Blueprint" in item.name:
                return False
            # Hints, medals, Company coins, Banana fairies, Crowns
            if "Hint" in item.name or item.name == "Banana Medal" or "Coin" in item.name or item.name == "Banana Fairy" or item.name == "Battle Crown":
                return False
            # Helm barrels
            if "Helm" in item.name and "Barrel" in item.name:
                return False
            # Misc items
            if item.name == "Pearl" or "Hoard" in item.name:
                return False
            return True

        def location_starts_empty(self, location: Location):
            """Check if a location starts empty based on item type and location type."""
            loc_obj = None
            item_obj = None
            # Events, collectables
            if ", " in location.item.name:
                return False
            if location.item.name == "BananaHoard":
                return False
            if location.item.name == "Boss Defeated" or location.item.name == "Bonus Completed":
                return False
            for loc in self.spoiler.LocationList.keys():
                if self.spoiler.LocationList[loc].name == location.name:
                    loc_obj = self.spoiler.LocationList[loc]
            for item in DK64RItem.ItemList.keys():
                if DK64RItem.ItemList[item].name == location.item.name:
                    item_obj = DK64RItem.ItemList[item]
            # Completely empty location. Can this happen? No? Anyway...
            if location.item is None:
                return True
            # NoItem
            if location.item.name == "No Item":
                return True
            # Junk item
            if item_obj is None:
                print(location.item.name)
                # TODO, figure out crash
                print(f"{item.name}, PLEASE REPORT THIS PRINT!!!!! It's the error, and I don't want to make it crash if I don't have to!")
                # raise Exception(f"{item.name} not found in ItemList. (Yes I made it crash again, no it shouldn't run on non-donk games)")
                return True
            if item_obj.type == Types.JunkItem:
                # In a location that can't have junk
                if loc_obj.type in (Types.Shop, Types.Shockwave, Types.Crown, Types.PreGivenMove, Types.CrateItem, Types.Enemies, Types.HalfMedal) or (
                    loc_obj.type == Types.Key or loc_obj.level == Levels.HideoutHelm
                ):
                    return True
            return False

        def updateBossKongs(self, spoiler):
            """Prevent a bug with microhints hinting boss locations as if they were Any Kong locations."""
            locations = {
                DK64RLocations.JapesKey: spoiler.settings.boss_kongs[Levels.JungleJapes],
                DK64RLocations.AztecKey: spoiler.settings.boss_kongs[Levels.AngryAztec],
                DK64RLocations.FactoryKey: spoiler.settings.boss_kongs[Levels.FranticFactory],
                DK64RLocations.GalleonKey: spoiler.settings.boss_kongs[Levels.GloomyGalleon],
                DK64RLocations.ForestKey: spoiler.settings.boss_kongs[Levels.FungiForest],
                DK64RLocations.CavesKey: spoiler.settings.boss_kongs[Levels.CrystalCaves],
                DK64RLocations.CastleKey: spoiler.settings.boss_kongs[Levels.CreepyCastle],
            }

            for loc in locations.keys():
                spoiler.LocationList[loc].kong = locations[loc]

        def collect(self, state: CollectionState, item: Item) -> bool:
            """Collect the item."""
            change = super().collect(state, item)
            if change:
                if self.player in state.dk64_logic_holder.keys():
                    state.dk64_logic_holder[self.player].AddArchipelagoItem(item)
                elif hasattr(self, "spoiler"):
                    state.dk64_logic_holder[self.player] = LogicVarHolder(self.spoiler, self.player)  # If the CollectionState dodged the creation of a logic_holder object, fix it here
                    state.dk64_logic_holder[self.player].UpdateFromArchipelagoItems(state)
            return change

        def remove(self, state: CollectionState, item: Item) -> bool:
            """Remove the item."""
            change = super().remove(state, item)
            if change:
                if self.player in state.dk64_logic_holder.keys():
                    state.dk64_logic_holder[self.player].RemoveArchipelagoItem(item)
                elif hasattr(self, "spoiler"):
                    state.dk64_logic_holder[self.player] = LogicVarHolder(self.spoiler, self.player)  # If the CollectionState dodged the creation of a logic_holder object, fix it here
                    state.dk64_logic_holder[self.player].UpdateFromArchipelagoItems(state)
            return change

        def _update_entrance_connections(self, state: CollectionState) -> None:
            """Update the entrance_connections dictionary with all reachable connected entrances."""
            self.entrance_connections.clear()
            if self.player in state.reachable_regions:
                regions_copy = list(state.reachable_regions[self.player])
                for region in regions_copy:
                    for entrance in region.exits:
                        if entrance.can_reach(state) and entrance.connected_region is not None:
                            self.entrance_connections[entrance.name] = entrance.connected_region.name

        def version_check(self, version: str, req_version: str) -> bool:
            """Check if the current version is greater than or equal to the one required for this slot data."""
            req_major = req_version.split(".")[0]
            req_minor = req_version.split(".")[1]
            req_patch = req_version.split(".")[2]

            version_major = version.split(".")[0]
            version_minor = version.split(".")[1]
            version_patch = version.split(".")[2]

            return (int(version_major), int(version_minor), int(version_patch)) >= (int(req_major), int(req_minor), int(req_patch))

        def interpret_slot_data(self, slot_data: dict[str, any]) -> dict[str, any]:
            """Parse slot data for any logical bits that need to match the real generation. Used by Universal Tracker."""
            # Parse the string data
            version = slot_data["Version"]
            if version != self.ap_version:
                print(f"Version mismatch: {version} != {self.ap_version}. You may experience unexpected behavior.")

            level_order = slot_data["LevelOrder"].split(", ")
            starting_kongs = slot_data["StartingKongs"].split(", ")
            medal_cb_req = slot_data["MedalCBRequirement"]
            fairy_req = slot_data["FairyRequirement"]
            pearl_req = slot_data["MermaidPearls"]
            jetpac_req = slot_data["JetpacReq"]
            boss_bananas = slot_data["BossBananas"].split(", ")
            boss_maps = slot_data["BossMaps"].split(", ")
            boss_kongs = slot_data["BossKongs"].split(", ")
            helm_order = slot_data["HelmOrder"].split(", ")
            open_lobbies = slot_data["OpenLobbies"]
            switchsanity = slot_data["SwitchSanity"]
            logic_type = slot_data["LogicType"]
            glitches_selected = slot_data["GlitchesSelected"].split(", ")
            starting_key_list = slot_data["StartingKeyList"].split(", ")
            progressive_switch_strength = slot_data.get("ProgressiveSwitchStrength", False)
            slam_levels_str = slot_data.get("SlamLevels", "")
            junk = slot_data["Junk"]
            blocker_data = list(map(lambda original_string: original_string[original_string.find(":") + 2 :], slot_data["BLockerValues"].split(", ")))
            blocker_item_type = list(map(lambda data: data.split(" ")[1], blocker_data))
            blocker_item_quantity = list(map(lambda data: int(data.split(" ")[0]), blocker_data))
            galleon_water = slot_data.get("GalleonWater", "lowered")

            if self.version_check(version, "1.1.0"):
                tricks_selected = slot_data.get("TricksSelected", []).split(", ")
                boulders_in_pool = slot_data.get("BouldersInPool", False)
                dropsanity = slot_data.get("Dropsanity", False)
                enemy_data = slot_data.get("EnemyData", {})
                shopkeepers = slot_data.get("Shopkeepers", False)
            else:
                raise ValueError(f"This world is generated with an old version of DK64 Randomizer. Please downgrade to the correct version: {version}.")

            # Added in half-medals/progressive medal reqs update
            if self.version_check(version, "1.1.11"):
                medal_cb_requirement_level = list(map(lambda lvl_and_value: lvl_and_value[lvl_and_value.find(":") + 2 :], slot_data["MedalCBRequirementLevel"].split(", ")))
                half_medals = slot_data["HalfMedals"]
            else:
                medal_cb_requirement_level = {}
                half_medals = False

            # Added in the bonus barrels update
            if self.version_check(version, "1.1.13"):
                minigame_data = slot_data["MinigameData"]
                autocomplete = slot_data["Autocomplete"]
                helm_barrel_count = slot_data["HelmBarrelCount"]
            else:
                minigame_data = {}
                autocomplete = True
                helm_barrel_count = 0

            # Added helm door settings
            if self.version_check(version, "1.4.16"):
                crown_door_item = slot_data.get("CrownDoorItem", "opened")
                crown_door_item_count = slot_data.get("CrownDoorItemCount", 1)
                coin_door_item = slot_data.get("CoinDoorItem", "opened")
                coin_door_item_count = slot_data.get("CoinDoorItemCount", 1)
            else:
                crown_door_item = "opened"
                crown_door_item_count = 1
                coin_door_item = "opened"
                coin_door_item_count = 1

            # Added smaller shops data visibility
            if self.version_check(version, "1.1.14"):
                smaller_shops_data = slot_data.get("SmallerShopsData", {})
            else:
                smaller_shops_data = {}

            # Added shop prices for UT
            if self.version_check(version, "1.4.11"):
                shop_prices = slot_data.get("ShopPrices", {})
            else:
                shop_prices = {}

            # Added entrance randomization data
            entrance_rando = slot_data.get("EntranceRando", [])

            relevant_data = {}
            relevant_data["LevelOrder"] = dict(enumerate([Levels[level] for level in level_order], start=1))
            relevant_data["StartingKongs"] = [Kongs[kong] for kong in starting_kongs]
            relevant_data["MedalCBRequirement"] = medal_cb_req
            relevant_data["MedalCBRequirementLevel"] = medal_cb_requirement_level
            relevant_data["FairyRequirement"] = fairy_req
            relevant_data["MermaidPearls"] = pearl_req
            relevant_data["JetpacReq"] = jetpac_req
            relevant_data["BossBananas"] = [int(cost) for cost in boss_bananas]
            relevant_data["BossMaps"] = [Maps[map] for map in boss_maps]
            relevant_data["BossKongs"] = [Kongs[kong] for kong in boss_kongs]
            relevant_data["LankyFreeingKong"] = slot_data["LankyFreeingKong"]
            relevant_data["HelmOrder"] = [int(room) for room in helm_order]
            relevant_data["SwitchSanity"] = switchsanity
            relevant_data["OpenLobbies"] = open_lobbies
            relevant_data["LogicType"] = logic_type
            relevant_data["TricksSelected"] = [TricksSelected[trick] for trick in tricks_selected if trick != ""]
            relevant_data["GlitchesSelected"] = [GlitchesSelected[glitch] for glitch in glitches_selected if glitch != ""]
            relevant_data["StartingKeyList"] = [DK64RItems[key] for key in starting_key_list if key != ""]
            relevant_data["ProgressiveSwitchStrength"] = progressive_switch_strength
            if progressive_switch_strength and slam_levels_str:
                slam_levels_list = []
                for level_slam in slam_levels_str.split(", "):
                    if ": " in level_slam:
                        slam_name = level_slam.split(": ")[1]
                        slam_levels_list.append(SlamRequirement[slam_name])
                relevant_data["SlamLevels"] = slam_levels_list
            else:
                relevant_data["SlamLevels"] = []
            relevant_data["JunkedLocations"] = junk
            relevant_data["BLockerEntryItems"] = [BarrierItems[item] for item in blocker_item_type]
            relevant_data["BLockerEntryCount"] = blocker_item_quantity
            relevant_data["HintsInPool"] = slot_data["HintsInPool"]
            relevant_data["BouldersInPool"] = boulders_in_pool
            relevant_data["Dropsanity"] = dropsanity
            relevant_data["EnemyData"] = enemy_data
            relevant_data["Shopkeepers"] = shopkeepers
            relevant_data["MinigameData"] = minigame_data
            relevant_data["Autocomplete"] = autocomplete
            relevant_data["HelmBarrelCount"] = helm_barrel_count
            relevant_data["CrownDoorItem"] = crown_door_item
            relevant_data["CrownDoorItemCount"] = crown_door_item_count
            relevant_data["CoinDoorItem"] = coin_door_item
            relevant_data["CoinDoorItemCount"] = coin_door_item_count
            relevant_data["HalfMedals"] = half_medals
            relevant_data["SmallerShopsData"] = smaller_shops_data
            relevant_data["ShopPrices"] = shop_prices
            relevant_data["EntranceRando"] = entrance_rando
            relevant_data["GalleonWater"] = galleon_water
            return relevant_data
