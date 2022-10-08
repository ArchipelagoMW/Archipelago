from typing import Dict, Union
from BaseClasses import MultiWorld
from Options import Option, Choice, DefaultOnToggle, Range, Toggle, DeathLink


class StageShuffle(Toggle):
    """Shuffles which stages appear in which stage slots. Villa and Castle Center cannot appear in any character stage
    slots, only on the main path. Castle Keep will always be at the very end. See the FAQ for more details."""
    display_name = "Stage Shuffle"


class SubweaponShuffle(DefaultOnToggle):
    """Shuffles all the sub-weapons within their own pool."""
    display_name = "Sub-weapon Shuffle"


class Special1sPerWarp(Range):
    """Sets how many Special1 jewels are needed per warp menu option unlock."""
    range_start = 1
    range_end = 5
    default = 1
    display_name = "Special1 Jewels Per Warp"


class TotalSpecial1s(Range):
    """Sets how many Speical1 jewels are in the pool in total. This cannot be less than 'Special1 Jewels Per Warp' times
    7."""
    range_start = 1
    range_end = 40
    default = 7
    display_name = "Total Special1 Jewels"


class DraculasChamberCondition(Choice):
    """Sets the requirements for opening the door to Dracula's chamber."""
    display_name = "Dracula's Chamber Condition"
    option_none = 0
    option_crystal = 1
    option_bosses = 2
    option_specials = 3
    default = 1


class Special2sRequired(Range):
    """Sets how many Special2 jewels are needed to enter Dracula's chamber. Only applies if Dracula's Chamber Condition
    is set to Special2s."""
    range_start = 1
    range_end = 40
    default = 10
    display_name = "Special2 Jewels Required"


class TotalSpecial2s(Range):
    """Sets how many Speical2 jewels are in the pool in total. This cannot be less than 'Special2 Jewels Required'. Only
    applies if Dracula's Chamber Condition is set to Special2s."""
    range_start = 1
    range_end = 40
    default = 10
    display_name = "Total Special2 Jewels"


class CarrieLogic(Toggle):
    """If enabled, the two Underground Waterway checks inside the crawlspace will be included; otherwise, they'll be
    left vanilla. Can be combined with 'Glitch Logic' to include Carrie-only skips."""
    display_name = "Carrie Logic"


class GlitchLogic(Toggle):
    """If enabled, sequence break glitches will be properly considered in logic (i.e. Left Tower Skip). Can be combined
    with 'Carrie Logic' to include Carrie-only glitches."""
    display_name = "Glitch Logic"


class LizardGeneratorItems(Toggle):
    """If enabled, the checks inside the Lizard-man generators in Castle Center will be included; otherwise, they'll be
    left vanilla. WARNING: picking all of these up can be a very frustrating and time-consuming process!"""
    display_name = "Include Lizard-man Generator Items"


class FightRenon(Choice):
    """Sets the condition on which the Renon fight will trigger.
    Vanilla = after spending more than 30,000 gold in his shop."""
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
    """Sets the condition on which the currently-controlled character's Bad Ending will trigger.
    Vanilla = after defeating vampire Vincent."""
    display_name = "Bad Ending Condition"
    option_never = 0
    option_vanilla = 1
    option_always = 2
    default = 1


class IncreaseItemLimit(DefaultOnToggle):
    """If enabled, the use item-holding limit will be increased from 10 to 99 of each item."""
    display_name = "Increase Item Limit"


class RevealInvisibleItems(DefaultOnToggle):
    """If enabled, all invisible pickups will be made visible."""
    display_name = "Reveal Invisible Items"


cv64_options: Dict[str, Option] = {
    "stage_shuffle": StageShuffle,
    "subweapon_shuffle": SubweaponShuffle,
    "special1s_per_warp": Special1sPerWarp,
    "total_special1s": TotalSpecial1s,
    "draculas_condition": DraculasChamberCondition,
    "special2s_required": Special2sRequired,
    "total_special2s": TotalSpecial2s,
    "carrie_logic": CarrieLogic,
    "glitch_logic": GlitchLogic,
    "lizard_generator_items": LizardGeneratorItems,
    "fight_renon": FightRenon,
    "fight_vincent": FightVincent,
    "bad_ending_condition": BadEndingCondition,
    "increase_item_limit": IncreaseItemLimit,
    "reveal_invisible_items": RevealInvisibleItems,
    "death_link": DeathLink,
}
