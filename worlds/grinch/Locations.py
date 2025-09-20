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
        "Whoville - First Visit": GrinchLocationData("Whoville", "Visitsanity", 100, [GrinchRamData(0x010000, value=0x07)]),
        "Whoville's Post Office - First Visit": GrinchLocationData("Post Office", "Visitsanity", 101, [GrinchRamData(0x010000, value=0x0A)]),
        "Whoville's City Hall - First Visit": GrinchLocationData("City Hall", "Visitsanity", 102, [GrinchRamData(0x010000, value=0x08)]),
        "Whoville's Clock Tower - First Visit": GrinchLocationData("Clock Tower", "Visitsanity", 103, [GrinchRamData(0x010000, value=0x09)]),
        "Who Forest - First Visit": GrinchLocationData("Who Forest", "Visitsanity", 104, [GrinchRamData(0x010000, value=0x0B)]),
        "Who Forest's Ski Resort - First Visit": GrinchLocationData("Ski Resort", "Visitsanity", 105, [GrinchRamData(0x010000, value=0x0C)]),
        "Who Forest's Civic Center - First Visit": GrinchLocationData("Civic Center", "Visitsanity", 106, [GrinchRamData(0x010000, value=0x0D)]),
        "Who Dump - First Visit": GrinchLocationData("Who Dump", "Visitsanity", 107, [GrinchRamData(0x010000, value=0x0E)]),
        "Who Dump's Minefield - First Visit": GrinchLocationData("Minefield", "Visitsanity", 108, [GrinchRamData(0x010000, value=0x11)]),
        "Who Dump's Power Plant - First Visit": GrinchLocationData("Power Plant", "Visitsanity", 109, [GrinchRamData(0x010000, value=0x10)]),
        "Who Dump's Generator Building - First Visit": GrinchLocationData("Generator Building", "Visitsanity", 110, [GrinchRamData(0x010000, value=0x0F)]),
        "Who Lake's South Shore- First Visit": GrinchLocationData("Who Lake", "Visitsanity", 111, [GrinchRamData(0x010000, value=0x12)]),
        "Who Lake's Submarine World - First Visit": GrinchLocationData("Submarine World", "Visitsanity", 112, [GrinchRamData(0x010000, value=0x17)]),
        "Who Lake's Scout's Hut - First Visit": GrinchLocationData("Scout's Hut", "Visitsanity", 113, [GrinchRamData(0x010000, value=0x13)]),
        "Who Lake's North Shore - First Visit": GrinchLocationData("North Shore", "Visitsanity", 114, [GrinchRamData(0x010000, value=0x14)]),
        "Who Lake's Mayor's Villa - First Visit": GrinchLocationData("Mayor's Villa", "Visitsanity", 115, [GrinchRamData(0x010000, value=0x16)]),
#Need to find mission completion address for handful of locations that are not documented.
#Missions that have value are those ones we need to find the check for
#Whoville Missions
        "Whoville's Post Office - Shuffling The Mail": GrinchLocationData("Post Office", "Whoville Missions", 201, [GrinchRamData(0x0100BE, binary_bit_pos=0)]),
        "Whoville - Smashing Snowmen": GrinchLocationData("Whoville", "Whoville Missions", 200, [GrinchRamData(0x0100C5, value=10)]),
        "Whoville - Painting The Mayor's Posters": GrinchLocationData("Whoville", "Whoville Missions", 202, [GrinchRamData(0x0100C6, value=10)]),
        "Whoville - Launching Eggs Into Houses": GrinchLocationData("Whoville", "Whoville Missions", 203, [GrinchRamData(0x0100C7, value=10)]),
        "Whoville's City Hall - Modifying The Mayor's Statue": GrinchLocationData("City Hall", "Whoville Missions", 204, [GrinchRamData(0x0100BE, binary_bit_pos=1)]),
        "Whoville's Clock Tower - Advancing The Countdown-To-Xmas Clock": GrinchLocationData("Clock Tower", "Whoville Missions", 205, [GrinchRamData(0x0100BE, binary_bit_pos=2)]),
        "Whoville - Squashing All Gifts": GrinchLocationData("Whoville", "Whoville Missions", 206, [GrinchRamData(0x01005C, value=500, bit_size=2)]),
#Who Forest Missions
        "Who Forest - Making Xmas Trees Droop": GrinchLocationData("Who Forest", "Who Forest Missions", 300, [GrinchRamData(0x0100C8, value=10)]),
        "Who Forest - Sabotaging Snow Cannon With Glue": GrinchLocationData("Who Forest", "Who Forest Missions", 301, [GrinchRamData(0x0100BE, binary_bit_pos=3)]),
        "Who Forest - Putting Beehives In Cabins": GrinchLocationData("Who Forest", "Who Forest Missions", 302, [GrinchRamData(0x0100CA, value=10)]),
        "Who Forest's Ski Resort - Sliming The Mayor's Skis": GrinchLocationData("Ski Resort", "Who Forest Missions", 303, [GrinchRamData(0x0100BE, binary_bit_pos=4)]),
        "Who Forest's Civic Center - Replacing The Candles On The Cake With Fireworks": GrinchLocationData("Civic Center", "Who Forest Missions", 304, [GrinchRamData(0x0100BE, binary_bit_pos=5)]),
        "Who Forest - Squashing All Gifts": GrinchLocationData("Who Forest", "Who Forest Missions", 305, [GrinchRamData(0x01005E, value=750, bit_size=2)]),
#Who Dump Missions
        "Who Dump - Stealing Food From Birds": GrinchLocationData("Who Dump", "Who Dump Missions", 400, [GrinchRamData(0x0100CB, value=10)]),
        "Who Dump - Feeding The Computer With Robot Parts": GrinchLocationData("Who Dump", "Who Dump Missions", 401, [GrinchRamData(0x0100BF, binary_bit_pos=2)]),
        "Who Dump - Infesting The Mayor's House With Rats": GrinchLocationData("Who Dump", "Who Dump Missions", 402, [GrinchRamData(0x0100BE, binary_bit_pos=6)]),
        "Who Dump - Conducting The Stinky Gas To Who-Bris' Shack": GrinchLocationData("Who Dump", "Who Dump Missions", 403, [GrinchRamData(0x0100BE, binary_bit_pos=7)]),
        "Who Dump's Minefield - Shaving Who Dump Guardian": GrinchLocationData("Minefield", "Who Dump Missions", 404, [GrinchRamData(0x0100BF, binary_bit_pos=0)]),
        "Who Dump's Generator Building - Short-Circuiting Power-Plant": GrinchLocationData("Generator Building", "Who Dump Missions", 405, [GrinchRamData(0x0100BF, binary_bit_pos=1)]),
        "Who Dump - Squashing All Gifts": GrinchLocationData("Who Dump", "Who Dump Missions", 406, [GrinchRamData(0x010060, value=750, bit_size=2)]),
#Who Lake Missions
        "Who Lake's South Shore - Putting Thistles In Shorts": GrinchLocationData("Who Lake", "Who Lake Missions", 500, [GrinchRamData(0x0100E5, value=10)]),
        "Who Lake's South Shore - Sabotaging The Tents": GrinchLocationData("Who Lake", "Who Lake Missions", 501, [GrinchRamData(0x0100E6, value=10)]),
        "Who Lake's North Shore - Drilling Holes In Canoes": GrinchLocationData("North Shore", "Who Lake Missions", 502, [GrinchRamData(0x0100EE, value=10)]),
        "Who Lake's Submarine World - Modifying The Marine Mobile": GrinchLocationData("Submarine World", "Who Lake Missions", 503, [GrinchRamData(0x0100BF, binary_bit_pos=4)]),
        "Who Lake's Mayor's Villa - Hooking The Mayor's Bed To The Motorboat": GrinchLocationData("Mayor's Villa", "Who Lake Missions", 504, [GrinchRamData(0x0100BF, binary_bit_pos=3)]),
        "Who Lake - Squashing All Gifts": GrinchLocationData("Who Lake", "Who Lake Missions", 505, [GrinchRamData(0x010062, value=1000, bit_size=2)]),
#Need to find binary values for individual blueprints, but all ram addresses are found
#Blueprints
#Binoculars Blueprints
        "Whoville - Binoculars Blueprint on Post Office Roof": GrinchLocationData("Whoville", "Binocular Blueprints", 600, [GrinchRamData(0x01020B, binary_bit_pos=2)]),
        "Whoville's City Hall - Binoculars Blueprint left side of Library": GrinchLocationData("City Hall", "Binocular Blueprints", 601, [GrinchRamData(0x01021F, binary_bit_pos=6)]),
        "Whoville's City Hall - Binoculars Blueprint front side of Library": GrinchLocationData("City Hall", "Binocular Blueprints", 602, [GrinchRamData(0x01021F, binary_bit_pos=5)]),
        "Whoville's City Hall - Binoculars Blueprint right side of Library": GrinchLocationData("City Hall", "Binocular Blueprints", 603, [GrinchRamData(0x01021F, binary_bit_pos=4)]),
#Rotten Egg Launcher Blueprints
        "Whoville - REL Blueprint left of City Hall": GrinchLocationData("Whoville", "Rotten Egg Launcher Blueprints", 700, [GrinchRamData(0x01020B, binary_bit_pos=0)]),
        "Whoville - REL Blueprint left of Clock Tower": GrinchLocationData("Whoville", "Rotten Egg Launcher Blueprints", 701, [GrinchRamData(0x01020B, binary_bit_pos=1)]),
        "Whoville's Post Office - REL Blueprint inside Silver Room": GrinchLocationData("Post Office", "Rotten Egg Launcher Blueprints", 702, [GrinchRamData(0x01021C, binary_bit_pos=1)]),
        "Whoville's Post Office - REL Blueprint at Entrance Door after Mission Completion": GrinchLocationData("Post Office", "Rotten Egg Launcher Blueprints", 703, [GrinchRamData(0x01021C, binary_bit_pos=2)]),
#Rocket Spring Blueprints
        "Who Forest - RS Blueprint behind Vacuum Tube": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 800, [GrinchRamData(0x010243, binary_bit_pos=3)]),
        "Who Forest - RS Blueprint in front of 2nd House near Vacuum Tube": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 801, [GrinchRamData(0x010243, binary_bit_pos=1)]),
        "Who Forest - RS Blueprint near Tree House on Ground": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 802, [GrinchRamData(0x010243, binary_bit_pos=4)]),
        "Who Forest - RS Blueprint behind Cable Car House": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 804, [GrinchRamData(0x010242, binary_bit_pos=7)]),
        "Who Forest - RS Blueprint near Who Snowball in Cave": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 805, [GrinchRamData(0x010242, binary_bit_pos=6)]),
        "Who Forest - RS Blueprint on Branch Platform closest to Glue Cannon": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 806, [GrinchRamData(0x010243, binary_bit_pos=2)]),
        "Who Forest - RS Blueprint on Branch Platform Near Beast": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 807, [GrinchRamData(0x010243, binary_bit_pos=0)]),
        "Who Forest - RS Blueprint on Branch Platform Elevated next to House": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 808, [GrinchRamData(0x010243, binary_bit_pos=6)]),
        "Who Forest - RS Blueprint on Tree House": GrinchLocationData("Who Forest", "Rocket Spring Blueprints", 809, [GrinchRamData(0x010243, binary_bit_pos=5)]),
#Slime Shooter Blueprints
        "Who Forest - SS Blueprint in Branch Platform Elevated House": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 900, [GrinchRamData(0x010244, binary_bit_pos=3)]),
        "Who Forest - SS Blueprint in Branch Platform House next to Beast": GrinchLocationData("Who Forest", "Slime Shooter Blueprint", 901, [GrinchRamData(0x010243, binary_bit_pos=7)]),
        "Who Forest - SS Blueprint in House in front of Civic Center Cave": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 902, [GrinchRamData(0x010244, binary_bit_pos=2)]),
        "Who Forest - SS Blueprint in House next to Tree House": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 903, [GrinchRamData(0x010244, binary_bit_pos=1)]),
        "Who Forest - SS Blueprint in House across from Tree House": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 904, [GrinchRamData(0x010244, binary_bit_pos=5)]),
        "Who Forest - SS Blueprint in 2nd House near Vacuum Tube Right Side": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 905, [GrinchRamData(0x010244, binary_bit_pos=4)]),
        "Who Forest - SS Blueprint in 2nd House near Vacuum Tube Left Side": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 906, [GrinchRamData(0x010244, binary_bit_pos=7)]),
        "Who Forest - SS Blueprint in 2nd House near Vacuum Tube inbetween Blueprints": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 907, [GrinchRamData(0x010244, binary_bit_pos=6)]),
        "Who Forest - SS Blueprint in House near Vacuum Tube": GrinchLocationData("Who Forest", "Slime Shooter Blueprints", 908, [GrinchRamData(0x010244, binary_bit_pos=0)]),
#Octopus Climbing Device
        "Who Dump - OCD Blueprint inside Middle Pipe": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1001, [GrinchRamData(0x010252, binary_bit_pos=3)]),
        "Who Dump - OCD Blueprint inside Right Pipe": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1002, [GrinchRamData(0x010252, binary_bit_pos=5)]),
        "Who Dump - OCD Blueprint in Vent to Mayor's House": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1003, [GrinchRamData(0x010252, binary_bit_pos=1)]),
        "Who Dump - OCD Blueprint inside Left Pipe": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1004, [GrinchRamData(0x010252, binary_bit_pos=4)]),
        "Who Dump - OCD Blueprint near Right Side of Power Plant Wall": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1005, [GrinchRamData(0x010252, binary_bit_pos=0)]),
        "Who Dump - OCD Blueprint near Who-Bris' Shack": GrinchLocationData("Who Dump", "Octopus Climbing Device Blueprints", 1006, [GrinchRamData(0x010252, binary_bit_pos=2)]),
        "Who Dump's Minefield - OCD Blueprint on Left Side of House": GrinchLocationData("Minefield", "Octopus Climbing Device Blueprints", 1007, [GrinchRamData(0x01026E, binary_bit_pos=2)]),
        "Who Dump's Minefield - OCD Blueprint on Right Side of Shack": GrinchLocationData("Minefield", "Octopus Climbing Device Blueprints", 1008, [GrinchRamData(0x01026E, binary_bit_pos=4)]),
        "Who Dump's Minefield - OCD Blueprint inside Guardian's House": GrinchLocationData("Minefield", "Octopus Climbing Device Blueprints", 1009, [GrinchRamData(0x01026E, binary_bit_pos=3)]),
#Marine Mobile Blueprints
        "Who Lake's South Shore - MM Blueprint on Bridge to Scout's Hut": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1100, [GrinchRamData(0x010281, binary_bit_pos=5)]),
        "Who Lake's South Shore - MM Blueprint across from Tent near Porcupine": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1101, [GrinchRamData(0x010281, binary_bit_pos=6)]),
        "Who Lake's South Shore - MM Blueprint near Outhouse": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1102, [GrinchRamData(0x010281, binary_bit_pos=7)]),
        "Who Lake's South Shore - MM Blueprint near Hill Bridge": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1103, [GrinchRamData(0x010282, binary_bit_pos=0)]),
        "Who Lake's South Shore - MM Blueprint on Scout's Hut Roof": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1104, [GrinchRamData(0x010281, binary_bit_pos=4)]),
        "Who Lake's South Shore - MM Blueprint on Grass Platform": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1105, [GrinchRamData(0x010281, binary_bit_pos=2)]),
        "Who Lake's South Shore - MM Blueprint across Zipline Platform": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1106, [GrinchRamData(0x010281, binary_bit_pos=3)]),
        "Who Lake's South Shore - MM Blueprint behind Summer Beast": GrinchLocationData("Who Lake", "Marine Mobile Blueprints", 1107, [GrinchRamData(0x010282, binary_bit_pos=1)]),
        "Who Lake's North Shore - MM Blueprint below Bridge": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1108, [GrinchRamData(0x010293, binary_bit_pos=0)]),
        "Who Lake's North Shore - MM Blueprint behind Skunk Hut": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1109, [GrinchRamData(0x010293, binary_bit_pos=2)]),
        "Who Lake's North Shore - MM Blueprint inside Skunk Hut": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1110, [GrinchRamData(0x010292, binary_bit_pos=6)]),
        "Who Lake's North Shore - MM Blueprint inside House's Fence": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1111, [GrinchRamData(0x010292, binary_bit_pos=7)]),
        "Who Lake's North Shore - MM Blueprint inside Boulder Box near Bridge": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1112, [GrinchRamData(0x010293, binary_bit_pos=3)]),
        "Who Lake's North Shore - MM Blueprint inside Boulder Box behind Skunk Hut": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1113, [GrinchRamData(0x010293, binary_bit_pos=4)]),
        "Who Lake's North Shore - MM Blueprint inside Drill House": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1114, [GrinchRamData(0x010292, binary_bit_pos=5)]),
        "Who Lake's North Shore - MM Blueprint on Crow Platform near Drill House": GrinchLocationData("North Shore", "Marine Mobile Blueprints", 1115, [GrinchRamData(0x010293, binary_bit_pos=1)]),
        #Grinch Copter Blueprints
        "Whoville's City Hall - GC Blueprint in Safe Room": GrinchLocationData("City Hall", "Grinch Copter Blueprints", 1200, [GrinchRamData(0x01021F, binary_bit_pos=7)]),
        "Whoville's City Hall - GC Blueprint in Statue Room": GrinchLocationData("City Hall", "Grinch Copter Blueprints", 1201, [GrinchRamData(0x010220, binary_bit_pos=0)]),
        "Whoville's Clock Tower - GC Blueprint in Bedroom": GrinchLocationData("Clock Tower", "Grinch Copter Blueprints", 1202, [GrinchRamData(0x010216, binary_bit_pos=3)]),
        "Whoville's Clock Tower - GC Blueprint in Bell Room": GrinchLocationData("Clock Tower", "Grinch Copter Blueprints", 1203, [GrinchRamData(0x010216, binary_bit_pos=2)]),
        "Who Forest's Ski Resort - GC Blueprint inside Dog's Fence": GrinchLocationData("Ski Resort", "Grinch Copter Blueprints", 1204, [GrinchRamData(0x010234, binary_bit_pos=7)]),
        "Who Forest's Ski Resort - GC Blueprint in Max Cave": GrinchLocationData("Ski Resort", "Grinch Copter Blueprints", 1205, [GrinchRamData(0x010234, binary_bit_pos=6)]),
        "Who Forest's Civic Center - GC Blueprint on Left Side in Bat Cave Wall": GrinchLocationData("Civic Center", "Grinch Copter Blueprints", 1206, [GrinchRamData(0x01022A, binary_bit_pos=7)]),
        "Who Forest's Civic Center - GC Blueprint in Frozen Ice": GrinchLocationData("Civic Center", "Grinch Copter Blueprints", 1207, [GrinchRamData(0x01022B, binary_bit_pos=0)]),
        "Who Dump's Power Plant - GC Blueprint in Max Cave": GrinchLocationData("Power Plant", "Grinch Copter Blueprints", 1208, [GrinchRamData(0x010265, binary_bit_pos=1)]),
        "Who Dump's Power Plant - GC Blueprint After First Gate": GrinchLocationData("Power Plant", "Grinch Copter Blueprints", 1209, [GrinchRamData(0x010265, binary_bit_pos=2)]),
        "Who Dump's Generator Building - GC Blueprint on the Highest Platform": GrinchLocationData("Generator Building", "Grinch Copter Blueprints", 1210, [GrinchRamData(0x01026B, binary_bit_pos=0)]),
        "Who Dump's Generator Building - GC Blueprint at the Entrance after Mission Completion": GrinchLocationData("Generator Building", "Grinch Copter Blueprints", 1211, [GrinchRamData(0x01026B, binary_bit_pos=1)]),
        "Who Lake's Submarine World - GC Blueprint Just Below Water Surface": GrinchLocationData("Submarine World", "Grinch Copter Blueprints", 1212, [GrinchRamData(0x010289, binary_bit_pos=3)]),
        "Who Lake's Submarine World - GC Blueprint Underwater": GrinchLocationData("Submarine World", "Grinch Copter Blueprints", 1213, [GrinchRamData(0x010289, binary_bit_pos=4)]),
        "Who Lake's Mayor's Villa - GC Blueprint on Tree Branch": GrinchLocationData("Mayor's Villa", "Grinch Copter Blueprints", 1214, [GrinchRamData(0x010275, binary_bit_pos=7)]),
        "Who Lake's Mayor's Villa - GC Blueprint in Pirate's Cave": GrinchLocationData("Mayor's Villa", "Grinch Copter Blueprints", 1215, [GrinchRamData(0x010275, binary_bit_pos=6)]),
#Sleigh Room Locations
        "Mount Crumpit's Sleigh Ride - Stealing All Gifts": GrinchLocationData("Sleigh Room", "Sleigh Ride", 1300, [GrinchRamData(0x0100BF, binary_bit_pos=6)]),
        "Mount Crumpit's Sleigh Ride - Neutralizing Santa": GrinchLocationData("Sleigh Room", "Sleigh Ride", None, [GrinchRamData(0x0100BF, binary_bit_pos=7)]),
#Heart of Stones
        "Whoville's Post Office - Heart of Stone": GrinchLocationData("Post Office", "Heart of Stones", 1400, [GrinchRamData(0x0101FA, binary_bit_pos=6)]),
        "Who Forest's Ski Resort - Heart of Stone": GrinchLocationData("Ski Resort", "Heart of Stones", 1401, [GrinchRamData(0x0101FA, binary_bit_pos=7)]),
        "Who Dump's Minefield - Heart of Stone": GrinchLocationData("Minefield", "Heart of Stones", 1402, [GrinchRamData(0x0101FB, binary_bit_pos=0)]),
        "Who Lake's North Shore - Heart of Stone": GrinchLocationData("North Shore", "Heart of Stones", 1403, [GrinchRamData(0x0101FB, binary_bit_pos=1)]),
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
        "Whoville - Exhaust Pipes": GrinchLocationData("Sleigh Room", "Sleigh Ride", 1600, [GrinchRamData(0x0101FB, binary_bit_pos=2)]),
        "Who Forest - Skis": GrinchLocationData("Sleigh Room", "Sleigh Ride", 1601, [GrinchRamData(0x0101FB, binary_bit_pos=3)]),
        "Who Dump - Tires": GrinchLocationData("Sleigh Room", "Sleigh Ride", 1602, [GrinchRamData(0x0101FB, binary_bit_pos=4)]),
        "Who Lake's Submarine World - Twin-End Tuba": GrinchLocationData("Sleigh Room", "Sleigh Ride", 1603, [GrinchRamData(0x0101FB, binary_bit_pos=6)]),
        "Who Lake's South Shore - GPS": GrinchLocationData("Sleigh Room", "Sleigh Ride", 1604, [GrinchRamData(0x0101FB, binary_bit_pos=5)]),
# Mount Crumpit Locations
        "Mount Crumpit - 1st Crate Squashed": GrinchLocationData("Mount Crumpit", "Mount Crumpit", 1700, [GrinchRamData(0x095343, value=1)]),
        "Mount Crumpit - 2nd Crate Squashed": GrinchLocationData("Mount Crumpit", "Mount Crumpit", 1701, [GrinchRamData(0x095343, value=2)]),
        "Mount Crumpit - 3rd Crate Squashed": GrinchLocationData("Mount Crumpit", "Mount Crumpit", 1702, [GrinchRamData(0x095343, value=3)]),
        "Mount Crumpit - 4th Crate Squashed": GrinchLocationData("Mount Crumpit", "Mount Crumpit", 1703, [GrinchRamData(0x095343, value=4)]),
        "Mount Crumpit - 5th Crate Squashed": GrinchLocationData("Mount Crumpit", "Mount Crumpit", 1704, [GrinchRamData(0x095343, value=5)]),
}

def grinch_locations_to_id() -> dict[str,int]:
    location_mappings: dict[str, int] = {}
    for LocationName, LocationData in grinch_locations.items():
        location_mappings.update({LocationName: GrinchLocation.get_apid(LocationData.id)})
    return location_mappings