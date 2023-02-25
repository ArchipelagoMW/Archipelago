from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule
from BaseClasses import Region, RegionType, Item, ItemClassification, MultiWorld, Entrance, Tutorial

from math import floor

from .Options import musedash_options
from .Items import MuseDashItem, MuseDashFixedItem
from .Locations import MuseDashLocation
from .MuseDashCollection import MuseDashCollections

client_version = 1


class MuseDashWebWorld(WebWorld):
    theme: "partyTime"

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
    """Muse Dash is a rhythm game, where you hit objects to the beat of one of 400+ songs.
    Have fun playing as cute girls, while you go through randomly chosen songs, until you reach the goal."""

    # World Options
    game: str = "Muse Dash"
    option_definitions = musedash_options
    topology_present = False
    data_version = 0
    web = MuseDashWebWorld()

    music_sheet_name: str = "Music Sheet"

    # Necessary Data
    museDashCollection = MuseDashCollections(290000, 2)

    item_name_to_id = {
        name: data.code for name, data in museDashCollection.AlbumItems.items() | museDashCollection.SongItems.items()
    }
    item_name_to_id[music_sheet_name] = museDashCollection.MusicSheetID

    location_name_to_id = {
        name: id for name, id in museDashCollection.AlbumLocations.items() | museDashCollection.SongLocations.items()
    }

    # Working Data
    victory_song_name: str = ""
    starting_songs: list[str]
    included_songs: list[str]
    needed_token_count: int
    location_count: int

    def generate_early(self):
        #Todo: Support Plando stuff? i.e. Starting Items, Goal Item etc

        dlc_songs = self.multiworld.allow_just_as_planned_dlc_songs[self.player]
        streamer_mode = self.multiworld.streamer_mode_enabled[self.player]

        diff_threshold = self.get_difficulty_range()

        available_song_keys = self.museDashCollection.get_all_songs_with_settings(dlc_songs, streamer_mode, diff_threshold[0], diff_threshold[1])
        self.create_song_pool(available_song_keys)

        #Todo: where should we have pre collected items?
        for song in self.starting_songs:
            self.multiworld.push_precollected(self.create_item(song))


    def create_song_pool(self, available_song_keys: list[str]):
        # Sanity checks to ensure we can even generate
        total_available_songs = len(available_song_keys)

        startingSongCount = self.multiworld.starting_song_count[self.player]
        if (total_available_songs < startingSongCount + 2): # Needs Starting Songs + Victory Song + At least 1 intermediary song
            raise Exception("Not enough songs available to satify the starting song count.")

        self.included_songs = list()
        self.starting_songs = list()

        self.victory_song_name = self.get_random_item_and_remove(available_song_keys)

        for _ in range(0, startingSongCount):
            self.starting_songs.append(self.get_random_item_and_remove(available_song_keys))

        for _ in range(0, self.multiworld.additional_song_count[self.player]):
            if (len(available_song_keys) <= 0):
                break

            self.included_songs.append(self.get_random_item_and_remove(available_song_keys))

        self.location_count = len(self.starting_songs) + len(self.included_songs)
        location_multiplier = 1 + (self.multiworld.additional_item_percentage[self.player] / 100.0)
        self.location_count = floor(self.location_count * location_multiplier)

        minimum_location_count = len(self.included_songs) + self.multiworld.music_sheet_count[self.player].value
        if (self.location_count < minimum_location_count):
            self.location_count = minimum_location_count


    def get_random_item_and_remove(self, list: list[str]) -> str:
        index = self.multiworld.random.randrange(0, len(list))
        choice = list[index]
        list.pop(index)
        return choice


    def create_item(self, name: str) -> Item:
        if (name == self.music_sheet_name):
            return MuseDashFixedItem(name, ItemClassification.progression_skip_balancing, self.player, self.museDashCollection.MusicSheetID)

        song = self.museDashCollection.SongItems.get(name)
        if (song != None):
            return MuseDashItem(name, self.player, song)

        album = self.museDashCollection.AlbumItems.get(name)
        if (album != None):
            return MuseDashItem(name, self.player, album)

        #Todo: Are items like this usually just return None?
        return MuseDashFixedItem(name, ItemClassification.filler, self.player, None)


    def create_items(self) -> None:
        song_keys_in_pool = list(self.included_songs)

        created_item_count = self.multiworld.music_sheet_count[self.player].value # Note: this does not count anything from Plando

        # First add all goal song tokens
        for _ in range(0, created_item_count):
            self.multiworld.itempool.append(self.create_item(self.music_sheet_name))

        # Next fill all remaining slots with song items
        needed_item_count = self.location_count
        while (created_item_count < needed_item_count):
            # If we have more items needed than keys, just iterate the list and add them all
            if (len(song_keys_in_pool) <= needed_item_count - created_item_count):
                for key in song_keys_in_pool:
                    self.multiworld.itempool.append(self.create_item(key))

                created_item_count += len(song_keys_in_pool)
                continue

            # Otherwise add a random assortment of songs
            self.multiworld.random.shuffle(song_keys_in_pool)
            for i in range(0, needed_item_count - created_item_count):
                self.multiworld.itempool.append(self.create_item(song_keys_in_pool[i]))

            created_item_count = needed_item_count


    def create_regions(self) -> None:
        # Basic Region Setup: Menu -> Song Select -> Songs
        mainMenu = Region("Menu", RegionType.Generic, "Menu", self.player, self.multiworld)
        songSelect = Region("Song Select", RegionType.Generic, "Song Select", self.player, self.multiworld)

        songSelectExit = Entrance(self.player, "Song Select Entrance", mainMenu)

        mainMenu.exits.append(songSelectExit)
        songSelectExit.connect(songSelect)

        self.multiworld.regions.append(mainMenu)
        self.multiworld.regions.append(songSelect)

        # Make a collection of all songs available for this rando
        # Final Song is excluded as it doesn't matter
        all_selected_locations = list(self.starting_songs)
        included_song_copy = list(self.included_songs)

        self.multiworld.random.shuffle(included_song_copy)
        all_selected_locations.extend(included_song_copy)

        two_item_location_count = self.location_count - len(all_selected_locations)

        # Make a region per song/album, then adds 1-2 item locations to them
        for i in range(0, len(all_selected_locations)):
            name = all_selected_locations[i]
            region = Region(name, RegionType.Generic, name, self.player, self.multiworld)

            # 2 Locations are defined per song
            location_name = name + "-0"
            region.locations.append(MuseDashLocation(self.player, location_name, self.museDashCollection.SongLocations[location_name], region))

            if (i < two_item_location_count):
                location_name = name + "-1"
                region.locations.append(MuseDashLocation(self.player, location_name, self.museDashCollection.SongLocations[location_name], region))

            regionExit = Entrance(self.player, name, songSelect)
            songSelect.exits.append(regionExit)
            regionExit.connect(region)
            self.multiworld.regions.append(region)


    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has(self.music_sheet_name, self.player, self.get_number_of_music_sheets_to_win())

        for location in self.multiworld.get_locations(self.player):
            itemName = location.name[0:(len(location.name) - 2)]
            if (itemName == self.victory_song_name):
                set_rule(location, lambda state: state.has(self.music_sheet_name, self.player, self.get_number_of_music_sheets_to_win()))
            else:
                set_rule(location, lambda state, place=itemName: state.has(place, self.player))


    def get_number_of_music_sheets_to_win(self) -> int:
        return min(self.multiworld.music_sheet_win_count[self.player].value, self.multiworld.music_sheet_count[self.player].value)

    def get_difficulty_range(self) -> list[int, int]:
        difficultyMode = self.multiworld.song_difficulty_mode[self.player]

        diffThreshold = [0, 20]
        if (difficultyMode == 1):
            diffThreshold[1] = 3
        elif (difficultyMode == 2):
            diffThreshold[0] = 4
            diffThreshold[1] = 5
        elif (difficultyMode == 3):
            diffThreshold[0] = 6
            diffThreshold[1] = 7
        elif (difficultyMode == 4):
            diffThreshold[0] = 8
            diffThreshold[1] = 9
        elif (difficultyMode == 5):
            diffThreshold[0] = 10
        elif (difficultyMode == 6):
            minDiff = self.multiworld.song_difficulty_min[self.player]
            maxDiff = self.multiworld.song_difficulty_max[self.player]

            #Cover for stupidity
            diffThreshold[0] = min(minDiff, maxDiff)
            diffThreshold[1] = max(minDiff, maxDiff)

        return diffThreshold


    def fill_slot_data(self):
        return {
            "victoryLocation": self.victory_song_name,
            "deathLink": self.multiworld.death_link[self.player].value,
            "musicSheetWinCount": self.get_number_of_music_sheets_to_win(),
            "gradeNeeded" : self.multiworld.grade_needed[self.player].value
        }
