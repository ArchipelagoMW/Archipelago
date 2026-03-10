import shutil
from typing import ClassVar, Dict, Any, Type, List, Union, Optional

import Utils
from BaseClasses import Tutorial, ItemClassification as ItemClass
from Options import PerGameCommonOptions, OptionError
from settings import Group, UserFilePath, LocalFolderPath, Bool
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import components, Component, icon_paths, launch_subprocess, Type as ComponentType
from . import Options, Items, Locations
from .Constants import *


def launch_client(*args: str):
    from .Client import launch
    launch_subprocess(launch, name=CLIENT_NAME, args=args)


components.append(
    Component(
        f"{GAME_NAME} Client",
        game_name=GAME_NAME,
        func=launch_client,
        component_type=ComponentType.CLIENT,
        supports_uri=True,
        icon="Saving Princess",
        description="Launch Saving Princess.\nAlso fetches and installs mod updates.",
    )
)

icon_paths["Saving Princess"] = f"ap:{__name__}/icon.png"


def get_default_launch_command() -> List[str]:
    """Returns platform-dependant default launch command for Saving Princess"""
    if Utils.is_windows:
        return []
    else:
        wine_path = shutil.which("wine")
        return [wine_path] if wine_path is not None else ["/usr/bin/wine"]


def get_default_launch_command() -> List[str]:
    """Returns platform-dependant default launch command for Saving Princess"""
    if Utils.is_windows:
        return []
    else:
        wine_path = shutil.which("wine")
        return [wine_path] if wine_path is not None else ["/usr/bin/wine"]


class SavingPrincessSettings(Group):
    class GamePath(UserFilePath):
        """Path to the game executable from which files are extracted"""
        description = "the Saving Princess game executable"
        is_exe = True
        md5s = [GAME_HASH]

    class InstallFolder(LocalFolderPath):
        """Path to the mod installation folder"""
        description = "the folder to install Saving Princess Archipelago to"

    class LaunchGame(Bool):
        """Set this to false to never autostart the game"""

    class LaunchCommandWithArgs(List[str]):
        """
        The console command that will be used to launch the game
        The command will be executed with the installation folder as the current directory
        Additional items in the list will be passed in as arguments
        """

    exe_path: GamePath = GamePath("Saving Princess.exe")
    install_folder: InstallFolder = InstallFolder("Saving Princess")
    launch_game: Union[LaunchGame, bool] = True
    launch_command_with_args: LaunchCommandWithArgs = LaunchCommandWithArgs(get_default_launch_command())


class SavingPrincessWeb(WebWorld):
    theme = "partyTime"
    bug_report_page = "https://github.com/LeonarthCG/saving-princess-archipelago/issues"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Saving Princess for Archipelago multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["LeonarthCG"]
    )
    tutorials = [setup_en]
    options_presets = Options.presets
    option_groups = Options.groups


class SavingPrincessWorld(World):
    """ 
    Explore a space station crawling with rogue machines and even rival bounty hunters
    with the same objective as you - but with far, far different intentions!

    Expand your arsenal as you collect upgrades to your trusty arm cannon and armor!
    """  # Excerpt from itch
    game = GAME_NAME
    web = SavingPrincessWeb()
    required_client_version = tuple(CLIENT_VERSION)

    topology_present = False

    item_name_to_id = {
        key: value.code for key, value in (Items.item_dict.items() - Items.item_dict_events.items())
    }
    location_name_to_id = {
        key: value.code for key, value in (Locations.location_dict.items() - Locations.location_dict_events.items())
    }

    item_name_groups = {
        "Weapons": {key for key in Items.item_dict_weapons.keys()},
        "Upgrades": {key for key in Items.item_dict_upgrades.keys()},
        "Keys": {key for key in Items.item_dict_keys.keys()},
        "Filler": {key for key in Items.item_dict_filler.keys()},
        "Traps": {key for key in Items.item_dict_traps.keys()},
    }

    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = Options.SavingPrincessOptions
    options: Options.SavingPrincessOptions
    settings_key = "saving_princess_settings"
    settings: ClassVar[SavingPrincessSettings]

    final_locks: int = 0
    is_pool_expanded: bool = False
    has_battle_log: bool = False
    has_extra_goodies: bool = False
    music_table: List[int]

    trap_chance: int
    filler_list: List[str]
    trap_list: List[str]

    arctic_door: DoorType
    volcanic_door: DoorType
    swamp_door: DoorType

    def generate_early(self) -> None:
        if not self.player_name.isascii():
            raise OptionError(f"{self.player_name}'s name must be only ASCII.")

        self.final_locks = self.options.final_locks.value
        self.is_pool_expanded = self.options.expanded_pool > 0
        self.has_battle_log = self.options.battle_log > 0
        self.has_extra_goodies = self.options.battle_log == Options.BattleLog.option_extra_goodies

        door_types: List[DoorType] = [
            DoorType.DOOR_TYPE_POWER, DoorType.DOOR_TYPE_FIRE, DoorType.DOOR_TYPE_ICE, DoorType.DOOR_TYPE_VOLT]
        match self.options.blast_doors:
            case self.options.blast_doors.option_vanilla:
                self.arctic_door = DoorType.DOOR_TYPE_POWER
                self.volcanic_door = DoorType.DOOR_TYPE_POWER
                self.swamp_door = DoorType.DOOR_TYPE_POWER
            case self.options.blast_doors.option_random_without_repeats:
                self.random.shuffle(door_types)
                self.arctic_door = door_types[0]
                self.volcanic_door = door_types[1]
                self.swamp_door = door_types[2]
            case self.options.blast_doors.option_fully_random:
                self.arctic_door = self.random.choice(door_types)
                self.volcanic_door = self.random.choice(door_types)
                self.swamp_door = self.random.choice(door_types)
            case self.options.blast_doors.option_remove_blast_doors:
                self.arctic_door = DoorType.DOOR_TYPE_NONE
                self.volcanic_door = DoorType.DOOR_TYPE_NONE
                self.swamp_door = DoorType.DOOR_TYPE_NONE

        self.music_table = list(range(16))
        if self.options.music_shuffle:
            self.random.shuffle(self.music_table)
            # find zzz and purple and swap them back to their original positions
            for song_id in [9, 13]:
                song_index = self.music_table.index(song_id)
                t = self.music_table[song_id]
                self.music_table[song_id] = song_id
                self.music_table[song_index] = t

        # make a list of items that can be filler and items that can be traps
        self.filler_list = list(Items.item_dict_filler.keys())
        self.trap_list = ([TRAP_ITEM_ICE] * self.options.ice_weight
                          + [TRAP_ITEM_SHAKES] * self.options.shake_weight
                          + [TRAP_ITEM_NINJA] * self.options.ninja_weight)

    def create_regions(self) -> None:
        from .Regions import create_regions
        create_regions(self.multiworld, self.player, self.is_pool_expanded, self.has_battle_log)

    def create_items(self) -> None:
        # now, for each item
        item_dict = Items.item_dict_expanded if self.is_pool_expanded else Items.item_dict_base
        if self.has_extra_goodies:
            item_dict.update(Items.item_dict_battle_log)
        for item_name, item_data in item_dict.items():
            # create count copies of the item
            for i in range(item_data.count):
                self.add_item(item_name)
            # and create count_extra useful copies of the item
            for i in range(item_data.count_extra):
                self.add_item(item_name, ItemClass.useful)

        # generate as many junk items as unfilled locations
        junk_count: int = len(self.multiworld.get_unfilled_locations(self.player))
        for i in range(junk_count):
            self.add_item(self.get_filler_item_name())

    def create_item(self, name: str) -> Items.SavingPrincessItem:
        return Items.item_dict[name].create_item(self.player)

    def create_item_with_class(self, name: str, classification: ItemClass) -> Items.SavingPrincessItem:
        item: Items.SavingPrincessItem = self.create_item(name)
        item.classification = classification
        return item

    def add_item(self, name: str, classification: Optional[ItemClass] = None):
        if classification is None:
            self.multiworld.itempool.append(self.create_item(name))
        else:
            self.multiworld.itempool.append(self.create_item_with_class(name, classification))

    def get_filler_item_name(self) -> str:
        # check if this is going to be a trap
        if len(self.trap_list) > 0 and self.random.randint(0, 99) < self.options.trap_chance:
            return self.random.choice(self.trap_list)
        # not a trap, return filler
        else:
            return self.random.choice(self.filler_list)

    def set_rules(self):
        from .Rules import set_rules
        set_rules(self)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict(
            # generation options
            "final_locks",
            "expanded_pool",
            "battle_log",
            # trap weights
            "ice_weight",
            "shake_weight",
            "ninja_weight",
            # gameplay options
            "instant_saving",
            "sprint_availability",
            "cliff_weapon_upgrade",
            "ace_weapon_upgrade",
            "iframes_duration",
            # link options
            "death_link",
            "trap_link",
            # aesthetic options
            "shake_intensity",
        )
        slot_data["arctic_door"] = self.arctic_door
        slot_data["volcanic_door"] = self.volcanic_door
        slot_data["swamp_door ="] = self.swamp_door
        slot_data["music_table"] = self.music_table
        return slot_data
