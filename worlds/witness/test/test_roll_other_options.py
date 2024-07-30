from ..test import WitnessTestBase

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
    }


class TestVanillaAutoElevatorsPanels(WitnessTestBase):
    options = {
        "puzzle_randomization": "none",
        "elevators_come_to_you": True,
        "shuffle_doors": "panels",
        "victory_condition": "mountain_box_short",
        "early_caves": True,
        "shuffle_vault_boxes": True,
        "mountain_lasers": 11,
    }


class TestMiscOptions(WitnessTestBase):
    options = {
        "death_link": True,
        "death_link_amnesty": 3,
        "laser_hints": True,
        "hint_amount": 40,
        "area_hint_percentage": 100,
    }


class TestMaxEntityShuffle(WitnessTestBase):
    options = {
        "shuffle_symbols": False,
        "shuffle_doors": "mixed",
        "shuffle_EPs": "individual",
        "obelisk_keys": True,
        "shuffle_lasers": "anywhere",
        "victory_condition": "mountain_box_long",
    }


class TestPostgameGroupedDoors(WitnessTestBase):
    options = {
        "shuffle_postgame": True,
        "shuffle_discarded_panels": True,
        "shuffle_doors": "doors",
        "door_groupings": "regional",
        "victory_condition": "elevator",
    }
