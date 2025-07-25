from BaseClasses import Region, MultiWorld
from .Locations import GrinchLocation, grinch_locations
from .Options import GrinchOptions

def create_regions(player: int, world: World, options: GrinchOptions):
    mainareas_list = [
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
        "Mayor's Villa"
    ]