from typing import Dict
from Options import Option, Choice, DefaultOnToggle, Range, Toggle, DeathLink


class CharacterStages(Choice):
    """Whether to include Reinhardt-only stages, Carrie-only stages, or both."""
    display_name = "Character Stages"
    option_both = 0
    option_both_no_branches = 1
    option_reinhardt_only = 2
    option_carrie_only = 3
    default = 0


class StageShuffle(Toggle):
    """Shuffles which stages appear in which stage slots. Villa and Castle Center will never appear in any character
    stage slots if all character stages are included; they can only be somewhere on the main path.
    Castle Keep will always be at the end of the line."""
    display_name = "Stage Shuffle"


class WarpShuffle(Choice):
    """Shuffles the order of the stages on the warp menu and thus the order they're unlocked in. Vanilla gives a warp
    list resembling the vanilla game's stage order even if the seed's stage order is shuffled."""
    display_name = "Warp Shuffle"
    option_off = 0
    option_on = 1
    option_vanilla = 2
    default = 0


class SubWeaponShuffle(Choice):
    """Shuffles all sub-weapons in the game within their own pool or in the main item pool (keeping them local or
    allowing them to be anywhere)."""
    display_name = "Sub-weapon Shuffle"
    option_off = 0
    option_own_pool = 1
    option_own_world = 2
    option_any_world = 3
    default = 0


class ExtraKeys(Choice):
    """Puts an additional copy of every key item in the pool for every key item that there is to ensure fewer specific
    locations are required. Chance gives each key item a 50% chance of having a duplicate instead of guaranteeing one
    for all of them."""
    display_name = "Extra Keys"
    option_off = 0
    option_on = 1
    option_chance = 2
    default = 0


class Special1sPerWarp(Range):
    """Sets how many Special1 jewels are needed per warp menu option unlock."""
    range_start = 1
    range_end = 10
    default = 1
    display_name = "Special1 Jewels Per Warp"


class TotalSpecial1s(Range):
    """Sets how many Speical1 jewels are in the pool in total. This cannot be less than Special1s Per Warp x 7."""
    range_start = 1
    range_end = 70
    default = 7
    display_name = "Total Special1 Jewels"


class DraculasCondition(Choice):
    """Sets the requirements for opening the door to Dracula's chamber."""
    display_name = "Dracula's Condition"
    option_none = 0
    option_crystal = 1
    option_bosses = 2
    option_specials = 3
    default = 1


class Special2sRequired(Range):
    """Sets how many Special2 jewels are needed to enter Dracula's chamber. Only applies if Dracula's Chamber Condition
    is set to Special2s."""
    range_start = 1
    range_end = 70
    default = 10
    display_name = "Special2 Jewels Required"


class TotalSpecial2s(Range):
    """Sets how many Speical2 jewels are in the pool in total. This cannot be less than 'Special2s Required'. Only
    applies if Dracula's Chamber Condition is set to Special2s."""
    range_start = 1
    range_end = 70
    default = 10
    display_name = "Total Special2 Jewels"


class BossesRequired(Range):
    """Sets how many bosses need to be defeated to enter Dracula's chamber. Only applies if Dracula's Chamber Condition
    is set to Bosses. Completely disabling the Renon and/or Vincent fights will decrease this number if above 14."""
    range_start = 1
    range_end = 16
    default = 14
    display_name = "Bosses Required"


class CarrieLogic(Toggle):
    """Adds the 2 checks inside Underground Waterway's crawlspace to the pool. If you are not yet certain that you
    (and everyone else if racing the same seed) will be playing as Carrie, don't enable this. Can be combined with
    Glitch Logic to include Carrie-only tricks."""
    display_name = "Carrie Logic"


class HardLogic(Toggle):
    """Properly considers sequence break tricks in logic (i.e. Left Tower skip). Can be combined with Carrie Logic to
    include Carrie-only skips. See the FAQ for a full list of tricks and glitches that may be logically required."""
    display_name = "Hard Logic"


class MultiHitBreakables(Toggle):
    """Adds the items that drop from the objects that break in three hits to the pool. There are 17 of these throughout
    the game adding up to 74 checks in total. The game will be modified to remember exactly which of their items you've
    picked up instead of simply whether they were broken or not."""
    display_name = "Multi-hit Breakables"


class EmptyBreakables(Toggle):
    """Adds 9 check locations in the form of breakables that normally have nothing (i.e. many Forest coffins, the candle
    in the Villa foyer that drops nothing, etc.) and some additional Red Jewels and/or moneybags into the item pool to
    compensate."""
    display_name = "Empty Breakables"


class LizardGeneratorItems(Toggle):
    """Adds the 6 items inside Castle Center 2F's Lizard-man generators to the pool. Picking up all of these can be a
    very time-consuming and luck-based process, so they are excluded by default."""
    display_name = "Lizard-man Generator Items"


class RenonFightCondition(Choice):
    """Sets the condition on which the Renon fight will trigger.
    Vanilla = after spending more than 30,000 gold in his shop."""
    display_name = "Renon Fight Condition"
    option_never = 0
    option_spend_30k = 1
    option_always = 2
    default = 0


class VincentFightCondition(Choice):
    """Sets the condition on which the vampire Vincent fight will trigger.
    Vanilla = after 16 or more in-game days pass."""
    display_name = "Vincent Fight Condition"
    option_never = 0
    option_wait_16_days = 1
    option_always = 2
    default = 0


class BadEndingCondition(Choice):
    """Sets the condition on which the currently-controlled character's Bad Ending will trigger.
    Vanilla = after defeating vampire Vincent."""
    display_name = "Bad Ending Condition"
    option_never = 0
    option_defeat_vincent = 1
    option_always = 2
    default = 0


class IncreaseItemLimit(DefaultOnToggle):
    """Increases the holding limit of usable items from 10 to 100 of each item."""
    display_name = "Increase Item Limit"


class NerfHealingItems(Toggle):
    """Decreases the amount of health healed by Roast Chickens to 25%, Roast Beefs to 50%, and Healing Kits to 80%."""
    display_name = "Nerf Healing Items"


class LoadingZoneHeals(DefaultOnToggle):
    """Whether end-of-level loading zones restore health and cure status aliments or not.
    Recommended off for those looking for more of a survival horror experience!"""


class InvisibleItems(Choice):
    """Controls which items are visible and which are invisible until picked up. 'Chance' gives each item a 50/50 chance
    of being visible or invisible."""
    display_name = "Invisible Items"
    option_reveal_all = 0
    option_vanilla = 1
    option_hide_all = 2
    option_chance = 3
    default = 1


class DropPreviousSubWeapon(Toggle):
    """When picking up a sub-weapon, the one you had before will drop behind you, so it can be taken back if desired."""
    display_name = "Drop Previous Sub-weapon"


class DisableTimeRestrictions(Toggle):
    """Disables the time restriction on every event and door that requires the current time to be something specific
     (sun/moon doors, meeting Rosa, and the Villa fountain). The Villa coffin is not affected by this."""
    display_name = "Disable Time Requirements"


class SkipWaterwayPlatforms(Toggle):
    """Opens the door to the third switch in Underground Waterway from the start so that the jumping across floating
    brick platforms won't have to be done."""
    display_name = "Skip Waterway Platforms"


class Countdown(Choice):
    """Displays, below the HUD clock, the number of unobtained progression-marked items or locations remaining in the
    stage you're currently in."""
    display_name = "Countdown"
    option_none = 0
    option_majors = 1
    option_all_locations = 2
    default = 0


class BackgroundMusic(Choice):
    """Randomizes or disables the music heard throughout the game. Randomized music is split into two pools: songs that
    loop and songs that don't."""
    display_name = "Background Music"
    option_normal = 0
    option_disabled = 1
    option_randomized = 2
    default = 0


class MapLighting(Choice):
    """Randomizes the lighting color RGB values on every map during every time of day to be literally anything.
    The colors and/or shading of the following things are affected: fog, maps, player, enemies, and some objects."""
    display_name = "Map Lighting"
    option_normal = 0
    option_randomized = 1
    default = 0


cv64_options: Dict[str, Option] = {
    "character_stages": CharacterStages,
    "stage_shuffle": StageShuffle,
    "warp_shuffle": WarpShuffle,
    "sub_weapon_shuffle": SubWeaponShuffle,
    "extra_keys": ExtraKeys,
    "special1s_per_warp": Special1sPerWarp,
    "total_special1s": TotalSpecial1s,
    "draculas_condition": DraculasCondition,
    "special2s_required": Special2sRequired,
    "total_special2s": TotalSpecial2s,
    "bosses_required": BossesRequired,
    "carrie_logic": CarrieLogic,
    "hard_logic": HardLogic,
    "multi_hit_breakables": MultiHitBreakables,
    "empty_breakables": EmptyBreakables,
    "lizard_generator_items": LizardGeneratorItems,
    "renon_fight_condition": RenonFightCondition,
    "vincent_fight_condition": VincentFightCondition,
    "bad_ending_condition": BadEndingCondition,
    "increase_item_limit": IncreaseItemLimit,
    "nerf_healing_items": NerfHealingItems,
    "loading_zone_heals": LoadingZoneHeals,
    "invisible_items": InvisibleItems,
    "drop_previous_sub_weapon": DropPreviousSubWeapon,
    "disable_time_restrictions": DisableTimeRestrictions,
    "skip_waterway_platforms": SkipWaterwayPlatforms,
    "countdown": Countdown,
    "background_music": BackgroundMusic,
    "map_lighting": MapLighting,
    "death_link": DeathLink,
}
