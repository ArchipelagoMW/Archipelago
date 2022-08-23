import random
from typing import List, Dict, Any
from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification, RegionType
from worlds.generic.Rules import set_rule
from ..AutoWorld import World, WebWorld
from . import Items, Locations, Options, Rules, Exits


class Hylics2Web(WebWorld):
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
    Hylics 2 is a surreal and unusual RPG, with an equally bizarre yet unique visual style. Play as Wayne, 
    travel the world, and gather your allies to defeat the nefarious Gibby in his Hylemxylem!
    """
    game: str = "Hylics 2"
    web = Hylics2Web()

    item_name_to_id = {data["name"]: item_id for item_id, data in Items.item_table.items()}
    location_name_to_id = {data["name"]: loc_id for loc_id, data in Locations.location_table.items()}
    option_definitions = Options.hylics2_options

    topology_present: bool = True
    remote_items: bool = True
    remote_start_inventory: bool = True

    data_version: 0


    def set_rules(self):
        Rules.set_rules(self)


    def create_item(self, name: str, classification: ItemClassification, code: int) -> "Item":
        return Hylics2Item(name, classification, code, self.player)


    def create_event(self, event: str):
        return Hylics2Item(event, ItemClassification.progression_skip_balancing, None, self.player)


    def generate_basic(self):
        # create location for beating the game and place Victory event there
        loc = Location(self.player, "Defeat Gibby", None, self.world.get_region("Hylemxylem", self.player))
        loc.place_locked_item(self.create_event("Victory"))
        set_rule(loc, lambda state: state._hylics2_has_upper_chamber_key(self.player)
            and state._hylics2_has_vessel_room_key(self.player))
        self.world.get_region("Hylemxylem", self.player).locations.append(loc)
        self.world.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        # create item pool
        pool = []
        
        # add regular items
        for i, data in Items.item_table.items():
            if data["count"] > 0:
                for j in range(data["count"]):
                    pool.append(self.create_item(data["name"], data["classification"], i))

        # add party members if option is enabled
        if self.world.party_shuffle[self.player]:
            for i, data in Items.party_item_table.items():
                pool.append(self.create_item(data["name"], data["classification"], i))

        # handle gesture shuffle options
        if self.world.gesture_shuffle[self.player] == 2: # vanilla locations
            gestures = Items.gesture_item_table
            self.world.get_location("Waynehouse: TV", self.player)\
                .place_locked_item(self.create_item(gestures[200678]["name"], # POROMER BLEB
                    gestures[200678]["classification"], 200678))
            self.world.get_location("Afterlife: TV", self.player)\
                .place_locked_item(self.create_item(gestures[200683]["name"], # TELEDENUDATE
                    gestures[200683]["classification"], 200683))
            self.world.get_location("New Muldul: TV", self.player)\
                .place_locked_item(self.create_item(gestures[200679]["name"], # SOUL CRISPER
                    gestures[200679]["classification"], 200679))
            self.world.get_location("Viewax's Edifice: TV", self.player)\
                .place_locked_item(self.create_item(gestures[200680]["name"], # TIME SIGIL
                    gestures[200680]["classification"], 200680))
            self.world.get_location("TV Island: TV", self.player)\
                .place_locked_item(self.create_item(gestures[200681]["name"], # CHARGE UP
                    gestures[200681]["classification"], 200681))
            self.world.get_location("Juice Ranch: TV", self.player)\
                .place_locked_item(self.create_item(gestures[200682]["name"], # FATE SANDBOX
                    gestures[200682]["classification"], 200682))
            self.world.get_location("Foglast: TV", self.player)\
                .place_locked_item(self.create_item(gestures[200684]["name"], # LINK MOLLUSC
                    gestures[200684]["classification"], 200684))
            self.world.get_location("Drill Castle: TV", self.player)\
                .place_locked_item(self.create_item(gestures[200688]["name"], # NEMATODE INTERFACE
                    gestures[200688]["classification"], 200688))
            self.world.get_location("Sage Airship: TV", self.player)\
                .place_locked_item(self.create_item(gestures[200685]["name"], # BOMBO - GENESIS
                    gestures[200685]["classification"], 200685))

        elif self.world.gesture_shuffle[self.player] == 1: # TVs only
            gestures = list(Items.gesture_item_table.items())
            tvs = list(Locations.tv_location_table.items())

            # if Extra Items in Logic is enabled place CHARGE UP first and make sure it doesn't get 
            # placed at Sage Airship: TV
            if self.world.extra_items_in_logic[self.player]:
                tv = random.choice(tvs)
                gest = gestures.index((200681, Items.gesture_item_table[200681]))
                while tv[1]["name"] == "Sage Airship: TV":
                    tv = random.choice(tvs)
                self.world.get_location(tv[1]["name"], self.player)\
                    .place_locked_item(self.create_item(gestures[gest][1]["name"], 
                        gestures[gest][1]["classification"], gestures[gest][0]))
                gestures.remove(gestures[gest])
                tvs.remove(tv)

            for i in range(len(gestures)):
                gest = random.choice(gestures)
                tv = random.choice(tvs)
                self.world.get_location(tv[1]["name"], self.player)\
                    .place_locked_item(self.create_item(gest[1]["name"], gest[1]["classification"], gest[0]))
                gestures.remove(gest)
                tvs.remove(tv)

        else: # add to pool like normal
            for i, data in Items.gesture_item_table.items():
                pool.append(self.create_item(data["name"], data["classification"], i))

        # add to world's pool
        self.world.itempool += pool


    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            "party_shuffle": self.world.party_shuffle[self.player].value,
            "gesture_shuffle": self.world.gesture_shuffle[self.player].value,
            "extra_items_in_logic": self.world.extra_items_in_logic[self.player].value,
            "death_link": self.world.death_link[self.player].value
        }
        return slot_data


    def create_regions(self) -> None:

        region_table: Dict[int, Region] = {
            0: Region("Menu", RegionType.Generic, "Menu", self.player, self.world),
            1: Region("Afterlife", RegionType.Generic, "Afterlife", self.player, self.world),
            2: Region("Waynehouse", RegionType.Generic, "Waynehouse", self.player, self.world),
            3: Region("World", RegionType.Generic, "World", self.player, self.world),
            4: Region("New Muldul", RegionType.Generic, "New Muldul", self.player, self.world),
            5: Region("New Muldul Vault", RegionType.Generic, "New Muldul Vault", self.player, self.world),
            6: Region("Viewax", RegionType.Generic, "Viewax's Edifice", self.player, self.world),
            7: Region("Airship", RegionType.Generic, "Airship", self.player, self.world),
            8: Region("Arcade Island", RegionType.Generic, "Arcade Island", self.player, self.world),
            9: Region("TV Island", RegionType.Generic, "TV Island", self.player, self.world),
            10: Region("Juice Ranch", RegionType.Generic, "Juice Ranch", self.player, self.world),
            11: Region("Shield Facility", RegionType.Generic, "Shield Facility", self.player, self.world),
            12: Region("Worm Pod", RegionType.Generic, "Worm Pod", self.player, self.world),
            13: Region("Foglast", RegionType.Generic, "Foglast", self.player, self.world),
            14: Region("Drill Castle", RegionType.Generic, "Drill Castle", self.player, self.world),
            15: Region("Sage Labyrinth", RegionType.Generic, "Sage Labyrinth", self.player, self.world),
            16: Region("Sage Airship", RegionType.Generic, "Sage Airship", self.player, self.world),
            17: Region("Hylemxylem", RegionType.Generic, "Hylemxylem", self.player, self.world)
        }
        
        # create regions from table
        for i, reg in region_table.items():
            self.world.regions.append(reg)
            # get all exits per region
            for j, exits in Exits.region_exit_table.items():
                if j == i:
                    for k in exits:
                        # create entrance and connect it to parent and destination regions
                        ent = Entrance(self.player, k, reg)
                        reg.exits.append(ent)
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
        if self.world.party_shuffle[self.player]:
            for i, data in Locations.party_location_table.items():
                region_table[data["region"]].locations\
                    .append(Hylics2Location(self.player, data["name"], i, region_table[data["region"]]))


class Hylics2Location(Location):
    game: str = "Hylics 2"


class Hylics2Item(Item):
    game: str = "Hylics 2"