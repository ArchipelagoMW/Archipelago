from typing import ClassVar, Dict, Any, Type, List, Union

import Utils
from BaseClasses import Tutorial, ItemClassification as ItemClass
from Options import PerGameCommonOptions, OptionError
from settings import Group, UserFilePath, LocalFolderPath, Bool
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import components, Component, launch_subprocess, Type as ComponentType
from . import Options, Items, Locations
from .Constants import *


def launch_client(*args: str):
    from .Client import launch
    launch_subprocess(launch, name=CLIENT_NAME, args=args)


components.append(
    Component(f"{GAME_NAME} Client", game_name=GAME_NAME, func=launch_client, component_type=ComponentType.CLIENT, supports_uri=True)
)


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

    class LaunchCommand(str):
        """
        The console command that will be used to launch the game
        The command will be executed with the installation folder as the current directory
        """

    exe_path: GamePath = GamePath("Saving Princess.exe")
    install_folder: InstallFolder = InstallFolder("Saving Princess")
    launch_game: Union[LaunchGame, bool] = True
    launch_command: LaunchCommand = LaunchCommand('"Saving Princess v0_8.exe"' if Utils.is_windows
                                                  else 'wine "Saving Princess v0_8.exe"')


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
    required_client_version = (0, 5, 0)

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

    is_pool_expanded: bool = False
    music_table: List[int] = list(range(16))

    def generate_early(self) -> None:
        if not self.player_name.isascii():
            raise OptionError(f"{self.player_name}'s name must be only ASCII.")
        self.is_pool_expanded = self.options.expanded_pool > 0
        if self.options.music_shuffle:
            self.random.shuffle(self.music_table)
            # find zzz and purple and swap them back to their original positions
            for song_id in [9, 13]:
                song_index = self.music_table.index(song_id)
                t = self.music_table[song_id]
                self.music_table[song_id] = song_id
                self.music_table[song_index] = t

    def create_regions(self) -> None:
        from .Regions import create_regions
        create_regions(self.multiworld, self.player, self.is_pool_expanded)

    def create_items(self) -> None:
        items_made: int = 0

        # now, for each item
        item_dict = Items.item_dict_expanded if self.is_pool_expanded else Items.item_dict_base
        for item_name, item_data in item_dict.items():
            # create count copies of the item
            for i in range(item_data.count):
                self.multiworld.itempool.append(self.create_item(item_name))
            items_made += item_data.count
            # and create count_extra useful copies of the item
            original_item_class: ItemClass = item_data.item_class
            item_data.item_class = ItemClass.useful
            for i in range(item_data.count_extra):
                self.multiworld.itempool.append(self.create_item(item_name))
            item_data.item_class = original_item_class
            items_made += item_data.count_extra

        # get the number of unfilled locations, that is, locations for items - items generated
        location_count = len(Locations.location_dict_base)
        if self.is_pool_expanded:
            location_count = len(Locations.location_dict_expanded)
        junk_count: int = location_count - items_made

        # and generate as many junk items as unfilled locations
        for i in range(junk_count):
            self.multiworld.itempool.append(self.create_item(self.get_filler_item_name()))

    def create_item(self, name: str) -> Items.SavingPrincessItem:
        return Items.item_dict[name].create_item(self.player)

    def get_filler_item_name(self) -> str:
        filler_list = list(Items.item_dict_filler.keys())
        # check if this is going to be a trap
        if self.random.randint(0, 99) < self.options.trap_chance:
            filler_list = list(Items.item_dict_traps.keys())
        # and return one of the names at random
        return self.random.choice(filler_list)

    def set_rules(self):
        from .Rules import set_rules
        set_rules(self)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict(
            "death_link",
            "expanded_pool",
            "instant_saving",
            "sprint_availability",
            "cliff_weapon_upgrade",
            "ace_weapon_upgrade",
            "shake_intensity",
            "iframes_duration",
        )
        slot_data["music_table"] = self.music_table
        return slot_data
