import typing
from BaseClasses import Item, Location, Tutorial
from worlds.AutoWorld import World, WebWorld

client_version = 0

class DLCqwebworld(WebWorld):
    tutorials = [Tutorial(
        "magic it is "
    )]

class DLCqworld(World):
    """
    DLCquest is a metroid ish game where everything is an in-game dlc.
    """
    game: str = "DLCquest"
    topology_present = False
    web = DLCqwebworld
