import typing
import os
import json
from .Items import item_data_table, action_item_data_table, cannon_item_data_table, item_table, SM64Item
from .Locations import location_table, SM64Location
from .Options import sm64_options_groups, SM64Options
from .Rules import set_rules
from .Regions import create_regions, sm64_level_to_entrances, SM64Levels
from BaseClasses import Item, Tutorial, ItemClassification, Region
from ..AutoWorld import World, WebWorld


class SM64Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up SM64EX for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["N00byKing"]
    )]

    option_groups = sm64_options_groups


class SM64World(World):
    """ 
    The first Super Mario game to feature 3D gameplay, it features freedom of movement within a large open world based on polygons,
    combined with traditional Mario gameplay, visual style, and characters.
    """

    game: str = "Super Mario 64"
    topology_present = False

    web = SM64Web()

    item_name_to_id = item_table
    location_name_to_id = location_table

    required_client_version = (0, 3, 5)

    area_connections: typing.Dict[int, int]

    options_dataclass = SM64Options

    number_of_stars: int
    move_rando_bitvec: int
    filler_count: int
    star_costs: typing.Dict[str, int]

    # Spoiler specific variable(s)
    star_costs_spoiler_key_maxlen = len(max([
        'First Floor Big Star Door',
        'Basement Big Star Door',
        'Second Floor Big Star Door',
        'MIPS 1',
        'MIPS 2',
        'Endless Stairs',
    ], key=len))


    def generate_early(self):
        max_stars = 120
        if (not self.options.enable_coin_stars):
            max_stars -= 15
        self.move_rando_bitvec = 0
        if self.options.enable_move_rando:
            double_jump_bitvec_offset = action_item_data_table['Double Jump'].code
            for action in self.options.move_rando_actions.value:
                max_stars -= 1
                self.move_rando_bitvec |= (1 << (action_item_data_table[action].code - double_jump_bitvec_offset))
        if self.options.exclamation_boxes:
            max_stars += 29
        self.number_of_stars = min(self.options.amount_of_stars, max_stars)
        self.filler_count = max_stars - self.number_of_stars
        self.star_costs = {
            'FirstBowserDoorCost': round(self.options.first_bowser_star_door_cost * self.number_of_stars / 100),
            'BasementDoorCost': round(self.options.basement_star_door_cost * self.number_of_stars / 100),
            'SecondFloorDoorCost': round(self.options.second_floor_star_door_cost * self.number_of_stars / 100),
            'MIPS1Cost': round(self.options.mips1_cost * self.number_of_stars / 100),
            'MIPS2Cost': round(self.options.mips2_cost * self.number_of_stars / 100),
            'StarsToFinish': round(self.options.stars_to_finish * self.number_of_stars / 100)
        }
        # Nudge MIPS 1 to match vanilla on default percentage
        if self.number_of_stars == 120 and self.options.mips1_cost == 12:
            self.star_costs['MIPS1Cost'] = 15
        self.topology_present = self.options.area_rando

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)

    def set_rules(self):
        self.area_connections = {}
        set_rules(self.multiworld, self.options, self.player, self.area_connections, self.star_costs, self.move_rando_bitvec)
        if self.topology_present:
            # Write area_connections to spoiler log
            for entrance, destination in self.area_connections.items():
                self.multiworld.spoiler.set_entrance(
                    sm64_level_to_entrances[entrance] + " Entrance",
                    sm64_level_to_entrances[destination],
                    'entrance', self.player)

    def create_item(self, name: str) -> Item:
        data = item_data_table[name]
        item = SM64Item(name, data.classification, data.code, self.player)

        return item

    def create_items(self):
        # 1Up Mushrooms
        self.multiworld.itempool += [self.create_item("1Up Mushroom") for i in range(0,self.filler_count)]
        # Power Stars
        star_range = self.number_of_stars
        # Vanilla 100 Coin stars have to removed from the pool if other max star increasing options are active.
        if self.options.enable_coin_stars == "vanilla":
            star_range -= 15
        self.multiworld.itempool += [self.create_item("Power Star") for i in range(0,star_range)]
        # Keys
        if (not self.options.progressive_keys):
            key1 = self.create_item("Basement Key")
            key2 = self.create_item("Second Floor Key")
            self.multiworld.itempool += [key1, key2]
        else:
            self.multiworld.itempool += [self.create_item("Progressive Key") for i in range(0,2)]
        # Caps
        self.multiworld.itempool += [self.create_item(cap_name) for cap_name in ["Wing Cap", "Metal Cap", "Vanish Cap"]]
        # Cannons
        if (self.options.buddy_checks):
            self.multiworld.itempool += [self.create_item(cannon_name) for cannon_name in cannon_item_data_table.keys()]
        # Moves
        double_jump_bitvec_offset = action_item_data_table['Double Jump'].code
        self.multiworld.itempool += [self.create_item(action)
                                     for action, itemdata in action_item_data_table.items()
                                     if self.move_rando_bitvec & (1 << itemdata.code - double_jump_bitvec_offset)]

    def generate_basic(self):
        if not (self.options.buddy_checks):
            self.multiworld.get_location("BoB: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock BoB"))
            self.multiworld.get_location("WF: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock WF"))
            self.multiworld.get_location("JRB: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock JRB"))
            self.multiworld.get_location("CCM: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock CCM"))
            self.multiworld.get_location("SSL: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock SSL"))
            self.multiworld.get_location("SL: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock SL"))
            self.multiworld.get_location("WDW: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock WDW"))
            self.multiworld.get_location("TTM: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock TTM"))
            self.multiworld.get_location("THI: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock THI"))
            self.multiworld.get_location("RR: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock RR"))

        if not self.options.exclamation_boxes:
            self.multiworld.get_location("CCM: 1Up Block Near Snowman", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("CCM: 1Up Block Ice Pillar", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("CCM: 1Up Block Secret Slide", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("BBH: 1Up Block Top of Mansion", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("HMC: 1Up Block above Pit", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("HMC: 1Up Block Past Rolling Rocks", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("SSL: 1Up Block Outside Pyramid", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("SSL: 1Up Block Pyramid Left Path", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("SSL: 1Up Block Pyramid Back", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("SL: 1Up Block Near Moneybags", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("SL: 1Up Block inside Igloo", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("WDW: 1Up Block in Downtown", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("TTM: 1Up Block on Red Mushroom", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("THI: 1Up Block THI Small near Start", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("THI: 1Up Block THI Large near Start", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("THI: 1Up Block Windy Area", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("TTC: 1Up Block Midway Up", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("TTC: 1Up Block at the Top", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("RR: 1Up Block Top of Red Coin Maze", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("RR: 1Up Block Under Fly Guy", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("RR: 1Up Block On House in the Sky", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Bowser in the Dark World 1Up Block on Tower", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Bowser in the Dark World 1Up Block near Goombas", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Cavern of the Metal Cap 1Up Block", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Vanish Cap Under the Moat 1Up Block", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Bowser in the Fire Sea 1Up Block Swaying Stairs", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Bowser in the Fire Sea 1Up Block Near Poles", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Wing Mario Over the Rainbow 1Up Block", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Bowser in the Sky 1Up Block", self.player).place_locked_item(self.create_item("1Up Mushroom"))

        if (self.options.enable_coin_stars == "vanilla"):
            self.multiworld.get_location("BoB: 100 Coins", self.player).place_locked_item(self.create_item("Power Star"))
            self.multiworld.get_location("WF: 100 Coins", self.player).place_locked_item(self.create_item("Power Star"))
            self.multiworld.get_location("JRB: 100 Coins", self.player).place_locked_item(self.create_item("Power Star"))
            self.multiworld.get_location("CCM: 100 Coins", self.player).place_locked_item(self.create_item("Power Star"))
            self.multiworld.get_location("BBH: 100 Coins", self.player).place_locked_item(self.create_item("Power Star"))
            self.multiworld.get_location("HMC: 100 Coins", self.player).place_locked_item(self.create_item("Power Star"))
            self.multiworld.get_location("LLL: 100 Coins", self.player).place_locked_item(self.create_item("Power Star"))
            self.multiworld.get_location("SSL: 100 Coins", self.player).place_locked_item(self.create_item("Power Star"))
            self.multiworld.get_location("DDD: 100 Coins", self.player).place_locked_item(self.create_item("Power Star"))
            self.multiworld.get_location("SL: 100 Coins", self.player).place_locked_item(self.create_item("Power Star"))
            self.multiworld.get_location("WDW: 100 Coins", self.player).place_locked_item(self.create_item("Power Star"))
            self.multiworld.get_location("TTM: 100 Coins", self.player).place_locked_item(self.create_item("Power Star"))
            self.multiworld.get_location("THI: 100 Coins", self.player).place_locked_item(self.create_item("Power Star"))
            self.multiworld.get_location("TTC: 100 Coins", self.player).place_locked_item(self.create_item("Power Star"))
            self.multiworld.get_location("RR: 100 Coins", self.player).place_locked_item(self.create_item("Power Star"))

    def get_filler_item_name(self) -> str:
        return "1Up Mushroom"

    def fill_slot_data(self):
        return {
            "AreaRando": self.area_connections,
            "MoveRandoVec": self.move_rando_bitvec,
            "DeathLink": self.options.death_link.value,
            "CompletionType": self.options.completion_type.value,
            **self.star_costs
        }

    def generate_output(self, output_directory: str):
        if self.multiworld.players != 1:
            return
        data = {
            "slot_data": self.fill_slot_data(),
            "location_to_item": {self.location_name_to_id[i.name] : item_table[i.item.name] for i in self.multiworld.get_locations()},
            "data_package": {
                "data": {
                    "games": {
                        self.game: {
                            "item_name_to_id": self.item_name_to_id,
                            "location_name_to_id": self.location_name_to_id
                        }
                    }
                }
            }
        }
        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apsm64ex"
        with open(os.path.join(output_directory, filename), 'w') as f:
            json.dump(data, f)

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        if self.topology_present:
            er_hint_data = {}
            for entrance, destination in self.area_connections.items():
                regions = [self.multiworld.get_region(sm64_level_to_entrances[destination], self.player)]
                if regions[0].name == "Tiny-Huge Island (Huge)":
                    # Special rules for Tiny-Huge Island's dual entrances
                    reverse_area_connections = {destination: entrance for entrance, destination in self.area_connections.items()}
                    entrance_name = sm64_level_to_entrances[reverse_area_connections[SM64Levels.TINY_HUGE_ISLAND_HUGE]] \
                                    + ' or ' + sm64_level_to_entrances[reverse_area_connections[SM64Levels.TINY_HUGE_ISLAND_TINY]]
                    regions[0] = self.multiworld.get_region("Tiny-Huge Island", self.player)
                else:
                    entrance_name = sm64_level_to_entrances[entrance]
                regions += regions[0].subregions
                for region in regions:
                    for location in region.locations:
                        er_hint_data[location.address] = entrance_name
            hint_data[self.player] = er_hint_data

    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        # Write calculated star costs to spoiler.
        star_cost_spoiler_header = '\n\n' + self.player_name + ' Star Costs for Super Mario 64:\n\n'
        spoiler_handle.write(star_cost_spoiler_header)
        # - Reformat star costs dictionary in spoiler to be a bit more readable.
        star_costs_spoiler = {}
        star_costs_copy = self.star_costs.copy()
        star_costs_spoiler['First Floor Big Star Door'] = star_costs_copy['FirstBowserDoorCost']
        star_costs_spoiler['Basement Big Star Door'] = star_costs_copy['BasementDoorCost']
        star_costs_spoiler['Second Floor Big Star Door'] = star_costs_copy['SecondFloorDoorCost']
        star_costs_spoiler['MIPS 1'] = star_costs_copy['MIPS1Cost']
        star_costs_spoiler['MIPS 2'] = star_costs_copy['MIPS2Cost']
        star_costs_spoiler['Endless Stairs'] = star_costs_copy['StarsToFinish']
        for star, cost in star_costs_spoiler.items():
            spoiler_handle.write(f"{star:{self.star_costs_spoiler_key_maxlen}s} = {cost}\n")
