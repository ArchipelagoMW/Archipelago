from BaseClasses import Tutorial, Region, Item, ItemClassification
from worlds.AutoWorld import WebWorld, World
from typing import List, ClassVar, Type
from math import floor
from Options import PerGameCommonOptions, OptionError

from .options import RotNOptions, rotn_option_groups
from .RiftCollections import RotNCollections
from .items import RotNSongItem, RotNFixedItem
from .locations import RotNLocation

class RotNWeb(WebWorld):
    theme = "stone"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Rift of the Necrodancer Archipelago mod",
        "English",
        "setup_en.md",
        "setup/en",
        ["studkid"]
    )]

    option_groups = rotn_option_groups

class RotNWorld(World):
    """
    Rift of the Necrodancer is a rhythm game where you hit monsters to the beat of one of 60+ songs.
    Play through a selection of randomly chosen songs, collecting diamonds
    until you have enough to play and complete the goal song!
    """
    game = "Rift of the Necrodancer"
    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = RotNOptions
    options: RotNOptions

    topology_present = False
    web = RotNWeb()
    ut_can_gen_without_yaml = True

    rift_collection = RotNCollections()
    filler_item_names = list(rift_collection.filler_items.keys())
    filler_item_weights = list(rift_collection.filler_weights.values())

    item_name_to_id = {name: code for name, code in rift_collection.item_names_to_id.items()}
    location_name_to_id = {name: code for name, code in rift_collection.location_names_to_id.items()}
    item_name_groups = rift_collection.getItemNameGroups()

    victory_song_name: str = ""
    victory_song_type: int = 0
    starting_songs: List[str] = []
    included_songs: List[str]
    final_song_ids: set[int] = set()
    location_count: int

    def generate_early(self):
        # Universal Tracker Support
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data: dict[str, any] = re_gen_passthrough[self.game]

            if "finalSongIDs" in slot_data:
                final = slot_data.get("finalSongIDs", [])
                self.included_songs = [key for key, song in self.rift_collection.song_items.items() if song.song_name in final]
                self.location_count = len(self.included_songs) * 2
            return
        
        min_diff = min(self.options.min_intensity.value, self.options.max_intensity.value)
        max_diff = max(self.options.min_intensity.value, self.options.max_intensity.value)

        starter_song_count = self.options.starting_song_count.value
        goal_song_pool = self.options.goal_song_pool.value

        while True:
            available_song_keys = self.rift_collection.getSongsWithSettings(self.options, min_diff, max_diff)
            available_song_keys = self.handle_plando(available_song_keys)

            # Find the proposed goal songs and add them to a new list
            victory_song_keys = []
            for goal_song_canidate in goal_song_pool:
                for index, available_song in enumerate(available_song_keys):
                    if goal_song_canidate == available_song:
                        # Include the canidates correlating index to the full list for later use
                        victory_song_keys.append([index, available_song])

            if victory_song_keys:
                chosen_song_index = self.random.randrange(0, len(victory_song_keys))
                self.victory_song_name = victory_song_keys[chosen_song_index][1]
                self.victory_song_type = self.rift_collection.song_items[self.victory_song_name].type
                # Replace the chosen goal song's index with the index from the full list we saved earlier.
                chosen_song_index = victory_song_keys[chosen_song_index][0]
            else:
                chosen_song_index = self.random.randrange(0, len(available_song_keys))
                self.victory_song_name = available_song_keys[chosen_song_index]
                self.victory_song_type = self.rift_collection.song_items[self.victory_song_name].type
            del available_song_keys[chosen_song_index]

            count_needed_for_start = max(0, starter_song_count - len(self.starting_songs))
            if len(available_song_keys) + len(self.included_songs) >= count_needed_for_start + 11:
                final_song_list = available_song_keys
                break

            # If the above fails, we want to adjust the difficulty thresholds.
            # Easier first, then harder
            if min_diff <= 1 and max_diff >= 40:
                raise OptionError("Failed to find enough songs, even with maximum difficulty thresholds.  (Did you exclude too many songs?)")
            elif min_diff <= 1:
                max_diff += 1
            else:
                min_diff -= 1

        self.create_song_pool(final_song_list)

        for song in self.starting_songs:
            self.multiworld.push_precollected(self.create_item(song))

    def handle_plando(self, available_song_keys: List[str]) -> List[str]:
        song_items = self.rift_collection.song_items

        start_items = self.options.start_inventory.value.keys()
        include_songs = self.options.include_songs.value
        exclude_songs = self.options.exclude_songs.value

        self.starting_songs = [s for s in start_items if s in available_song_keys]
        self.included_songs = [s for s in include_songs if s in available_song_keys and s not in self.starting_songs]

        return [s for s in available_song_keys if s not in start_items
                and s not in include_songs and s not in exclude_songs]
    
    def create_song_pool(self, available_song_keys: List[str]):
        starting_song_count = self.options.starting_song_count.value
        additional_song_count = self.options.additional_song_count.value

        self.random.shuffle(available_song_keys)

        # First, we must double check if the player has included too many guaranteed songs
        included_song_count = len(self.included_songs)
        if included_song_count > additional_song_count:
            # If so, we want to thin the list, thus let's get the starter songs while we are at it.
            self.random.shuffle(self.included_songs)
            while len(self.included_songs) > additional_song_count:
                next_song = self.included_songs.pop()
                if len(self.starting_songs) < starting_song_count:
                    self.starting_songs.append(next_song)

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
        if name == self.rift_collection.DIAMOND_NAME:
            return RotNFixedItem(name, ItemClassification.progression_skip_balancing,
                                 self.rift_collection.DIAMOND_CODE, self.player)
        
        filler = self.rift_collection.filler_items.get(name)
        if filler:
            return RotNFixedItem(name, ItemClassification.filler, filler, self.player)
        
        song = self.rift_collection.song_items[name]
        self.final_song_ids.add(song.song_name)
        return RotNSongItem(name, self.player, song)
    
    def get_filler_item_name(self):
        return self.random.choices(self.filler_item_names, self.filler_item_weights)[0]
    
    def create_items(self) -> None:
        song_keys_in_pool = self.included_songs.copy()

        # Note: Item count will be off if plando is involved.
        item_count = self.get_diamond_count()

        # First add all goal song tokens
        for _ in range(0, item_count):
            self.multiworld.itempool.append(self.create_item(self.rift_collection.DIAMOND_NAME))

        # Then add 1 copy of every song
        item_count += len(self.included_songs)
        for song in self.included_songs:
            self.multiworld.itempool.append(self.create_item(song))

        # At this point, if a player is using traps, it's possible that they have filled all locations
        items_left = self.location_count - item_count
        if items_left <= 0:
            return

        # When it comes to filling remaining spaces, we have 2 options. A useless filler or additional songs.
        # First fill 50% with the filler. The rest is to be duplicate songs.
        filler_count = floor(items_left * (self.options.duplicate_song_percentage / 100))
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
        for name in all_selected_locations:
            for j in range(2):
                loc = RotNLocation(self.player, f"{name}-{j}", self.rift_collection.song_locations[f"{name}-{j}"], menu_region)
                loc.access_rule = lambda state, item=name: state.has(item, self.player)
                menu_region.locations.append(loc)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: \
            state.has(self.rift_collection.DIAMOND_NAME, self.player, self.get_diamond_win_count())
                      
    def get_diamond_count(self) -> int:
        multiplier = self.options.diamond_count_percentage.value / 100.0
        song_count = len(self.starting_songs) + len(self.included_songs)
        return max(1, floor(song_count * multiplier))
    
    def get_diamond_win_count(self) -> int:
        multiplier = self.options.diamond_win_percentage.value / 100.0
        diamond_count = self.get_diamond_count()
        return max(1, floor(diamond_count * multiplier))
    
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, any]) -> dict[str, any]:
        return slot_data
    
    def fill_slot_data(self):
        return {
            "victoryLocation": self.victory_song_name,
            "victoryType": self.victory_song_type,
            "diamondWinCount": self.get_diamond_win_count(),
            "gradeNeeded": self.options.grade_needed.value,
            "fullComboNeeded": self.options.full_combo_needed.value,
            "remixes": self.options.include_remix.value,
            "minigameMode": self.options.include_minigames.value,
            "bossMode": self.options.include_boss_battle.value,
            "finalSongIDs": self.final_song_ids,
        }