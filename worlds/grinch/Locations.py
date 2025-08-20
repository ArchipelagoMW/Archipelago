from typing import NamedTuple, Optional

from .RamHandler import GrinchRamData
from BaseClasses import Location, Region


class GrinchLocationData(NamedTuple):
    region: str
    location_group: str
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
        "Enter Whoville": GrinchLocationData("Whoville", "Visitsanity", 100, [GrinchRamData(0x010000, value=0x07)]),
        "Enter the Post Office": GrinchLocationData("Post Office", "Visitsanity", 101, [GrinchRamData(0x010000, value=0x0A)]),
        "Enter the Town Hall": GrinchLocationData("City Hall", "Visitsanity", 102, [GrinchRamData(0x010000, value=0x08)]),
        "Enter the Countdown-To-Xmas Clock Tower": GrinchLocationData("Countdown to X-Mas Clock Tower", "Visitsanity", 103, [GrinchRamData(0x010000, value=0x09)]),
        "Enter Who Forest": GrinchLocationData("Who Forest", "Visitsanity", 104, [GrinchRamData(0x010000, value=0x0B)]),
        "Enter the Ski Resort": GrinchLocationData("Ski Resort", "Visitsanity", 105, [GrinchRamData(0x010000, value=0x0C)]),
        "Enter the Civic Center": GrinchLocationData("Civic Center", "Visitsanity", 106, [GrinchRamData(0x010000, value=0x0D)]),
        "Enter Who Dump": GrinchLocationData("Who Dump", "Visitsanity", 107, [GrinchRamData(0x010000, value=0x0E)]),
        "Enter the Minefield": GrinchLocationData("Minefield", "Visitsanity", 108, [GrinchRamData(0x010000, value=0x11)]),
        "Enter the Power Plant": GrinchLocationData("Power Plant", "Visitsanity", 109, [GrinchRamData(0x010000, value=0x10)]),
        "Enter the Generator Building": GrinchLocationData("Generator Building", "Visitsanity", 110, [GrinchRamData(0x010000, value=0x0F)]),
        "Enter Who Lake": GrinchLocationData("Who Lake", "Visitsanity", 111, [GrinchRamData(0x010000, value=0x12)]),
        "Enter the Submarine World": GrinchLocationData("Submarine World", "Visitsanity", 112, [GrinchRamData(0x010000, value=0x17)]),
        "Enter the Scout's Hut": GrinchLocationData("Scout's Hut", "Visitsanity", 113, [GrinchRamData(0x010000, value=0x13)]),
        "Enter the North Shore": GrinchLocationData("North Shore", "Visitsanity", 114, [GrinchRamData(0x010000, value=0x14)]),
        "Enter the Mayor's Villa": GrinchLocationData("Mayor's Villa", "Visitsanity", 115, [GrinchRamData(0x010000, value=0x16)]),
#Need to find mission completion address for handful of locations that are not documented.
#Missions that have value are those ones we need to find the check for
#Whoville Missions
        "Shuffling The Mail": GrinchLocationData("Post Office", "Whoville Missions", 201, [GrinchRamData(0x0100BE, binary_bit_pos=0)]),
        "Smashing Snowmen": GrinchLocationData("Whoville", "Whoville Missions", 200, [GrinchRamData(0x0100C5, value=10)]),
        "Painting The Mayor's Posters": GrinchLocationData("Whoville", "Whoville Missions", 202, [GrinchRamData(0x0100C6, value=10)]),
        "Launching Eggs Into Houses": GrinchLocationData("Whoville", "Whoville Missions", 203, [GrinchRamData(0x0100C7, value=10)]),
        "Modifying The Mayor's Statue": GrinchLocationData("City Hall", "Whoville Missions", 204, [GrinchRamData(0x0100BE, binary_bit_pos=1)]),
        "Advancing The Countdown-To-Xmas Clock": GrinchLocationData("Countdown to X-Mas Clock Tower", "Whoville Missions", 205, [GrinchRamData(0x0100BE, binary_bit_pos=2)]),
        "Squashing All Gifts in Whoville": GrinchLocationData("Whoville", "Whoville Missions", 206, [GrinchRamData(0x01005C, value=500)]),
#Who Forest Missions
        "Making Xmas Trees Droop": GrinchLocationData("Who Forest", "Who Forest Missions", 300, [GrinchRamData(0x0100C8, value=10)]),
        "Sabotaging Snow Cannon With Glue": GrinchLocationData("Who Forest", "Who Forest Missions", 301, [GrinchRamData(0x0100BE, binary_bit_pos=3)]),
        "Putting Beehives In Cabins": GrinchLocationData("Who Forest", "Who Forest Missions", 302, [GrinchRamData(0x0100CA, value=10)]),
        "Sliming The Mayor's Skis": GrinchLocationData("Ski Resort", "Who Forest Missions", 303, [GrinchRamData(0x0100BE, binary_bit_pos=4)]),
        "Replacing The Candles On The Cake With Fireworks": GrinchLocationData("Civic Center", "Who Forest Missions", 304, [GrinchRamData(0x0100BE, binary_bit_pos=5)]),
        "Squashing All Gifts in Who Forest": GrinchLocationData("Who Forest", "Who Forest Missions", 305, [GrinchRamData(0x01005E, value=750)]),
#Who Dump Missions
        "Stealing Food From Birds": GrinchLocationData("Who Dump", "Who Dump Missions", 400, [GrinchRamData(0x0100CB, value=10)]),
        "Feeding The Computer With Robot Parts": GrinchLocationData("Who Dump", "Who Dump Missions", 401, [GrinchRamData(0x0100BF, binary_bit_pos=2)]),
        "Infesting The Mayor's House With Rats": GrinchLocationData("Who Dump", "Who Dump Missions", 402, [GrinchRamData(0x0100BE, binary_bit_pos=6)]),
        "Conducting The Stinky Gas To Who-Bris' Shack": GrinchLocationData("Who Dump", "Who Dump Missions", 403, [GrinchRamData(0x0100BE, binary_bit_pos=7)]),
        "Shaving Who Dump Guardian": GrinchLocationData("Minefield", "Who Dump Missions", 404, [GrinchRamData(0x0100BF, binary_bit_pos=0)]),
        "Short-Circuiting Power-Plant": GrinchLocationData("Generator Building", "Who Dump Missions", 405, [GrinchRamData(0x0100BF, binary_bit_pos=1)]),
        "Squashing All Gifts in Who Dump": GrinchLocationData("Who Dump", "Who Dump Missions", 406, [GrinchRamData(0x010060, value=750)]),
#Who Lake Missions
        "Putting Thistles In Shorts": GrinchLocationData("Who Lake", "Who Lake Missions", 500, [GrinchRamData(0x0100E6, value=10)]),
        "Sabotaging The Tents": GrinchLocationData("Who Lake", "Who Lake Missions", 501, [GrinchRamData(0x0100E5, value=10)]),
        "Drilling Holes In Canoes": GrinchLocationData("North Shore", "Who Lake Missions", 502, [GrinchRamData(0x0100EE, value=10)]),
        "Modifying The Marine Mobile": GrinchLocationData("Submarine World", "Who Lake Missions", 503, [GrinchRamData(0x0100BF, binary_bit_pos=4)]),
        "Hooking The Mayor's Bed To The Motorboat": GrinchLocationData("Mayor's Villa", "Who Lake Missions", 504, [GrinchRamData(0x0100BF, binary_bit_pos=3)]),
        "Squashing All Gifts in Who Lake": GrinchLocationData("Who Lake", "Who Lake Missions", 505, [GrinchRamData(0x010062, value=1000)]),
#Need to find binary values for individual blueprints, but all ram addresses are found
#Blueprints
#Binoculars Blueprints
        "Binoculars Blueprint - Post Office Roof": GrinchLocationData("Whoville", "Binocular Blueprints", 600, [GrinchRamData(0x01020B, binary_bit_pos=2)]),
        "Binoculars Blueprint - City Hall Library - Left Side": GrinchLocationData("City Hall", "Binocular Blueprints", 601, [GrinchRamData(0x01021F, binary_bit_pos=6)]),
        "Binoculars Blueprint - City Hall Library - Front Side": GrinchLocationData("City Hall", "Binocular Blueprints", 602, [GrinchRamData(0x01021F, binary_bit_pos=5)]),
        "Binoculars Blueprint - City Hall Library - Right Side": GrinchLocationData("City Hall", "Binocular Blueprints", 603, [GrinchRamData(0x01021F, binary_bit_pos=4)]),
#Rotten Egg Launcher Blueprints
        "REL Blueprint - Outside City Hall": GrinchLocationData("Whoville", "Rotten Egg Launcher Blueprints", 700, [GrinchRamData(0x01020B, binary_bit_pos=0)]),
        "REL Blueprint - Outside Clock Tower": GrinchLocationData("Whoville", "Rotten Egg Launcher Blueprints", 701, [GrinchRamData(0x01020B, binary_bit_pos=1)]),
        "REL Blueprint - Post Office - Inside Silver Room": GrinchLocationData("Post Office", "Rotten Egg Launcher Blueprints", 702, [GrinchRamData(0x01021C, binary_bit_pos=1)]),
        "REL Blueprint - Post Office - After Mission Completion": GrinchLocationData("Post Office", "Rotten Egg Launcher Blueprints", 703, [GrinchRamData(0x01021C, binary_bit_pos=2)]),
#Rocket Spring Blueprints
        "RS Blueprint - Behind Vacuum": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 800, [GrinchRamData(0x010243, binary_bit_pos=3)]),
        "RS Blueprint - Front of 2nd House near entrance": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 801, [GrinchRamData(0x010243, binary_bit_pos=1)]),
        "RS Blueprint - Near Tree House on Ground": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 802, [GrinchRamData(0x010243, binary_bit_pos=4)]),
        "RS Blueprint - Near Cable Car House": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 804, [GrinchRamData(0x010242, binary_bit_pos=7)]),
        "RS Blueprint - Near Who Snowball in Cave": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 805, [GrinchRamData(0x010242, binary_bit_pos=6)]),
        "RS Blueprint - Branch Platform Closest to Glue Cannon": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 806, [GrinchRamData(0x010243, binary_bit_pos=2)]),
        "RS Blueprint - Branch Platform Near Beast": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 807, [GrinchRamData(0x010243, binary_bit_pos=0)]),
        "RS Blueprint - Branch Platform Ledge Grab House": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 808, [GrinchRamData(0x010243, binary_bit_pos=6)]),
        "RS Blueprint - On Tree House": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 809, [GrinchRamData(0x010243, binary_bit_pos=5)]),
#Slime Shooter Blueprints
        "SS Blueprint - Branch Platform Elevated House": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 900, [GrinchRamData(0x010244, binary_bit_pos=3)]),
        "SS Blueprint - Branch Platform House next to Beast": GrinchLocationData("Who Forest", "Slime Shooter Blueprint", 901, [GrinchRamData(0x010243, binary_bit_pos=7)]),
        "SS Blueprint - House near Civic Center Cave": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 902, [GrinchRamData(0x010244, binary_bit_pos=2)]),
        "SS Blueprint - House next to Tree House": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 903, [GrinchRamData(0x010244, binary_bit_pos=1)]),
        "SS Blueprint - House across from Tree House": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 904, [GrinchRamData(0x010244, binary_bit_pos=5)]),
        "SS Blueprint - 2nd House near entrance right side": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 905, [GrinchRamData(0x010244, binary_bit_pos=4)]),
        "SS Blueprint - 2nd House near entrance left side": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 906, [GrinchRamData(0x010244, binary_bit_pos=7)]),
        "SS Blueprint - 2nd House near entrance inbetween blueprints": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 907, [GrinchRamData(0x010244, binary_bit_pos=6)]),
        "SS Blueprint - House near entrance": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 908, [GrinchRamData(0x010244, binary_bit_pos=0)]),
#Octopus Climbing Device
        "OCD Blueprint - Middle Pipe": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1001, [GrinchRamData(0x010252, binary_bit_pos=3)]),
        "OCD Blueprint - Right Pipe": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1002, [GrinchRamData(0x010252, binary_bit_pos=5)]),
        "OCD Blueprint - Mayor's House Rat Vent": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1003, [GrinchRamData(0x010252, binary_bit_pos=1)]),
        "OCD Blueprint - Left Pipe": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1004, [GrinchRamData(0x010252, binary_bit_pos=4)]),
        "OCD Blueprint - Near Power Plant Wall on right side": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1005, [GrinchRamData(0x010252, binary_bit_pos=0)]),
        "OCD Blueprint - Near Who-Bris' Shack": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1006, [GrinchRamData(0x010252, binary_bit_pos=2)]),
        "OCD Blueprint - Guardian's House - Left Side": GrinchLocationData("Minefield", "Octopus Climbing Device Blueprints", 1007, [GrinchRamData(0x01026E, binary_bit_pos=2)]),
        "OCD Blueprint - Guardian's House - Right Side": GrinchLocationData("Minefield", "Octopus Climbing Device Blueprints", 1008, [GrinchRamData(0x01026E, binary_bit_pos=4)]),
        "OCD Blueprint - Inside Guardian's House": GrinchLocationData("Minefield", "Octopus Climbing Device Blueprints", 1009, [GrinchRamData(0x01026E, binary_bit_pos=3)]),
#Marine Mobile Blueprints
        "MM Blueprint - South Shore - Bridge to Scout's Hut": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1100, [GrinchRamData(0x010281, binary_bit_pos=5)]),
        "MM Blueprint - South Shore - Tent near Porcupine": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1101, [GrinchRamData(0x010281, binary_bit_pos=6)]),
        "MM Blueprint - South Shore - Near Outhouse": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1102, [GrinchRamData(0x010281, binary_bit_pos=7)]),
        "MM Blueprint - South Shore - Near Hill Bridge": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1103, [GrinchRamData(0x010282, binary_bit_pos=0)]),
        "MM Blueprint - South Shore - Scout's Hut Roof": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1104, [GrinchRamData(0x010281, binary_bit_pos=4)]),
        "MM Blueprint - South Shore - Grass Platform": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1105, [GrinchRamData(0x010281, binary_bit_pos=2)]),
        "MM Blueprint - South Shore - Zipline by Beast": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1106, [GrinchRamData(0x010281, binary_bit_pos=3)]),
        "MM Blueprint - South Shore - Behind Summer Beast": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1107, [GrinchRamData(0x010282, binary_bit_pos=1)]),
        "MM Blueprint - North Shore - Below Bridge": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1108, [GrinchRamData(0x010293, binary_bit_pos=0)]),
        "MM Blueprint - North Shore - Behind Skunk Hut": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1109, [GrinchRamData(0x010293, binary_bit_pos=2)]),
        "MM Blueprint - North Shore - Inside Skunk Hut": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1110, [GrinchRamData(0x010292, binary_bit_pos=6)]),
        "MM Blueprint - North Shore - Fenced in Area": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1111, [GrinchRamData(0x010292, binary_bit_pos=7)]),
        "MM Blueprint - North Shore - Boulder Box near Bridge": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1112, [GrinchRamData(0x010293, binary_bit_pos=3)]),
        "MM Blueprint - North Shore - Boulder Box behind Skunk Hut": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1113, [GrinchRamData(0x010293, binary_bit_pos=4)]),
        "MM Blueprint - North Shore - Inside Drill House": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1114, [GrinchRamData(0x010292, binary_bit_pos=5)]),
        "MM Blueprint - North Shore - Crow Platform near Drill House": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1115, [GrinchRamData(0x010293, binary_bit_pos=1)]),
        #Grinch Copter Blueprints
        "GC Blueprint - Whoville City Hall - Safe Room": GrinchLocationData("City Hall", "Grinch Copter Blueprints", 1200, [GrinchRamData(0x01021F, binary_bit_pos=7)]),
        "GC Blueprint - Whoville City Hall - Statue Room": GrinchLocationData("City Hall", "Grinch Copter Blueprints", 1201, [GrinchRamData(0x010220, binary_bit_pos=0)]),
        "GC Blueprint - Whoville Clock Tower - Before Bells": GrinchLocationData("Countdown to X-Mas Clock Tower", "Grinch Copter Blueprints", 1202, [GrinchRamData(0x010216, binary_bit_pos=3)]),
        "GC Blueprint - Whoville Clock Tower - After Bells": GrinchLocationData("Countdown to X-Mas Clock Tower", "Grinch Copter Blueprints", 1203, [GrinchRamData(0x010216, binary_bit_pos=2)]),
        "GC Blueprint - Who Forest Ski Resort - Inside Dog's Fence": GrinchLocationData("Ski Resort", "Grinch Copter Blueprints", 1204, [GrinchRamData(0x010234, binary_bit_pos=7)]),
        "GC Blueprint - Who Forest Ski Resort - Max Cave": GrinchLocationData("Ski Resort", "Grinch Copter Blueprints", 1205, [GrinchRamData(0x010234, binary_bit_pos=6)]),
        "GC Blueprint - Who Forest Civic Center - Climb across Bat Cave wall": GrinchLocationData("Civic Center", "Grinch Copter Blueprints", 1206, [GrinchRamData(0x01022A, binary_bit_pos=7)]),
        "GC Blueprint - Who Forest Civic Center - Shoot Icicle in Bat Entrance": GrinchLocationData("Civic Center", "Grinch Copter Blueprints", 1207, [GrinchRamData(0x01022B, binary_bit_pos=0)]),
        "GC Blueprint - Who Dump Power Plant - Max Cave": GrinchLocationData("Power Plant", "Grinch Copter Blueprints", 1208, [GrinchRamData(0x010265, binary_bit_pos=1)]),
        "GC Blueprint - Who Dump Power Plant - After First Gate": GrinchLocationData("Power Plant", "Grinch Copter Blueprints", 1209, [GrinchRamData(0x010265, binary_bit_pos=2)]),
        "GC Blueprint - Who Dump Generator Building - Before Mission": GrinchLocationData("Generator Building", "Grinch Copter Blueprints", 1210, [GrinchRamData(0x01026B, binary_bit_pos=0)]),
        "GC Blueprint - Who Dump Generator Building - After Mission": GrinchLocationData("Generator Building", "Grinch Copter Blueprints", 1211, [GrinchRamData(0x01026B, binary_bit_pos=1)]),
        "GC Blueprint - Who Lake South Shore - Submarine World - Above Surface": GrinchLocationData("Submarine World", "Grinch Copter Blueprints", 1212, [GrinchRamData(0x010289, binary_bit_pos=3)]),
        "GC Blueprint - Who Lake South Shore - Submarine World - Underwater": GrinchLocationData("Submarine World", "Grinch Copter Blueprints", 1213, [GrinchRamData(0x010289, binary_bit_pos=4)]),
        "GC Blueprint - Who Lake North Shore - Mayor's Villa - Tree Branch": GrinchLocationData("Mayor's Villa", "Grinch Copter Blueprints", 1214, [GrinchRamData(0x010275, binary_bit_pos=7)]),
        "GC Blueprint - Who Lake North Shore - Mayor's Villa - Cave": GrinchLocationData("Mayor's Villa", "Grinch Copter Blueprints", 1215, [GrinchRamData(0x010275, binary_bit_pos=6)]),
#Sleigh Room Locations
        "Stealing All Gifts": GrinchLocationData("Sleigh Room", "Sleigh Ride", 1300, [GrinchRamData(0x0100BF, binary_bit_pos=6)]),
        "Neutralizing Santa": GrinchLocationData("Sleigh Room", "Sleigh Ride", None, [GrinchRamData(0x0100BF, binary_bit_pos=7)]),
#Heart of Stones
        # "Heart of Stone - Whoville": GrinchLocationData("Post Office", "Heart of Stones"), 1400, [GrinchRamData()]),
        # "Heart of Stone - Who Forest": GrinchLocationData("Ski Resort", "Heart of Stones"), 1401, [GrinchRamData()]),
        # "Heart of Stone - Who Dump": GrinchLocationData("Minefield", "Heart of Stones"), 1402, [GrinchRamData()]),
        # "Heart of Stone - Who Lake": GrinchLocationData("North Shore", "Heart of Stones"), 1402, [GrinchRamData()]),
#Supadow Minigames
        # "Spin N' Win - Easy": GrinchLocationData("Spin N' Win Supadow", "Supadow Minigames"), 1500, [GrinchRamData()]),
        # "Spin N' Win - Hard": GrinchLocationData("Spin N' Win Supadow", "Supadow Minigames"), 1501, [GrinchRamData()]),
        # "Spin N' Win - Real Tough": GrinchLocationData("Spin N' Win Supadow", "Supadow Minigames"), 1502, [GrinchRamData()]),
        # "Dankamania - Easy - 15 Points": GrinchLocationData("Dankamania Supadow", "Supadow Minigames"), 1503, [GrinchRamData()]),
        # "Dankamania - Hard - 15 Points": GrinchLocationData("Dankamania Supadow", "Supadow Minigames"), 1504, [GrinchRamData()]),
        # "Dankamania - Real Tough - 15 Points": GrinchLocationData("Dankamania Supadow", "Supadow Minigames"), 1505, [GrinchRamData()]),
        # "The Copter Race Contest - Easy": GrinchLocationData("The Copter Race Contest Supadow", "Supadow Minigames"), 1506, [GrinchRamData()]),
        # "The Copter Race Contest - Hard": GrinchLocationData("The Copter Race Contest Supadow", "Supadow Minigames"), 1507, [GrinchRamData()]),
        # "The Copter Race Contest - Real Tough": GrinchLocationData("The Copter Race Contest Supadow", "Supadow Minigames"), 1508, [GrinchRamData()]),
        # "Bike Race - 1st Place":  GrinchLocationData("Bike Race", "Supadow Minigames"), 1509, [GrinchRamData()]),
        # "Bike Race - Top 2": GrinchLocationData("Bike Race", "Supadow Minigames"), 1510, [GrinchRamData()]),
        # "Bike Race - Top 3": GrinchLocationData("Bike Race", "Supadow Minigames"), 1511, [GrinchRamData()]),
}

def grinch_locations_to_id() -> dict[str,int]:
    location_mappings: dict[str, int] = {}
    for LocationName, LocationData in grinch_locations.items():
        location_mappings.update({LocationName: GrinchLocation.get_apid(LocationData.id)})
    return location_mappings