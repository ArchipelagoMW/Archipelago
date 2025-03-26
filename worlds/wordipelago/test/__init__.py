from typing import Any, ClassVar, Dict, Iterable, List, Mapping, Union

from BaseClasses import CollectionState, Entrance, Item, Location, Region

from test.bases import WorldTestBase
from test.general import gen_steps, setup_multiworld
from test.multiworld.test_multiworlds import MultiworldTestBase

from .. import WordipelagoWorld


class WordipelagoTestBase(WorldTestBase):
    game = "Wordipelago"
    world: WordipelagoWorld