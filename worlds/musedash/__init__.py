from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Item, ItemClassification, Tutorial
from typing import List, ClassVar, Type, Set
from math import floor
from Options import PerGameCommonOptions, OptionError

from .Options import MuseDashOptions, md_option_groups
from .Items import MuseDashSongItem, MuseDashFixedItem
from .Locations import MuseDashLocation
from .MuseDashCollection import MuseDashCollections
from .Presets import MuseDashPresets


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
    options_presets = MuseDashPresets
    option_groups = md_option_groups


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
    filler_item_names = list(md_collection.filler_item_weights.keys())
    filler_item_weights = list(md_collection.filler_item_weights.values())

    item_name_to_id = {name: code for name, code in md_collection.item_names_to_id.items()}
    location_name_to_id = {name: code for name, code in md_collection.location_names_to_id.items()}
    item_name_groups = {
        "Songs": {name for name in md_collection.song_items.keys()},
        "Filler Items": {name for name in md_collection.filler_items.keys()},
        "Traps": {name for name in md_collection.trap_items.keys()}
    }

    # Working Data
    victory_song_name: str = ""
    starting_songs: List[str]
    included_songs: List[str]
    needed_token_count: int
    location_count: int

    def generate_early(self):
        dlc_songs = {key for key in self.options.dlc_packs.value}

        streamer_mode = self.options.streamer_mode_enabled
        (lower_diff_threshold, higher_diff_threshold) = self.get_difficulty_range()

        # The minimum amount of songs to make an ok rando would be Starting Songs + 10 interim songs + Goal song.
        # - Interim songs being equal to max starting song count.
        # Note: The worst settings still allow 25 songs (Streamer Mode + No DLC).
        starter_song_count = self.options.starting_song_count.value

        while True:
            # In most cases this should only need to run once
            available_song_keys = self.md_collection.get_songs_with_settings(
                dlc_songs, bool(streamer_mode.value), lower_diff_threshold, higher_diff_threshold)

            available_song_keys = self.handle_plando(available_song_keys, dlc_songs)

            count_needed_for_start = max(0, starter_song_count - len(self.starting_songs))
            if len(available_song_keys) + len(self.included_songs) >= count_needed_for_start + 11:
                final_song_list = available_song_keys
                break

            # If the above fails, we want to adjust the difficulty thresholds.
            # Easier first, then harder
            if lower_diff_threshold <= 1 and higher_diff_threshold >= 11:
                raise OptionError("Failed to find enough songs, even with maximum difficulty thresholds. "
                                  "Too many songs have been excluded or set to be starter songs.")
            elif lower_diff_threshold <= 1:
                higher_diff_threshold += 1
            else:
                lower_diff_threshold -= 1

        self.create_song_pool(final_song_list)

        for song in self.starting_songs:
            self.multiworld.push_precollected(self.create_item(song))

    def handle_plando(self, available_song_keys: List[str], dlc_songs: Set[str]) -> List[str]:
        song_items = self.md_collection.song_items

        start_items = self.options.start_inventory.value.keys()
        include_songs = self.options.include_songs.value
        exclude_songs = self.options.exclude_songs.value
        chosen_goal_songs = sorted(self.options.goal_song)

        self.starting_songs = [s for s in start_items if s in song_items]
        self.starting_songs = self.md_collection.filter_songs_to_dlc(self.starting_songs, dlc_songs)
        self.included_songs = [s for s in include_songs if s in song_items and s not in self.starting_songs]
        self.included_songs = self.md_collection.filter_songs_to_dlc(self.included_songs, dlc_songs)

        # Making sure songs chosen for goal are allowed by DLC and remove the chosen from being added to the pool.
        if chosen_goal_songs:
            chosen_goal_songs = self.md_collection.filter_songs_to_dlc(chosen_goal_songs, dlc_songs)
            if chosen_goal_songs:
                self.random.shuffle(chosen_goal_songs)
                self.victory_song_name = chosen_goal_songs.pop()
                if self.victory_song_name in self.starting_songs:
                    self.starting_songs.remove(self.victory_song_name)
                if self.victory_song_name in self.included_songs:
                    self.included_songs.remove(self.victory_song_name)

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
            if not self.victory_song_name:
                self.victory_song_name = self.included_songs.pop()
            while len(self.included_songs) > additional_song_count:
                next_song = self.included_songs.pop()
                if len(self.starting_songs) < starting_song_count:
                    self.starting_songs.append(next_song)
        elif not self.victory_song_name:
            # If not, choose a random victory song from the available songs
            chosen_song = self.random.randrange(0, len(available_song_keys) + included_song_count)
            if chosen_song < included_song_count:
                self.victory_song_name = self.included_songs[chosen_song]
                del self.included_songs[chosen_song]
            else:
                self.victory_song_name = available_song_keys[chosen_song - included_song_count]
                del available_song_keys[chosen_song - included_song_count]
        elif self.victory_song_name in available_song_keys:
            available_song_keys.remove(self.victory_song_name)

        # Next, make sure the starting songs are fulfilled
        if len(self.starting_songs) < starting_song_count:
            for _ in range(len(self.starting_songs), starting_song_count):
                if len(available_song_keys) > 0:
                    self.starting_songs.append(available_song_keys.pop())
                else:
                    self.starting_songs.append(self.included_songs.pop())

        # Then attempt to fulfill any remaining songs for interim songs
        if len(self.included_songs) < additional_song_count:
            for _ in range(len(self.included_songs), self.options.additional_song_count):
                if len(available_song_keys) <= 0:
                    break
                self.included_songs.append(available_song_keys.pop())

        self.location_count = 2 * (len(self.starting_songs) + len(self.included_songs))

    def create_item(self, name: str) -> Item:
        if name == self.md_collection.MUSIC_SHEET_NAME:
            return MuseDashFixedItem(name, ItemClassification.progression_deprioritized_skip_balancing,
                                     self.md_collection.MUSIC_SHEET_CODE, self.player)

        filler = self.md_collection.filler_items.get(name)
        if filler:
            return MuseDashFixedItem(name, ItemClassification.filler, filler, self.player)

        trap = self.md_collection.trap_items.get(name)
        if trap:
            return MuseDashFixedItem(name, ItemClassification.trap, trap, self.player)

        song = self.md_collection.song_items[name]
        return MuseDashSongItem(name, self.player, song)

    def get_filler_item_name(self) -> str:
        return self.random.choices(self.filler_item_names, self.filler_item_weights)[0]

    def create_items(self) -> None:
        song_keys_in_pool = self.included_songs.copy()

        # Note: Item count will be off if plando is involved.
        item_count = self.get_music_sheet_count()

        # First add all goal song tokens
        for _ in range(0, item_count):
            self.multiworld.itempool.append(self.create_item(self.md_collection.MUSIC_SHEET_NAME))

        # Then add 1 copy of every song
        item_count += len(self.included_songs)
        for song in self.included_songs:
            self.multiworld.itempool.append(self.create_item(song))

        # Then add all traps, making sure we don't over fill
        trap_count = min(self.location_count - item_count, self.get_trap_count())
        trap_list = self.get_available_traps()
        if len(trap_list) > 0 and trap_count > 0:
            for _ in range(0, trap_count):
                index = self.random.randrange(0, len(trap_list))
                self.multiworld.itempool.append(self.create_item(trap_list[index]))

            item_count += trap_count

        # At this point, if a player is using traps, it's possible that they have filled all locations
        items_left = self.location_count - item_count
        if items_left <= 0:
            return

        # When it comes to filling remaining spaces, we have 2 options. A useless filler or additional songs.
        # First fill 50% with the filler. The rest is to be duplicate songs.
        filler_count = floor(0.5 * items_left)
        items_left -= filler_count

        for _ in range(0, filler_count):
            self.multiworld.itempool.append(self.create_item(self.get_filler_item_name()))

        # All remaining spots are filled with duplicate songs. Duplicates are set to useful instead of progression
        # to cut down on the number of progression items that Muse Dash puts into the pool.

        # This is for the extraordinary case of needing to fill a lot of items.
        while items_left > len(song_keys_in_pool):
            for key in song_keys_in_pool:
                item = self.create_item(key)
                item.classification = ItemClassification.useful
                self.multiworld.itempool.append(item)

            items_left -= len(song_keys_in_pool)
            continue

        # Otherwise add a random assortment of songs
        self.random.shuffle(song_keys_in_pool)
        for i in range(0, items_left):
            item = self.create_item(song_keys_in_pool[i])
            item.classification = ItemClassification.useful
            self.multiworld.itempool.append(item)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions += [menu_region]

        # Make a collection of all songs available for this rando.
        # 1. All starting songs
        # 2. All other songs shuffled
        # Doing it in this order ensures that starting songs are first in line to getting 2 locations.
        # Final song is excluded as for the purpose of this rando, it doesn't matter.

        all_selected_locations = self.starting_songs.copy()
        included_song_copy = self.included_songs.copy()

        self.random.shuffle(included_song_copy)
        all_selected_locations.extend(included_song_copy)

        # Adds 2 item locations per song/album to the menu region.
        for i in range(0, len(all_selected_locations)):
            name = all_selected_locations[i]
            loc1 = MuseDashLocation(self.player,  name + "-0", self.md_collection.song_locations[name + "-0"], menu_region)
            loc1.access_rule = lambda state, place=name: state.has(place, self.player)
            menu_region.locations.append(loc1)

            loc2 = MuseDashLocation(self.player,  name + "-1", self.md_collection.song_locations[name + "-1"], menu_region)
            loc2.access_rule = lambda state, place=name: state.has(place, self.player)
            menu_region.locations.append(loc2)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: \
            state.has(self.md_collection.MUSIC_SHEET_NAME, self.player, self.get_music_sheet_win_count())

    def get_available_traps(self) -> List[str]:
        full_trap_list = self.md_collection.trap_items.keys()
        if self.md_collection.MUSE_PLUS_DLC not in self.options.dlc_packs.value:
            full_trap_list = [trap for trap in full_trap_list if trap not in self.md_collection.sfx_trap_items]

        return [trap for trap in full_trap_list if trap in self.options.chosen_traps.value]

    def get_trap_count(self) -> int:
        multiplier = self.options.trap_count_percentage.value / 100.0
        trap_count = len(self.starting_songs) + len(self.included_songs)
        return max(0, floor(trap_count * multiplier))

    def get_music_sheet_count(self) -> int:
        multiplier = self.options.music_sheet_count_percentage.value / 100.0
        song_count = len(self.starting_songs) + len(self.included_songs)
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
            "gradeNeeded": self.options.grade_needed.value,
        }
