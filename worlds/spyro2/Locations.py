from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import Spyro2Item

class Spyro2LocationCategory(IntEnum):
    TALISMAN = 0,
    ORB = 1,
    EVENT = 2,
    GEM_25 = 3,
    GEM_50 = 4,
    GEM_75 = 5,
    GEM_100 = 6,
    SKILLPOINT = 7,
    SKILLPOINT_GOAL = 8,
    TOTAL_GEM = 9,
    SHORES_TOKEN = 10,
    MONEYBAGS = 11,
    LIFE_BOTTLE = 12,
    GEM = 13,
    SPIRIT_PARTICLE = 14


class Spyro2LocationData(NamedTuple):
    name: str
    default_item: str
    category: Spyro2LocationCategory


class Spyro2Location(Location):
    game: str = "Spyro 2"
    category: Spyro2LocationCategory
    default_item_name: str

    def __init__(
        self,
        player: int,
        name: str,
        category: Spyro2LocationCategory,
        default_item_name: str,
        address: Optional[int] = None,
        parent: Optional[Region] = None
    ):
        super().__init__(player, name, address, parent)
        self.default_item_name = default_item_name
        self.category = category
        self.name = name

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 1230000
        table_offset = 1000

        # Order follows the in-memory order of talismans and orbs.
        table_order = [
            "Summer Forest","Glimmer","Idol Springs","Colossus","Hurricos","Aquaria Towers","Sunny Beach","Ocean Speedway","Crush's Dungeon",
            "Autumn Plains","Skelos Badlands","Crystal Glacier","Breeze Harbor","Zephyr","Metro Speedway","Scorch","Shady Oasis","Magma Cone","Fracture Hills","Icy Speedway","Gulp's Overlook",
            "Winter Tundra","Mystic Marsh","Cloud Temples","Canyon Speedway","Robotica Farms","Metropolis","Dragon Shores","Ripto's Arena",
            "Inventory"
        ]

        output = {}
        for i, region_name in enumerate(table_order):
            if len(location_tables[region_name]) > table_offset:
                raise Exception("A location table has {} entries, that is more than {} entries (table #{})".format(len(location_tables[region_name]), table_offset, i))

            output.update({location_data.name: id for id, location_data in enumerate(location_tables[region_name], base_id + (table_offset * i))})

        return output

    def place_locked_item(self, item: Spyro2Item):
        self.item = item
        self.locked = True
        item.location = self


# To ensure backwards compatibility, do not reorder locations or insert new ones in the middle of a list.
location_tables = {
    # Homeworld 1
    "Summer Forest": [
        Spyro2LocationData("Summer Forest: Hunter's Challenge", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Summer Forest: On a secret ledge", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Summer Forest: Atop a ladder", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Summer Forest: Behind the door", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Summer Forest: Moneybags Unlock: Swim", "Moneybags Unlock - Swim", Spyro2LocationCategory.MONEYBAGS),
        Spyro2LocationData("Summer Forest: Moneybags Unlock: Door to Aquaria Towers", "Moneybags Unlock - Door to Aquaria Towers", Spyro2LocationCategory.MONEYBAGS),
        Spyro2LocationData("Summer Forest: First Life Bottle Near Glimmer", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
        Spyro2LocationData("Summer Forest: Second Life Bottle Near Glimmer", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
        Spyro2LocationData("Summer Forest: Life Bottle Near Sunny Beach", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Glimmer": [
        Spyro2LocationData("Glimmer: Talisman", "Summer Forest Talisman", Spyro2LocationCategory.TALISMAN),
        Spyro2LocationData("Glimmer: Lizard hunt", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Glimmer: Gem Lamp Flight outdoors", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Glimmer: Gem Lamp Flight in cave", "Orb", Spyro2LocationCategory.ORB),
        # The following leads to too restrictive a start.
        #Spyro2LocationData("Glimmer: Moneybags Unlock: Glimmer Bridge", "Moneybags Unlock - Glimmer Bridge", Spyro2LocationCategory.MONEYBAGS),
    ],
    "Idol Springs": [
        Spyro2LocationData("Idol Springs: Talisman", "Summer Forest Talisman", Spyro2LocationCategory.TALISMAN),
        Spyro2LocationData("Idol Springs: Foreman Bud's puzzles", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Idol Springs: Hula Girl rescue", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Idol Springs: Land on Idol (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Idol Springs: Land on Idol (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
        Spyro2LocationData("Idol Springs: Life Bottle", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Colossus": [
        Spyro2LocationData("Colossus: Talisman", "Summer Forest Talisman", Spyro2LocationCategory.TALISMAN),
        Spyro2LocationData("Colossus: Hockey vs. Goalie", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Colossus: Hockey one on one", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Colossus: Evil spirit search", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Colossus: Perfect in Hockey (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Colossus: Perfect in Hockey (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
        Spyro2LocationData("Colossus: Life Bottle", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Hurricos": [
        Spyro2LocationData("Hurricos: Talisman", "Summer Forest Talisman", Spyro2LocationCategory.TALISMAN),
        # This is the in-memory order.
        Spyro2LocationData("Hurricos: Factory Glide 2", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Hurricos: Stone thief chase", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Hurricos: Factory Glide 1", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Hurricos: All Windmills (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Hurricos: All Windmills (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
        Spyro2LocationData("Hurricos: Life Bottle", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Aquaria Towers": [
        Spyro2LocationData("Aquaria Towers: Talisman", "Summer Forest Talisman", Spyro2LocationCategory.TALISMAN),
        Spyro2LocationData("Aquaria Towers: Seahorse Rescue", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Aquaria Towers: Manta ride I", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Aquaria Towers: Manta ride II", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Aquaria Towers: Moneybags Unlock: Aquaria Towers Submarine", "Moneybags Unlock - Aquaria Towers Submarine", Spyro2LocationCategory.MONEYBAGS),
        Spyro2LocationData("Aquaria Towers: All Seaweed (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Aquaria Towers: All Seaweed (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
        Spyro2LocationData("Aquaria Towers: Life Bottle", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Sunny Beach": [
        Spyro2LocationData("Sunny Beach: Talisman", "Summer Forest Talisman", Spyro2LocationCategory.TALISMAN),
        Spyro2LocationData("Sunny Beach: Blasting boxes", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Sunny Beach: Turtle soup I", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Sunny Beach: Turtle soup II", "Orb", Spyro2LocationCategory.ORB),
    ],
    "Ocean Speedway": [
        Spyro2LocationData("Ocean Speedway: Follow Hunter", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Ocean Speedway: Under 1:10 (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Ocean Speedway: Under 1:10 (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
    ],
    "Crush's Dungeon": [
        Spyro2LocationData("Crush's Dungeon: Crush Defeated", "Crush Defeated", Spyro2LocationCategory.EVENT),
        Spyro2LocationData("Crush's Dungeon: Perfect (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Crush's Dungeon: Perfect (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
    ],
    # Homeworld 2
    "Autumn Plains": [
        Spyro2LocationData("Autumn Plains: The end of the wall", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Autumn Plains: Long glide!", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Autumn Plains: Moneybags Unlock: Zephyr Portal", "Moneybags Unlock - Zephyr Portal", Spyro2LocationCategory.MONEYBAGS),
        Spyro2LocationData("Autumn Plains: Moneybags Unlock: Climb", "Moneybags Unlock - Climb", Spyro2LocationCategory.MONEYBAGS),
        Spyro2LocationData("Autumn Plains: Moneybags Unlock: Shady Oasis Portal", "Moneybags Unlock - Shady Oasis Portal", Spyro2LocationCategory.MONEYBAGS),
        Spyro2LocationData("Autumn Plains: Moneybags Unlock: Icy Speedway Portal", "Moneybags Unlock - Icy Speedway Portal", Spyro2LocationCategory.MONEYBAGS),
        Spyro2LocationData("Autumn Plains: Life Bottle", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Skelos Badlands": [
        Spyro2LocationData("Skelos Badlands: Talisman", "Autumn Plains Talisman", Spyro2LocationCategory.TALISMAN),
        Spyro2LocationData("Skelos Badlands: Lava lizards I", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Skelos Badlands: Lava lizards II", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Skelos Badlands: Dem bones", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Skelos Badlands: All Cacti (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Skelos Badlands: All Cacti (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
        Spyro2LocationData("Skelos Badlands: Catbat Quartet (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Skelos Badlands: Catbat Quartet (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
        Spyro2LocationData("Skelos Badlands: Life Bottle", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Crystal Glacier": [
        Spyro2LocationData("Crystal Glacier: Talisman", "Autumn Plains Talisman", Spyro2LocationCategory.TALISMAN),
        Spyro2LocationData("Crystal Glacier: Draclet cave", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Crystal Glacier: George the snow leopard", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Crystal Glacier: Moneybags Unlock: Crystal Glacier Bridge", "Moneybags Unlock - Crystal Glacier Bridge", Spyro2LocationCategory.MONEYBAGS),
        Spyro2LocationData("Crystal Glacier: Life Bottle", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Breeze Harbor": [
        Spyro2LocationData("Breeze Harbor: Talisman", "Autumn Plains Talisman", Spyro2LocationCategory.TALISMAN),
        Spyro2LocationData("Breeze Harbor: Gear grab", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Breeze Harbor: Mine blast", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Breeze Harbor: Life Bottle by Final Bonfire", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
        Spyro2LocationData("Breeze Harbor: Life Bottle by Final Cannon", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Zephyr": [
        Spyro2LocationData("Zephyr: Talisman", "Autumn Plains Talisman", Spyro2LocationCategory.TALISMAN),
        Spyro2LocationData("Zephyr: Cowlek corral I", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Zephyr: Cowlek corral II", "Orb", Spyro2LocationCategory.ORB),
        # This is the in-memory order.
        Spyro2LocationData("Zephyr: Sowing seeds II", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Zephyr: Sowing seeds I", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Zephyr: Life Bottle", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Metro Speedway": [
        Spyro2LocationData("Metro Speedway: Grab the Loot", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Metro Speedway: Under 1:15 (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Metro Speedway: Under 1:15 (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
    ],
    "Scorch": [
        Spyro2LocationData("Scorch: Talisman", "Autumn Plains Talisman", Spyro2LocationCategory.TALISMAN),
        Spyro2LocationData("Scorch: Barrel of Monkeys", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Scorch: Capture the flags", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Scorch: All Trees (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Scorch: All Trees (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
        Spyro2LocationData("Scorch: Life Bottle", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Shady Oasis": [
        Spyro2LocationData("Shady Oasis: Talisman", "Autumn Plains Talisman", Spyro2LocationCategory.TALISMAN),
        Spyro2LocationData("Shady Oasis: Catch 3 thieves", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Shady Oasis: Free Hippos", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Shady Oasis: Life Bottle", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Magma Cone": [
        Spyro2LocationData("Magma Cone: Talisman", "Autumn Plains Talisman", Spyro2LocationCategory.TALISMAN),
        Spyro2LocationData("Magma Cone: Crystal geysers I", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Magma Cone: Crystal geysers II", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Magma Cone: Party crashers", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Magma Cone: Moneybags Unlock: Magma Cone Elevator", "Moneybags Unlock - Magma Cone Elevator", Spyro2LocationCategory.MONEYBAGS),
        Spyro2LocationData("Magma Cone: Life Bottle by Moneybags", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
        Spyro2LocationData("Magma Cone: Life Bottle on Ledge 1", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
        Spyro2LocationData("Magma Cone: Life Bottle on Ledge 2", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
        Spyro2LocationData("Magma Cone: Life Bottle on Ledge 3", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Fracture Hills": [
        Spyro2LocationData("Fracture Hills: Talisman", "Autumn Plains Talisman", Spyro2LocationCategory.TALISMAN),
        # This is the in-memory order.
        Spyro2LocationData("Fracture Hills: Earthshaper bash", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Fracture Hills: Free the faun", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Fracture Hills: Alchemist escort", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Fracture Hills: 3 Laps of Supercharge (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Fracture Hills: 3 Laps of Supercharge (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
        Spyro2LocationData("Fracture Hills: Life Bottle", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Icy Speedway": [
        Spyro2LocationData("Icy Speedway: Parasail through Rings", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Icy Speedway: Under 1:15 (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Icy Speedway: Under 1:15 (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
    ],
    "Gulp's Overlook": [
        Spyro2LocationData("Gulp's Overlook: Gulp Defeated", "Gulp Defeated", Spyro2LocationCategory.EVENT),
        Spyro2LocationData("Gulp's Overlook: Perfect (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Gulp's Overlook: Perfect (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
        Spyro2LocationData("Gulp's Overlook: Hit Ripto (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Gulp's Overlook: Hit Ripto (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
    ],
    # Homeworld 3
    "Winter Tundra": [
        Spyro2LocationData("Winter Tundra: On the tall wall", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Winter Tundra: Top of the waterfall", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Winter Tundra: Smash the rock", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Winter Tundra: Moneybags Unlock: Canyon Speedway Portal", "Moneybags Unlock - Canyon Speedway Portal", Spyro2LocationCategory.MONEYBAGS),
        Spyro2LocationData("Winter Tundra: Moneybags Unlock: Headbash", "Moneybags Unlock - Headbash", Spyro2LocationCategory.MONEYBAGS),
    ],
    "Mystic Marsh": [
        Spyro2LocationData("Mystic Marsh: Fix the fountain", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Mystic Marsh: Very versatile thieves!", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Mystic Marsh: Retrieve professor's pencil", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Mystic Marsh: Life Bottle by Basil", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
        Spyro2LocationData("Mystic Marsh: Life Bottle by Cooking Pot", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Cloud Temples": [
        Spyro2LocationData("Cloud Temples: Agent Zero's secret hideout", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Cloud Temples: Ring tower bells", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Cloud Temples: Break down doors", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Cloud Temples: Life Bottle", "Filler", Spyro2LocationCategory.LIFE_BOTTLE),
    ],
    "Canyon Speedway": [
        Spyro2LocationData("Canyon Speedway: Shoot down balloons", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Canyon Speedway: Under 1:10 (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Canyon Speedway: Under 1:10 (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
    ],
    "Robotica Farms": [
        Spyro2LocationData("Robotica Farms: Switch on bug light", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Robotica Farms: Clear tractor path", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Robotica Farms: Exterminate crow bugs", "Orb", Spyro2LocationCategory.ORB),
        # There is a memory address for a skill point here, but it is not implemented.
    ],
    "Metropolis": [
        Spyro2LocationData("Metropolis: Conquer invading cows", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Metropolis: Shoot down sheep saucers I", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Metropolis: Shoot down sheep saucers II", "Orb", Spyro2LocationCategory.ORB),
        Spyro2LocationData("Metropolis: Ox bombing", "Orb", Spyro2LocationCategory.ORB),
    ],
    "Dragon Shores": [
        Spyro2LocationData("Dragon Shores: Tunnel o' Love", "Dragon Shores Token", Spyro2LocationCategory.SHORES_TOKEN),
        Spyro2LocationData("Dragon Shores: Shooting Gallery I", "Dragon Shores Token", Spyro2LocationCategory.SHORES_TOKEN),
        Spyro2LocationData("Dragon Shores: Shooting Gallery II", "Dragon Shores Token", Spyro2LocationCategory.SHORES_TOKEN),
        Spyro2LocationData("Dragon Shores: Shooting Gallery III", "Dragon Shores Token", Spyro2LocationCategory.SHORES_TOKEN),
        Spyro2LocationData("Dragon Shores: Rollercoaster I", "Dragon Shores Token", Spyro2LocationCategory.SHORES_TOKEN),
        Spyro2LocationData("Dragon Shores: Rollercoaster II", "Dragon Shores Token", Spyro2LocationCategory.SHORES_TOKEN),
        Spyro2LocationData("Dragon Shores: Rollercoaster III", "Dragon Shores Token", Spyro2LocationCategory.SHORES_TOKEN),
        Spyro2LocationData("Dragon Shores: Dunk Tank I", "Dragon Shores Token", Spyro2LocationCategory.SHORES_TOKEN),
        Spyro2LocationData("Dragon Shores: Dunk Tank II", "Dragon Shores Token", Spyro2LocationCategory.SHORES_TOKEN),
        Spyro2LocationData("Dragon Shores: Dunk Tank III", "Dragon Shores Token", Spyro2LocationCategory.SHORES_TOKEN),
    ],
    "Ripto's Arena": [
        Spyro2LocationData("Ripto's Arena: Ripto Defeated", "Ripto Defeated", Spyro2LocationCategory.EVENT),
        Spyro2LocationData("Ripto's Arena: Perfect (Skill Point)", "Filler", Spyro2LocationCategory.SKILLPOINT),
        Spyro2LocationData("Ripto's Arena: Perfect (Goal)", "Skill Point", Spyro2LocationCategory.SKILLPOINT_GOAL),
    ],
    "Inventory": [
        Spyro2LocationData("Total Gems: 500", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 1000", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 1500", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 2000", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 2500", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 3000", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 3500", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 4000", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 4500", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 5000", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 5500", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 6000", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 6500", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 7000", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 7500", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 8000", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 8500", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 9000", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 9500", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Total Gems: 10000", "Filler", Spyro2LocationCategory.TOTAL_GEM),
        Spyro2LocationData("Summer Forest: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Summer Forest: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Summer Forest: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Summer Forest: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Glimmer: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Glimmer: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Glimmer: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Glimmer: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Idol Springs: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Idol Springs: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Idol Springs: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Idol Springs: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Colossus: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Colossus: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Colossus: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Colossus: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Hurricos: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Hurricos: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Hurricos: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Hurricos: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Aquaria Towers: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Aquaria Towers: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Aquaria Towers: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Aquaria Towers: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Sunny Beach: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Sunny Beach: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Sunny Beach: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Sunny Beach: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Ocean Speedway: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Ocean Speedway: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Ocean Speedway: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Ocean Speedway: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Autumn Plains: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Autumn Plains: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Autumn Plains: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Autumn Plains: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Skelos Badlands: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Skelos Badlands: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Skelos Badlands: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Skelos Badlands: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Crystal Glacier: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Crystal Glacier: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Crystal Glacier: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Crystal Glacier: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Breeze Harbor: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Breeze Harbor: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Breeze Harbor: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Breeze Harbor: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Zephyr: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Zephyr: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Zephyr: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Zephyr: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Metro Speedway: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Metro Speedway: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Metro Speedway: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Metro Speedway: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Scorch: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Scorch: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Scorch: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Scorch: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Shady Oasis: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Shady Oasis: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Shady Oasis: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Shady Oasis: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Magma Cone: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Magma Cone: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Magma Cone: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Magma Cone: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Fracture Hills: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Fracture Hills: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Fracture Hills: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Fracture Hills: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Icy Speedway: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Icy Speedway: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Icy Speedway: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Icy Speedway: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Winter Tundra: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Winter Tundra: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Winter Tundra: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Winter Tundra: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Mystic Marsh: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Mystic Marsh: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Mystic Marsh: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Mystic Marsh: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Cloud Temples: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Cloud Temples: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Cloud Temples: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Cloud Temples: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Canyon Speedway: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Canyon Speedway: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Canyon Speedway: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Canyon Speedway: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Robotica Farms: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Robotica Farms: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Robotica Farms: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Robotica Farms: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
        Spyro2LocationData("Metropolis: 25% Gems", "Filler", Spyro2LocationCategory.GEM_25),
        Spyro2LocationData("Metropolis: 50% Gems", "Filler", Spyro2LocationCategory.GEM_50),
        Spyro2LocationData("Metropolis: 75% Gems", "Filler", Spyro2LocationCategory.GEM_75),
        Spyro2LocationData("Metropolis: All Gems", "Filler", Spyro2LocationCategory.GEM_100),
    ]
}

summer_gems = []
for i in range(60):
    summer_gems += [Spyro2LocationData(f"Summer Forest: Gem {i + 1}", "Summer Forest Red Gem", Spyro2LocationCategory.GEM)]
for i in range(40):
    summer_gems += [Spyro2LocationData(f"Summer Forest: Gem {i + 61}", "Summer Forest Green Gem", Spyro2LocationCategory.GEM)]
for i in range(27):
    summer_gems += [Spyro2LocationData(f"Summer Forest: Gem {i + 101}", "Summer Forest Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(10):
    summer_gems += [Spyro2LocationData(f"Summer Forest: Gem {i + 128}", "Summer Forest Gold Gem", Spyro2LocationCategory.GEM)]
for i in range(1):
    summer_gems += [Spyro2LocationData(f"Summer Forest: Gem {i + 138}", "Summer Forest Pink Gem", Spyro2LocationCategory.GEM)]
location_tables["Summer Forest"] = location_tables["Summer Forest"] + summer_gems

glimmer_gems = []
for i in range(32):
    glimmer_gems += [Spyro2LocationData(f"Glimmer: Gem {i + 1}", "Glimmer Red Gem", Spyro2LocationCategory.GEM)]
for i in range(59):
    glimmer_gems += [Spyro2LocationData(f"Glimmer: Gem {i + 33}", "Glimmer Green Gem", Spyro2LocationCategory.GEM)]
for i in range(34):
    glimmer_gems += [Spyro2LocationData(f"Glimmer: Gem {i + 92}", "Glimmer Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(8):
    glimmer_gems += [Spyro2LocationData(f"Glimmer: Gem {i + 126}", "Glimmer Gold Gem", Spyro2LocationCategory.GEM)]
location_tables["Glimmer"] = location_tables["Glimmer"] + glimmer_gems

idol_gems = []
for i in range(60):
    idol_gems += [Spyro2LocationData(f"Idol Springs: Gem {i + 1}", "Idol Springs Red Gem", Spyro2LocationCategory.GEM)]
for i in range(45):
    idol_gems += [Spyro2LocationData(f"Idol Springs: Gem {i + 61}", "Idol Springs Green Gem", Spyro2LocationCategory.GEM)]
for i in range(38):
    idol_gems += [Spyro2LocationData(f"Idol Springs: Gem {i + 106}", "Idol Springs Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(6):
    idol_gems += [Spyro2LocationData(f"Idol Springs: Gem {i + 144}", "Idol Springs Gold Gem", Spyro2LocationCategory.GEM)]
location_tables["Idol Springs"] = location_tables["Idol Springs"] + idol_gems

colossus_gems = []
for i in range(39):
    colossus_gems += [Spyro2LocationData(f"Colossus: Gem {i + 1}", "Colossus Red Gem", Spyro2LocationCategory.GEM)]
for i in range(53):
    colossus_gems += [Spyro2LocationData(f"Colossus: Gem {i + 40}", "Colossus Green Gem", Spyro2LocationCategory.GEM)]
for i in range(39):
    colossus_gems += [Spyro2LocationData(f"Colossus: Gem {i + 93}", "Colossus Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(6):
    colossus_gems += [Spyro2LocationData(f"Colossus: Gem {i + 132}", "Colossus Gold Gem", Spyro2LocationCategory.GEM)]
location_tables["Colossus"] = location_tables["Colossus"] + colossus_gems

hurricos_gems = []
for i in range(37):
    hurricos_gems += [Spyro2LocationData(f"Hurricos: Gem {i + 1}", "Hurricos Red Gem", Spyro2LocationCategory.GEM)]
for i in range(29):
    hurricos_gems += [Spyro2LocationData(f"Hurricos: Gem {i + 38}", "Hurricos Green Gem", Spyro2LocationCategory.GEM)]
for i in range(35):
    hurricos_gems += [Spyro2LocationData(f"Hurricos: Gem {i + 67}", "Hurricos Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(13):
    hurricos_gems += [Spyro2LocationData(f"Hurricos: Gem {i + 102}", "Hurricos Gold Gem", Spyro2LocationCategory.GEM)]
location_tables["Hurricos"] = location_tables["Hurricos"] + hurricos_gems

aquaria_gems = []
for i in range(41):
    aquaria_gems += [Spyro2LocationData(f"Aquaria Towers: Gem {i + 1}", "Aquaria Towers Red Gem", Spyro2LocationCategory.GEM)]
for i in range(57):
    aquaria_gems += [Spyro2LocationData(f"Aquaria Towers: Gem {i + 42}", "Aquaria Towers Green Gem", Spyro2LocationCategory.GEM)]
for i in range(32):
    aquaria_gems += [Spyro2LocationData(f"Aquaria Towers: Gem {i + 99}", "Aquaria Towers Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(6):
    aquaria_gems += [Spyro2LocationData(f"Aquaria Towers: Gem {i + 131}", "Aquaria Towers Gold Gem", Spyro2LocationCategory.GEM)]
for i in range(1):
    aquaria_gems += [Spyro2LocationData(f"Aquaria Towers: Gem {i + 137}", "Aquaria Towers Pink Gem", Spyro2LocationCategory.GEM)]
location_tables["Aquaria Towers"] = location_tables["Aquaria Towers"] + aquaria_gems

sunny_gems = []
for i in range(22):
    sunny_gems += [Spyro2LocationData(f"Sunny Beach: Gem {i + 1}", "Sunny Beach Red Gem", Spyro2LocationCategory.GEM)]
for i in range(49):
    sunny_gems += [Spyro2LocationData(f"Sunny Beach: Gem {i + 23}", "Sunny Beach Green Gem", Spyro2LocationCategory.GEM)]
for i in range(38):
    sunny_gems += [Spyro2LocationData(f"Sunny Beach: Gem {i + 72}", "Sunny Beach Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(9):
    sunny_gems += [Spyro2LocationData(f"Sunny Beach: Gem {i + 110}", "Sunny Beach Gold Gem", Spyro2LocationCategory.GEM)]
location_tables["Sunny Beach"] = location_tables["Sunny Beach"] + sunny_gems

autumn_gems = []
for i in range(41):
    autumn_gems += [Spyro2LocationData(f"Autumn Plains: Gem {i + 1}", "Autumn Plains Red Gem", Spyro2LocationCategory.GEM)]
for i in range(22):
    autumn_gems += [Spyro2LocationData(f"Autumn Plains: Gem {i + 42}", "Autumn Plains Green Gem", Spyro2LocationCategory.GEM)]
for i in range(32):
    autumn_gems += [Spyro2LocationData(f"Autumn Plains: Gem {i + 64}", "Autumn Plains Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(8):
    autumn_gems += [Spyro2LocationData(f"Autumn Plains: Gem {i + 96}", "Autumn Plains Gold Gem", Spyro2LocationCategory.GEM)]
for i in range(3):
    autumn_gems += [Spyro2LocationData(f"Autumn Plains: Gem {i + 104}", "Autumn Plains Pink Gem", Spyro2LocationCategory.GEM)]
location_tables["Autumn Plains"] = location_tables["Autumn Plains"] + autumn_gems

skelos_gems = []
for i in range(22):
    skelos_gems += [Spyro2LocationData(f"Skelos Badlands: Gem {i + 1}", "Skelos Badlands Red Gem", Spyro2LocationCategory.GEM)]
for i in range(24):
    skelos_gems += [Spyro2LocationData(f"Skelos Badlands: Gem {i + 23}", "Skelos Badlands Green Gem", Spyro2LocationCategory.GEM)]
for i in range(38):
    skelos_gems += [Spyro2LocationData(f"Skelos Badlands: Gem {i + 47}", "Skelos Badlands Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(9):
    skelos_gems += [Spyro2LocationData(f"Skelos Badlands: Gem {i + 85}", "Skelos Badlands Gold Gem", Spyro2LocationCategory.GEM)]
for i in range(2):
    skelos_gems += [Spyro2LocationData(f"Skelos Badlands: Gem {i + 94}", "Skelos Badlands Pink Gem", Spyro2LocationCategory.GEM)]
location_tables["Skelos Badlands"] = location_tables["Skelos Badlands"] + skelos_gems

crystal_gems = []
for i in range(28):
    crystal_gems += [Spyro2LocationData(f"Crystal Glacier: Gem {i + 1}", "Crystal Glacier Red Gem", Spyro2LocationCategory.GEM)]
for i in range(26):
    crystal_gems += [Spyro2LocationData(f"Crystal Glacier: Gem {i + 29}", "Crystal Glacier Green Gem", Spyro2LocationCategory.GEM)]
for i in range(41):
    crystal_gems += [Spyro2LocationData(f"Crystal Glacier: Gem {i + 55}", "Crystal Glacier Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(9):
    crystal_gems += [Spyro2LocationData(f"Crystal Glacier: Gem {i + 96}", "Crystal Glacier Gold Gem", Spyro2LocationCategory.GEM)]
for i in range(1):
    crystal_gems += [Spyro2LocationData(f"Crystal Glacier: Gem {i + 105}", "Crystal Glacier Pink Gem", Spyro2LocationCategory.GEM)]
location_tables["Crystal Glacier"] = location_tables["Crystal Glacier"] + crystal_gems

breeze_gems = []
for i in range(19):
    breeze_gems += [Spyro2LocationData(f"Breeze Harbor: Gem {i + 1}", "Breeze Harbor Red Gem", Spyro2LocationCategory.GEM)]
for i in range(28):
    breeze_gems += [Spyro2LocationData(f"Breeze Harbor: Gem {i + 20}", "Breeze Harbor Green Gem", Spyro2LocationCategory.GEM)]
for i in range(35):
    breeze_gems += [Spyro2LocationData(f"Breeze Harbor: Gem {i + 48}", "Breeze Harbor Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(15):
    breeze_gems += [Spyro2LocationData(f"Breeze Harbor: Gem {i + 83}", "Breeze Harbor Gold Gem", Spyro2LocationCategory.GEM)]
location_tables["Breeze Harbor"] = location_tables["Breeze Harbor"] + breeze_gems

zephyr_gems = []
for i in range(49):
    zephyr_gems += [Spyro2LocationData(f"Zephyr: Gem {i + 1}", "Zephyr Red Gem", Spyro2LocationCategory.GEM)]
for i in range(53):
    zephyr_gems += [Spyro2LocationData(f"Zephyr: Gem {i + 50}", "Zephyr Green Gem", Spyro2LocationCategory.GEM)]
for i in range(23):
    zephyr_gems += [Spyro2LocationData(f"Zephyr: Gem {i + 103}", "Zephyr Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(8):
    zephyr_gems += [Spyro2LocationData(f"Zephyr: Gem {i + 126}", "Zephyr Gold Gem", Spyro2LocationCategory.GEM)]
for i in range(2):
    zephyr_gems += [Spyro2LocationData(f"Zephyr: Gem {i + 134}", "Zephyr Pink Gem", Spyro2LocationCategory.GEM)]
location_tables["Zephyr"] = location_tables["Zephyr"] + zephyr_gems

scorch_gems = []
for i in range(47):
    scorch_gems += [Spyro2LocationData(f"Scorch: Gem {i + 1}", "Scorch Red Gem", Spyro2LocationCategory.GEM)]
for i in range(29):
    scorch_gems += [Spyro2LocationData(f"Scorch: Gem {i + 48}", "Scorch Green Gem", Spyro2LocationCategory.GEM)]
for i in range(39):
    scorch_gems += [Spyro2LocationData(f"Scorch: Gem {i + 77}", "Scorch Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(10):
    scorch_gems += [Spyro2LocationData(f"Scorch: Gem {i + 116}", "Scorch Gold Gem", Spyro2LocationCategory.GEM)]
location_tables["Scorch"] = location_tables["Scorch"] + scorch_gems

shady_gems = []
for i in range(35):
    shady_gems += [Spyro2LocationData(f"Shady Oasis: Gem {i + 1}", "Shady Oasis Red Gem", Spyro2LocationCategory.GEM)]
for i in range(35):
    shady_gems += [Spyro2LocationData(f"Shady Oasis: Gem {i + 36}", "Shady Oasis Green Gem", Spyro2LocationCategory.GEM)]
for i in range(39):
    shady_gems += [Spyro2LocationData(f"Shady Oasis: Gem {i + 71}", "Shady Oasis Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(10):
    shady_gems += [Spyro2LocationData(f"Shady Oasis: Gem {i + 110}", "Shady Oasis Gold Gem", Spyro2LocationCategory.GEM)]
location_tables["Shady Oasis"] = location_tables["Shady Oasis"] + shady_gems

magma_gems = []
for i in range(33):
    magma_gems += [Spyro2LocationData(f"Magma Cone: Gem {i + 1}", "Magma Cone Red Gem", Spyro2LocationCategory.GEM)]
for i in range(36):
    magma_gems += [Spyro2LocationData(f"Magma Cone: Gem {i + 34}", "Magma Cone Green Gem", Spyro2LocationCategory.GEM)]
for i in range(41):
    magma_gems += [Spyro2LocationData(f"Magma Cone: Gem {i + 70}", "Magma Cone Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(9):
    magma_gems += [Spyro2LocationData(f"Magma Cone: Gem {i + 111}", "Magma Cone Gold Gem", Spyro2LocationCategory.GEM)]
location_tables["Magma Cone"] = location_tables["Magma Cone"] + magma_gems

fracture_gems = []
for i in range(36):
    fracture_gems += [Spyro2LocationData(f"Fracture Hills: Gem {i + 1}", "Fracture Hills Red Gem", Spyro2LocationCategory.GEM)]
for i in range(32):
    fracture_gems += [Spyro2LocationData(f"Fracture Hills: Gem {i + 37}", "Fracture Hills Green Gem", Spyro2LocationCategory.GEM)]
for i in range(37):
    fracture_gems += [Spyro2LocationData(f"Fracture Hills: Gem {i + 69}", "Fracture Hills Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(9):
    fracture_gems += [Spyro2LocationData(f"Fracture Hills: Gem {i + 106}", "Fracture Hills Gold Gem", Spyro2LocationCategory.GEM)]
for i in range(1):
    fracture_gems += [Spyro2LocationData(f"Fracture Hills: Gem {i + 115}", "Fracture Hills Pink Gem", Spyro2LocationCategory.GEM)]
location_tables["Fracture Hills"] = location_tables["Fracture Hills"] + fracture_gems

winter_gems = []
for i in range(32):
    winter_gems += [Spyro2LocationData(f"Winter Tundra: Gem {i + 1}", "Winter Tundra Red Gem", Spyro2LocationCategory.GEM)]
for i in range(29):
    winter_gems += [Spyro2LocationData(f"Winter Tundra: Gem {i + 33}", "Winter Tundra Green Gem", Spyro2LocationCategory.GEM)]
for i in range(18):
    winter_gems += [Spyro2LocationData(f"Winter Tundra: Gem {i + 62}", "Winter Tundra Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(22):
    winter_gems += [Spyro2LocationData(f"Winter Tundra: Gem {i + 80}", "Winter Tundra Gold Gem", Spyro2LocationCategory.GEM)]
location_tables["Winter Tundra"] = location_tables["Winter Tundra"] + winter_gems

mystic_gems = []
for i in range(54):
    mystic_gems += [Spyro2LocationData(f"Mystic Marsh: Gem {i + 1}", "Mystic Marsh Red Gem", Spyro2LocationCategory.GEM)]
for i in range(38):
    mystic_gems += [Spyro2LocationData(f"Mystic Marsh: Gem {i + 55}", "Mystic Marsh Green Gem", Spyro2LocationCategory.GEM)]
for i in range(40):
    mystic_gems += [Spyro2LocationData(f"Mystic Marsh: Gem {i + 93}", "Mystic Marsh Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(7):
    mystic_gems += [Spyro2LocationData(f"Mystic Marsh: Gem {i + 133}", "Mystic Marsh Gold Gem", Spyro2LocationCategory.GEM)]
location_tables["Mystic Marsh"] = location_tables["Mystic Marsh"] + mystic_gems

cloud_gems = []
for i in range(36):
    cloud_gems += [Spyro2LocationData(f"Cloud Temples: Gem {i + 1}", "Cloud Temples Red Gem", Spyro2LocationCategory.GEM)]
for i in range(27):
    cloud_gems += [Spyro2LocationData(f"Cloud Temples: Gem {i + 37}", "Cloud Temples Green Gem", Spyro2LocationCategory.GEM)]
for i in range(37):
    cloud_gems += [Spyro2LocationData(f"Cloud Temples: Gem {i + 64}", "Cloud Temples Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(10):
    cloud_gems += [Spyro2LocationData(f"Cloud Temples: Gem {i + 101}", "Cloud Temples Gold Gem", Spyro2LocationCategory.GEM)]
for i in range(1):
    cloud_gems += [Spyro2LocationData(f"Cloud Temples: Gem {i + 111}", "Cloud Temples Pink Gem", Spyro2LocationCategory.GEM)]
location_tables["Cloud Temples"] = location_tables["Cloud Temples"] + cloud_gems

robotica_gems = []
for i in range(29):
    robotica_gems += [Spyro2LocationData(f"Robotica Farms: Gem {i + 1}", "Robotica Farms Red Gem", Spyro2LocationCategory.GEM)]
for i in range(53):
    robotica_gems += [Spyro2LocationData(f"Robotica Farms: Gem {i + 30}", "Robotica Farms Green Gem", Spyro2LocationCategory.GEM)]
for i in range(37):
    robotica_gems += [Spyro2LocationData(f"Robotica Farms: Gem {i + 83}", "Robotica Farms Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(8):
    robotica_gems += [Spyro2LocationData(f"Robotica Farms: Gem {i + 120}", "Robotica Farms Gold Gem", Spyro2LocationCategory.GEM)]
location_tables["Robotica Farms"] = location_tables["Robotica Farms"] + robotica_gems

metropolis_gems = []
for i in range(39):
    metropolis_gems += [Spyro2LocationData(f"Metropolis: Gem {i + 1}", "Metropolis Red Gem", Spyro2LocationCategory.GEM)]
for i in range(38):
    metropolis_gems += [Spyro2LocationData(f"Metropolis: Gem {i + 40}", "Metropolis Green Gem", Spyro2LocationCategory.GEM)]
for i in range(41):
    metropolis_gems += [Spyro2LocationData(f"Metropolis: Gem {i + 78}", "Metropolis Blue Gem", Spyro2LocationCategory.GEM)]
for i in range(8):
    metropolis_gems += [Spyro2LocationData(f"Metropolis: Gem {i + 119}", "Metropolis Gold Gem", Spyro2LocationCategory.GEM)]
location_tables["Metropolis"] = location_tables["Metropolis"] + metropolis_gems

# To ensure backwards compatibility, do not move gem location IDs.
for level in location_tables.keys():
    if level not in ["Summer Forest", "Ocean Speedway", "Crush's Dungeon", "Autumn Plains", "Metro Speedway", "Icy Speedway", "Gulp's Overlook", "Winter Tundra", "Canyon Speedway", "Dragon Shores", "Ripto's Arena", "Inventory"]:
        location_tables[level] = location_tables[level] + [Spyro2LocationData(f"{level}: All Spirit Particles", "Filler", Spyro2LocationCategory.SPIRIT_PARTICLE)]

location_dictionary: Dict[str, Spyro2LocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
