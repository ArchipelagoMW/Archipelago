from typing import ClassVar, Any, Union, List

import Utils
from BaseClasses import Tutorial, Region, Item, ItemClassification, Location
from Options import OptionError
from settings import Group, UserFilePath, LocalFolderPath, Bool
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import components, Component, launch_subprocess, Type as ComponentType

from .constants import *
from . import options

from .general_items import cartridge_items, cartridge_item_group

from .games import barbuta, porgy, vainger, night_manor
from .games.barbuta import items, locations, regions
from .games.porgy import items, locations, regions
from .games.vainger import items, locations, regions
from .games.night_manor import items, locations, regions


def launch_client(*args: str):
    from .Client import launch
    launch_subprocess(launch(*args), name=CLIENT_NAME)


components.append(
    Component(f"UFO 50", game_name="UFO 50", func=launch_client, component_type=ComponentType.CLIENT,
              supports_uri=True)
)


class UFO50Settings(Group):
    class GamePath(UserFilePath):
        """Path to the game executable"""
        is_exe = True

    class InstallFolder(LocalFolderPath):
        """Path to the mod installation folder"""
        description = "the folder to install UFO 50 Archipelago to (do not select vanilla UFO 50 folder)"

    class LaunchGame(Bool):
        """Set this to false to never autostart the game"""

    class LaunchCommand(str):
        """
        The console command that will be used to launch the game
        The command will be executed with the installation folder as the current directory
        """

    class AllowUnimplemented (Bool):
        """
        Allow the player to choose unimplemented games.
        These games will only send checks when the player does the Garden, Gold, or Cherry checks.
        This can cause issues because the time per check is much higher than normal, and some games are very long.
        """

    exe_path: GamePath = GamePath("ufo50.exe")
    install_folder: InstallFolder = InstallFolder("UFO 50")
    launch_game: Union[LaunchGame, bool] = True
    launch_command: LaunchCommand = LaunchCommand("ufo50.exe" if Utils.is_windows
                                                  else "wine ufo50.exe")
    allow_unimplemented: Union[AllowUnimplemented, bool] = False


class UFO50Web(WebWorld):
    theme = "partyTime"
    bug_report_page = "https://github.com/UFO-50-Archipelago/Archipelago/issues"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up UFO 50 for Archipelago multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["LeonarthCG"]
    )
    tutorials = [setup_en]
    option_groups = options.ufo50_option_groups


# games with an actual implementation
# add to this list as part of your PR
# try to keep them in the same order as on the main menu
ufo50_games: Dict = {
    "Barbuta": barbuta,
    "Porgy": porgy,
    "Vainger": vainger,
    "Night Manor": night_manor,
}

allowable_unimplemented: set[str] = {"Ninpek", "Magic Garden", "Velgress", "Waldorf's Journey"}


# for the purpose of generically making the gift, gold, and cherry locations
unimplemented_ufo50_games: List[str] = [name for name in game_ids.keys() if name not in ufo50_games.keys()]

# doing something like this in the world class itself led to weird errors
temp_ufo50_location_name_to_id = {k: v for game in ufo50_games.values() for k, v in game.locations.get_locations().items()}
for game in unimplemented_ufo50_games:
    base_id = get_game_base_id(game)
    temp_ufo50_location_name_to_id[f"{game} - Garden"] = base_id + 997
    temp_ufo50_location_name_to_id[f"{game} - Gold"] = base_id + 998
    temp_ufo50_location_name_to_id[f"{game} - Cherry"] = base_id + 999


class UFO50World(World):
    """ 
    UFO 50 is a collection of 50 single and multiplayer games from the creators of Spelunky, Downwell, Air Land & Sea,
    Skorpulac, Catacomb Kids, and Madhouse.
    Jump in and explore a variety of genres, from platformers and shoot 'em ups to puzzle games and RPGs.
    Our goal is to combine a familiar 8-bit aesthetic with new ideas and modern game design sensibilities.
    """  # Excerpt from https://50games.fun/
    game = GAME_NAME
    web = UFO50Web()
    required_client_version = (0, 5, 0)
    topology_present = False

    item_name_to_id = {k: v for game in ufo50_games.values() for k, v in game.items.get_items().items()}
    item_name_to_id.update(cartridge_items)
    item_name_to_id.update({"Intentional Nothing Filler Item": base_id - 100})
    location_name_to_id = temp_ufo50_location_name_to_id

    item_name_groups = {k: v for game in ufo50_games.values() for k, v in game.items.get_item_groups().items()}
    item_name_groups.update(cartridge_item_group)
    location_name_groups = {k: v for game in ufo50_games.values() for k, v in game.locations.get_location_groups().items()}

    options_dataclass = options.UFO50Options
    options: options.UFO50Options
    settings_key = "ufo_50_settings"
    settings: ClassVar[UFO50Settings]

    # for universal tracker support
    using_ut: bool
    ut_passthrough: Dict[str, Any]
    ut_can_gen_without_yaml = True  # class var that tells it to ignore the player yaml

    included_games: List[str]  # list of games that are going to be played by this player
    included_unimplemented_games: List[str]  # list of included unimplemented games being played by this player

    starting_games: List[str]  # the games you start with unlocked
    goal_games: List[str]  # the games that are your goals

    porgy_lantern_and_radar_slots_req: Dict[str, int]

    def generate_early(self) -> None:
        if not self.player_name.isascii():
            raise OptionError(f"{self.player_name}'s name must be only ASCII.")

        # for universal tracker support
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "UFO 50" in self.multiworld.re_gen_passthrough:
                self.ut_passthrough = self.multiworld.re_gen_passthrough["UFO 50"]
                # sets the games that ended up on as the always_on_games, turns off random_choice_games
                id_to_game = {v: k for k, v in game_ids.items()}
                self.options.always_on_games.value = {id_to_game[game_id] for game_id in self.ut_passthrough["included_games"]}
                self.options.random_choice_games.value.clear()
                self.options.random_choice_game_count.value = 0
                self.options.goal_games.value = {id_to_game[game_id] for game_id in self.ut_passthrough["goal_games"]}
                self.options.goal_game_amount.value = 50
                # UT doesn't show locations that aren't actually in your slot, so this is fine
                self.options.cherry_allowed_games.value = {game_name for game_name in game_ids.keys()}

                self.options.porgy_fuel_difficulty.value = self.ut_passthrough[options.PorgyFuelDifficulty.internal_name]
                self.options.porgy_check_on_touch.value = self.ut_passthrough[options.PorgyCheckOnTouch.internal_name]
                self.options.porgy_radar.value = self.ut_passthrough[options.PorgyRadar.internal_name]
                self.options.porgy_lanternless.value = self.ut_passthrough[options.PorgyLanternless.internal_name]

        included_game_names = sorted(self.options.always_on_games.value)
        # exclude always on games from random choice games
        maybe_games = sorted(self.options.random_choice_games.value - self.options.always_on_games.value)
        # if the number of games you want is higher than the number of games you chose, enable all chosen
        if self.options.random_choice_game_count >= len(maybe_games):
            included_game_names += maybe_games
        elif self.options.random_choice_game_count and maybe_games:
            included_game_names += self.random.sample(maybe_games, self.options.random_choice_game_count.value)

        if not included_game_names:
            raise OptionError(f"UFO 50: {self.player_name} has not selected any games.")

        self.included_games = []
        self.included_unimplemented_games = []
        for game_name in included_game_names:
            if game_name in ufo50_games.keys():
                self.included_games.append(game_name)
            else:
                self.included_unimplemented_games.append(game_name)

        if self.included_unimplemented_games and not self.settings.allow_unimplemented:
            for game_name in self.included_unimplemented_games:
                if game_name in allowable_unimplemented:
                    break
            else:
                raise OptionError(f"UFO 50: {self.player_name} has selected an unimplemented game, but the host "
                                  f"does not have them enabled. Please enable the host.yaml setting or remove the "
                                  f"unimplemented games from the selected games.\n"
                                  f"Unimplemented games: {self.included_unimplemented_games}")

        if not self.included_games and not self.settings.allow_unimplemented:
            for game_name in self.included_unimplemented_games:
                if game_name in allowable_unimplemented:
                    break
            else:
                raise OptionError(f"UFO 50: {self.player_name} has not selected any games that have implementations. "
                                  f"Please select at least one game that has an actual implementation, or have the "
                                  f"host enable the host.yaml setting to allow them.\n"
                                  f"The following games have actual implementations: {[name for name in ufo50_games]}")
        self.options.goal_games.value = [game_name for game_name in self.options.goal_games if game_name in included_game_names]
        potential_goal_games = [game_name for game_name in included_game_names if game_name in self.options.goal_games]
        if self.options.goal_game_amount >= len(potential_goal_games):
            self.goal_games = potential_goal_games
        else:
            self.goal_games = self.random.choices(potential_goal_games, k=self.options.goal_game_amount.value)

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        victory_location = Location(self.player, "Completed All Games", None, menu)
        victory_location.place_locked_item(Item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        menu.locations.append(victory_location)

        for game_name in self.included_games:
            game = ufo50_games[game_name]
            game_regions = game.regions.create_regions_and_rules(self)
            for region in game_regions.values():
                self.multiworld.regions.append(region)
            game_menu = self.get_region(f"{game.game_name} - Menu")
            menu.connect(game_menu, f"Boot {game.game_name}",
                         rule=lambda state, name=game.game_name: state.has(f"{name} Cartridge", self.player))

        for game_name in self.included_unimplemented_games:
            locs = {
                f"{game_name} - Garden": self.location_name_to_id[f"{game_name} - Garden"],
                f"{game_name} - Gold": self.location_name_to_id[f"{game_name} - Gold"],
            }
            if game_name in self.options.cherry_allowed_games:
                locs[f"{game_name} - Cherry"] = self.location_name_to_id[f"{game_name} - Cherry"]
            region = Region(f"{game_name} Region", self.player, self.multiworld)
            region.add_locations(locs)
            menu.connect(region, f"Boot {game_name}",
                         rule=lambda state, name=game_name: state.has(f"{name} Cartridge", self.player))

    def create_item(self, name: str, item_class: ItemClassification = None) -> Item:
        # figure out which game it's from and call its create_item
        game_name = name.split(" - ", 1)[0]
        if game_name in ufo50_games:
            return ufo50_games[game_name].items.create_item(name, self, item_class)
        if name.endswith("Cartridge"):
            item_class = item_class or ItemClassification.progression
        return Item(name, item_class or ItemClassification.filler, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        created_items: List[Item] = []
        for game_name in self.included_games:
            game = ufo50_games[game_name]
            created_items += game.items.create_items(self)

        included_game_names = self.included_games + self.included_unimplemented_games
        # check precollected items for cartridges, add them to the starting games list
        precollected_cartridges = set()
        self.starting_games = []
        for item in self.multiworld.precollected_items[self.player]:
            if item.name.endswith("Cartridge"):
                game_name = item.name.split(" Cartridge")[0]
                if game_name not in self.starting_games and game_name in included_game_names:
                    self.starting_games.append(game_name)
                    precollected_cartridges.add(game_name)

        # if your starting game amount is higher than included games, then they're all starting games
        if self.options.starting_game_amount >= len(included_game_names):
            self.starting_games = included_game_names
        else:
            addtl_games_to_start_with = max(self.options.starting_game_amount.value - len(self.starting_games), 0)
            self.starting_games += self.random.choices(
                [game for game in included_game_names if game not in self.starting_games],
                k=addtl_games_to_start_with)
            for game_name in self.starting_games:
                if game_name in ufo50_games.keys():
                    break
            else:
                # remove a game, add an implemented game, unless none are implemented
                # since we're popping, we don't need to worry about removing a precollected cartridge
                if self.included_games and addtl_games_to_start_with > 0:
                    self.starting_games.pop()
                    self.starting_games.append(self.random.choice(self.included_games))

        all_games = self.included_games + self.included_unimplemented_games
        for game_name in all_games:
            cartridge = self.create_item(f"{game_name} Cartridge",
                                         ItemClassification.progression | ItemClassification.useful)
            if game_name in self.starting_games and game_name not in precollected_cartridges:
                self.multiworld.push_precollected(cartridge)
            else:
                created_items.append(cartridge)

        unfilled_locations = self.multiworld.get_unfilled_locations(self.player)
        extra_items_needed = len(unfilled_locations) - len(created_items)

        # debug, delete this later once it all works nicely
        if extra_items_needed < 0:
            raise Exception("Too many items for the number of games, need to fix this somehow.")

        for _ in range(extra_items_needed):
            created_items.append(self.create_item(self.get_filler_item_name(), ItemClassification.filler))

        self.multiworld.itempool += created_items

    def get_filler_item_name(self) -> str:
        if not self.included_games:
            return "Intentional Nothing Filler Item"
        return ufo50_games[self.random.choice(self.included_games)].items.get_filler_item_name(self)

    def fill_slot_data(self) -> Dict[str, Any]:
        included_games = [game_ids[game_name] for game_name in self.included_games]
        included_games += [game_ids[game_name] for game_name in self.included_unimplemented_games]
        goal_games = [game_ids[game_name] for game_name in self.goal_games]
        cherry_games = [game_ids[game_name] for game_name in self.goal_games
                        if game_name in self.options.cherry_allowed_games]
        slot_data = {
            "included_games": included_games,
            "goal_games": goal_games,
            "cherry_games": cherry_games,
            options.PorgyFuelDifficulty.internal_name: self.options.porgy_fuel_difficulty.value,
            options.PorgyCheckOnTouch.internal_name: self.options.porgy_check_on_touch.value,
            options.PorgyRadar.internal_name: self.options.porgy_radar.value,
            options.PorgyLanternless.internal_name: self.options.porgy_lanternless.value,
        }
        return slot_data

    # for the universal tracker, doesn't get called in standard gen
    # docs: https://github.com/FarisTheAncient/Archipelago/blob/tracker/worlds/tracker/docs/re-gen-passthrough.md
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        return slot_data
