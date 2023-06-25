from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule
from BaseClasses import Region, Item, ItemClassification, Entrance, Tutorial

from math import floor

from .Options import musedash_options
from .Items import MuseDashSongItem, MuseDashFixedItem
from .Locations import MuseDashLocation
from .MuseDashCollection import MuseDashCollections


class MuseDashWebWorld(WebWorld):
    theme = "partyTime"

    bug_report_page = "https://github.com/DeamonHunter/ArchipelagoMuseDash/issues"
    setup_en = Tutorial(
        "Mod Setup and Use Guide",
        "A guide to setting up the Muse Dash Archipelago Mod on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["DeamonHunter"]
    )

    tutorials = [setup_en]


class MuseDashWorld(World):
    """Muse Dash is a rhythm game where you hit objects to the beat of one of 400+ songs.
    Play through a selection of randomly chosen songs, collecting music sheets until you have enough to play and complete the goal song!"""

    # FUTURE OPTIONS
    # - Album Rando.
    # - Added items for characters/elfin/portraits.
    # - Support for blacklisting/plando-ing certain songs.

    # World Options
    game: str = "Muse Dash"
    option_definitions = musedash_options
    topology_present = False
    data_version = 6
    web = MuseDashWebWorld()

    music_sheet_name: str = "Music Sheet"

    # Necessary Data
    muse_dash_collection = MuseDashCollections(2900000, 2)

    item_name_to_id = {
        name: data.code for name, data in muse_dash_collection.album_items.items() | muse_dash_collection.song_items.items()
    }
    item_name_to_id[music_sheet_name] = muse_dash_collection.MUSIC_SHEET_CODE
    for item in muse_dash_collection.sfx_trap_items.items() | muse_dash_collection.vfx_trap_items.items():
        item_name_to_id[item[0]] = item[1]

    location_name_to_id = {
        name: id for name, id in muse_dash_collection.album_locations.items() | muse_dash_collection.song_locations.items()
    }

    # Working Data
    victory_song_name: str = ""
    starting_songs: list  # Todo: Update to list[str] when python 3.8 is no longer used
    included_songs: list  # Todo: Update to list[str] when python 3.8 is no longer used
    needed_token_count: int
    location_count: int

    def generate_early(self):
        dlc_songs = self.multiworld.allow_just_as_planned_dlc_songs[self.player]
        streamer_mode = self.multiworld.streamer_mode_enabled[self.player]
        (lower_diff_threshold, higher_diff_threshold) = self.get_difficulty_range()

        # The minimum amount of songs to make an ok rando would be Starting Songs + 10 interim songs + Goal song.
        # - Interim songs being equal to max starting song count.
        # Note: The worst settings still allow 25 songs (Streamer Mode + No DLC). And this max requires 21 songs. (10 + 10 + 1)
        starter_song_count = self.multiworld.starting_song_count[self.player].value

        final_song_list = None
        while True:
            # In most cases this should only need to run once
            available_song_keys = self.muse_dash_collection.get_songs_with_settings(dlc_songs, streamer_mode, lower_diff_threshold, higher_diff_threshold)
            available_song_keys = self.handle_plando(available_song_keys)

            count_needed_for_start = max(0, starter_song_count - len(self.starting_songs))
            if len(available_song_keys) + len(self.included_songs) >= count_needed_for_start + 11:
                final_song_list = available_song_keys
                break

            # If the above fails, we want to adjust the difficulty thresholds. We mostly want to make things easier rather than harder.
            if lower_diff_threshold <= 1 and higher_diff_threshold >= 11:
                raise Exception("Failed to find enough songs, even with maximum difficulty thresholds. Something went catastrophically wrong.")
            elif lower_diff_threshold <= 1:
                higher_diff_threshold += 1
            else:
                lower_diff_threshold -= 1

        self.create_song_pool(final_song_list)

        for song in self.starting_songs:
            self.multiworld.push_precollected(self.create_item(song))

    # Todo: Update this to list[str] when python 3.8 stops being used
    def handle_plando(self, available_song_keys: list) -> list:
        start_items = self.multiworld.start_inventory[self.player].value.keys()
        include_songs = self.multiworld.include_songs[self.player].value
        exclude_songs = self.multiworld.exclude_songs[self.player].value

        self.starting_songs = [s for s in start_items if s in self.muse_dash_collection.song_items]
        self.included_songs = [s for s in include_songs if (s in self.muse_dash_collection.song_items) and (s not in self.starting_songs)]
        return [s for s in available_song_keys if (s not in start_items) and (s not in include_songs) and (s not in exclude_songs)]

    # Todo: Update this to list[str] when python 3.8 stops being used
    def create_song_pool(self, available_song_keys: list):
        starting_song_count = self.multiworld.starting_song_count[self.player].value
        additional_song_count = self.multiworld.additional_song_count[self.player].value

        self.multiworld.random.shuffle(available_song_keys)

        # First, we must double check if the player has included too many guaranteed songs
        included_song_count = len(self.included_songs)
        if included_song_count > additional_song_count:
            # If so, we want to thin the list, thus let's get the goal song and starter songs while we are at it.
            self.multiworld.random.shuffle(self.included_songs)
            self.victory_song_name = self.included_songs.pop()
            while len(self.included_songs) > additional_song_count:
                next_song = self.included_songs.pop()
                if len(self.starting_songs) < starting_song_count:
                    self.starting_songs.append(next_song)
        else:
            # If not, choose a random victory song from the available songs
            chosen_song = self.multiworld.random.randrange(0, len(available_song_keys) + included_song_count)
            if chosen_song < included_song_count:
                self.victory_song_name = self.included_songs[chosen_song]
                del self.included_songs[chosen_song]
            else:
                self.victory_song_name = available_song_keys[chosen_song - included_song_count]
                del available_song_keys[chosen_song - included_song_count]

        # Next, make sure the starting songs are fufilled
        if len(self.starting_songs) < starting_song_count:
            for _ in range(len(self.starting_songs), starting_song_count):
                if len(available_song_keys) > 0:
                    self.starting_songs.append(available_song_keys.pop())
                else:
                    self.starting_songs.append(self.included_songs.pop())

        # Then attempt to fufill any remaining songs for interim songs
        if len(self.included_songs) < additional_song_count:
            for _ in range(len(self.included_songs), self.multiworld.additional_song_count[self.player]):
                if len(available_song_keys) <= 0:
                    break
                self.included_songs.append(available_song_keys.pop())

        self.location_count = len(self.starting_songs) + len(self.included_songs)
        location_multiplier = 1 + (self.get_additional_item_percentage() / 100.0)
        self.location_count = floor(self.location_count * location_multiplier)

        minimum_location_count = len(self.included_songs) + self.get_music_sheet_count()
        if self.location_count < minimum_location_count:
            self.location_count = minimum_location_count

    def create_item(self, name: str) -> Item:
        if name == self.music_sheet_name:
            return MuseDashFixedItem(name, ItemClassification.progression_skip_balancing,
                                     self.muse_dash_collection.MUSIC_SHEET_CODE, self.player)

        trap = self.muse_dash_collection.vfx_trap_items.get(name)
        if trap:
            return MuseDashFixedItem(name, ItemClassification.trap, trap, self.player)

        trap = self.muse_dash_collection.sfx_trap_items.get(name)
        if trap:
            return MuseDashFixedItem(name, ItemClassification.trap, trap, self.player)

        song = self.muse_dash_collection.song_items.get(name)
        if song:
            return MuseDashSongItem(name, self.player, song)

        return MuseDashFixedItem(name, ItemClassification.filler, None, self.player)

    def create_items(self) -> None:
        song_keys_in_pool = list(self.included_songs)

        # Note: Item count will be off if plando is involved.
        item_count = self.get_music_sheet_count()

        # First add all goal song tokens
        for _ in range(0, item_count):
            self.multiworld.itempool.append(self.create_item(self.music_sheet_name))

        # Then add all traps
        trap_count = self.get_trap_count()
        trap_list = self.get_available_traps()
        if len(trap_list) > 0 and trap_count > 0:
            for _ in range(0, trap_count):
                index = self.multiworld.random.randrange(0, len(trap_list))
                choice = trap_list[index]
                self.multiworld.itempool.append(self.create_item(choice[0]))

            item_count += trap_count

        # Next fill all remaining slots with song items
        needed_item_count = self.location_count
        while (item_count < needed_item_count):
            # If we have more items needed than keys, just iterate the list and add them all
            if len(song_keys_in_pool) <= needed_item_count - item_count:
                for key in song_keys_in_pool:
                    self.multiworld.itempool.append(self.create_item(key))

                item_count += len(song_keys_in_pool)
                continue

            # Otherwise add a random assortment of songs
            self.multiworld.random.shuffle(song_keys_in_pool)
            for i in range(0, needed_item_count - item_count):
                self.multiworld.itempool.append(self.create_item(song_keys_in_pool[i]))

            item_count = needed_item_count

    def create_regions(self) -> None:
        # Basic Region Setup: Menu -> Song Select -> Songs
        menu_region = Region("Menu", self.player, self.multiworld)
        song_select_region = Region("Song Select", self.player, self.multiworld)

        song_select_entrance = Entrance(self.player, "Song Select Entrance", menu_region)

        menu_region.exits.append(song_select_entrance)
        song_select_entrance.connect(song_select_region)

        self.multiworld.regions.append(menu_region)
        self.multiworld.regions.append(song_select_region)

        # Make a collection of all songs available for this rando.
        # 1. All starting songs
        # 2. All other songs shuffled
        # Doing it in this order ensures that starting songs are first in line to getting 2 locations.
        # Final song is excluded as for the purpose of this rando, it doesn't matter.

        all_selected_locations = list(self.starting_songs)
        included_song_copy = list(self.included_songs)

        self.multiworld.random.shuffle(included_song_copy)
        all_selected_locations.extend(included_song_copy)

        two_item_location_count = self.location_count - len(all_selected_locations)

        # Make a region per song/album, then adds 1-2 item locations to them
        for i in range(0, len(all_selected_locations)):
            name = all_selected_locations[i]
            region = Region(name, self.player, self.multiworld)

            # 2 Locations are defined per song
            location_name = name + "-0"
            region.locations.append(MuseDashLocation(self.player, location_name,
                self.muse_dash_collection.song_locations[location_name], region))

            if i < two_item_location_count:
                location_name = name + "-1"
                region.locations.append(MuseDashLocation(self.player, location_name,
                    self.muse_dash_collection.song_locations[location_name], region))

            region_exit = Entrance(self.player, name, song_select_region)
            song_select_region.exits.append(region_exit)
            region_exit.connect(region)
            self.multiworld.regions.append(region)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has(self.music_sheet_name, self.player, self.get_music_sheet_win_count())

        for location in self.multiworld.get_locations(self.player):
            item_name = location.name[0:(len(location.name) - 2)]
            if item_name == self.victory_song_name:
                set_rule(location, lambda state: state.has(self.music_sheet_name, self.player, self.get_music_sheet_win_count()))
            else:
                set_rule(location, lambda state, place=item_name: state.has(place, self.player))

    def get_available_traps(self) -> list:
        dlc_songs = self.multiworld.allow_just_as_planned_dlc_songs[self.player]

        trap_list = list()
        if self.multiworld.available_trap_types[self.player].value & 1 != 0:
            trap_list += self.muse_dash_collection.vfx_trap_items.items()

        # SFX options are only available under Just as Planned DLC.
        if dlc_songs and self.multiworld.available_trap_types[self.player].value & 2 != 0:
            trap_list += self.muse_dash_collection.sfx_trap_items.items()

        return trap_list

    def get_additional_item_percentage(self) -> int:
        trap_count = self.multiworld.trap_count_percentage[self.player].value
        song_count = self.multiworld.music_sheet_count_percentage[self.player].value
        return max(trap_count + song_count, self.multiworld.additional_item_percentage[self.player].value)

    def get_trap_count(self) -> int:
        multiplier = self.multiworld.trap_count_percentage[self.player].value / 100.0
        trap_count = (len(self.starting_songs) * 2) + len(self.included_songs)
        return max(0, floor(trap_count * multiplier))

    def get_music_sheet_count(self) -> int:
        multiplier = self.multiworld.music_sheet_count_percentage[self.player].value / 100.0
        song_count = (len(self.starting_songs) * 2) + len(self.included_songs)
        return max(1, floor(song_count * multiplier))

    def get_music_sheet_win_count(self) -> int:
        multiplier = self.multiworld.music_sheet_win_count_percentage[self.player].value / 100.0
        sheet_count = self.get_music_sheet_count()
        return max(1, floor(sheet_count * multiplier))

    # Todo: Update to list[int] when python 3.8 is no longer used.
    def get_difficulty_range(self) -> list:
        difficulty_mode = self.multiworld.song_difficulty_mode[self.player]

        # Valid difficulties are between 1 and 11. But make it 0 to 12 for safety
        difficulty_bounds = [0, 12]
        if difficulty_mode == 1:
            difficulty_bounds[1] = 3
        elif difficulty_mode == 2:
            difficulty_bounds[0] = 4
            difficulty_bounds[1] = 5
        elif difficulty_mode == 3:
            difficulty_bounds[0] = 6
            difficulty_bounds[1] = 7
        elif difficulty_mode == 4:
            difficulty_bounds[0] = 8
            difficulty_bounds[1] = 9
        elif difficulty_mode == 5:
            difficulty_bounds[0] = 10
        elif difficulty_mode == 6:
            minimum_difficulty = self.multiworld.song_difficulty_min[self.player].value
            maximum_difficulty = self.multiworld.song_difficulty_max[self.player].value

            difficulty_bounds[0] = min(minimum_difficulty, maximum_difficulty)
            difficulty_bounds[1] = max(minimum_difficulty, maximum_difficulty)

        return difficulty_bounds

    def fill_slot_data(self):
        return {
            "victoryLocation": self.victory_song_name,
            "deathLink": self.multiworld.death_link[self.player].value,
            "musicSheetWinCount": self.get_music_sheet_win_count(),
            "gradeNeeded" : self.multiworld.grade_needed[self.player].value
        }
