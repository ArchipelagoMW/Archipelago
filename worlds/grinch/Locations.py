from typing import NamedTuple, Optional

from BaseClasses import Location
from BaseClasses import ItemClassification as IC

class GrinchLocationData(NamedTuple):
    region: str
    location_group: str
    id: Optional[int]
    classification: IC
    update_ram_addr: list[GrinchRamData]
    value: Optional[int] = None #I can either set or add either hex or unsigned values through Client.py
    binary_bit_pos: Optional[int] = None
    bit_size: int = 1

class GrinchLocation(Location):
    game: str = "The Grinch"
    location_group: str

    @staticmethod
    def get_apid(code: int):
        base_id: int = 42069
        return base_id + code

grinch_locations = {
#Going to use current map id as indicator whether or not you visited a location
#Visitsanity
    "Enter Whoville": GrinchLocationData("Visitsanity", 100, [GrinchRamData(0x80010000, value=0x07)]),
    "Enter the Post Office": GrinchLocationData("Visitsanity", 101, [GrinchRamData(0x80010000, value=0x0A)]),
    "Enter the Town Hall": GrinchLocationData("Visitsanity", 102, [GrinchRamData(0x80010000, value=0x08)]),
    "Enter the Countdown-To-Xmas Clock Tower": GrinchLocationData("Visitsanity", 103, [GrinchRamData(0x80010000, value=0x09)]),
    "Enter Who Forest": GrinchLocationData("Visitsanity", 104, [GrinchRamData(0x80010000, value=0x0B)]),
    "Enter the Ski Resort": GrinchLocationData("Visitsanity", 105, [GrinchRamData(0x80010000, value=0x0C)]),
    "Enter the Civic Center": GrinchLocationData("Visitsanity", 106, [GrinchRamData(0x80010000, value=0x0D)]),
    "Enter Who Dump": GrinchLocationData("Visitsanity", 107, [GrinchRamData(0x80010000, value=0x0E)]),
    "Enter the Guardian's House Mine Field": GrinchLocationData("Visitsanity", 108, [GrinchRamData(0x80010000, value=0x11)]),
    "Enter the exterior of the Power Plant": GrinchLocationData("Visitsanity", 109, [GrinchRamData(0x80010000, value=0x10)]),
    "Enter the interior of the Power Plant": GrinchLocationData("Visitsanity", 110, [GrinchRamData(0x80010000, value=0x0F)]),
    "Enter Who Lake": GrinchLocationData("Visitsanity", 111, [GrinchRamData(0x80010000, value=0x12)]),
    "Enter the Submarine World": GrinchLocationData("Visitsanity", 112, [GrinchRamData(0x80010000, value=0x17)]),
    "Enter the Scout's Hut": GrinchLocationData("Visitsanity", 113, [GrinchRamData(0x80010000, value=0x13)]),
    "Enter the North Shore": GrinchLocationData("Visitsanity", 114, [GrinchRamData(0x80010000, value=0x14)]),
    "Enter the Mayor's Villa": GrinchLocationData("Visitsanity", 115, [GrinchRamData(0x80010000, value=0x16)]),
#Need to find mission completion address for handful of locations that are not documented.
#Missions that have value are those ones we need to find the check for
#Whoville Missions
    "Smashing Snowmen": GrinchLocationData("Whoville Missions", 200, [GrinchRamData(0x8001020C, value=10)]),
    "Shuffling The Mail": GrinchLocationData("Whoville Missions", 201, [GrinchRamData(0x800100BE, binary_bit_pos=1)]),
    "Painting The Mayor's Posters": GrinchLocationData("Whoville Missions", 202, [GrinchRamData(0x800100C6, value=10)]),
    "Launching Eggs Into Houses": GrinchLocationData("Whoville Missions", 203, [GrinchRamData(0x800100C7, value=10)]),
    "Modifying The Mayor's Statue": GrinchLocationData("Whoville Missions", 204, [GrinchRamData(0x800100BE, binary_bit_pos=2)]),
    "Advancing The Countdown-To-Xmas Clock": GrinchLocationData("Whoville Missions", 205, [GrinchRamData(0x800100BE, binary_bit_pos=3)]),
    "Squashing All Gifts in Whoville": GrinchLocationData("Whoville Missions", 206, [GrinchRamData(0x8001005C, value=500)]),
#Who Forest Missions
    "Making Xmas Trees Droop": GrinchLocationData("Who Forest Missions", 300, [GrinchRamData(0x800100C8, value=10)]),
    "Sabotaging Snow Cannon With Glue": GrinchLocationData("Who Forest Missions", 301, [GrinchRamData(0x800100BE, binary_bit_pos=4)]),
    "Putting Beehives In Cabins": GrinchLocationData("Who Forest Missions", 302, [GrinchRamData(0x800100CA, value=10)]),
    "Sliming The Mayor's Skis": GrinchLocationData("Who Forest Missions", 303, [GrinchRamData(0x800100BE, binary_bit_pos=5)]),
    "Replacing The Candles On The Cake With Fireworks": GrinchLocationData("Who Forest Missions", 304, [GrinchRamData(0x800100BE, binary_bit_pos=6)]),
    "Squashing All Gifts in Who Forest": GrinchLocationData("Who Forest Missions", 305, [GrinchRamData(0x8001005E, value=750)]),
#Who Dump Missions
    "Stealing Food From Birds": GrinchLocationData("Who Dump Missions", 400, [GrinchRamData(0x800100CB, value=10)]),
    "Feeding The Computer With Robot Parts": GrinchLocationData("Who Dump Missions", 401, [GrinchRamData(0x800100BF, binary_bit_pos=3)]),
    "Infesting The Mayor's House With Rats": GrinchLocationData("Who Dump Missions", 402, [GrinchRamData(0x800100BE, binary_bit_pos=7)]),
    "Conducting The Stinky Gas To Who-Bris' Shack": GrinchLocationData("Who Dump Missions", 403, [GrinchRamData(0x800100BE, binary_bit_pos=8)]),
    "Shaving Who Dump Guardian": GrinchLocationData("Who Dump Missions", 404, [GrinchRamData(0x800100BF, binary_bit_pos=1)]),
    "Short-Circuiting Power-Plant": GrinchLocationData("Who Dump Missions", 405, [GrinchRamData(0x800100BF, binary_bit_pos=2)]),
    "Squashing All Gifts in Who Dump": GrinchLocationData("Who Dump Missions", 406, [GrinchRamData(0x80010060, value=750)]),
#Who Lake Missions
    "Putting Thistles In Shorts": GrinchLocationData("Who Lake Missions", 500, [GrinchRamData(0x800100E6, value=10)]),
    "Sabotaging The Tents": GrinchLocationData("Who Lake Missions", 501, [GrinchRamData(0x800100E5, value=10)]),
    "Drilling Holes In Canoes": GrinchLocationData("Who Lake Missions", 502, [GrinchRamData(0x800100EE, value=10)]),
    "Modifying The Marine Mobile": GrinchLocationData("Who Lake Missions", 503, [GrinchRamData(0x800100BF, binary_bit_pos=5)]),
    "Hooking The Mayor's Bed To The Motorboat": GrinchLocationData("Who Lake Missions", 504, [GrinchRamData(0x800100BF, binary_bit_pos=4)]),
    "Squashing All Gifts in Who Lake": GrinchLocationData("Who Lake Missions", 505, [GrinchRamData(0x80010062, value=1000)]),
#Need to find binary values for individual blueprints, but all ram addresses are found
#Blueprints
#Binoculars Blueprints
    "Binoculars Blueprint - Post Office Roof": GrinchLocationData("Binocular Blueprints", 600, [GrinchRamData(0x80100824, binary_bit_pos=0)]),
    "Binoculars Blueprint - City Hall Library - Left Side": GrinchLocationData("Binocular Blueprints", 601, [GrinchRamData(0x8001021F, binary_bit_pos=0)]),
    "Binoculars Blueprint - City Hall Library - Front Side": GrinchLocationData("Binocular Blueprints", 602, [GrinchRamData(0x8001021F, binary_bit_pos=0)]),
    "Binoculars Blueprint - City Hall Library - Right Side": GrinchLocationData("Binocular Blueprints", 603, [GrinchRamData(0x8001021F, binary_bit_pos=0)]),
#Rotten Egg Launcher Blueprints
    "Rotten Egg Launcher Blueprint - Outside City Hall": GrinchLocationData("Rotten Egg Launcher Blueprints", 700, [GrinchRamData()]),
    "Rotten Egg Launcher Blueprint - Outside Clock Tower": GrinchLocationData("Rotten Egg Launcher Blueprints", 701, [GrinchRamData()]),
    "Rotten Egg Launcher Blueprint - Post Office - Front of Silver Door": GrinchLocationData("Rotten Egg Launcher Blueprints", 702, [GrinchRamData()]),
    "Rotten Egg Launcher Blueprint - Post Office - After Mission Completion": GrinchLocationData("Rotten Egg Launcher Blueprints", 703, [GrinchRamData()]),
#Rocket Spring Blueprints
    "Rocket Spring Blueprint - Behind Vacuum": GrinchLocationData("Rocket Spring Blueprints", 800, [GrinchRamData()]),
    "Rocket Spring Blueprint - Front of 2nd House near entrance": GrinchLocationData("Rocket Spring Blueprints", 801, [GrinchRamData()]),
    "Rocket Spring Blueprint - Near Tree House on Ground": GrinchLocationData("Rocket Spring Blueprints", 802, [GrinchRamData()]),
    "Rocket Spring Blueprint - Near Cable Car House": GrinchLocationData("Rocket Spring Blueprints", 804, [GrinchRamData()]),
    "Rocket Spring Blueprint - Near Who Snowball in Cave": GrinchLocationData("Rocket Spring Blueprints", 805, [GrinchRamData()]),
    "Rocket Spring Blueprint - Branch Platform Closest to Glue Cannon": GrinchLocationData("Rocket Spring Blueprints", 806, [GrinchRamData()]),
    "Rocket Spring Blueprint - Branch Platform Near Beast": GrinchLocationData("Rocket Spring Blueprints", 807, [GrinchRamData()]),
    "Rocket Spring Blueprint - Branch Platform Ledge Grab House": GrinchLocationData("Rocket Spring Blueprints", 808, [GrinchRamData()]),
    "Rocket Spring Blueprint - On Tree House": GrinchLocationData("Rocket Spring Blueprints", 809, [GrinchRamData()]),
#Slime Shooter Blueprints
    "Slime Shooter Blueprint - Branch Platform Elevated House": GrinchLocationData("Slime Shooter Blueprints", 900, [GrinchRamData()]),
    "Slime Shooter Blueprint - Branch Platform House next to Beast": GrinchLocationData("Slime Shooter Blueprint", 901, [GrinchRamData()]),
    "Slime Shooter Blueprint - House near Civic Center Cave": GrinchLocationData("Slime Shooter Blueprints", 902, [GrinchRamData()]),
    "Slime Shooter Blueprint - House next to Tree House": GrinchLocationData("Slime Shooter Blueprints", 903, [GrinchRamData()]),
    "Slime Shooter Blueprint - House across from Tree House": GrinchLocationData("Slime Shooter Blueprints", 904, [GrinchRamData()]),
    "Slime Shooter Blueprint - 2nd House near entrance right side": GrinchLocationData("Slime Shooter Blueprints", 905, [GrinchRamData()]),
    "Slime Shooter Blueprint - 2nd House near entrance left side": GrinchLocationData("Slime Shooter Blueprints", 906, [GrinchRamData()]),
    "Slime Shooter Blueprint - 2nd House near entrance inbetween blueprints": GrinchLocationData("Slime Shooter Blueprints", 907, [GrinchRamData()]),
    "Slime Shooter Blueprint - House near entrance": GrinchLocationData("Slime Shooter Blueprints", 908, [GrinchRamData()]),
#Octopus Climbing Device
    "Octopus Climbing Device Blueprint - Middle Pipe": GrinchLocationData("Octopus Climbing Device Blueprints", 1001, [GrinchRamData()]),
    "Octopus Climbing Device Blueprint - Right Pipe": GrinchLocationData("Octopus Climbing Device Blueprints", 1002, [GrinchRamData()]),
    "Octopus Climbing Device Blueprint - Mayor's House Vent Cage": GrinchLocationData("Octopus Climbing Device Blueprints", 1003, [GrinchRamData()]),
    "Octopus Climbing Device Blueprint - Left Pipe": GrinchLocationData("Octopus Climbing Device Blueprints", 1004, [GrinchRamData()]),
    "Octopus Climbing Device Blueprint - Near Power Plant Wall on left side": GrinchLocationData("Octopus Climbing Device Blueprints", 1005, [GrinchRamData()]),
    "Octopus Climbing Device Blueprint - Near Who-Bris' Shack": GrinchLocationData("Octopus Climbing Device Blueprints", 1006, [GrinchRamData()]),
    "Octopus Climbing Device Blueprint - Guardian's House - Left side of Guardian House": GrinchLocationData("Octopus Climbing Device Blueprints", 1007, [GrinchRamData()]),
    "Octopus Climbing Device Blueprint - Guardian's House - Right side of Guardian House": GrinchLocationData("Octopus Climbing Device Blueprints", 1008, [GrinchRamData()]),
    "Octopus Climbing Device Blueprint - Inside Guardian's House": GrinchLocationData("Octopus Climbing Device Blueprints", 1009, [GrinchRamData()]),
#Marine Mobile Blueprints
    "Marine Mobile Blueprint - South Shore - Bridge to Scout's Hut": GrinchLocationData("Marine Mobile Blueprints", 1100, [GrinchRamData()]),
    "Marine Mobile Blueprint - South Shore - Tent near Porcupine": GrinchLocationData("Marine Mobile Blueprints", 1101, [GrinchRamData()]),
    "Marine Mobile Blueprint - South Shore - Near Scout Shack": GrinchLocationData("Marine Mobile Blueprints", 1102, [GrinchRamData()]),
    "Marine Mobile Blueprint - South Shore - Under a Hill Bridge": GrinchLocationData("Marine Mobile Blueprints", 1103, [GrinchRamData()]),
    "Marine Mobile Blueprint - South Shore - Scout's Hut Roof": GrinchLocationData("Marine Mobile Blueprints", 1104, [GrinchRamData()]),
    "Marine Mobile Blueprint - South Shore - Jump from Boulder": GrinchLocationData("Marine Mobile Blueprints", 1105, [GrinchRamData()]),
    "Marine Mobile Blueprint - South Shore - Rope Swing by Beast": GrinchLocationData("Marine Mobile Blueprints", 1106, [GrinchRamData()]),
    "Marine Mobile Blueprint - South Shore - Near Summer Beast": GrinchLocationData("Marine Mobile Blueprints", 1107, [GrinchRamData()]),
    "Marine Mobile Blueprint - North Shore - Below Bridge": GrinchLocationData("Marine Mobile Blueprints", 1108, [GrinchRamData()]),
    "Marine Mobile Blueprint - North Shore - Behind Skunk Hut": GrinchLocationData("Marine Mobile Blueprints", 1109, [GrinchRamData()]),
    "Marine Mobile Blueprint - North Shore - Inside Skunk Hut": GrinchLocationData("Marine Mobile Blueprints", 1110, [GrinchRamData()]),
    "Marine Mobile Blueprint - North Shore - Fenced in Area": GrinchLocationData("Marine Mobile Blueprints", 1111, [GrinchRamData()]),
    "Marine Mobile Blueprint - North Shore - Boulder Box near Bridge": GrinchLocationData("Marine Mobile Blueprints", 1112, [GrinchRamData()]),
    "Marine Mobile Blueprint - North Shore - Boulder Box behind Skunk Hut": GrinchLocationData("Marine Mobile Blueprints", 1113, [GrinchRamData()]),
    "Marine Mobile Blueprint - North Shore - Inside Drill House": GrinchLocationData("Marine Mobile Blueprints", 1114, [GrinchRamData()]),
    "Marine Mobile Blueprint - North Shore - Crow Platform": GrinchLocationData("Marine Mobile Blueprints", 1115, [GrinchRamData()]),
#Grinch Copter Blueprints
    "Grinch Copter Blueprint - Whoville City Hall - Safe Room": GrinchLocationData("Grinch Copter Blueprints", 1200, [GrinchRamData()]),
    "Grinch Copter Blueprint - Whoville City Hall - Statue Room": GrinchLocationData("Grinch Copter Blueprints", 1201, [GrinchRamData()]),
    "Grinch Copter Blueprint - Whoville Clock Tower - Before Bells": GrinchLocationData("Grinch Copter Blueprints", 1202, [GrinchRamData()]),
    "Grinch Copter Blueprint - Whoville Clock Tower - After Bells": GrinchLocationData("Grinch Copter Blueprints", 1203, [GrinchRamData()]),
    "Grinch Copter Blueprint - Who Forest Ski Resort - Inside Dog's Fence": GrinchLocationData("Grinch Copter Blueprints", 1204, [GrinchRamData()]),
    "Grinch Copter Blueprint - Who Forest Ski Resort - Max Cave": GrinchLocationData("Grinch Copter Blueprints", 1205, [GrinchRamData()]),
    "Grinch Copter Blueprint - Who Forest Civic Center - Climb across wall": GrinchLocationData("Grinch Copter Blueprints", 1206, [GrinchRamData()]),
    "Grinch Copter Blueprint - Who Forest Civic Center - Icicle": GrinchLocationData("Grinch Copter Blueprints", 1207, [GrinchRamData()]),
    "Grinch Copter Blueprint - Who Dump Outside of Power Plant - First": GrinchLocationData("Grinch Copter Blueprints", 1208, [GrinchRamData()]),
    "Grinch Copter Blueprint - Who Dump Outside of Power Plant - Second Gate": GrinchLocationData("Grinch Copter Blueprints", 1209, [GrinchRamData()]),
    "Grinch Copter Blueprint - Who Dump Inside of Power Plant - Before Mission": GrinchLocationData("Grinch Copter Blueprints", 1210, [GrinchRamData()]),
    "Grinch Copter Blueprint - Who Dump Inside of Power Plant - After Mission": GrinchLocationData("Grinch Copter Blueprints", 1211, [GrinchRamData()]),
    "Grinch Copter Blueprint - Who Lake South Shore - Submarine World - Above Surface": GrinchLocationData("Grinch Copter Blueprints", 1212, [GrinchRamData()]),
    "Grinch Copter Blueprint - Who Lake South Shore - Submarine World - Underwater": GrinchLocationData("Grinch Copter Blueprints", 1213, [GrinchRamData()]),
    "Grinch Copter Blueprint - Who Lake North Shore - Mayor's Villa - Tree Branch": GrinchLocationData("Grinch Copter Blueprints", 1214, [GrinchRamData()]),
    "Grinch Copter Blueprint - Who Lake North Shore - Mayor's Villa - Cave": GrinchLocationData("Grinch Copter Blueprints", 1215, [GrinchRamData()])
#Sleigh Room Locations
    "Stealing All Gifts": GrinchLocationData("Sleigh Ride", 1300, [GrinchRamData(0x800100BF, binary_bit_pos=7)]),
    "Neutralizing Santa": GrinchLocationData("Sleigh Ride", 1301, [GrinchRamData(0x800100BF, binary_bit_pos=8)]),
}