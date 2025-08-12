from ..options import ElevatorsComeToYou
from ..test.bases import WitnessTestBase

# These are just some random options combinations, just to catch whether I broke anything obvious


class TestExpertNonRandomizedEPs(WitnessTestBase):
    options = {
        "disable_non_randomized": True,
        "puzzle_randomization": "sigma_expert",
        "shuffle_EPs": "individual",
        "ep_difficulty": "eclipse",
        "victory_condition": "challenge",
        "shuffle_discarded_panels": False,
        "shuffle_boat": False,
        "shuffle_dog": "off",
    }


class TestVanillaAutoElevatorsPanels(WitnessTestBase):
    options = {
        "puzzle_randomization": "none",
        "elevators_come_to_you": ElevatorsComeToYou.valid_keys - ElevatorsComeToYou.default,  # Opposite of default
        "shuffle_doors": "panels",
        "victory_condition": "mountain_box_short",
        "early_caves": True,
        "shuffle_vault_boxes": True,
        "mountain_lasers": 11,
        "shuffle_dog": "puzzle_skip",
    }


class TestMiscOptions(WitnessTestBase):
    options = {
        "death_link": True,
        "death_link_amnesty": 3,
        "laser_hints": True,
        "hint_amount": 40,
        "area_hint_percentage": 100,
        "vague_hints": "experimental",
    }


class TestMaxEntityShuffle(WitnessTestBase):
    options = {
        "shuffle_symbols": False,
        "shuffle_doors": "mixed",
        "shuffle_EPs": "individual",
        "obelisk_keys": True,
        "shuffle_lasers": "anywhere",
        "victory_condition": "mountain_box_long",
        "shuffle_dog": "random_item",
    }


class TestPostgameGroupedDoors(WitnessTestBase):
    options = {
        "puzzle_randomization": "umbra_variety",
        "shuffle_postgame": True,
        "shuffle_discarded_panels": True,
        "shuffle_doors": "doors",
        "door_groupings": "regional",
        "victory_condition": "elevator",
    }


class TestPostgamePanels(WitnessTestBase):
    options = {
        "victory_condition": "mountain_box_long",
        "shuffle_postgame": True
    }
