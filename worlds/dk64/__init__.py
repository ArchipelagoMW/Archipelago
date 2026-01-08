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


from BaseClasses import Location
from worlds.dk64.ap_version import version as ap_version

baseclasses_loaded = False
try:
    from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification, CollectionState
    import BaseClasses
    import settings

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
        zip_path = "vendor/linux.zip"
        copy_dependencies(zip_path, "linux.zip")
    else:
        raise Exception(f"Unsupported platform: {platform_type}")

    sys.path.append("worlds/dk64/")
    sys.path.append("worlds/dk64/archipelago/")
    sys.path.append("custom_worlds/dk64.apworld/dk64/")
    sys.path.append("custom_worlds/dk64.apworld/dk64/archipelago/")

    import randomizer.ItemPool as DK64RItemPool

    from randomizer.Enums.Items import Items as DK64RItems
    from randomizer.SettingStrings import decrypt_settings_string_enum
    from archipelago.Items import DK64Item, full_item_table, setup_items
    from archipelago.Options import DK64Options, Goal
    from archipelago.Regions import all_locations, create_regions, connect_regions
    from archipelago.Rules import set_rules
    from archipelago.client.common import check_version
    from worlds.AutoWorld import WebWorld, World, AutoLogicRegister
    from archipelago.Logic import LogicVarHolder, logic_item_name_to_id
    from randomizer.Spoiler import Spoiler
    from randomizer.Settings import Settings
    from randomizer.ShuffleWarps import LinkWarps
    from randomizer.Enums.Settings import LogicType, ShuffleLoadingZones
    from randomizer.Patching.ApplyRandomizer import patching_response
    from version import version
    from randomizer.Patching.EnemyRando import randomize_enemies_0
    from randomizer.Fill import ShuffleItems, Generate_Spoiler, IdentifyMajorItems
    from randomizer.CompileHints import compileMicrohints
    from archipelago.Hints import CompileArchipelagoHints
    from randomizer.Enums.Types import Types, BarrierItems
    from randomizer.Enums.Kongs import Kongs
    from randomizer.Enums.Levels import Levels
    from randomizer.Enums.Maps import Maps
    from randomizer.Enums.Locations import Locations as DK64RLocations
    from randomizer.Enums.Settings import WinConditionComplex, SwitchsanityLevel, GlitchesSelected, MicrohintsEnabled, HardModeSelected, RemovedBarriersSelected, ItemRandoListSelected
    from randomizer.Enums.Switches import Switches
    from randomizer.Enums.SwitchTypes import SwitchType
    from randomizer.Lists import Item as DK64RItem
    from randomizer.Lists.Switches import SwitchInfo
    from worlds.LauncherComponents import Component, components, Type, icon_paths
    import randomizer.ShuffleExits as ShuffleExits
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

    components.append(Component("DK64 Client", "DK64Client", func=launch_client, component_type=Type.CLIENT, icon="dk64"))
    icon_paths["dk64"] = f"ap:{__name__}/base-hack/assets/DKTV/logo3.png"

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

        release_branch: ReleaseVersion = ReleaseVersion("master")

    class DK64Web(WebWorld):
        """WebWorld for DK64."""

        theme = "jungle"

        setup_en = Tutorial("Multiworld Setup Guide", "A guide to setting up the Donkey Kong 64 randomizer connected to an Archipelago Multiworld.", "English", "setup_en.md", "setup/en", ["PoryGone"])

        tutorials = [setup_en]

    class DK64World(World):
        """Donkey Kong 64 is a 3D collectathon platforming game.

        Play as the whole DK Crew and rescue the Golden Banana hoard from King K. Rool.
        """

        game: str = "Donkey Kong 64"
        options_dataclass = DK64Options
        options: DK64Options
        topology_present = False
        settings: typing.ClassVar[DK64Settings]

        item_name_to_id = {name: data.code for name, data in full_item_table.items()}
        location_name_to_id = all_locations

        web = DK64Web()

        def __init__(self, multiworld: MultiWorld, player: int):
            """Initialize the DK64 world."""
            self.rom_name_available_event = threading.Event()
            self.hint_data_available = threading.Event()
            super().__init__(multiworld, player)

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

        def _get_slot_data(self):
            """Get the slot data."""
            return {
                # "death_link": self.options.death_link.value,
            }

        def generate_early(self):
            """Generate the world."""
            # V1 LIMITATION: We are restricting settings pretty heavily. This string serves as the base for all seeds, with AP options overriding some options
            self.settings_string = "fjNPxAMxDIUx0QSpbHPUlZlBLg5gPQ+oBwRDIhKlsa58Iz8fiNEpEtiFKi4bVAhMF6AAd+AAOCAAGGAAGKAAAdm84FBiMhjoStwFIKW2wLcBJIBpmTVRCjFIKUUwGTLK/BQBuAIMAN4CBwBwAYQAOIECQByAoUAOYGCwB0A4YeXIITIagOrIrwAZTiU1QwkoSjuq1ZLEjQxUKi2oy9FRFgETEUAViyxyN2S8XeRQOQ7GXtOQM8nGDIAyqcEQgAFwoAFwwAEw4AExAAD1oADxIACxQABxYADxgACxoAB1wAFp8r0CS5UtnsshhHMk9Gw+M1drAwGcuqwqis0FMqLRjilACgrBovKATiotEkXENPGtLINIiNdHYAHQC8KggJCgsMDQ4QERIUFRYYGRocHR4gISIjJCUmJygpKissLS4vMDEyMzQ1rL4AwADCAMQAnQCyAGkAUQA"
            settings_dict = decrypt_settings_string_enum(self.settings_string)
            settings_dict["archipelago"] = True
            settings_dict["starting_kongs_count"] = self.options.starting_kong_count.value
            settings_dict["open_lobbies"] = self.options.open_lobbies.value
            settings_dict["krool_in_boss_pool"] = self.options.krool_in_boss_pool.value
            settings_dict["helm_phase_count"] = self.options.helm_phase_count.value
            settings_dict["krool_phase_count"] = self.options.krool_phase_count.value
            settings_dict["medal_cb_req"] = self.options.medal_cb_req.value
            settings_dict["randomize_blocker_required_amounts"] = self.options.randomize_blocker_required_amounts.value
            settings_dict["blocker_text"] = self.options.blocker_max.value
            settings_dict["mermaid_gb_pearls"] = self.options.mermaid_gb_pearls.value
            blocker_options = [
                self.options.level1_blocker,
                self.options.level2_blocker,
                self.options.level3_blocker,
                self.options.level4_blocker,
                self.options.level5_blocker,
                self.options.level6_blocker,
                self.options.level7_blocker,
                self.options.level8_blocker,
            ]

            for i, blocker in enumerate(blocker_options):
                settings_dict[f"blocker_{i}"] = blocker.value
            settings_dict["item_rando_list_selected"] = []

            always_enabled_categories = [
                ItemRandoListSelected.shop,
                ItemRandoListSelected.banana,
                ItemRandoListSelected.toughbanana,
                ItemRandoListSelected.crown,
                ItemRandoListSelected.blueprint,
                ItemRandoListSelected.key,
                ItemRandoListSelected.medal,
                ItemRandoListSelected.nintendocoin,
                ItemRandoListSelected.kong,
                ItemRandoListSelected.fairy,
                ItemRandoListSelected.rainbowcoin,
                ItemRandoListSelected.beanpearl,
                ItemRandoListSelected.junkitem,
                ItemRandoListSelected.crateitem,
                ItemRandoListSelected.rarewarecoin,
                ItemRandoListSelected.shockwave,
            ]
            settings_dict["item_rando_list_selected"].extend(always_enabled_categories)

            if self.options.hints_in_item_pool.value:
                settings_dict["item_rando_list_selected"].append(ItemRandoListSelected.hint)

            settings_dict["medal_requirement"] = self.options.medal_requirement.value
            settings_dict["rareware_gb_fairies"] = self.options.rareware_gb_fairies.value
            settings_dict["mirror_mode"] = self.options.mirror_mode.value
            if hasattr(self.multiworld, "generation_is_fake") and hasattr(self.multiworld, "re_gen_passthrough") and "Donkey Kong 64" in self.multiworld.re_gen_passthrough:
                settings_dict["hard_shooting"] = self.multiworld.re_gen_passthrough["Donkey Kong 64"]["HardShooting"]
            else:
                settings_dict["hard_shooting"] = self.options.hard_shooting.value
            settings_dict["hard_mode"] = self.options.hard_mode.value
            settings_dict["hard_mode_selected"] = []
            for hard in self.options.hard_mode_selected:
                if hard == "hard_enemies":
                    settings_dict["hard_mode_selected"].append(HardModeSelected.hard_enemies)
                elif hard == "shuffled_jetpac_enemies":
                    settings_dict["hard_mode_selected"].append(HardModeSelected.shuffled_jetpac_enemies)
                elif hard == "strict_helm_timer":
                    settings_dict["hard_mode_selected"].append(HardModeSelected.strict_helm_timer)
                elif hard == "donk_in_the_dark_world":
                    settings_dict["hard_mode_selected"].append(HardModeSelected.donk_in_the_dark_world)
                elif hard == "donk_in_the_sky":
                    settings_dict["hard_mode_selected"].append(HardModeSelected.donk_in_the_sky)
            settings_dict["krool_key_count"] = self.options.krool_key_count.value
            if hasattr(self.multiworld, "generation_is_fake"):
                settings_dict["krool_key_count"] = 8  # if gen is fake, don't pick random keys to start with, trust the slot data
            settings_dict["switchsanity"] = self.options.switchsanity.value
            settings_dict["logic_type"] = self.options.logic_type.value
            settings_dict["remove_barriers_enabled"] = bool(self.options.remove_barriers_selected)
            settings_dict["remove_barriers_selected"] = []
            for barrier in self.options.remove_barriers_selected:
                if barrier == "japes_coconut_gates":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.japes_coconut_gates)
                elif barrier == "japes_shellhive_gate":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.japes_shellhive_gate)
                elif barrier == "aztec_tunnel_door":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.aztec_tunnel_door)
                elif barrier == "aztec_5dtemple_switches":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.aztec_5dtemple_switches)
                elif barrier == "aztec_llama_switches":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.aztec_llama_switches)
                elif barrier == "aztec_tiny_temple_ice":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.aztec_tiny_temple_ice)
                elif barrier == "factory_testing_gate":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.factory_testing_gate)
                elif barrier == "factory_production_room":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.factory_production_room)
                elif barrier == "galleon_lighthouse_gate":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.galleon_lighthouse_gate)
                elif barrier == "galleon_shipyard_area_gate":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.galleon_shipyard_area_gate)
                elif barrier == "castle_crypt_doors":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.castle_crypt_doors)
                elif barrier == "galleon_seasick_ship":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.galleon_seasick_ship)
                elif barrier == "forest_green_tunnel":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.forest_green_tunnel)
                elif barrier == "forest_yellow_tunnel":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.forest_yellow_tunnel)
                elif barrier == "caves_igloo_pads":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.caves_igloo_pads)
                elif barrier == "caves_ice_walls":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.caves_ice_walls)
                elif barrier == "galleon_treasure_room":
                    settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.galleon_treasure_room)
            settings_dict["glitches_selected"] = []
            for glitch in self.options.glitches_selected:
                if glitch == "advanced_platforming":
                    settings_dict["glitches_selected"].append(GlitchesSelected.advanced_platforming)
                elif glitch == "moonkicks":
                    settings_dict["glitches_selected"].append(GlitchesSelected.moonkicks)
                elif glitch == "phase_swimming":
                    settings_dict["glitches_selected"].append(GlitchesSelected.phase_swimming)
                elif glitch == "swim_through_shores":
                    settings_dict["glitches_selected"].append(GlitchesSelected.swim_through_shores)
                elif glitch == "troff_n_scoff_skips":
                    settings_dict["glitches_selected"].append(GlitchesSelected.troff_n_scoff_skips)
                elif glitch == "moontail":
                    settings_dict["glitches_selected"].append(GlitchesSelected.moontail)
            settings_dict["starting_keys_list_selected"] = []
            for item in self.options.start_inventory:
                if item == "Key 1":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.JungleJapesKey)
                elif item == "Key 2":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.AngryAztecKey)
                elif item == "Key 3":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.FranticFactoryKey)
                elif item == "Key 4":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.GloomyGalleonKey)
                elif item == "Key 5":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.FungiForestKey)
                elif item == "Key 6":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.CrystalCavesKey)
                elif item == "Key 7":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.CreepyCastleKey)
                elif item == "Key 8":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.HideoutHelmKey)
            if self.options.goal == Goal.option_all_keys:
                settings_dict["win_condition_item"] = WinConditionComplex.req_key
                settings_dict["win_condition_count"] = 8
            if self.options.goal == Goal.option_dk_rap:
                settings_dict["win_condition_item"] = WinConditionComplex.dk_rap_items
            settings = Settings(settings_dict, self.random)
            # Archipelago really wants the number of locations to match the number of items. Keep track of how many locations we've made here
            settings.location_pool_size = 0
            # Set all the static slot data that UT needs to know. Most of these would have already been decided in normal generation by now, so they are just overwritten here.
            if hasattr(self.multiworld, "generation_is_fake"):
                if hasattr(self.multiworld, "re_gen_passthrough"):
                    if "Donkey Kong 64" in self.multiworld.re_gen_passthrough:
                        passthrough = self.multiworld.re_gen_passthrough["Donkey Kong 64"]
                        settings.level_order = passthrough["LevelOrder"]
                        # Switch logic lifted out of level shuffle due to static levels for UT
                        if settings.alter_switch_allocation:
                            allocation = [1, 1, 1, 1, 2, 2, 3, 3]
                            for x in range(8):
                                level = settings.level_order[x + 1]
                                settings.switch_allocation[level] = allocation[x]
                        settings.starting_kong_list = passthrough["StartingKongs"]
                        settings.starting_kong = settings.starting_kong_list[0]  # fake a starting kong so that we don't force a different kong
                        settings.medal_requirement = passthrough["JetpacReq"]
                        settings.rareware_gb_fairies = passthrough["FairyRequirement"]
                        settings.BLockerEntryItems = passthrough["BLockerEntryItems"]
                        settings.BLockerEntryCount = passthrough["BLockerEntryCount"]
                        settings.medal_cb_req = passthrough["MedalCBRequirement"]
                        settings.mermaid_gb_pearls = passthrough["MermaidPearls"]
                        settings.BossBananas = passthrough["BossBananas"]
                        settings.boss_maps = passthrough["BossMaps"]
                        settings.boss_kongs = passthrough["BossKongs"]
                        settings.lanky_freeing_kong = passthrough["LankyFreeingKong"]
                        settings.helm_order = passthrough["HelmOrder"]
                        settings.logic_type = LogicType[passthrough["LogicType"]]
                        settings.glitches_selected = passthrough["GlitchesSelected"]
                        settings.open_lobbies = passthrough["OpenLobbies"]
                        settings.starting_key_list = passthrough["StartingKeyList"]
                        # There's multiple sources of truth for helm order.
                        settings.helm_donkey = 0 in settings.helm_order
                        settings.helm_diddy = 4 in settings.helm_order
                        settings.helm_lanky = 3 in settings.helm_order
                        settings.helm_tiny = 2 in settings.helm_order
                        settings.helm_chunky = 1 in settings.helm_order
                        # Switchsanity
                        for switch, data in passthrough["SwitchSanity"].items():
                            needed_kong = Kongs[data["kong"]]
                            switch_type = SwitchType[data["type"]]
                            settings.switchsanity_data[Switches[switch]] = SwitchInfo(switch, needed_kong, switch_type, 0, 0, [])
                        for loc in passthrough["JunkedLocations"]:
                            del self.location_name_to_id[loc]
            # We need to set the freeing kongs here early, as they won't get filled in any other part of the AP process
            settings.diddy_freeing_kong = self.random.randint(0, 4)
            # Lanky freeing kong actually changes logic, so UT should use the slot data rather than genning a new one.
            if not hasattr(self.multiworld, "generation_is_fake"):
                settings.lanky_freeing_kong = self.random.randint(0, 4)
            settings.tiny_freeing_kong = self.random.randint(0, 4)
            settings.chunky_freeing_kong = self.random.randint(0, 4)
            self.spoiler = Spoiler(settings)
            # Undo any changes to this location's name, until we find a better way to prevent this from confusing the tracker and the AP code that is responsible for sending out items
            self.spoiler.LocationList[DK64RLocations.FactoryDonkeyDKArcade].name = "Factory Donkey DK Arcade Round 1"
            self.spoiler.settings.shuffled_location_types.append(Types.ArchipelagoItem)

            for item in self.options.start_inventory:
                item_obj = DK64RItem.ItemList[logic_item_name_to_id.get(item)]
                if item_obj.type not in [Types.Key, Types.Shop, Types.Shockwave, Types.TrainingBarrel, Types.Climbing]:
                    # Ensure that the items in the start inventory are only keys, shops, shockwaves, training barrels or climbing items
                    raise ValueError(f"Invalid item type for starting inventory: {item}. Starting inventory can only contain keys or moves.")

            Generate_Spoiler(self.spoiler)
            # Handle Loading Zones - this will handle LO and (someday?) LZR appropriately
            if self.spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.none:
                # UT should not reshuffle the level order, but should update the exits
                if not hasattr(self.multiworld, "generation_is_fake"):
                    ShuffleExits.ExitShuffle(self.spoiler, skip_verification=True)
                self.spoiler.UpdateExits()

            # Handle hint preparation by initiating some variables
            self.hint_data = {
                "kong": [],
                "key": [],
                "woth": [],
                "major": [],
                "deep": [],
            }
            self.foreignMicroHints = {}

            # Handle locations that start empty due to being junk
            self.junked_locations = []

        def create_regions(self) -> None:
            """Create the regions."""
            create_regions(self.multiworld, self.player, self.spoiler)

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
            LinkWarps(self.spoiler)  # I am very skeptical that this works at all - must be resolved if we want to do more than Isles warps preactivated
            connect_regions(self, self.spoiler.settings)

            self.multiworld.get_location("Banana Hoard", self.player).place_locked_item(DK64Item("Banana Hoard", ItemClassification.progression_skip_balancing, 0xD64060, self.player))  # TEMP?

        def generate_output(self, output_directory: str):
            """Generate the output."""
            try:
                spoiler = self.spoiler
                spoiler.settings.archipelago = True
                spoiler.settings.random = self.random
                spoiler.settings.player_name = self.multiworld.get_player_name(self.player)
                spoiler.first_move_item = None  # Not relevant with Fast Start always enabled
                spoiler.pregiven_items = []
                for item in self.multiworld.precollected_items[self.player]:
                    dk64_item = logic_item_name_to_id[item.name]
                    # Only moves can be pushed to the pregiven_items list
                    if DK64RItem.ItemList[dk64_item].type in [Types.Shop, Types.Shockwave, Types.TrainingBarrel, Types.Climbing]:
                        spoiler.pregiven_items.append(dk64_item)
                local_trap_count = 0
                ap_item_is_major_item = False
                self.junked_locations = []
                # Read through all item assignments in this AP world and find their DK64 equivalents so we can update our world state for patching purposes
                for ap_location in self.multiworld.get_locations(self.player):
                    # We never need to place Collectibles or Events in our world state
                    if "Collectible" in ap_location.name or "Event" in ap_location.name:
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
                            spoiler.LocationList[dk64_location_id].PlaceItem(spoiler, DK64RItems.ArchipelagoItem)
                            # If Jetpac has an progression AP item, we should hint is as if it were a major item
                            if dk64_location_id == DK64RLocations.RarewareCoin and ap_item.advancement:
                                ap_item_is_major_item = True
                        # Collectibles don't get placed in the LocationList
                        elif "Collectible" in ap_item.name:
                            continue
                        else:
                            dk64_item = logic_item_name_to_id[ap_item.name]
                            if dk64_item is not None:
                                if dk64_item in [DK64RItems.IceTrapBubble, DK64RItems.IceTrapReverse, DK64RItems.IceTrapSlow]:
                                    local_trap_count += 1

                                dk64_location = spoiler.LocationList[dk64_location_id]
                                # Most of these item restrictions should be handled by item rules, so this is a failsafe.
                                # Junk items can't be placed in shops, bosses, or arenas. Fortunately this is junk, so we can just patch a NoItem there instead.
                                # Shops are allowed to get Junk items placed by AP in order to artificially slightly reduce the number of checks in shops.
                                if DK64RItem.ItemList[dk64_item].type == Types.JunkItem and (dk64_location.type in [Types.Shop, Types.Key, Types.Crown]):
                                    dk64_item = DK64RItems.NoItem
                                    self.junked_locations.append(ap_location.name)
                                # Blueprints can't be on fairies for technical reasons. Instead we'll patch it in as an AP item and have AP handle it.
                                if dk64_item in DK64RItemPool.Blueprints() and dk64_location.type == Types.Fairy:
                                    dk64_item = DK64RItems.ArchipelagoItem
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
                microhints_enabled = True
                hints_enabled = True
                if hints_enabled or microhints_enabled:
                    self.hint_data_available.wait()

                if hints_enabled:
                    CompileArchipelagoHints(self, self.hint_data)

                if microhints_enabled:
                    # Finalize microhints
                    shopkeepers = [DK64RItems.Candy, DK64RItems.Cranky, DK64RItems.Funky, DK64RItems.Snide]
                    helm_prog_items = [DK64RItems.BaboonBlast, DK64RItems.BaboonBalloon, DK64RItems.Monkeyport, DK64RItems.GorillaGrab, DK64RItems.ChimpyCharge, DK64RItems.GorillaGone]
                    instruments = [DK64RItems.Bongos, DK64RItems.Guitar, DK64RItems.Trombone, DK64RItems.Saxophone, DK64RItems.Triangle]
                    hinted_slams = []
                    if DK64RItems.ProgressiveSlam in self.foreignMicroHints.keys() and DK64RItems.ProgressiveSlam in self.spoiler.microhints:
                        # Break down the slam hint to retrieve raw data
                        text1 = "Ladies and Gentlemen! It appears that one fighter has come unequipped to properly handle this reptilian beast. Perhaps they should have looked in "
                        hinted_slams = self.spoiler.microhints[DK64RItems.ProgressiveSlam].replace(text1, "")
                        hinted_slams.replace(" for the elusive slam.", "")
                        hinted_slams.split(" or ")
                    for hintedItem in self.foreignMicroHints.keys():
                        text = ""
                        if hintedItem in instruments or hintedItem in helm_prog_items:
                            text = f"\x07{self.foreignMicroHints[hintedItem][0]}\x07 would be better off looking in \x07{self.foreignMicroHints[hintedItem][1]}\x07 for this.".upper()
                        elif hintedItem == DK64RItems.ProgressiveSlam:
                            for slam in self.foreignMicroHints[DK64RItems.ProgressiveSlam]:
                                hinted_slams.append(f"\x07{slam[0]}: {slam[1]}\x07")
                            slam_text = " or ".join(hinted_slams)
                            text = f"Ladies and Gentlemen! It appears that one fighter has come unequipped to properly handle this reptilian beast. Perhaps they should have looked in {slam_text} for the elusive slam.".upper()
                        elif hintedItem in shopkeepers:
                            text = f"{hintedItem.name} has gone on a space mission to \x07{self.foreignMicroHints[hintedItem][0]} {self.foreignMicroHints[hintedItem][1]}\x07.".upper()
                        for letter in text:
                            if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
                                text = text.replace(letter, " ")
                        self.spoiler.microhints[DK64RItem.ItemList[hintedItem].name] = text

                spoiler.majorItems = IdentifyMajorItems(spoiler)
                if ap_item_is_major_item:
                    spoiler.majorItems.append(DK64RItems.ArchipelagoItem)
                patch_data, _ = patching_response(spoiler)
                patch_file = self.update_seed_results(patch_data, spoiler, self.player)
                out_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.lanky")
                print(out_path)
                # with open("output/" + f"{self.multiworld.get_out_file_name_base(self.player)}.lanky", "w") as f:
                with open(out_path, "w") as f:
                    f.write(patch_file)
                # Copy the patch file to the outpath
                # shutil.copy("output/" + f"{self.multiworld.get_out_file_name_base(self.player)}.lanky", out_path)
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
                players = {autoworld.player for autoworld in multiworld.get_game_worlds("Donkey Kong 64")}
                # Locations that could get a "deep locations" hint:
                deep_location_names = [
                    "Returning the Banana Fairies",
                    "Japes Diddy Minecart",
                    "Aztec Diddy Vulture Race",
                    "Aztec Tiny Beetle Race",
                    "Factory Donkey DK Arcade Round 1",
                    "Forest Chunky Minecart",
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
                    "Aztec Tiny Llama Temple Lava Pedestals",
                    "Galleon Chunky Cannon Game",
                    "Galleon Tiny Medal",
                    "Factory Chunky Toy Monster",
                    "Castle Tiny Car Race",
                    "Caves Dirt: Giant Kosha",
                    "Castle Lanky Tower",
                    "Castle Donkey Tree Sniping",
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
                    if players:
                        if loc.item.name in ("Donkey", "Diddy", "Lanky", "Tiny", "Chunky") and player in players:
                            autoworld.hint_data["kong"].append(loc)
                        if loc.item.name in ("Key 1", "Key 2", "Key 4", "Key 5") and player in players:
                            autoworld.hint_data["key"].append(loc)
                        if loc.player in players and loc.name in deep_location_names:
                            locworld.hint_data["deep"].append(loc)
                        if player in players and autoworld.isMajorItem(loc.item) and (not autoworld.spoiler.settings.key_8_helm or loc.name != "The End of Helm"):
                            autoworld.hint_data["major"].append(loc)
                            # Skip item at location and see if game is still beatable
                            state = CollectionState(multiworld)
                            state.locations_checked.add(loc)
                            if not multiworld.can_beat_game(state):
                                autoworld.hint_data["woth"].append(loc)
                    # Also gather any information on microhinted items
                    if player in players and loc.item.name in microHintItemNames and microHintItemNames[loc.item.name] in microhint_categories[autoworld.spoiler.settings.microhints_enabled]:
                        if player != loc.player:
                            if microHintItemNames[loc.item.name] in autoworld.foreignMicroHints.keys():
                                autoworld.foreignMicroHints[microHintItemNames[loc.item.name]].append([multiworld.get_player_name(loc.player), loc.name[:80]])
                            else:
                                autoworld.foreignMicroHints[microHintItemNames[loc.item.name]] = [multiworld.get_player_name(loc.player), loc.name[:80]]

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

        def fill_slot_data(self) -> dict:
            """Fill the slot data."""
            return {
                "Goal": self.options.goal.value,
                "ClimbingShuffle": self.options.climbing_shuffle.value,
                "PlayerNum": self.player,
                "death_link": self.options.death_link.value,
                "ring_link": self.options.ring_link.value,
                "tag_link": self.options.tag_link.value,
                "receive_notifications": self.options.receive_notifications.value,
                "LevelOrder": ", ".join([level.name for order, level in self.spoiler.settings.level_order.items()]),
                "StartingKongs": ", ".join([kong.name for kong in self.spoiler.settings.starting_kong_list]),
                "ForestTime": self.spoiler.settings.fungi_time_internal.name,
                "GalleonWater": self.spoiler.settings.galleon_water_internal.name,
                "MedalCBRequirement": self.spoiler.settings.medal_cb_req,
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
                "SwitchSanity": {switch.name: {"kong": data.kong.name, "type": data.switch_type.name} for switch, data in self.spoiler.settings.switchsanity_data.items()},
                "LogicType": self.spoiler.settings.logic_type.name,
                "GlitchesSelected": ", ".join([glitch.name for glitch in self.spoiler.settings.glitches_selected]),
                "StartingKeyList": ", ".join([key.name for key in self.spoiler.settings.starting_key_list]),
                "HardShooting": self.options.hard_shooting.value,
                "Junk": self.junked_locations,
                "HintsInPool": self.options.hints_in_item_pool.value,
                "Version": ap_version,
            }

        def write_spoiler(self, spoiler_handle: typing.TextIO):
            """Write the spoiler."""
            spoiler_handle.write("\n")
            spoiler_handle.write("Additional Settings info for player: " + self.player_name)
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
            if self.spoiler.settings.switchsanity != SwitchsanityLevel.off:
                spoiler_handle.write("Switchsanity Settings: \n")
                for switch, data in self.spoiler.settings.switchsanity_data.items():
                    if self.spoiler.settings.switchsanity == SwitchsanityLevel.helm_access:
                        if switch not in (Switches.IslesHelmLobbyGone, Switches.IslesMonkeyport):
                            continue
                    spoiler_handle.write(f"  - {switch.name}: {data.kong.name} with {data.switch_type.name}\n")
            spoiler_handle.write("Generated Time: " + time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()) + " GMT")
            spoiler_handle.write("\n")
            spoiler_handle.write("Randomizer Version: " + self.spoiler.settings.version)
            spoiler_handle.write("\n")
            spoiler_handle.write("APWorld Version: " + ap_version)
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
            # Events, colored bananas
            if "," in item.name:
                return False
            # Not progression
            if item.classification != ItemClassification.progression and item.classification != ItemClassification.progression_skip_balancing:
                return False
            # Golden bananas and blueprints
            if item.name == "Golden Banana" or "Blueprint" in item.name:
                return False
            # Hints, medals, Company coins, Banana fairies
            if "Hint" in item.name or item.name == "Banana Medal" or "Coin" in item.name or item.name == "Banana Fairy":
                return False
            # Helm barrels
            if "Helm" in item.name and "Barrel" in item.name:
                return False
            # Misc items
            if item.name == "Pearl" or item.name == "The Bean" or "Hoard" in item.name:
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
                if loc_obj.type in (Types.Shop, Types.Shockwave, Types.Crown, Types.PreGivenMove, Types.CrateItem, Types.Enemies) or (loc_obj.type == Types.Key or loc_obj.level == Levels.HideoutHelm):
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
                    state.dk64_logic_holder[self.player].UpdateFromArchipelagoItems(state)
                elif hasattr(self, "spoiler"):
                    state.dk64_logic_holder[self.player] = LogicVarHolder(self.spoiler, self.player)  # If the CollectionState dodged the creation of a logic_holder object, fix it here
                    state.dk64_logic_holder[self.player].UpdateFromArchipelagoItems(state)
            return change

        def interpret_slot_data(self, slot_data: dict[str, any]) -> dict[str, any]:
            """Parse slot data for any logical bits that need to match the real generation. Used by Universal Tracker."""
            # Parse the string data
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
            hard_shooting = slot_data.get("HardShooting", False)
            junk = slot_data["Junk"]
            blocker_data = list(map(lambda original_string: original_string[original_string.find(":") + 2 :], slot_data["BLockerValues"].split(", ")))
            blocker_item_type = list(map(lambda data: data.split(" ")[1], blocker_data))
            blocker_item_quantity = list(map(lambda data: int(data.split(" ")[0]), blocker_data))

            relevant_data = {}
            relevant_data["LevelOrder"] = dict(enumerate([Levels[level] for level in level_order], start=1))
            relevant_data["StartingKongs"] = [Kongs[kong] for kong in starting_kongs]
            relevant_data["MedalCBRequirement"] = medal_cb_req
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
            relevant_data["GlitchesSelected"] = [GlitchesSelected[glitch] for glitch in glitches_selected if glitch != ""]
            relevant_data["StartingKeyList"] = [DK64RItems[key] for key in starting_key_list if key != ""]
            relevant_data["HardShooting"] = hard_shooting
            relevant_data["JunkedLocations"] = junk
            relevant_data["BLockerEntryItems"] = [BarrierItems[item] for item in blocker_item_type]
            relevant_data["BLockerEntryCount"] = blocker_item_quantity
            relevant_data["HintsInPool"] = slot_data["HintsInPool"]
            return relevant_data
