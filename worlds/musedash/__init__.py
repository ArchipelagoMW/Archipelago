from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule
from BaseClasses import Region, RegionType, Item, ItemClassification, MultiWorld, Entrance, Tutorial

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

    # Necessary Data
    museDashCollection = MuseDashCollections(95000, 2)

    item_name_to_id = {
        name: data.code for name, data in museDashCollection.AlbumItems.items() | museDashCollection.SongItems.items()
    }
    item_name_to_id["Victory"] = museDashCollection.VictoryItemID
    item_name_to_id["Nothing"] = museDashCollection.EmptyItemID

    location_name_to_id = {
        name: id for name, id in museDashCollection.AlbumLocations.items() | museDashCollection.SongLocations.items()
    }

    # Working Data
    victory_song_name: str = ""
    starting_songs: list[str]
    included_songs: list[str]

    def generate_early(self):
        available_song_keys = list()
        if (self.multiworld.allow_just_as_planned_dlc_songs[self.player]):
            available_song_keys.extend(self.museDashCollection.SongItems.keys())
        else:
            available_song_keys.extend(self.museDashCollection.BaseSongItems.keys())

        self.included_songs = list()
        self.starting_songs = list()

        self.victory_song_name = self.multiworld.random.choice(available_song_keys)
        available_song_keys.remove(self.victory_song_name)

        #Todo: maybe count starting items already taken
        startingSongCount = self.multiworld.starting_song_count[self.player]
        for _ in range(0, startingSongCount):
            item = self.multiworld.random.choice(available_song_keys)
            available_song_keys.remove(item)
            self.multiworld.push_precollected(self.create_item(item))
            self.starting_songs.append(item)

        for _ in range(0, self.multiworld.additional_song_count[self.player] - 1):
            if (len(available_song_keys) <= 0):
                break

            item = self.multiworld.random.choice(available_song_keys)
            available_song_keys.remove(item)
            self.included_songs.append(item)


    def generate_basic(self):
        victory_location = self.multiworld.get_location(self.victory_song_name + "-0", self.player)
        victory_location.place_locked_item(self.museDashCollection.create_victory_item(self.player))
        victory_location = self.multiworld.get_location(self.victory_song_name + "-1", self.player)
        victory_location.place_locked_item(self.museDashCollection.create_empty_item(self.player))

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)


    def create_item(self, name: str) -> Item:
        song = self.museDashCollection.SongItems.get(name)
        if (song != None):
            return MuseDashItem(name, self.player, song)

        album = self.museDashCollection.AlbumItems.get(name)
        if (album != None):
            return MuseDashItem(name, self.player, self.museDashCollection.Albums.get(name))

        #Todo: Are items like this usually just return None?
        return MuseDashFixedItem(name, ItemClassification.Filler, self.player, None)


    def create_items(self) -> None:
        all_song_item_keys = list(self.included_songs)
        all_song_item_keys.append(self.victory_song_name)

        # Start by adding 2 items for all spaces that have been included
        for itemName in all_song_item_keys:
            self.multiworld.itempool.append(self.create_item(itemName))
            self.multiworld.itempool.append(self.create_item(itemName))

        # Next figure out how many extra items that are needed.
        # - Each song that the player starts add 2 locations to the pool.
        # - But the victory song cannot have anything other than victory. (-2 locations)
        excludedItemCount = (len(self.starting_songs) - 1) * 2

        # Get the amount of these extra spaces that should be replaced with the goal song
        extra_goal_songs = min(excludedItemCount, self.multiworld.extra_goal_song_items[self.player])
        for _ in range(0, extra_goal_songs):
            self.multiworld.itempool.append(self.create_item(self.victory_song_name))

        # Determine if the leftover songs are empty items or random songs.
        extra_items_are_songs = self.multiworld.extra_items_are_songs[self.player]
        for _ in range(0, excludedItemCount - extra_goal_songs):
            if (extra_items_are_songs):
                songKey = self.multiworld.random.choice(all_song_item_keys)
                self.multiworld.itempool.append(self.create_item(songKey))
                all_song_item_keys.remove(songKey)
            else:
                self.multiworld.itempool.append(self.museDashCollection.create_empty_item(self.player))


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
        all_selected_locations = set(self.included_songs)
        for item in self.starting_songs:
            all_selected_locations.add(item)
        all_selected_locations.add(self.victory_song_name)

        for name in all_selected_locations:
            region = Region(name, RegionType.Generic, name, self.player, self.multiworld)

            # 2 Locations are defined per song
            location_name = name + "-0"
            region.locations.append(MuseDashLocation(self.player, location_name, self.museDashCollection.SongLocations[location_name], region))
            location_name = name + "-1"
            region.locations.append(MuseDashLocation(self.player, location_name, self.museDashCollection.SongLocations[location_name], region))

            regionExit = Entrance(self.player, name, songSelect)
            songSelect.exits.append(regionExit)
            regionExit.connect(region)
            self.multiworld.regions.append(region)


    def set_rules(self) -> None:
        for location in self.multiworld.get_locations(self.player):
            itemName = location.name[0:(len(location.name) - 2)]
            set_rule(location, lambda state, place=itemName: state.has(place, self.player))


    def fill_slot_data(self):
        return {
            # "deathLink": self.world.death_link[self.player].value, Todo: Add DeathLink
            "victoryLocation": self.victory_song_name,
            # Todo: Other options include "checkAlbums", "checkSongs"
        }
