from typing import Dict, List, Any
from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification
from worlds.generic.Rules import set_rule
from . import Exits, Items, Locations, Rules
from .Options import Hylics2Options
from worlds.AutoWorld import WebWorld, World


class Hylics2Web(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to settings up the Hylics 2 randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["TRPG"]
    )]


class Hylics2World(World):
    """
    Hylics 2 is a surreal and unusual RPG, with a bizarre yet unique visual style. Play as Wayne,
    travel the world, and gather your allies to defeat the nefarious Gibby in his Hylemxylem!
    """
    game: str = "Hylics 2"
    web = Hylics2Web()

    all_items = {**Items.item_table, **Items.gesture_item_table, **Items.party_item_table,
        **Items.medallion_item_table}
    all_locations = {**Locations.location_table, **Locations.tv_location_table, **Locations.party_location_table,
        **Locations.medallion_location_table}

    item_name_to_id = {data["name"]: item_id for item_id, data in all_items.items()}
    location_name_to_id = {data["name"]: loc_id for loc_id, data in all_locations.items()}

    options_dataclass = Hylics2Options
    options: Hylics2Options


    def set_rules(self):
        Rules.set_rules(self)


    def create_item(self, name: str) -> "Hylics2Item":
        item_id: int = self.item_name_to_id[name]

        return Hylics2Item(name, self.all_items[item_id]["classification"], item_id, player=self.player)


    def create_event(self, event: str):
        return Hylics2Item(event, ItemClassification.progression_skip_balancing, None, self.player)


    def create_items(self):
        # create item pool
        pool = []

        # add regular items
        for item in Items.item_table.values():
            if item["count"] > 0:
                for _ in range(item["count"]):
                    pool.append(self.create_item(item["name"]))

        # add party members if option is enabled
        if self.options.party_shuffle:
            for item in Items.party_item_table.values():
                pool.append(self.create_item(item["name"]))

        # handle gesture shuffle
        if not self.options.gesture_shuffle: # add gestures to pool like normal
            for item in Items.gesture_item_table.values():
                pool.append(self.create_item(item["name"]))

        # add '10 Bones' items if medallion shuffle is enabled
        if self.options.medallion_shuffle:
            for item in Items.medallion_item_table.values():
                for _ in range(item["count"]):
                    pool.append(self.create_item(item["name"]))

        # add to world's pool
        self.multiworld.itempool += pool


    def pre_fill(self):
        # handle gesture shuffle options
        if self.options.gesture_shuffle == 2: # vanilla locations
            gestures = Items.gesture_item_table
            self.multiworld.get_location("Waynehouse: TV", self.player)\
                .place_locked_item(self.create_item("POROMER BLEB"))
            self.multiworld.get_location("Afterlife: TV", self.player)\
                .place_locked_item(self.create_item("TELEDENUDATE"))
            self.multiworld.get_location("New Muldul: TV", self.player)\
                .place_locked_item(self.create_item("SOUL CRISPER"))
            self.multiworld.get_location("Viewax's Edifice: TV", self.player)\
                .place_locked_item(self.create_item("TIME SIGIL"))
            self.multiworld.get_location("TV Island: TV", self.player)\
                .place_locked_item(self.create_item("CHARGE UP"))
            self.multiworld.get_location("Juice Ranch: TV", self.player)\
                .place_locked_item(self.create_item("FATE SANDBOX"))
            self.multiworld.get_location("Foglast: TV", self.player)\
                .place_locked_item(self.create_item("LINK MOLLUSC"))
            self.multiworld.get_location("Drill Castle: TV", self.player)\
                .place_locked_item(self.create_item("NEMATODE INTERFACE"))
            self.multiworld.get_location("Sage Airship: TV", self.player)\
                .place_locked_item(self.create_item("BOMBO - GENESIS"))

        elif self.options.gesture_shuffle == 1: # TVs only
            gestures = [gesture["name"] for gesture in Items.gesture_item_table.values()]
            tvs = [tv["name"] for tv in Locations.tv_location_table.values()]

            # if Extra Items in Logic is enabled place CHARGE UP first and make sure it doesn't get
            # placed at Sage Airship: TV or Foglast: TV
            if self.options.extra_items_in_logic:
                tv = self.random.choice(tvs)
                while tv == "Sage Airship: TV" or tv == "Foglast: TV":
                    tv = self.random.choice(tvs)
                self.multiworld.get_location(tv, self.player)\
                    .place_locked_item(self.create_item("CHARGE UP"))
                gestures.remove("CHARGE UP")
                tvs.remove(tv)

            self.random.shuffle(gestures)
            self.random.shuffle(tvs)
            while gestures:
                gesture = gestures.pop()
                tv = tvs.pop()
                self.get_location(tv).place_locked_item(self.create_item(gesture))


    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            "party_shuffle": self.options.party_shuffle.value,
            "medallion_shuffle": self.options.medallion_shuffle.value,
            "random_start": int(self.options.start_location != "waynehouse"),
            "start_location" : self.options.start_location.current_option_name,
            "death_link": self.options.death_link.value
        }
        return slot_data


    def create_regions(self) -> None:

        region_table: Dict[int, Region] = {
            0: Region("Menu", self.player, self.multiworld),
            1: Region("Afterlife", self.player, self.multiworld),
            2: Region("Waynehouse", self.player, self.multiworld),
            3: Region("World", self.player, self.multiworld),
            4: Region("New Muldul", self.player, self.multiworld),
            5: Region("New Muldul Vault", self.player, self.multiworld),
            6: Region("Viewax", self.player, self.multiworld, "Viewax's Edifice"),
            7: Region("Airship", self.player, self.multiworld),
            8: Region("Arcade Island", self.player, self.multiworld),
            9: Region("TV Island", self.player, self.multiworld),
            10: Region("Juice Ranch", self.player, self.multiworld),
            11: Region("Shield Facility", self.player, self.multiworld),
            12: Region("Worm Pod", self.player, self.multiworld),
            13: Region("Foglast", self.player, self.multiworld),
            14: Region("Drill Castle", self.player, self.multiworld),
            15: Region("Sage Labyrinth", self.player, self.multiworld),
            16: Region("Sage Airship", self.player, self.multiworld),
            17: Region("Hylemxylem", self.player, self.multiworld)
        }

        # create regions from table
        for i, reg in region_table.items():
            self.multiworld.regions.append(reg)
            # get all exits per region
            for j, exits in Exits.region_exit_table.items():
                if j == i:
                    for k in exits:
                        # create entrance and connect it to parent and destination regions
                        ent = Entrance(self.player, f"{reg.name} {k}", reg)
                        reg.exits.append(ent)
                        if k == "New Game":
                            if self.options.start_location == "waynehouse":
                                ent.connect(region_table[2])
                            elif self.options.start_location == "viewaxs_edifice":
                                ent.connect(region_table[6])
                            elif self.options.start_location == "tv_island":
                                ent.connect(region_table[9])
                            elif self.options.start_location == "shield_facility":
                                ent.connect(region_table[11])
                        else:
                            for name, num in Exits.exit_lookup_table.items():
                                if k == name:
                                    ent.connect(region_table[num])

        # add regular locations
        for i, data in Locations.location_table.items():
            region_table[data["region"]].locations\
                .append(Hylics2Location(self.player, data["name"], i, region_table[data["region"]]))
        for i, data in Locations.tv_location_table.items():
            region_table[data["region"]].locations\
                .append(Hylics2Location(self.player, data["name"], i, region_table[data["region"]]))

        # add party member locations if option is enabled
        if self.options.party_shuffle:
            for i, data in Locations.party_location_table.items():
                region_table[data["region"]].locations\
                    .append(Hylics2Location(self.player, data["name"], i, region_table[data["region"]]))

        # add medallion locations if option is enabled
        if self.options.medallion_shuffle:
            for i, data in Locations.medallion_location_table.items():
                region_table[data["region"]].locations\
                    .append(Hylics2Location(self.player, data["name"], i, region_table[data["region"]]))

        # create location for beating the game and place Victory event there
        loc = Location(self.player, "Defeat Gibby", None, self.multiworld.get_region("Hylemxylem", self.player))
        loc.place_locked_item(self.create_event("Victory"))
        set_rule(loc, lambda state: (
                state.has("UPPER CHAMBER KEY", self.player)
                and state.has("VESSEL ROOM KEY", self.player)
            ))
        self.multiworld.get_region("Hylemxylem", self.player).locations.append(loc)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)


class Hylics2Location(Location):
    game: str = "Hylics 2"


class Hylics2Item(Item):
    game: str = "Hylics 2"
