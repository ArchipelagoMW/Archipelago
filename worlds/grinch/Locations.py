from typing import NamedTuple, Optional

from BaseClasses import Location
from BaseClasses import ItemClassification as IC

class GrinchLocationData(NamedTuple):
    region: str
    type: str
    code: Optional[int]
    classification: IC
    update_ram_addr: Optional[list[GrinchRamData]] = None
    value: Optional[int] = None #I can either set or add either hex or unsigned values through Client.py
    binary_bit_pos: Optional[int] = None
    bit_size: int = 1

class GrinchLocation(Location):
    game: str = "The Grinch"
    location_group: str

grinch_locations = {
#Visitsanity
    "Enter Whoville": GrinchLocationData("Visitsanity", 100, [GrinchRamData()]),
    "Enter the Post Office": GrinchLocationData("Visitsanity", 101, [GrinchRamData()]),
    "Enter the Town Hall": GrinchLocationData("Visitsanity", 102, [GrinchRamData()]),
    "Enter the Countdown-To-Xmas Clock Tower": GrinchLocationData("Visitsanity", 103, [GrinchRamData()]),
    "Enter Who Forest": GrinchLocationData("Visitsanity", 104, [GrinchRamData()]),
    "Enter the Ski Resort": GrinchLocationData("Visitsanity", 105, [GrinchRamData()]),
    "Enter the Civic Center": GrinchLocationData("Visitsanity", 106, [GrinchRamData()]),
    "Enter Who Dump": GrinchLocationData("Visitsanity", 107, [GrinchRamData()]),
    "Enter the Guardian's House Mine Field": GrinchLocationData("Visitsanity", 108, [GrinchRamData()]),
    "Enter the exterior of the Power Plant": GrinchLocationData("Visitsanity", 109, [GrinchRamData()]),
    "Enter the interior of the Power Plant": GrinchLocationData("Visitsanity", 110, [GrinchRamData()]),
    "Enter Who Lake": GrinchLocationData("Visitsanity", 111, [GrinchRamData()]),
    "Enter the Submarine World": GrinchLocationData("Visitsanity", 112, [GrinchRamData()]),
    "Enter the Scout's Hut": GrinchLocationData("Visitsanity", 113, [GrinchRamData()]),
    "Enter the North Shore": GrinchLocationData("Visitsanity", 114, [GrinchRamData()]),
    "Enter the Mayor's Villa": GrinchLocationData("Visitsanity", 115, [GrinchRamData()]),
#Whoville Missions
    "Smashing Snowmen": GrinchLocationData("Whoville Missions", 200, [GrinchRamData()]),
    "Shuffling The Mail": GrinchLocationData("Whoville Missions", 201, [GrinchRamData()]),
    "Painting The Mayor's Posters": GrinchLocationData("Whoville Missions", 202, [GrinchRamData()]),
    "Launching Eggs Into Houses": GrinchLocationData("Whoville Missions", 203, [GrinchRamData()]),
    "Modifying The Mayor's Statue": GrinchLocationData("Whoville Missions", 204, [GrinchRamData()]),
    "Advancing The Countdown-To-Xmas Clock": GrinchLocationData("Whoville Missions", 205, [GrinchRamData()]),
    "Squashing All Gifts in Whoville": GrinchLocationData("Whoville Missions", 206, [GrinchRamData()]),
#Who Forest Missions
    "Making Xmas Trees Droop": GrinchLocationData("Who Forest Missions", 300, [GrinchRamData()]),
    "Sabotaging Snow Cannon With Glue": GrinchLocationData("Who Forest Missions", 301, [GrinchRamData()]),
    "Putting Beehives In Cabins": GrinchLocationData("Who Forest Missions", 302, [GrinchRamData()]),
    "Sliming The Mayor's Skis": GrinchLocationData("Who Forest Missions", 303, [GrinchRamData()]),
    "Replacing The Candles On The Cake With Fireworks": GrinchLocationData("Who Forest Missions", 304, [GrinchRamData()]),
    "Squashing All Gifts in Who Forest": GrinchLocationData("Who Forest Missions", 305, [GrinchRamData()]),
#Who Dump Missions
    "Stealing Food From Birds": GrinchLocationData("Who Dump Missions", 400, [GrinchRamData()]),
    "Feeding The Computer With Robot Parts": GrinchLocationData("Who Dump Missions", 401, [GrinchRamData()]),
    "Infesting The Mayor's House With Rats": GrinchLocationData("Who Dump Missions", 402, [GrinchRamData()]),
    "Conducting The Stinky Gas To Who-Bris' Shack": GrinchLocationData("Who Dump Missions", 403, [GrinchRamData()]),
    "Shaving Who Dump Guardian": GrinchLocationData("Who Dump Missions", 404, [GrinchRamData()]),
    "Short-Circuiting Power-Plant": GrinchLocationData("Who Dump Missions", 405, [GrinchRamData()]),
    "Squashing All Gifts in Who Dump": GrinchLocationData("Who Dump Missions", 406, [GrinchRamData()]),
#Who Lake Missions
    "Putting Thistles In Shorts": GrinchLocationData("Who Lake Missions", 500, [GrinchRamData()]),
    "Sabotaging The Tents": GrinchLocationData("Who Lake Missions", 501, [GrinchRamData()]),
    "Drilling Holes In Canoes": GrinchLocationData("Who Lake Missions", 502, [GrinchRamData()]),
    "Modifying The Marine Mobile": GrinchLocationData("Who Lake Missions", 503, [GrinchRamData()]),
    "Hooking The Mayor's Bed To The Motorboat": GrinchLocationData("Who Lake Missions", 504, [GrinchRamData()]),
    "Squashing All Gifts in Who Lake": GrinchLocationData("Who Lake Missions", 505, [GrinchRamData()]),
#Binoculars Blueprints
    "Binoculars Blueprint - Post Office Roof": GrinchLocationData("Binocular Blueprints", 600, [GrinchRamData()]),
    "Binoculars Blueprint - City Hall Library - Left Side": GrinchLocationData("Binocular Blueprints", 601, [GrinchRamData()]),
    "Binoculars Blueprint - City Hall Library - Front Side": GrinchLocationData("Binocular Blueprints", 602, [GrinchRamData()]),
    "Binoculars Blueprint - City Hall Library - Right Side": GrinchLocationData("Binocular Blueprints", 603, [GrinchRamData()]),
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
}