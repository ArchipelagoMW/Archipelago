from BaseClasses import Region, MultiWorld
from .Locations import GrinchLocation, grinch_locations
from .Options import GrinchOptions

mainareas_list = [
    "Mount Crumpit",
    "Whoville",
    "Who Forest",
    "Who Dump",
    "Who Lake"
]

subareas_list = [
    "Post Office",
    "City Hall",
    "Countdown to X-Mas Tower",
    "Ski Resort",
    "Civic Center",
    "Minefield",
    "Outside Power Plant",
    "Inside Power Plant",
    "Submarine World",
    "Scout's Hut",
    "North Shore",
    "Mayor's Villa",
    "Sleigh Room"
]

supadow_list = [
    "Spin N' Win Supadow",
    "Dankamania Supadow",
    "The Copter Race Contest Supadow"
]
def create_regions(player: int, world: World, options: GrinchOptions):
