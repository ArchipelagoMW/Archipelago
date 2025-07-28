from typing import NamedTuple, Optional

from .RamHandler import GrinchRamData
from BaseClasses import Location, Region


class GrinchLocationData(NamedTuple):
    region: str
    location_group: str
    id: Optional[int]
    update_ram_addr: list[GrinchRamData]

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
    "Enter Whoville": GrinchLocationData("Whoville", "Visitsanity", 100, [GrinchRamData(0x80010000, value=0x07)]),
    "Enter the Post Office": GrinchLocationData("Post Office", "Visitsanity", 101, [GrinchRamData(0x80010000, value=0x0A)]),
    "Enter the Town Hall": GrinchLocationData("City Hall", "Visitsanity", 102, [GrinchRamData(0x80010000, value=0x08)]),
    "Enter the Countdown-To-Xmas Clock Tower": GrinchLocationData("Countdown to X-Mas Clock Tower", "Visitsanity", 103, [GrinchRamData(0x80010000, value=0x09)]),
    "Enter Who Forest": GrinchLocationData("Who Forest", "Visitsanity", 104, [GrinchRamData(0x80010000, value=0x0B)]),
    "Enter the Ski Resort": GrinchLocationData("Ski Resort", "Visitsanity", 105, [GrinchRamData(0x80010000, value=0x0C)]),
    "Enter the Civic Center": GrinchLocationData("Civic Center", "Visitsanity", 106, [GrinchRamData(0x80010000, value=0x0D)]),
    "Enter Who Dump": GrinchLocationData("Who Dump", "Visitsanity", 107, [GrinchRamData(0x80010000, value=0x0E)]),
    "Enter the Minefield": GrinchLocationData("Minefield", "Visitsanity", 108, [GrinchRamData(0x80010000, value=0x11)]),
    "Enter the Power Plant": GrinchLocationData("Power Plant", "Visitsanity", 109, [GrinchRamData(0x80010000, value=0x10)]),
    "Enter the Generator Building": GrinchLocationData("Generator Building", "Visitsanity", 110, [GrinchRamData(0x80010000, value=0x0F)]),
    "Enter Who Lake": GrinchLocationData("Who Lake", "Visitsanity", 111, [GrinchRamData(0x80010000, value=0x12)]),
    "Enter the Submarine World": GrinchLocationData("Submarine World", "Visitsanity", 112, [GrinchRamData(0x80010000, value=0x17)]),
    "Enter the Scout's Hut": GrinchLocationData("Scout's Hut", "Visitsanity", 113, [GrinchRamData(0x80010000, value=0x13)]),
    "Enter the North Shore": GrinchLocationData("North Shore", "Visitsanity", 114, [GrinchRamData(0x80010000, value=0x14)]),
    "Enter the Mayor's Villa": GrinchLocationData("Mayor's Villa", "Visitsanity", 115, [GrinchRamData(0x80010000, value=0x16)]),
#Need to find mission completion address for handful of locations that are not documented.
#Missions that have value are those ones we need to find the check for
#Whoville Missions
    "Smashing Snowmen": GrinchLocationData("Whoville", "Whoville Missions", 200, [GrinchRamData(0x8001020C, value=10)]),
    "Shuffling The Mail": GrinchLocationData("Post Office", "Whoville Missions", 201, [GrinchRamData(0x800100BE, binary_bit_pos=1)]),
    "Painting The Mayor's Posters": GrinchLocationData("Whoville", "Whoville Missions", 202, [GrinchRamData(0x800100C6, value=10)]),
    "Launching Eggs Into Houses": GrinchLocationData("Whoville", "Whoville Missions", 203, [GrinchRamData(0x800100C7, value=10)]),
    "Modifying The Mayor's Statue": GrinchLocationData("City Hall", "Whoville Missions", 204, [GrinchRamData(0x800100BE, binary_bit_pos=2)]),
    "Advancing The Countdown-To-Xmas Clock": GrinchLocationData("Countdown to X-Mas Clock Tower", "Whoville Missions", 205, [GrinchRamData(0x800100BE, binary_bit_pos=3)]),
    # "Squashing All Gifts in Whoville": GrinchLocationData("Whoville", "Whoville Missions", 206, [GrinchRamData(0x8001005C, value=500)]),
#Who Forest Missions
    "Making Xmas Trees Droop": GrinchLocationData("Who Forest", "Who Forest Missions", 300, [GrinchRamData(0x800100C8, value=10)]),
    "Sabotaging Snow Cannon With Glue": GrinchLocationData("Who Forest", "Who Forest Missions", 301, [GrinchRamData(0x800100BE, binary_bit_pos=4)]),
    "Putting Beehives In Cabins": GrinchLocationData("Who Forest", "Who Forest Missions", 302, [GrinchRamData(0x800100CA, value=10)]),
    "Sliming The Mayor's Skis": GrinchLocationData("Ski Resort", "Who Forest Missions", 303, [GrinchRamData(0x800100BE, binary_bit_pos=5)]),
    "Replacing The Candles On The Cake With Fireworks": GrinchLocationData("Civic Center", "Who Forest Missions", 304, [GrinchRamData(0x800100BE, binary_bit_pos=6)]),
    # "Squashing All Gifts in Who Forest": GrinchLocationData("Who Forest", "Who Forest Missions", 305, [GrinchRamData(0x8001005E, value=750)]),
#Who Dump Missions
    "Stealing Food From Birds": GrinchLocationData("Who Dump", "Who Dump Missions", 400, [GrinchRamData(0x800100CB, value=10)]),
    "Feeding The Computer With Robot Parts": GrinchLocationData("Who Dump", "Who Dump Missions", 401, [GrinchRamData(0x800100BF, binary_bit_pos=3)]),
    "Infesting The Mayor's House With Rats": GrinchLocationData("Who Dump", "Who Dump Missions", 402, [GrinchRamData(0x800100BE, binary_bit_pos=7)]),
    "Conducting The Stinky Gas To Who-Bris' Shack": GrinchLocationData("Who Dump", "Who Dump Missions", 403, [GrinchRamData(0x800100BE, binary_bit_pos=8)]),
    "Shaving Who Dump Guardian": GrinchLocationData("Minefield", "Who Dump Missions", 404, [GrinchRamData(0x800100BF, binary_bit_pos=1)]),
    "Short-Circuiting Power-Plant": GrinchLocationData("Generator Building", "Who Dump Missions", 405, [GrinchRamData(0x800100BF, binary_bit_pos=2)]),
    # "Squashing All Gifts in Who Dump": GrinchLocationData("Who Dump", "Who Dump Missions", 406, [GrinchRamData(0x80010060, value=750)]),
#Who Lake Missions
    "Putting Thistles In Shorts": GrinchLocationData("Who Lake", "Who Lake Missions", 500, [GrinchRamData(0x800100E6, value=10)]),
    "Sabotaging The Tents": GrinchLocationData("Who Lake", "Who Lake Missions", 501, [GrinchRamData(0x800100E5, value=10)]),
    "Drilling Holes In Canoes": GrinchLocationData("North Shore", "Who Lake Missions", 502, [GrinchRamData(0x800100EE, value=10)]),
    "Modifying The Marine Mobile": GrinchLocationData("Submarine World", "Who Lake Missions", 503, [GrinchRamData(0x800100BF, binary_bit_pos=5)]),
    "Hooking The Mayor's Bed To The Motorboat": GrinchLocationData("Mayor's Villa", "Who Lake Missions", 504, [GrinchRamData(0x800100BF, binary_bit_pos=4)]),
    # "Squashing All Gifts in Who Lake": GrinchLocationData("Who Lake", "Who Lake Missions", 505, [GrinchRamData(0x80010062, value=1000)]),
#Need to find binary values for individual blueprints, but all ram addresses are found
#Blueprints
#Binoculars Blueprints
    "Binoculars Blueprint - Post Office Roof": GrinchLocationData("Whoville", "Binocular Blueprints", 600, [GrinchRamData(0x80100825, binary_bit_pos=3)]),
    "Binoculars Blueprint - City Hall Library - Left Side": GrinchLocationData("City Hall", "Binocular Blueprints", 601, [GrinchRamData(0x8001020B, binary_bit_pos=7)]),
    "Binoculars Blueprint - City Hall Library - Front Side": GrinchLocationData("City Hall", "Binocular Blueprints", 602, [GrinchRamData(0x8001020B, binary_bit_pos=6)]),
    "Binoculars Blueprint - City Hall Library - Right Side": GrinchLocationData("City Hall", "Binocular Blueprints", 603, [GrinchRamData(0x8001020B, binary_bit_pos=5)]),
#Rotten Egg Launcher Blueprints
    "Rotten Egg Launcher Blueprint - Outside City Hall": GrinchLocationData("Whoville", "Rotten Egg Launcher Blueprints", 700, [GrinchRamData(0x8001020B, binary_bit_pos=1)]),
    "Rotten Egg Launcher Blueprint - Outside Clock Tower": GrinchLocationData("Whoville", "Rotten Egg Launcher Blueprints", 701, [GrinchRamData(0x8001020B, binary_bit_pos=2)]),
    "Rotten Egg Launcher Blueprint - Post Office - Front of Silver Door": GrinchLocationData("Post Office", "Rotten Egg Launcher Blueprints", 702, [GrinchRamData(0x8001021C, binary_bit_pos=2)]),
    "Rotten Egg Launcher Blueprint - Post Office - After Mission Completion": GrinchLocationData("Post Office", "Rotten Egg Launcher Blueprints", 703, [GrinchRamData(0x8001021C, binary_bit_pos=3)]),
#Rocket Spring Blueprints
    "Rocket Spring Blueprint - Behind Vacuum": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 800, [GrinchRamData(0x80010243, binary_bit_pos=4)]),
    "Rocket Spring Blueprint - Front of 2nd House near entrance": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 801, [GrinchRamData(0x80010243, binary_bit_pos=2)]),
    "Rocket Spring Blueprint - Near Tree House on Ground": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 802, [GrinchRamData(0x80010243, binary_bit_pos=5)]),
    "Rocket Spring Blueprint - Near Cable Car House": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 804, [GrinchRamData(0x80010242, binary_bit_pos=8)]),
    "Rocket Spring Blueprint - Near Who Snowball in Cave": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 805, [GrinchRamData(0x80010242, binary_bit_pos=7)]),
    "Rocket Spring Blueprint - Branch Platform Closest to Glue Cannon": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 806, [GrinchRamData(0x80010243, binary_bit_pos=3)]),
    "Rocket Spring Blueprint - Branch Platform Near Beast": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 807, [GrinchRamData(0x80010243, binary_bit_pos=1)]),
    "Rocket Spring Blueprint - Branch Platform Ledge Grab House": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 808, [GrinchRamData(0x80010243, binary_bit_pos=7)]),
    "Rocket Spring Blueprint - On Tree House": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 809, [GrinchRamData(0x80010243, binary_bit_pos=6)]),
#Slime Shooter Blueprints
    "Slime Shooter Blueprint - Branch Platform Elevated House": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 900, [GrinchRamData(0x80010244, binary_bit_pos=4)]),
    "Slime Shooter Blueprint - Branch Platform House next to Beast": GrinchLocationData("Who Forest", "Slime Shooter Blueprint", 901, [GrinchRamData(0x80010243, binary_bit_pos=8)]),
    "Slime Shooter Blueprint - House near Civic Center Cave": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 902, [GrinchRamData(0x80010244, binary_bit_pos=3)]),
    "Slime Shooter Blueprint - House next to Tree House": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 903, [GrinchRamData(0x80010244, binary_bit_pos=2)]),
    "Slime Shooter Blueprint - House across from Tree House": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 904, [GrinchRamData(0x80010244, binary_bit_pos=6)]),
    "Slime Shooter Blueprint - 2nd House near entrance right side": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 905, [GrinchRamData(0x80010244, binary_bit_pos=5)]),
    "Slime Shooter Blueprint - 2nd House near entrance left side": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 906, [GrinchRamData(0x80010244, binary_bit_pos=8)]),
    "Slime Shooter Blueprint - 2nd House near entrance inbetween blueprints": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 907, [GrinchRamData(0x80010244, binary_bit_pos=7)]),
    "Slime Shooter Blueprint - House near entrance": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 908, [GrinchRamData(0x80010244, binary_bit_pos=1)]),
#Octopus Climbing Device
    "Octopus Climbing Device Blueprint - Middle Pipe": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1001, [GrinchRamData(0x80010252, binary_bit_pos=4)]),
    "Octopus Climbing Device Blueprint - Right Pipe": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1002, [GrinchRamData(0x80010252, binary_bit_pos=6)]),
    "Octopus Climbing Device Blueprint - Mayor's House Rat Vent": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1003, [GrinchRamData(0x80010252, binary_bit_pos=2)]),
    "Octopus Climbing Device Blueprint - Left Pipe": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1004, [GrinchRamData(0x80010252, binary_bit_pos=5)]),
    "Octopus Climbing Device Blueprint - Near Power Plant Wall on right side": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1005, [GrinchRamData(0x80010252, binary_bit_pos=1)]),
    "Octopus Climbing Device Blueprint - Near Who-Bris' Shack": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1006, [GrinchRamData(0x80010252, binary_bit_pos=3)]),
    "Octopus Climbing Device Blueprint - Guardian's House - Left Side": GrinchLocationData("Minefield", "Octopus Climbing Device Blueprints", 1007, [GrinchRamData(0x8001026E, binary_bit_pos=3)]),
    "Octopus Climbing Device Blueprint - Guardian's House - Right Side": GrinchLocationData("Minefield", "Octopus Climbing Device Blueprints", 1008, [GrinchRamData(0x8001026E, binary_bit_pos=5)]),
    "Octopus Climbing Device Blueprint - Inside Guardian's House": GrinchLocationData("Minefield", "Octopus Climbing Device Blueprints", 1009, [GrinchRamData(0x8001026E, binary_bit_pos=3)]),
#Marine Mobile Blueprints
    "Marine Mobile Blueprint - South Shore - Bridge to Scout's Hut": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1100, [GrinchRamData(0x80010281, binary_bit_pos=6)]),
    "Marine Mobile Blueprint - South Shore - Tent near Porcupine": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1101, [GrinchRamData(0x80010281, binary_bit_pos=7)]),
    "Marine Mobile Blueprint - South Shore - Near Outhouse": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1102, [GrinchRamData(0x80010281, binary_bit_pos=8)]),
    "Marine Mobile Blueprint - South Shore - Near Hill Bridge": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1103, [GrinchRamData(0x80010282, binary_bit_pos=1)]),
    "Marine Mobile Blueprint - South Shore - Scout's Hut Roof": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1104, [GrinchRamData(0x80010281, binary_bit_pos=5)]),
    "Marine Mobile Blueprint - South Shore - Grass Platform": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1105, [GrinchRamData(0x80010281, binary_bit_pos=3)]),
    "Marine Mobile Blueprint - South Shore - Zipline by Beast": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1106, [GrinchRamData(0x80010281, binary_bit_pos=4)]),
    "Marine Mobile Blueprint - South Shore - Behind Summer Beast": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1107, [GrinchRamData(0x80010282, binary_bit_pos=2)]),
    "Marine Mobile Blueprint - North Shore - Below Bridge": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1108, [GrinchRamData(0x80010293, binary_bit_pos=1)]),
    "Marine Mobile Blueprint - North Shore - Behind Skunk Hut": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1109, [GrinchRamData(0x80010293, binary_bit_pos=3)]),
    "Marine Mobile Blueprint - North Shore - Inside Skunk Hut": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1110, [GrinchRamData(0x80010292, binary_bit_pos=7)]),
    "Marine Mobile Blueprint - North Shore - Fenced in Area": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1111, [GrinchRamData(0x80010292, binary_bit_pos=8)]),
    "Marine Mobile Blueprint - North Shore - Boulder Box near Bridge": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1112, [GrinchRamData(0x80010293, binary_bit_pos=4)]),
    "Marine Mobile Blueprint - North Shore - Boulder Box behind Skunk Hut": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1113, [GrinchRamData(0x80010293, binary_bit_pos=5)]),
    "Marine Mobile Blueprint - North Shore - Inside Drill House": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1114, [GrinchRamData(0x80010292, binary_bit_pos=6)]),
    "Marine Mobile Blueprint - North Shore - Crow Platform near Drill House": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1115, [GrinchRamData(0x80010293, binary_bit_pos=2)]),
#Grinch Copter Blueprints
    "Grinch Copter Blueprint - Whoville City Hall - Safe Room": GrinchLocationData("City Hall", "Grinch Copter Blueprints", 1200, [GrinchRamData(0x8001020B, binary_bit_pos=8)]),
    "Grinch Copter Blueprint - Whoville City Hall - Statue Room": GrinchLocationData("City Hall", "Grinch Copter Blueprints", 1201, [GrinchRamData(0x80010220, binary_bit_pos=1)]),
    "Grinch Copter Blueprint - Whoville Clock Tower - Before Bells": GrinchLocationData("Countdown to X-Mas Clock Tower", "Grinch Copter Blueprints", 1202, [GrinchRamData(0x80010265, binary_bit_pos=4)]),
    "Grinch Copter Blueprint - Whoville Clock Tower - After Bells": GrinchLocationData("Countdown to X-Mas Clock Tower", "Grinch Copter Blueprints", 1203, [GrinchRamData(0x80010265, binary_bit_pos=3)]),
    "Grinch Copter Blueprint - Who Forest Ski Resort - Inside Dog's Fence": GrinchLocationData("Ski Resort", "Grinch Copter Blueprints", 1204, [GrinchRamData(0x80010234, binary_bit_pos=8)]),
    "Grinch Copter Blueprint - Who Forest Ski Resort - Max Cave": GrinchLocationData("Ski Resort", "Grinch Copter Blueprints", 1205, [GrinchRamData(0x80010234, binary_bit_pos=7)]),
    "Grinch Copter Blueprint - Who Forest Civic Center - Climb across Bat Cave wall": GrinchLocationData("Civic Center", "Grinch Copter Blueprints", 1206, [GrinchRamData(0x8001022A, binary_bit_pos=8)]),
    "Grinch Copter Blueprint - Who Forest Civic Center - Shoot Icicle in Bat Entrance": GrinchLocationData("Civic Center", "Grinch Copter Blueprints", 1207, [GrinchRamData(0x8001022B, binary_bit_pos=1)]),
    "Grinch Copter Blueprint - Who Dump Power Plant - Max Cave": GrinchLocationData("Power Plant", "Grinch Copter Blueprints", 1208, [GrinchRamData(0x80010265, binary_bit_pos=2)]),
    "Grinch Copter Blueprint - Who Dump Power Plant - After First Gate": GrinchLocationData("Power Plant", "Grinch Copter Blueprints", 1209, [GrinchRamData(0x80010265, binary_bit_pos=3)]),
    "Grinch Copter Blueprint - Who Dump Generator Building - Before Mission": GrinchLocationData("Generator Building", "Grinch Copter Blueprints", 1210, [GrinchRamData(0x8001026B, binary_bit_pos=1)]),
    "Grinch Copter Blueprint - Who Dump Generator Building - After Mission": GrinchLocationData("Generator Building", "Grinch Copter Blueprints", 1211, [GrinchRamData(0x8001026B, binary_bit_pos=2)]),
    "Grinch Copter Blueprint - Who Lake South Shore - Submarine World - Above Surface": GrinchLocationData("Submarine World", "Grinch Copter Blueprints", 1212, [GrinchRamData(0x80010289, binary_bit_pos=4)]),
    "Grinch Copter Blueprint - Who Lake South Shore - Submarine World - Underwater": GrinchLocationData("Submarine World", "Grinch Copter Blueprints", 1213, [GrinchRamData(0x80010289, binary_bit_pos=5)]),
    "Grinch Copter Blueprint - Who Lake North Shore - Mayor's Villa - Tree Branch": GrinchLocationData("Mayor's Villa", "Grinch Copter Blueprints", 1214, [GrinchRamData(0x80010275, binary_bit_pos=8)]),
    "Grinch Copter Blueprint - Who Lake North Shore - Mayor's Villa - Cave": GrinchLocationData("Mayor's Villa", "Grinch Copter Blueprints", 1215, [GrinchRamData(0x80010275, binary_bit_pos=7)]),
#Sleigh Room Locations
    "Stealing All Gifts": GrinchLocationData("Sleigh Room", "Sleigh Ride", 1300, [GrinchRamData(0x800100BF, binary_bit_pos=7)]),
    "Neutralizing Santa": GrinchLocationData("Sleigh Room", "Sleigh Ride", None, [GrinchRamData(0x800100BF, binary_bit_pos=8)])
}

def grinch_locations_to_id() -> dict[str,int]:
    location_mappings: dict[str, int] = {}
    for LocationName, LocationData in grinch_locations.items():
        location_mappings.update({LocationName: GrinchLocation.get_apid(LocationData.id)})
    return location_mappings