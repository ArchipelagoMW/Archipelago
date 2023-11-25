from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Item, ItemClassification, Entrance, Tutorial
from typing import List, ClassVar, Type
from math import floor
from Options import PerGameCommonOptions

from .Options import MuseDashOptions
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

    setup_es = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Español",
        "setup_es.md",
        "setup/es",
        ["Shiny"]
    )

    tutorials = [setup_en, setup_es]


class MuseDashWorld(World):
    """Muse Dash is a rhythm game where you hit objects to the beat of one of 400+ songs.
    Play through a selection of randomly chosen songs, collecting music sheets
    until you have enough to play and complete the goal song!"""

    # FUTURE OPTIONS
    # - Album Rando.
    # - Added items for characters/elfin/portraits.
    # - Support for blacklisting/plando-ing certain songs.

    # World Options
    game = "Muse Dash"
    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = MuseDashOptions
    options: MuseDashOptions

    topology_present = False
    web = MuseDashWebWorld()

    # Necessary Data
    md_collection = MuseDashCollections()

    item_name_to_id = {name: code for name, code in md_collection.item_names_to_id.items()}
    location_name_to_id = {name: code for name, code in md_collection.location_names_to_id.items()}

    # Working Data
    victory_song_name: str = ""
    starting_songs: List[str]
    included_songs: List[str]
    needed_token_count: int
    location_count: int

    def generate_early(self):
        dlc_songs = {key for key in self.options.dlc_packs.value}
        if (self.options.allow_just_as_planned_dlc_songs.value):
            dlc_songs.add(self.md_collection.MUSE_PLUS_DLC)

        streamer_mode = self.options.streamer_mode_enabled
        (lower_diff_threshold, higher_diff_threshold) = self.get_difficulty_range()

        # The minimum amount of songs to make an ok rando would be Starting Songs + 10 interim songs + Goal song.
        # - Interim songs being equal to max starting song count.
        # Note: The worst settings still allow 25 songs (Streamer Mode + No DLC).
        starter_song_count = self.options.starting_song_count.value

        while True:
            # In most cases this should only need to run once
            available_song_keys = self.md_collection.get_songs_with_settings(
                dlc_songs, streamer_mode, lower_diff_threshold, higher_diff_threshold)

            available_song_keys = self.handle_plando(available_song_keys)

            count_needed_for_start = max(0, starter_song_count - len(self.starting_songs))
            if len(available_song_keys) + len(self.included_songs) >= count_needed_for_start + 11:
                final_song_list = available_song_keys
                break

            # If the above fails, we want to adjust the difficulty thresholds.
            # Easier first, then harder
            if lower_diff_threshold <= 1 and higher_diff_threshold >= 11:
                raise Exception("Failed to find enough songs, even with maximum difficulty thresholds.")
            elif lower_diff_threshold <= 1:
                higher_diff_threshold += 1
            else:
                lower_diff_threshold -= 1

        self.create_song_pool(final_song_list)

        for song in self.starting_songs:
            self.multiworld.push_precollected(self.create_item(song))

    def handle_plando(self, available_song_keys: List[str]) -> List[str]:
        song_items = self.md_collection.song_items

        start_items = self.options.start_inventory.value.keys()
        include_songs = self.options.include_songs.value
        exclude_songs = self.options.exclude_songs.value

        self.starting_songs = [s for s in start_items if s in song_items]
        self.included_songs = [s for s in include_songs if s in song_items and s not in self.starting_songs]

        return [s for s in available_song_keys if s not in start_items
                and s not in include_songs and s not in exclude_songs]

    def create_song_pool(self, available_song_keys: List[str]):
        starting_song_count = self.options.starting_song_count.value
        additional_song_count = self.options.additional_song_count.value

        self.random.shuffle(available_song_keys)

        # First, we must double check if the player has included too many guaranteed songs
        included_song_count = len(self.included_songs)
        if included_song_count > additional_song_count:
            # If so, we want to thin the list, thus let's get the goal song and starter songs while we are at it.
            self.random.shuffle(self.included_songs)
            self.victory_song_name = self.included_songs.pop()
            while len(self.included_songs) > additional_song_count:
                next_song = self.included_songs.pop()
                if len(self.starting_songs) < starting_song_count:
                    self.starting_songs.append(next_song)
        else:
            # If not, choose a random victory song from the available songs
            chosen_song = self.random.randrange(0, len(available_song_keys) + included_song_count)
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
            for _ in range(len(self.included_songs), self.options.additional_song_count):
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
        if name == self.md_collection.MUSIC_SHEET_NAME:
            return MuseDashFixedItem(name, ItemClassification.progression_skip_balancing,
                                     self.md_collection.MUSIC_SHEET_CODE, self.player)

        trap = self.md_collection.vfx_trap_items.get(name)
        if trap:
            return MuseDashFixedItem(name, ItemClassification.trap, trap, self.player)

        trap = self.md_collection.sfx_trap_items.get(name)
        if trap:
            return MuseDashFixedItem(name, ItemClassification.trap, trap, self.player)

        album = self.md_collection.album_items.get(name)
        if album:
            return MuseDashSongItem(name, self.player, album)

        song = self.md_collection.song_items.get(name)
        return MuseDashSongItem(name, self.player, song)

    def create_items(self) -> None:
        song_keys_in_pool = self.included_songs.copy()

        # Note: Item count will be off if plando is involved.
        item_count = self.get_music_sheet_count()

        # First add all goal song tokens
        for _ in range(0, item_count):
            self.multiworld.itempool.append(self.create_item(self.md_collection.MUSIC_SHEET_NAME))

        # Then add all traps
        trap_count = self.get_trap_count()
        trap_list = self.get_available_traps()
        if len(trap_list) > 0 and trap_count > 0:
            for _ in range(0, trap_count):
                index = self.random.randrange(0, len(trap_list))
                self.multiworld.itempool.append(self.create_item(trap_list[index]))

            item_count += trap_count

        # Next fill all remaining slots with song items
        needed_item_count = self.location_count
        while item_count < needed_item_count:
            # If we have more items needed than keys, just iterate the list and add them all
            if len(song_keys_in_pool) <= needed_item_count - item_count:
                for key in song_keys_in_pool:
                    self.multiworld.itempool.append(self.create_item(key))

                item_count += len(song_keys_in_pool)
                continue

            # Otherwise add a random assortment of songs
            self.random.shuffle(song_keys_in_pool)
            for i in range(0, needed_item_count - item_count):
                self.multiworld.itempool.append(self.create_item(song_keys_in_pool[i]))

            item_count = needed_item_count

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        song_select_region = Region("Song Select", self.player, self.multiworld)
        self.multiworld.regions += [menu_region, song_select_region]
        menu_region.connect(song_select_region)

        # Make a collection of all songs available for this rando.
        # 1. All starting songs
        # 2. All other songs shuffled
        # Doing it in this order ensures that starting songs are first in line to getting 2 locations.
        # Final song is excluded as for the purpose of this rando, it doesn't matter.

        all_selected_locations = self.starting_songs.copy()
        included_song_copy = self.included_songs.copy()

        self.random.shuffle(included_song_copy)
        all_selected_locations.extend(included_song_copy)

        two_item_location_count = self.location_count - len(all_selected_locations)

        # Make a region per song/album, then adds 1-2 item locations to them
        for i in range(0, len(all_selected_locations)):
            name = all_selected_locations[i]
            region = Region(name, self.player, self.multiworld)
            self.multiworld.regions.append(region)
            song_select_region.connect(region, name, lambda state, place=name: state.has(place, self.player))

            # Up to 2 Locations are defined per song
            region.add_locations({name + "-0": self.md_collection.song_locations[name + "-0"]}, MuseDashLocation)
            if i < two_item_location_count:
                region.add_locations({name + "-1": self.md_collection.song_locations[name + "-1"]}, MuseDashLocation)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: \
            state.has(self.md_collection.MUSIC_SHEET_NAME, self.player, self.get_music_sheet_win_count())

    def get_available_traps(self) -> List[str]:
        sfx_traps_available = self.options.allow_just_as_planned_dlc_songs.value

        trap_list = []
        if self.options.available_trap_types.value & 1 != 0:
            trap_list += self.md_collection.vfx_trap_items.keys()

        # SFX options are only available under Just as Planned DLC.
        if sfx_traps_available and self.options.available_trap_types.value & 2 != 0:
            trap_list += self.md_collection.sfx_trap_items.keys()

        return trap_list

    def get_additional_item_percentage(self) -> int:
        trap_count = self.options.trap_count_percentage.value
        song_count = self.options.music_sheet_count_percentage.value
        return max(trap_count + song_count, self.options.additional_item_percentage.value)

    def get_trap_count(self) -> int:
        multiplier = self.options.trap_count_percentage.value / 100.0
        trap_count = (len(self.starting_songs) * 2) + len(self.included_songs)
        return max(0, floor(trap_count * multiplier))

    def get_music_sheet_count(self) -> int:
        multiplier = self.options.music_sheet_count_percentage.value / 100.0
        song_count = (len(self.starting_songs) * 2) + len(self.included_songs)
        return max(1, floor(song_count * multiplier))

    def get_music_sheet_win_count(self) -> int:
        multiplier = self.options.music_sheet_win_count_percentage.value / 100.0
        sheet_count = self.get_music_sheet_count()
        return max(1, floor(sheet_count * multiplier))

    def get_difficulty_range(self) -> List[int]:
        difficulty_mode = self.options.song_difficulty_mode

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
            minimum_difficulty = self.options.song_difficulty_min.value
            maximum_difficulty = self.options.song_difficulty_max.value

            difficulty_bounds[0] = min(minimum_difficulty, maximum_difficulty)
            difficulty_bounds[1] = max(minimum_difficulty, maximum_difficulty)

        return difficulty_bounds

    def fill_slot_data(self):
        return {
            "victoryLocation": self.victory_song_name,
            "deathLink": self.options.death_link.value,
            "musicSheetWinCount": self.get_music_sheet_win_count(),
            "gradeNeeded": self.options.grade_needed.value
        }
