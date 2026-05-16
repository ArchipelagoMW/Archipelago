from .bases import BabaIsYouTestBase

from ..levels import LEVEL_DATA

from BaseClasses import CollectionState

class TestBlossoms(BabaIsYouTestBase):
    options = {
        "goal": 0,
        "force_clear_blossoms": False,
        "blossom_petals": 8,
        "blossoms": 10,
        "first_gate_blossoms": 6,
        "second_gate_blossoms": 6,
        "third_gate_blossoms": 6,
    }