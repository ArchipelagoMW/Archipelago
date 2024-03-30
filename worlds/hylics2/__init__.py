from typing import Dict, List, Any
from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification
from worlds.generic.Rules import set_rule
from . import Exits, Items, Locations, Options, Rules
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
    option_definitions = Options.hylics2_options

    data_version = 3

    start_location = "Waynehouse"


    def set_rules(self):
        Rules.set_rules(self)


    def create_item(self, name: str) -> "Hylics2Item":
        item_id: int = self.item_name_to_id[name]

        return Hylics2Item(name, self.all_items[item_id]["classification"], item_id, player=self.player)


    def create_event(self, event: str):
        return Hylics2Item(event, ItemClassification.progression_skip_balancing, None, self.player)


    # set random starting location if option is enabled
    def generate_early(self):
        if self.multiworld.random_start[self.player]:
            i = self.random.randint(0, 3)
            if i == 0:
                self.start_location = "Waynehouse"
            elif i == 1:
                self.start_location = "Viewax's Edifice"
            elif i == 2:
                self.start_location = "TV Island"
            elif i == 3:
                self.start_location = "Shield Facility"

    def create_items(self):
        # create item pool
        pool = []

        # add regular items
        for item in Items.item_table.values():
            if item["count"] > 0:
                for _ in range(item["count"]):
                    pool.append(self.create_item(item["name"]))

        # add party members if option is enabled
        if self.multiworld.party_shuffle[self.player]:
            for item in Items.party_item_table.values():
                pool.append(self.create_item(item["name"]))

        # handle gesture shuffle
        if not self.multiworld.gesture_shuffle[self.player]: # add gestures to pool like normal
            for item in Items.gesture_item_table.values():
                pool.append(self.create_item(item["name"]))

        # add '10 Bones' items if medallion shuffle is enabled
        if self.multiworld.medallion_shuffle[self.player]:
            for item in Items.medallion_item_table.values():
                for _ in range(item["count"]):
                    pool.append(self.create_item(item["name"]))

        # add to world's pool
        self.multiworld.itempool += pool


    def pre_fill(self):
        # handle gesture shuffle options
        if self.multiworld.gesture_shuffle[self.player] == 2: # vanilla locations
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

        elif self.multiworld.gesture_shuffle[self.player] == 1: # TVs only
            gestures = [gesture["name"] for gesture in Items.gesture_item_table.values()]
            tvs = [tv["name"] for tv in Locations.tv_location_table.values()]

            # if Extra Items in Logic is enabled place CHARGE UP first and make sure it doesn't get
            # placed at Sage Airship: TV or Foglast: TV
            if self.multiworld.extra_items_in_logic[self.player]:
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
            "party_shuffle": self.multiworld.party_shuffle[self.player].value,
            "medallion_shuffle": self.multiworld.medallion_shuffle[self.player].value,
            "random_start" : self.multiworld.random_start[self.player].value,
            "start_location" : self.start_location,
            "death_link": self.multiworld.death_link[self.player].value
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
                        if k == "New Game" and self.multiworld.random_start[self.player]:
                            if self.start_location == "Waynehouse":
                                ent.connect(region_table[2])
                            elif self.start_location == "Viewax's Edifice":
                                ent.connect(region_table[6])
                            elif self.start_location == "TV Island":
                                ent.connect(region_table[9])
                            elif self.start_location == "Shield Facility":
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
        if self.multiworld.party_shuffle[self.player]:
            for i, data in Locations.party_location_table.items():
                region_table[data["region"]].locations\
                    .append(Hylics2Location(self.player, data["name"], i, region_table[data["region"]]))

        # add medallion locations if option is enabled
        if self.multiworld.medallion_shuffle[self.player]:
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
