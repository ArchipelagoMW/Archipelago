from dataclasses import dataclass
from typing import Dict, Union, Protocol, runtime_checkable

from Options import Option, Range, DeathLink, SpecialRange, Toggle, Choice


@runtime_checkable
class StardewOption(Protocol):
    internal_name: str


@dataclass
class StardewOptions:
    options: Dict[str, Union[bool, int]]

    def __getitem__(self, item: Union[str, StardewOption]) -> Union[bool, int]:
        if isinstance(item, StardewOption):
            item = item.internal_name

        return self.options.get(item, None)


class Goal(Choice):
    """What's your goal with this play-through?
    With Community Center, the world will be completed once you complete the Community Center.
    With Grandpa's Evaluation, the world will be completed once 4 candles are lit around Grandpa's Shrine.
    With Bottom of the Mines, the world will be completed once you reach level 120 in the local mineshaft.
    With Cryptic Note, the world will be completed once you complete the quest "Cryptic Note" where Mr Qi asks you to reach floor 100 in the Skull Cavern
    With Master Angler, the world will be completed once you have caught every fish in the game. Pairs well with Fishsanity"""
    internal_name = "goal"
    display_name = "Goal"
    option_community_center = 0
    option_grandpa_evaluation = 1
    option_bottom_of_the_mines = 2
    option_cryptic_note = 3
    option_master_angler = 4

    @classmethod
    def get_option_name(cls, value) -> str:
        if value == cls.option_grandpa_evaluation:
            return "Grandpa's Evaluation"

        return super().get_option_name(value)


class StartingMoney(SpecialRange):
    """Amount of gold when arriving at the farm.
    Set to -1 or unlimited for infinite money in this playthrough"""
    internal_name = "starting_money"
    display_name = "Starting Gold"
    range_start = -1
    range_end = 50000
    default = 5000

    special_range_names = {
        "unlimited": -1,
        "vanilla": 500,
        "extra": 2000,
        "rich": 5000,
        "very rich": 20000,
        "filthy rich": 50000,
    }


class ResourcePackMultiplier(SpecialRange):
    """How many items will be in the resource pack. A lower setting mean fewer resources in each pack.
    A higher setting means more resources in each pack. Easy (200) doubles the default quantity.
    This also include Friendship bonuses that replace the one from the Bulletin Board."""
    internal_name = "resource_pack_multiplier"
    default = 100
    range_start = 0
    range_end = 200
    # step = 25
    display_name = "Resource Pack Multiplier"

    special_range_names = {
        "resource packs disabled": 0,
        "half packs": 50,
        "normal packs": 100,
        "double packs": 200,
    }


class BundleRandomization(Choice):
    """What items are needed for the community center bundles?
    With Vanilla, you get the standard bundles from the game
    With Thematic, every bundle will require random items within their original category
    With Shuffled, every bundle will require random items without logic"""
    internal_name = "bundle_randomization"
    display_name = "Bundle Randomization"
    default = 1
    option_vanilla = 0
    option_thematic = 1
    option_shuffled = 2


class BundlePrice(Choice):
    """How many items are needed for the community center bundles?
    With Very Cheap, every bundle will require two items fewer than usual
    With Cheap, every bundle will require 1 item fewer than usual
    With Normal, every bundle will require the vanilla number of items
    With Expensive, every bundle will require 1 extra item"""
    internal_name = "bundle_price"
    display_name = "Bundle Price"
    default = 2
    option_very_cheap = 0
    option_cheap = 1
    option_normal = 2
    option_expensive = 3


class EntranceRandomization(Choice):
    """Should area entrances be randomized?
    With Disabled, no entrance randomization is done
    With Pelican Town, only buildings in the main town area are randomized with each other
    With Non Progression, only buildings that are always available are randomized with each other
    """
    # With Buildings, All buildings in the world are randomized with each other
    # With Everything, All buildings and areas are randomized with each other
    # With Chaos, same as everything, but the buildings are shuffled again every in-game day. You can't learn it!

    internal_name = "entrance_randomization"
    display_name = "Entrance Randomization"
    default = 0
    option_disabled = 0
    option_pelican_town = 1
    option_non_progression = 2
    # option_buildings = 3
    # option_everything = 4
    # option_chaos = 4


class BackpackProgression(Choice):
    """How is the backpack progression handled?
    With Vanilla, you can buy them at Pierre's.
    With Progressive, you will randomly find Progressive Backpack to upgrade.
    With Early Progressive, you can expect you first Backpack before the second season, and the third before the forth
        season.
    """
    internal_name = "backpack_progression"
    display_name = "Backpack Progression"
    default = 2
    option_vanilla = 0
    option_progressive = 1
    option_early_progressive = 2


class ToolProgression(Choice):
    """How is the tool progression handled?
    With Vanilla, Clint will upgrade your tools with ore.
    With Progressive, you will randomly find Progressive Tool to upgrade.
    With World Checks, the tools of different quality will be found in the world."""
    internal_name = "tool_progression"
    display_name = "Tool Progression"
    default = 1
    option_vanilla = 0
    option_progressive = 1


class TheMinesElevatorsProgression(Choice):
    """How is The Mines' Elevator progression handled?
    With Vanilla, you will unlock a new elevator floor every 5 floor in the mine.
    With Progressive, you will randomly find Progressive Mine Elevator to go deeper. Location are sent for reaching
        every level multiple of 5.
    With Progressive from previous floor, you will randomly find Progressive Mine Elevator to go deeper. Location are
        sent for taking the ladder or stair to every level multiple of 5, taking the elevator does not count."""
    internal_name = "elevator_progression"
    display_name = "Elevator Progression"
    default = 2
    option_vanilla = 0
    option_progressive = 1
    option_progressive_from_previous_floor = 2


class SkillProgression(Choice):
    """How is the skill progression handled?
    With Vanilla, you will level up and get the normal reward at each level.
    With Progressive, the xp will be counted internally, locations will be sent when you gain a virtual level. Your real
        levels will be scattered around the world."""
    internal_name = "skill_progression"
    display_name = "Skill Progression"
    default = 1
    option_vanilla = 0
    option_progressive = 1


class BuildingProgression(Choice):
    """How is the building progression handled?
    With Vanilla, you will buy each building and upgrade one at the time.
    With Progressive, you will receive the buildings and will be able to build the first one of each building for free,
        once it is received. If you want more of the same building, it will cost the vanilla price.
        This option INCLUDES the shipping bin as a building you need to receive.
    With Progressive early shipping bin, you can expect to receive the shipping bin before the end of the first season.
    """
    internal_name = "building_progression"
    display_name = "Building Progression"
    default = 2
    option_vanilla = 0
    option_progressive = 1
    option_progressive_early_shipping_bin = 2


class ArcadeMachineLocations(Choice):
    """How are the Arcade Machines handled?
    With Vanilla, the arcade machines are not included in the Archipelago shuffling.
    With Victories, each Arcade Machine will contain one check on victory
    With Victories Easy, the arcade machines are both made considerably easier to be more accessible for the average
        player.
    With Full Shuffling, the arcade machines will contain multiple checks each, and different buffs that make the game
        easier are in the item pool. Junimo Kart has one check at the end of each level.
        Journey of the Prairie King has one check after each boss, plus one check for each vendor equipment.
    """
    internal_name = "arcade_machine_locations"
    display_name = "Arcade Machine Locations"
    default = 3
    option_disabled = 0
    option_victories = 1
    option_victories_easy = 2
    option_full_shuffling = 3


class HelpWantedLocations(SpecialRange):
    """How many "Help Wanted" quests need to be completed as ArchipelagoLocations
    Out of every 7 quests, 4 will be item deliveries, and then 1 of each for: Fishing, Gathering and Slaying Monsters.
    Choosing a multiple of 7 is recommended."""
    internal_name = "help_wanted_locations"
    default = 7
    range_start = 0
    range_end = 56
    # step = 7
    display_name = "Number of Help Wanted locations"

    special_range_names = {
        "none": 0,
        "minimum": 7,
        "normal": 14,
        "lots": 28,
        "maximum": 56,
    }


class Fishsanity(Choice):
    """Locations for catching fish?
    With None, there are no locations for catching fish
    With Legendaries, each of the 5 legendary fish are locations that contain items
    With Special, a curated selection of strong fish are locations that contain items
    With Random Selection, a random selection of fish are locations that contain items
    With All, every single fish in the game is a location that contains an item. Pairs well with the Master Angler Goal
    """
    internal_name = "fishsanity"
    display_name = "Fishsanity"
    default = 0
    option_none = 0
    option_legendaries = 1
    option_special = 2
    option_random_selection = 3
    option_all = 4


class NumberOfPlayerBuffs(Range):
    """Number of buffs to the player of each type that exist as items in the pool.
    Buffs include movement speed (+25% multiplier, stacks additively)
    and daily luck bonus (0.025 flat value per buff)"""
    internal_name = "player_buff_number"
    display_name = "Number of Player Buffs"
    range_start = 0
    range_end = 12
    default = 4
    # step = 1


class MultipleDaySleepEnabled(Toggle):
    """Should you be able to sleep automatically multiple day strait?"""
    internal_name = "multiple_day_sleep_enabled"
    display_name = "Multiple Day Sleep Enabled"
    default = 1


class MultipleDaySleepCost(SpecialRange):
    """How must gold it cost to sleep through multiple days? You will have to pay that amount for each day slept."""
    internal_name = "multiple_day_sleep_cost"
    display_name = "Multiple Day Sleep Cost"
    range_start = 0
    range_end = 200
    # step = 25

    special_range_names = {
        "free": 0,
        "cheap": 25,
        "medium": 50,
        "expensive": 100,
    }


class ExperienceMultiplier(SpecialRange):
    """How fast do you want to level up. A lower setting mean less experience.
    A higher setting means more experience."""
    internal_name = "experience_multiplier"
    display_name = "Experience Multiplier"
    range_start = 25
    range_end = 400
    # step = 25
    default = 200

    special_range_names = {
        "half": 50,
        "vanilla": 100,
        "double": 200,
        "triple": 300,
        "quadruple": 400,
    }


class DebrisMultiplier(Choice):
    """How much debris spawn on the player's farm?
    With Vanilla, debris spawns normally
    With Half, debris will spawn at half the normal rate
    With Quarter, debris will spawn at one quarter of the normal rate
    With None, No debris will spawn on the farm, ever
    With Start Clear, debris will spawn at the normal rate, but the farm will be completely clear when starting the game
    """
    internal_name = "debris_multiplier"
    display_name = "Debris Multiplier"
    default = 1
    option_vanilla = 0
    option_half = 1
    option_quarter = 2
    option_none = 3
    option_start_clear = 4


class QuickStart(Toggle):
    """Do you want the quick start package? You will get a few items to help early game automation,
    so you can use the multiple day sleep at its maximum."""
    internal_name = "quick_start"
    display_name = "Quick Start"
    default = 1


class Gifting(Toggle):
    """Do you want to enable gifting items to and from other Stardew Valley worlds?"""
    internal_name = "gifting"
    display_name = "Gifting"
    default = 1


class GiftTax(SpecialRange):
    """Joja Prime will deliver gifts within one business day, for a price!
    Sending a gift will cost a percentage of the item's monetary value as a tax on the sender"""
    internal_name = "gift_tax"
    display_name = "Gift Tax"
    range_start = 0
    range_end = 400
    # step = 20
    default = 20

    special_range_names = {
        "no tax": 0,
        "soft tax": 20,
        "rough tax": 40,
        "full tax": 100,
        "oppressive tax": 200,
        "nightmare tax": 400,
    }


stardew_valley_options: Dict[str, type(Option)] = {
    option.internal_name: option
    for option in [
        StartingMoney,
        ResourcePackMultiplier,
        BundleRandomization,
        BundlePrice,
        EntranceRandomization,
        BackpackProgression,
        ToolProgression,
        SkillProgression,
        BuildingProgression,
        TheMinesElevatorsProgression,
        ArcadeMachineLocations,
        HelpWantedLocations,
        Fishsanity,
        NumberOfPlayerBuffs,
        Goal,
        MultipleDaySleepEnabled,
        MultipleDaySleepCost,
        ExperienceMultiplier,
        DebrisMultiplier,
        QuickStart,
        Gifting,
        GiftTax,
    ]
}
default_options = {option.internal_name: option.default for option in stardew_valley_options.values()}
stardew_valley_options["death_link"] = DeathLink


def fetch_options(world, player: int) -> StardewOptions:
    return StardewOptions({option: get_option_value(world, player, option) for option in stardew_valley_options})


def get_option_value(world, player: int, name: str) -> Union[bool, int]:
    assert name in stardew_valley_options, f"{name} is not a valid option for Stardew Valley."

    value = getattr(world, name)

    if issubclass(stardew_valley_options[name], Toggle):
        return bool(value[player].value)
    return value[player].value
