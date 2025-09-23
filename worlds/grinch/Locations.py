from typing import NamedTuple, Optional

from .RamHandler import GrinchRamData
from BaseClasses import Location, Region


class GrinchLocationData(NamedTuple):
    region: str
    location_group: str #list[str]
    id: Optional[int]
    update_ram_addr: list[GrinchRamData]
    reset_addr: Optional[list[GrinchRamData]] = None # Addresses to update once we find the item

class GrinchLocation(Location):
    game: str = "The Grinch"

    @staticmethod
    def get_apid(id: int):
        base_id: int = 42069
        return base_id + id if id is not None else None

    def __init__(self, player: int, name: str, parent: Region, data: GrinchLocationData):
        address = None if data.id is None else GrinchLocation.get_apid(data.id)
        super(GrinchLocation, self).__init__(player, name, address=address, parent=parent)

        self.code = data.id
        self.region = data.region
        self.type = data.location_group
        self.address = self.address

grinch_locations = {
#Going to use current map id as indicator whether or not you visited a location
#Visitsanity
        "WV - First Visit": GrinchLocationData("Whoville", "Visitsanity", 100, [GrinchRamData(0x010000, value=0x07)]),
        "WV - Post Office - First Visit": GrinchLocationData("Post Office", "Visitsanity", 101, [GrinchRamData(0x010000, value=0x0A)]),
        "WV - City Hall - First Visit": GrinchLocationData("City Hall", "Visitsanity", 102, [GrinchRamData(0x010000, value=0x08)]),
        "WV - Clock Tower - First Visit": GrinchLocationData("Clock Tower", "Visitsanity", 103, [GrinchRamData(0x010000, value=0x09)]),
        "WF - First Visit": GrinchLocationData("Who Forest", "Visitsanity", 104, [GrinchRamData(0x010000, value=0x0B)]),
        "WF - Ski Resort - First Visit": GrinchLocationData("Ski Resort", "Visitsanity", 105, [GrinchRamData(0x010000, value=0x0C)]),
        "WF - Civic Center - First Visit": GrinchLocationData("Civic Center", "Visitsanity", 106, [GrinchRamData(0x010000, value=0x0D)]),
        "WD - First Visit": GrinchLocationData("Who Dump", "Visitsanity", 107, [GrinchRamData(0x010000, value=0x0E)]),
        "WD - Minefield - First Visit": GrinchLocationData("Minefield", "Visitsanity", 108, [GrinchRamData(0x010000, value=0x11)]),
        "WD - Power Plant - First Visit": GrinchLocationData("Power Plant", "Visitsanity", 109, [GrinchRamData(0x010000, value=0x10)]),
        "WD - Generator Building - First Visit": GrinchLocationData("Generator Building", "Visitsanity", 110, [GrinchRamData(0x010000, value=0x0F)]),
        "WL - South Shore- First Visit": GrinchLocationData("Who Lake", "Visitsanity", 111, [GrinchRamData(0x010000, value=0x12)]),
        "WL - Submarine World - First Visit": GrinchLocationData("Submarine World", "Visitsanity", 112, [GrinchRamData(0x010000, value=0x17)]),
        "WL - Scout's Hut - First Visit": GrinchLocationData("Scout's Hut", "Visitsanity", 113, [GrinchRamData(0x010000, value=0x13)]),
        "WL - North Shore - First Visit": GrinchLocationData("North Shore", "Visitsanity", 114, [GrinchRamData(0x010000, value=0x14)]),
        "WL - Mayor's Villa - First Visit": GrinchLocationData("Mayor's Villa", "Visitsanity", 115, [GrinchRamData(0x010000, value=0x16)]),
#Need to find mission completion address for handful of locations that are not documented.
#Missions that have value are those ones we need to find the check for
#Whoville Missions
        "WV - Post Office - Shuffling The Mail": GrinchLocationData("Post Office", "Whoville Missions", 201, [GrinchRamData(0x0100BE, binary_bit_pos=0)]),
        "WV - Smashing Snowmen": GrinchLocationData("Whoville", "Whoville Missions", 200, [GrinchRamData(0x0100C5, value=10)]),
        "WV - Painting The Mayor's Posters": GrinchLocationData("Whoville", "Whoville Missions", 202, [GrinchRamData(0x0100C6, value=10)]),
        "WV - Launching Eggs Into Houses": GrinchLocationData("Whoville", "Whoville Missions", 203, [GrinchRamData(0x0100C7, value=10)]),
        "WV - City Hall - Modifying The Mayor's Statue": GrinchLocationData("City Hall", "Whoville Missions", 204, [GrinchRamData(0x0100BE, binary_bit_pos=1)]),
        "WV - Clock Tower - Advancing The Countdown-To-Xmas Clock": GrinchLocationData("Clock Tower", "Whoville Missions", 205, [GrinchRamData(0x0100BE, binary_bit_pos=2)]),
        "WV - Squashing All Gifts": GrinchLocationData("Whoville", "Whoville Missions", 206, [GrinchRamData(0x01005C, value=500, bit_size=2)]),
#Who Forest Missions
        "WF - Making Xmas Trees Droop": GrinchLocationData("Who Forest", "Who Forest Missions", 300, [GrinchRamData(0x0100C8, value=10)]),
        "WF - Sabotaging Snow Cannon With Glue": GrinchLocationData("Who Forest", "Who Forest Missions", 301, [GrinchRamData(0x0100BE, binary_bit_pos=3)]),
        "WF - Putting Beehives In Cabins": GrinchLocationData("Who Forest", "Who Forest Missions", 302, [GrinchRamData(0x0100CA, value=10)]),
        "WF - Ski Resort - Sliming The Mayor's Skis": GrinchLocationData("Ski Resort", "Who Forest Missions", 303, [GrinchRamData(0x0100BE, binary_bit_pos=4)]),
        "WF - Civic Center - Replacing The Candles On The Cake With Fireworks": GrinchLocationData("Civic Center", "Who Forest Missions", 304, [GrinchRamData(0x0100BE, binary_bit_pos=5)]),
        "WF - Squashing All Gifts": GrinchLocationData("Who Forest", "Who Forest Missions", 305, [GrinchRamData(0x01005E, value=750, bit_size=2)]),
#Who Dump Missions
        "WD - Stealing Food From Birds": GrinchLocationData("Who Dump", "Who Dump Missions", 400, [GrinchRamData(0x0100CB, value=10)]),
        "WD - Feeding The Computer With Robot Parts": GrinchLocationData("Who Dump", "Who Dump Missions", 401, [GrinchRamData(0x0100BF, binary_bit_pos=2)]),
        "WD - Infesting The Mayor's House With Rats": GrinchLocationData("Who Dump", "Who Dump Missions", 402, [GrinchRamData(0x0100BE, binary_bit_pos=6)]),
        "WD - Conducting The Stinky Gas To Who-Bris' Shack": GrinchLocationData("Who Dump", "Who Dump Missions", 403, [GrinchRamData(0x0100BE, binary_bit_pos=7)]),
        "WD - Minefield - Shaving Who Dump Guardian": GrinchLocationData("Minefield", "Who Dump Missions", 404, [GrinchRamData(0x0100BF, binary_bit_pos=0)]),
        "WD - Generator Building - Short-Circuiting Power-Plant": GrinchLocationData("Generator Building", "Who Dump Missions", 405, [GrinchRamData(0x0100BF, binary_bit_pos=1)]),
        "WD - Squashing All Gifts": GrinchLocationData("Who Dump", "Who Dump Missions", 406, [GrinchRamData(0x010060, value=750, bit_size=2)]),
#Who Lake Missions
        "WL - South Shore - Putting Thistles In Shorts": GrinchLocationData("Who Lake", "Who Lake Missions", 500, [GrinchRamData(0x0100E5, value=10)]),
        "WL - South Shore - Sabotaging The Tents": GrinchLocationData("Who Lake", "Who Lake Missions", 501, [GrinchRamData(0x0100E6, value=10)]),
        "WL - North Shore - Drilling Holes In Canoes": GrinchLocationData("North Shore", "Who Lake Missions", 502, [GrinchRamData(0x0100EE, value=10)]),
        "WL - Submarine World - Modifying The Marine Mobile": GrinchLocationData("Submarine World", "Who Lake Missions", 503, [GrinchRamData(0x0100BF, binary_bit_pos=4)]),
        "WL - Mayor's Villa - Hooking The Mayor's Bed To The Motorboat": GrinchLocationData("Mayor's Villa", "Who Lake Missions", 504, [GrinchRamData(0x0100BF, binary_bit_pos=3)]),
        "WL - Squashing All Gifts": GrinchLocationData("Who Lake", "Who Lake Missions", 505, [GrinchRamData(0x010062, value=1000, bit_size=2)]),
#Need to find binary values for individual blueprints, but all ram addresses are found
#Blueprints
#Binoculars Blueprints
        "WV - Binoculars BP on Post Office Roof": GrinchLocationData("Whoville", "Binocular Blueprints", 600, [GrinchRamData(0x01020B, binary_bit_pos=2)]),
        "WV - City Hall - Binoculars BP left side of Library": GrinchLocationData("City Hall", "Binocular Blueprints", 601, [GrinchRamData(0x01021F, binary_bit_pos=6)]),
        "WV - City Hall - Binoculars BP front side of Library": GrinchLocationData("City Hall", "Binocular Blueprints", 602, [GrinchRamData(0x01021F, binary_bit_pos=5)]),
        "WV - City Hall - Binoculars BP right side of Library": GrinchLocationData("City Hall", "Binocular Blueprints", 603, [GrinchRamData(0x01021F, binary_bit_pos=4)]),
#Rotten Egg Launcher Blueprints
        "WV - REL BP left of City Hall": GrinchLocationData("Whoville", "Rotten Egg Launcher Blueprints", 700, [GrinchRamData(0x01020B, binary_bit_pos=0)]),
        "WV - REL BP left of Clock Tower": GrinchLocationData("Whoville", "Rotten Egg Launcher Blueprints", 701, [GrinchRamData(0x01020B, binary_bit_pos=1)]),
        "WV - Post Office - REL BP inside Silver Room": GrinchLocationData("Post Office", "Rotten Egg Launcher Blueprints", 702, [GrinchRamData(0x01021C, binary_bit_pos=1)]),
        "WV - Post Office - REL BP at Entrance Door after Mission Completion": GrinchLocationData("Post Office", "Rotten Egg Launcher Blueprints", 703, [GrinchRamData(0x01021C, binary_bit_pos=2)]),
#Rocket Spring Blueprints
        "WF - RS BP behind Vacuum Tube": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 800, [GrinchRamData(0x010243, binary_bit_pos=3)]),
        "WF - RS BP in front of 2nd House near Vacuum Tube": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 801, [GrinchRamData(0x010243, binary_bit_pos=1)]),
        "WF - RS BP near Tree House on Ground": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 802, [GrinchRamData(0x010243, binary_bit_pos=4)]),
        "WF - RS BP behind Cable Car House": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 804, [GrinchRamData(0x010242, binary_bit_pos=7)]),
        "WF - RS BP near Who Snowball in Cave": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 805, [GrinchRamData(0x010242, binary_bit_pos=6)]),
        "WF - RS BP on Branch Platform closest to Glue Cannon": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 806, [GrinchRamData(0x010243, binary_bit_pos=2)]),
        "WF - RS BP on Branch Platform Near Beast": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 807, [GrinchRamData(0x010243, binary_bit_pos=0)]),
        "WF - RS BP on Branch Platform Elevated next to House": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 808, [GrinchRamData(0x010243, binary_bit_pos=6)]),
        "WF - RS BP on Tree House": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 809, [GrinchRamData(0x010243, binary_bit_pos=5)]),
#Slime Shooter Blueprints
        "WF - SS BP in Branch Platform Elevated House": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 900, [GrinchRamData(0x010244, binary_bit_pos=3)]),
        "WF - SS BP in Branch Platform House next to Beast": GrinchLocationData("Who Forest", "Slime Shooter Blueprint", 901, [GrinchRamData(0x010243, binary_bit_pos=7)]),
        "WF - SS BP in House in front of Civic Center Cave": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 902, [GrinchRamData(0x010244, binary_bit_pos=2)]),
        "WF - SS BP in House next to Tree House": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 903, [GrinchRamData(0x010244, binary_bit_pos=1)]),
        "WF - SS BP in House across from Tree House": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 904, [GrinchRamData(0x010244, binary_bit_pos=5)]),
        "WF - SS BP in 2nd House near Vacuum Tube Right Side": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 905, [GrinchRamData(0x010244, binary_bit_pos=4)]),
        "WF - SS BP in 2nd House near Vacuum Tube Left Side": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 906, [GrinchRamData(0x010244, binary_bit_pos=7)]),
        "WF - SS BP in 2nd House near Vacuum Tube inbetween Blueprints": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 907, [GrinchRamData(0x010244, binary_bit_pos=6)]),
        "WF - SS BP in House near Vacuum Tube": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 908, [GrinchRamData(0x010244, binary_bit_pos=0)]),
#Octopus Climbing Device
        "WD - OCD BP inside Middle Pipe": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1001, [GrinchRamData(0x010252, binary_bit_pos=3)]),
        "WD - OCD BP inside Right Pipe": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1002, [GrinchRamData(0x010252, binary_bit_pos=5)]),
        "WD - OCD BP in Vent to Mayor's House": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1003, [GrinchRamData(0x010252, binary_bit_pos=1)]),
        "WD - OCD BP inside Left Pipe": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1004, [GrinchRamData(0x010252, binary_bit_pos=4)]),
        "WD - OCD BP near Right Side of Power Plant Wall": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1005, [GrinchRamData(0x010252, binary_bit_pos=0)]),
        "WD - OCD BP near Who-Bris' Shack": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1006, [GrinchRamData(0x010252, binary_bit_pos=2)]),
        "WD - Minefield - OCD BP on Left Side of House": GrinchLocationData("Minefield", "Octopus Climbing Device Blueprints", 1007, [GrinchRamData(0x01026E, binary_bit_pos=2)]),
        "WD - Minefield - OCD BP on Right Side of Shack": GrinchLocationData("Minefield", "Octopus Climbing Device Blueprints", 1008, [GrinchRamData(0x01026E, binary_bit_pos=4)]),
        "WD - Minefield - OCD BP inside Guardian's House": GrinchLocationData("Minefield", "Octopus Climbing Device Blueprints", 1009, [GrinchRamData(0x01026E, binary_bit_pos=3)]),
#Marine Mobile Blueprints
        "WL - South Shore - MM BP on Bridge to Scout's Hut": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1100, [GrinchRamData(0x010281, binary_bit_pos=5)]),
        "WL - South Shore - MM BP across from Tent near Porcupine": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1101, [GrinchRamData(0x010281, binary_bit_pos=6)]),
        "WL - South Shore - MM BP near Outhouse": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1102, [GrinchRamData(0x010281, binary_bit_pos=7)]),
        "WL - South Shore - MM BP near Hill Bridge": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1103, [GrinchRamData(0x010282, binary_bit_pos=0)]),
        "WL - South Shore - MM BP on Scout's Hut Roof": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1104, [GrinchRamData(0x010281, binary_bit_pos=4)]),
        "WL - South Shore - MM BP on Grass Platform": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1105, [GrinchRamData(0x010281, binary_bit_pos=2)]),
        "WL - South Shore - MM BP across Zipline Platform": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1106, [GrinchRamData(0x010281, binary_bit_pos=3)]),
        "WL - South Shore - MM BP behind Summer Beast": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1107, [GrinchRamData(0x010282, binary_bit_pos=1)]),
        "WL - North Shore - MM BP below Bridge": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1108, [GrinchRamData(0x010293, binary_bit_pos=0)]),
        "WL - North Shore - MM BP behind Skunk Hut": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1109, [GrinchRamData(0x010293, binary_bit_pos=2)]),
        "WL - North Shore - MM BP inside Skunk Hut": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1110, [GrinchRamData(0x010292, binary_bit_pos=6)]),
        "WL - North Shore - MM BP inside House's Fence": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1111, [GrinchRamData(0x010292, binary_bit_pos=7)]),
        "WL - North Shore - MM BP inside Boulder Box near Bridge": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1112, [GrinchRamData(0x010293, binary_bit_pos=3)]),
        "WL - North Shore - MM BP inside Boulder Box behind Skunk Hut": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1113, [GrinchRamData(0x010293, binary_bit_pos=4)]),
        "WL - North Shore - MM BP inside Drill House": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1114, [GrinchRamData(0x010292, binary_bit_pos=5)]),
        "WL - North Shore - MM BP on Crow Platform near Drill House": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1115, [GrinchRamData(0x010293, binary_bit_pos=1)]),
        #Grinch Copter Blueprints
        "WV - City Hall - GC BP in Safe Room": GrinchLocationData("City Hall", "Grinch Copter Blueprints", 1200, [GrinchRamData(0x01021F, binary_bit_pos=7)]),
        "WV - City Hall - GC BP in Statue Room": GrinchLocationData("City Hall", "Grinch Copter Blueprints", 1201, [GrinchRamData(0x010220, binary_bit_pos=0)]),
        "WV - Clock Tower - GC BP in Bedroom": GrinchLocationData("Clock Tower", "Grinch Copter Blueprints", 1202, [GrinchRamData(0x010216, binary_bit_pos=3)]),
        "WV - Clock Tower - GC BP in Bell Room": GrinchLocationData("Clock Tower", "Grinch Copter Blueprints", 1203, [GrinchRamData(0x010216, binary_bit_pos=2)]),
        "WF - Ski Resort - GC BP inside Dog's Fence": GrinchLocationData("Ski Resort", "Grinch Copter Blueprints", 1204, [GrinchRamData(0x010234, binary_bit_pos=7)]),
        "WF - Ski Resort - GC BP in Max Cave": GrinchLocationData("Ski Resort", "Grinch Copter Blueprints", 1205, [GrinchRamData(0x010234, binary_bit_pos=6)]),
        "WF - Civic Center - GC BP on Left Side in Bat Cave Wall": GrinchLocationData("Civic Center", "Grinch Copter Blueprints", 1206, [GrinchRamData(0x01022A, binary_bit_pos=7)]),
        "WF - Civic Center - GC BP in Frozen Ice": GrinchLocationData("Civic Center", "Grinch Copter Blueprints", 1207, [GrinchRamData(0x01022B, binary_bit_pos=0)]),
        "WD - Power Plant - GC BP in Max Cave": GrinchLocationData("Power Plant", "Grinch Copter Blueprints", 1208, [GrinchRamData(0x010265, binary_bit_pos=1)]),
        "WD - Power Plant - GC BP After First Gate": GrinchLocationData("Power Plant", "Grinch Copter Blueprints", 1209, [GrinchRamData(0x010265, binary_bit_pos=2)]),
        "WD - Generator Building - GC BP on the Highest Platform": GrinchLocationData("Generator Building", "Grinch Copter Blueprints", 1210, [GrinchRamData(0x01026B, binary_bit_pos=0)]),
        "WD - Generator Building - GC BP at the Entrance after Mission Completion": GrinchLocationData("Generator Building", "Grinch Copter Blueprints", 1211, [GrinchRamData(0x01026B, binary_bit_pos=1)]),
        "WL - Submarine World - GC BP Just Below Water Surface": GrinchLocationData("Submarine World", "Grinch Copter Blueprints", 1212, [GrinchRamData(0x010289, binary_bit_pos=3)]),
        "WL - Submarine World - GC BP Underwater": GrinchLocationData("Submarine World", "Grinch Copter Blueprints", 1213, [GrinchRamData(0x010289, binary_bit_pos=4)]),
        "WL - Mayor's Villa - GC BP on Tree Branch": GrinchLocationData("Mayor's Villa", "Grinch Copter Blueprints", 1214, [GrinchRamData(0x010275, binary_bit_pos=7)]),
        "WL - Mayor's Villa - GC BP in Pirate's Cave": GrinchLocationData("Mayor's Villa", "Grinch Copter Blueprints", 1215, [GrinchRamData(0x010275, binary_bit_pos=6)]),
#Sleigh Room Locations
        "MC - Sleigh Ride - Stealing All Gifts": GrinchLocationData("Sleigh Room", "Sleigh Ride", 1300, [GrinchRamData(0x0100BF, binary_bit_pos=6)]),
        "MC - Sleigh Ride - Neutralizing Santa": GrinchLocationData("Sleigh Room", "Sleigh Ride", None, [GrinchRamData(0x010000, value=0x3E)]),#[GrinchRamData(0x0100BF, binary_bit_pos=7)]),
#Heart of Stones
        "WV - Post Office - Heart of Stone": GrinchLocationData("Post Office", "Heart of Stones", 1400, [GrinchRamData(0x0101FA, binary_bit_pos=6)]),
        "WF - Ski Resort - Heart of Stone": GrinchLocationData("Ski Resort", "Heart of Stones", 1401, [GrinchRamData(0x0101FA, binary_bit_pos=7)]),
        "WD - Minefield - Heart of Stone": GrinchLocationData("Minefield", "Heart of Stones", 1402, [GrinchRamData(0x0101FB, binary_bit_pos=0)]),
        "WL - North Shore - Heart of Stone": GrinchLocationData("North Shore", "Heart of Stones", 1403, [GrinchRamData(0x0101FB, binary_bit_pos=1)]),
#Supadow Minigames
        # "Spin N' Win - Easy": GrinchLocationData("Spin N' Win", "Supadow Minigames", 1500, [GrinchRamData()]),
        # "Spin N' Win - Hard": GrinchLocationData("Spin N' Win", "Supadow Minigames", 1501, [GrinchRamData()]),
        # "Spin N' Win - Real Tough": GrinchLocationData("Spin N' Win", "Supadow Minigames", 1502, [GrinchRamData()]),
        # "Dankamania - Easy - 15 Points": GrinchLocationData("Dankamania", "Supadow Minigames", 1503, [GrinchRamData()]),
        # "Dankamania - Hard - 15 Points": GrinchLocationData("Dankamania", "Supadow Minigames", 1504, [GrinchRamData()]),
        # "Dankamania - Real Tough - 15 Points": GrinchLocationData("Dankamania", "Supadow Minigames", 1505, [GrinchRamData()]),
        # "The Copter Race Contest - Easy": GrinchLocationData("The Copter Race Contest", "Supadow Minigames", 1506, [GrinchRamData()]),
        # "The Copter Race Contest - Hard": GrinchLocationData("The Copter Race Contest", "Supadow Minigames", 1507, [GrinchRamData()]),
        # "The Copter Race Contest - Real Tough": GrinchLocationData("The Copter Race Contest", "Supadow Minigames", 1508, [GrinchRamData()]),
        # "Bike Race - 1st Place":  GrinchLocationData("Bike Race", "Supadow Minigames", 1509, [GrinchRamData()]),
        # "Bike Race - Top 2": GrinchLocationData("Bike Race", "Supadow Minigames", 1510, [GrinchRamData()]),
        # "Bike Race - Top 3": GrinchLocationData("Bike Race", "Supadow Minigames", 1511, [GrinchRamData()]),
# Sleigh Part Locations
        "WV - Exhaust Pipes": GrinchLocationData("Sleigh Room", "Sleigh Ride", 1600, [GrinchRamData(0x0101FB, binary_bit_pos=2)]),
        "WF - Skis": GrinchLocationData("Sleigh Room", "Sleigh Ride", 1601, [GrinchRamData(0x0101FB, binary_bit_pos=3)]),
        "WD - Tires": GrinchLocationData("Sleigh Room", "Sleigh Ride", 1602, [GrinchRamData(0x0101FB, binary_bit_pos=4)]),
        "WL - Submarine World - Twin-End Tuba": GrinchLocationData("Sleigh Room", "Sleigh Ride", 1603, [GrinchRamData(0x0101FB, binary_bit_pos=6)]),
        "WL - South Shore - GPS": GrinchLocationData("Sleigh Room", "Sleigh Ride", 1604, [GrinchRamData(0x0101FB, binary_bit_pos=5)]),
# Mount Crumpit Locations
        "MC - 1st Crate Squashed": GrinchLocationData("Mount Crumpit", "Mount Crumpit", 1700, [GrinchRamData(0x095343, value=1)]),
        "MC - 2nd Crate Squashed": GrinchLocationData("Mount Crumpit", "Mount Crumpit", 1701, [GrinchRamData(0x095343, value=2)]),
        "MC - 3rd Crate Squashed": GrinchLocationData("Mount Crumpit", "Mount Crumpit", 1702, [GrinchRamData(0x095343, value=3)]),
        "MC - 4th Crate Squashed": GrinchLocationData("Mount Crumpit", "Mount Crumpit", 1703, [GrinchRamData(0x095343, value=4)]),
        "MC - 5th Crate Squashed": GrinchLocationData("Mount Crumpit", "Mount Crumpit", 1704, [GrinchRamData(0x095343, value=5)]),
}

def grinch_locations_to_id() -> dict[str,int]:
    location_mappings: dict[str, int] = {}
    for LocationName, LocationData in grinch_locations.items():
        location_mappings.update({LocationName: GrinchLocation.get_apid(LocationData.id)})
    return location_mappings