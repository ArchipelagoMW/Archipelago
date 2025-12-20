import typing

from BaseClasses import MultiWorld
from test.bases import WorldTestBase
from worlds.legend_of_dragoon import LegendOfDragoonWorld
from worlds import AutoWorld
from worlds.AutoWorld import World, call_all

from BaseClasses import Location, MultiWorld, CollectionState, Item

class LegendOfDragoonTestBase(WorldTestBase):
    game = "The Legend of Dragoon"
    world = LegendOfDragoonWorld