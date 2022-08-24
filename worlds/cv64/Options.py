from typing import Dict, Union
from BaseClasses import MultiWorld
from Options import Option, Choice, DefaultOnToggle, Range, Toggle, DeathLink


class IncreaseItemLimit(DefaultOnToggle):
    """If enabled, the use item-holding limit will be increased from 10 to 99 of each item."""
    display_name = "Increase Item Limit"


class RevealInvisibleItems(DefaultOnToggle):
    """If enabled, all invisible pickup items will be made visible."""
    display_name = "Reveal Invisible Items"


class StartLocation(Choice):
    """Sets the player's starting location."""
    display_name = "Start Location"
    option_forest = 0
    option_villa = 1
    option_cc = 2
    option_random_stage = 3
    option_random_map = 4


class StageShuffle(Toggle):
    """Shuffles the order the stages link up in. The Villa coffin can send you to one of two stages depending on the
    time of day, and both Castle Center elevator bridges are intact for both characters and also lead to different
    places regardless of the chosen character or setting."""
    display_name = "Stage Shuffle"


class DraculasChamberCondition(Choice):
    """Sets the requirements for opening the door to Dracula's chamber."""
    display_name = "Dracula's Chamber Condition"
    option_none = 0
    option_crystal = 1
    option_bosses = 2
    option_specials = 3
    default = 1


class FightRenon(Choice):
    """Sets the condition on which the Renon fight will trigger.
    Vanilla = after spending 30,000 gold in his shop."""
    display_name = "Fight Renon"
    option_never = 0
    option_vanilla = 1
    option_always = 2
    default = 1


class FightVincent(Choice):
    """Sets the condition on which the vampire Vincent fight will trigger.
    Vanilla = after 16 or more in-game days pass."""
    display_name = "Fight Vincent"
    option_never = 0
    option_vanilla = 1
    option_always = 2
    default = 1


class BadEndingCondition(Choice):
    """Sets the condition on which the bad ending will trigger.
    Vanilla = if vampire Vincent was fought."""
    display_name = "Bad Ending Condition"
    option_never = 0
    option_vanilla = 1
    option_always = 2
    default = 1


class NumberOfStages(Range):
    """Sets how many stages are included besides Castle Keep."""
    range_start = 1
    range_end = 13
    default = 10
    display_name = "Number of Stages"


class Special2sPerWarp(Range):
    """Sets how many Special2s are needed per warp menu option unlock."""
    range_start = 0
    range_end = 9
    default = 5
    display_name = "Special2s Per Warp"


class ExtraSpecial2s(Range):
    """Sets how many extra Speical2s are in the pool in addition to what's needed to select every warp destination."""
    range_start = 0
    range_end = 20
    default = 10
    display_name = "Extra Special2s"


class Special1sRequired(Range):
    """Sets how many Special1s are needed to enter Dracula's chamber (if Dracula's Chamber Condition is set to
    Special1s)."""
    range_start = 0
    range_end = 50
    default = 10
    display_name = "Special1s Required"


class ExtraSpecial1s(Range):
    """Sets how many extra Speical1s are in the pool in addition to what's needed to enter Dracula's chamber."""
    range_start = 0
    range_end = 13
    default = 10
    display_name = "Extra Special1s"


class CarrieLogic(Toggle):
    """If enabled, the two Underground Waterway checks beyond the crawlspace will be included; otherwise, they'll be
    left vanilla. Can be combined with Glitch Logic to include Carrie-only glitches."""
    display_name = "Carrie Logic"


class GlitchLogic(Toggle):
    """If enabled, sequence break glitches will be properly considered in logic (i.e. Left Tower Skip). Can be combined
    with Carrie Logic to include Carrie-only glitches."""
    display_name = "Glitch Logic"


cv64_options: Dict[str, Option] = {
    "number_of_stages": NumberOfStages,
    "start_location": StartLocation,
    "stage_shuffle": StageShuffle,
    "special2s_per_warp": Special2sPerWarp,
    "extra_special2s": ExtraSpecial2s,
    "draculas_condition": DraculasChamberCondition,
    "special1s_required": Special1sRequired,
    "extra_special1s": ExtraSpecial1s,
    "carrie_logic": CarrieLogic,
    "glitch_logic": GlitchLogic,
    "fight_renon": FightRenon,
    "fight_vincent": FightVincent,
    "bad_ending_condition": BadEndingCondition,
    "increase_item_limit": IncreaseItemLimit,
    "reveal_invisible_items": RevealInvisibleItems,
    "death_link": DeathLink,
}


#def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
#    return get_option_value(world, player, name) > 0


#def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, dict]:
#    option = getattr(world, name, None)
#    if option is None:
#        return 0

#    return option[player].value
