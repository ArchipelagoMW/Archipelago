from typing import Any, Dict

from .options import *

witness_option_presets: Dict[str, Dict[str, Any]] = {
    # Great for short syncs & scratching that "speedrun with light routing elements" itch.
    "Short & Dense": {
        "progression_balancing": 30,

        "puzzle_randomization": PuzzleRandomization.option_sigma_normal,

        "shuffle_symbols": False,
        "shuffle_doors": ShuffleDoors.option_panels,
        "door_groupings": DoorGroupings.option_off,
        "shuffle_boat": True,
        "shuffle_lasers": ShuffleLasers.option_local,
        "obelisk_keys": ObeliskKeys.option_false,

        "disable_non_randomized_puzzles": True,
        "shuffle_discarded_panels": False,
        "shuffle_vault_boxes": False,
        "shuffle_EPs": ShuffleEnvironmentalPuzzles.option_off,
        "EP_difficulty": EnvironmentalPuzzlesDifficulty.option_normal,
        "shuffle_postgame": False,

        "victory_condition": VictoryCondition.option_mountain_box_short,
        "mountain_lasers": 7,
        "challenge_lasers": 11,

        "early_caves": EarlyCaves.option_off,
        "elevators_come_to_you": False,

        "trap_percentage": TrapPercentage.default,
        "puzzle_skip_amount": PuzzleSkipAmount.default,
        "hint_amount": HintAmount.default,
        "area_hint_percentage": AreaHintPercentage.default,
        "laser_hints": LaserHints.default,
        "death_link": DeathLink.default,
        "death_link_amnesty": DeathLinkAmnesty.default,
    },

    # For relative beginners who want to move to the next step.
    "Advanced, But Chill": {
        "progression_balancing": 30,

        "puzzle_randomization": PuzzleRandomization.option_sigma_normal,

        "shuffle_symbols": True,
        "shuffle_doors": ShuffleDoors.option_doors,
        "door_groupings": DoorGroupings.option_regional,
        "shuffle_boat": True,
        "shuffle_lasers": ShuffleLasers.option_off,
        "obelisk_keys": ObeliskKeys.option_false,

        "disable_non_randomized_puzzles": False,
        "shuffle_discarded_panels": True,
        "shuffle_vault_boxes": True,
        "shuffle_EPs": ShuffleEnvironmentalPuzzles.option_obelisk_sides,
        "EP_difficulty": EnvironmentalPuzzlesDifficulty.option_normal,
        "shuffle_postgame": False,

        "victory_condition": VictoryCondition.option_mountain_box_long,
        "mountain_lasers": 6,
        "challenge_lasers": 9,

        "early_caves": EarlyCaves.option_off,
        "elevators_come_to_you": False,

        "trap_percentage": TrapPercentage.default,
        "puzzle_skip_amount": 15,
        "hint_amount": HintAmount.default,
        "area_hint_percentage": AreaHintPercentage.default,
        "laser_hints": LaserHints.default,
        "death_link": DeathLink.default,
        "death_link_amnesty": DeathLinkAmnesty.default,
    },

    # Allsanity but without the BS (no expert, no tedious EPs).
    "Nice Allsanity": {
        "progression_balancing": 50,

        "puzzle_randomization": PuzzleRandomization.option_sigma_normal,

        "shuffle_symbols": True,
        "shuffle_doors": ShuffleDoors.option_mixed,
        "door_groupings": DoorGroupings.option_off,
        "shuffle_boat": True,
        "shuffle_lasers": ShuffleLasers.option_anywhere,
        "obelisk_keys": ObeliskKeys.option_true,

        "disable_non_randomized_puzzles": False,
        "shuffle_discarded_panels": True,
        "shuffle_vault_boxes": True,
        "shuffle_EPs": ShuffleEnvironmentalPuzzles.option_individual,
        "EP_difficulty": EnvironmentalPuzzlesDifficulty.option_normal,
        "shuffle_postgame": False,

        "victory_condition": VictoryCondition.option_challenge,
        "mountain_lasers": 6,
        "challenge_lasers": 9,

        "early_caves": EarlyCaves.option_off,
        "elevators_come_to_you": True,

        "trap_percentage": TrapPercentage.default,
        "puzzle_skip_amount": 15,
        "hint_amount": HintAmount.default,
        "area_hint_percentage": AreaHintPercentage.default,
        "laser_hints": LaserHints.default,
        "death_link": DeathLink.default,
        "death_link_amnesty": DeathLinkAmnesty.default,
    },
}
