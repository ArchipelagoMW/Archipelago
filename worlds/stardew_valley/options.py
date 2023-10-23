from dataclasses import dataclass
from typing import Dict

from Options import Range, SpecialRange, Toggle, Choice, OptionSet, PerGameCommonOptions, DeathLink, Option
from .mods.mod_data import ModNames


class Goal(Choice):
    """What's your goal with this play-through?
    Community Center: The world will be completed once you complete the Community Center.
    Grandpa's Evaluation: The world will be completed once 4 candles are lit at Grandpa's Shrine.
    Bottom of the Mines: The world will be completed once you reach level 120 in the mineshaft.
    Cryptic Note: The world will be completed once you complete the quest "Cryptic Note" where Mr Qi asks you to reach floor 100 in the Skull Cavern.
    Master Angler: The world will be completed once you have caught every fish in the game. Pairs well with Fishsanity.
    Complete Collection: The world will be completed once you have completed the museum by donating every possible item. Pairs well with Museumsanity.
    Full House: The world will be completed once you get married and have two kids. Pairs well with Friendsanity.
    Greatest Walnut Hunter: The world will be completed once you find all 130 Golden Walnuts
    Perfection: The world will be completed once you attain Perfection, based on the vanilla definition.
    """
    internal_name = "goal"
    display_name = "Goal"
    default = 0
    option_community_center = 0
    option_grandpa_evaluation = 1
    option_bottom_of_the_mines = 2
    option_cryptic_note = 3
    option_master_angler = 4
    option_complete_collection = 5
    option_full_house = 6
    option_greatest_walnut_hunter = 7
    # option_junimo_kart =
    # option_prairie_king =
    # option_fector_challenge =
    # option_craft_master =
    # option_mystery_of_the_stardrops =
    # option_protector_of_the_valley =
    # option_full_shipment =
    # option_legend =
    # option_beloved_farmer =
    # option_master_of_the_five_ways =
    option_perfection = 25

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


class ProfitMargin(SpecialRange):
    """Multiplier over all gold earned in-game by the player."""
    internal_name = "profit_margin"
    display_name = "Profit Margin"
    range_start = 25
    range_end = 400
    # step = 25
    default = 100

    special_range_names = {
        "quarter": 25,
        "half": 50,
        "normal": 100,
        "double": 200,
        "triple": 300,
        "quadruple": 400,
    }


class BundleRandomization(Choice):
    """What items are needed for the community center bundles?
    Vanilla: Standard bundles from the vanilla game
    Thematic: Every bundle will require random items compatible with their original theme
    Shuffled: Every bundle will require random items and follow no particular structure"""
    internal_name = "bundle_randomization"
    display_name = "Bundle Randomization"
    default = 1
    option_vanilla = 0
    option_thematic = 1
    option_shuffled = 2


class BundlePrice(Choice):
    """How many items are needed for the community center bundles?
    Very Cheap: Every bundle will require 2 items fewer than usual
    Cheap: Every bundle will require 1 item fewer than usual
    Normal: Every bundle will require the vanilla number of items
    Expensive: Every bundle will require 1 extra item when applicable"""
    internal_name = "bundle_price"
    display_name = "Bundle Price"
    default = 2
    option_very_cheap = 0
    option_cheap = 1
    option_normal = 2
    option_expensive = 3


class EntranceRandomization(Choice):
    """Should area entrances be randomized?
    Disabled: No entrance randomization is done
    Pelican Town: Only buildings in the main town area are randomized among each other
    Non Progression: Only buildings that are always available are randomized with each other
    Buildings: All Entrances that Allow you to enter a building using a door are randomized with each other
    Chaos: Same as above, but the entrances get reshuffled every single day!
    """
    # Everything: All buildings and areas are randomized with each other
    # Chaos, same as everything: but the buildings are shuffled again every in-game day. You can't learn it!
    # Buildings One-way: Entrance pairs are disconnected, they aren't two-way!
    # Everything One-way: Entrance pairs are disconnected, and every entrance is in the shuffle
    # Chaos One-way: Entrance pairs are disconnected, and they change every day!

    internal_name = "entrance_randomization"
    display_name = "Entrance Randomization"
    default = 0
    option_disabled = 0
    option_pelican_town = 1
    option_non_progression = 2
    option_buildings = 3
    # option_everything = 4
    option_chaos = 5
    # option_buildings_one_way = 6
    # option_everything_one_way = 7
    # option_chaos_one_way = 8


class SeasonRandomization(Choice):
    """Should seasons be randomized?
    All settings allow you to choose which season you want to play next (from those unlocked) at the end of a season.
    Disabled: You will start in Spring with all seasons unlocked.
    Randomized: The seasons will be unlocked randomly as Archipelago items.
    Randomized Not Winter: The seasons are randomized, but you're guaranteed not to start with winter.
    Progressive: You will start in Spring and unlock the seasons in their original order.
    """
    internal_name = "season_randomization"
    display_name = "Season Randomization"
    default = 1
    option_disabled = 0
    option_randomized = 1
    option_randomized_not_winter = 2
    option_progressive = 3


class Cropsanity(Choice):
    """Formerly named "Seed Shuffle"
    Pierre now sells a random amount of seasonal seeds and Joja sells them without season requirements, but only in huge packs.
    Disabled: All the seeds are unlocked from the start, there are no location checks for growing and harvesting crops
    Shuffled: Seeds are unlocked as archipelago item, for each seed there is a location check for growing and harvesting that crop
    """
    internal_name = "cropsanity"
    display_name = "Cropsanity"
    default = 1
    option_disabled = 0
    option_shuffled = 1


class BackpackProgression(Choice):
    """How is the backpack progression handled?
    Vanilla: You can buy them at Pierre's General Store.
    Progressive: You will randomly find Progressive Backpack upgrades.
    Early Progressive: You can expect your first Backpack in sphere 1.
    """
    internal_name = "backpack_progression"
    display_name = "Backpack Progression"
    default = 2
    option_vanilla = 0
    option_progressive = 1
    option_early_progressive = 2


class ToolProgression(Choice):
    """How is the tool progression handled?
    Vanilla: Clint will upgrade your tools with ore.
    Progressive: You will randomly find Progressive Tool upgrades."""
    internal_name = "tool_progression"
    display_name = "Tool Progression"
    default = 1
    option_vanilla = 0
    option_progressive = 1


class ElevatorProgression(Choice):
    """How is Elevator progression handled?
    Vanilla: You will unlock new elevator floors for yourself.
    Progressive: You will randomly find Progressive Mine Elevators to go deeper. Locations are sent for reaching
        every elevator level.
    Progressive from previous floor: Same as progressive, but you must reach elevator floors on your own,
        you cannot use the elevator to check elevator locations"""
    internal_name = "elevator_progression"
    display_name = "Elevator Progression"
    default = 2
    option_vanilla = 0
    option_progressive = 1
    option_progressive_from_previous_floor = 2


class SkillProgression(Choice):
    """How is the skill progression handled?
    Vanilla: You will level up and get the normal reward at each level.
    Progressive: The xp will be earned internally, locations will be sent when you earn a level. Your real
        levels will be scattered around the multiworld."""
    internal_name = "skill_progression"
    display_name = "Skill Progression"
    default = 1
    option_vanilla = 0
    option_progressive = 1


class BuildingProgression(Choice):
    """How is the building progression handled?
    Vanilla: You will buy each building normally.
    Progressive: You will receive the buildings and will be able to build the first one of each type for free,
        once it is received. If you want more of the same building, it will cost the vanilla price.
    Progressive early shipping bin: You can expect your shipping bin in sphere 1.
    """
    internal_name = "building_progression"
    display_name = "Building Progression"
    default = 2
    option_vanilla = 0
    option_progressive = 1
    option_progressive_early_shipping_bin = 2


class FestivalLocations(Choice):
    """Locations for attending and participating in festivals
    With Disabled, you do not need to attend festivals
    With Easy, there are checks for participating in festivals
    With Hard, the festival checks are only granted when the player performs well in the festival
    """
    internal_name = "festival_locations"
    display_name = "Festival Locations"
    default = 1
    option_disabled = 0
    option_easy = 1
    option_hard = 2


class ArcadeMachineLocations(Choice):
    """How are the Arcade Machines handled?
    Disabled: The arcade machines are not included in the Archipelago shuffling.
    Victories: Each Arcade Machine will contain one check on victory
    Victories Easy: The arcade machines are both made considerably easier to be more accessible for the average
        player.
    Full Shuffling: The arcade machines will contain multiple checks each, and different buffs that make the game
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


class SpecialOrderLocations(Choice):
    """How are the Special Orders handled?
    Disabled: The special orders are not included in the Archipelago shuffling.
    Board Only: The Special Orders on the board in town are location checks
    Board and Qi: The Special Orders from Qi's walnut room are checks, as well as the board in town
    """
    internal_name = "special_order_locations"
    display_name = "Special Order Locations"
    default = 1
    option_disabled = 0
    option_board_only = 1
    option_board_qi = 2


class HelpWantedLocations(SpecialRange):
    """How many "Help Wanted" quests need to be completed as Archipelago Locations
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
    None: There are no locations for catching fish
    Legendaries: Each of the 5 legendary fish are checks
    Special: A curated selection of strong fish are checks
    Randomized: A random selection of fish are checks
    All: Every single fish in the game is a location that contains an item. Pairs well with the Master Angler Goal
    Exclude Legendaries: Every fish except legendaries
    Exclude Hard Fish: Every fish under difficulty 80
    Only Easy Fish: Every fish under difficulty 50
    """
    internal_name = "fishsanity"
    display_name = "Fishsanity"
    default = 0
    option_none = 0
    option_legendaries = 1
    option_special = 2
    option_randomized = 3
    alias_random_selection = option_randomized
    option_all = 4
    option_exclude_legendaries = 5
    option_exclude_hard_fish = 6
    option_only_easy_fish = 7


class Museumsanity(Choice):
    """Locations for museum donations?
    None: There are no locations for donating artifacts and minerals to the museum
    Milestones: The donation milestones from the vanilla game are checks
    Randomized: A random selection of minerals and artifacts are checks
    All: Every single donation will be a check
    """
    internal_name = "museumsanity"
    display_name = "Museumsanity"
    default = 1
    option_none = 0
    option_milestones = 1
    option_randomized = 2
    option_all = 3


class Friendsanity(Choice):
    """Locations for friendships?
    None: There are no checks for befriending villagers
    Bachelors: Each heart of a bachelor is a check
    Starting NPCs: Each heart for npcs that are immediately available is a check
    All: Every heart with every NPC is a check, including Leo, Kent, Sandy, etc
    All With Marriage: Marriage candidates must also be dated, married, and befriended up to 14 hearts.
    """
    internal_name = "friendsanity"
    display_name = "Friendsanity"
    default = 0
    option_none = 0
    # option_marry_one_person = 1
    option_bachelors = 2
    option_starting_npcs = 3
    option_all = 4
    option_all_with_marriage = 5


# Conditional Setting - Friendsanity not None
class FriendsanityHeartSize(Range):
    """If using friendsanity, how many hearts are received per item, and how many hearts must be earned to send a check
    A higher value will lead to fewer heart items in the item pool, reducing bloat"""
    internal_name = "friendsanity_heart_size"
    display_name = "Friendsanity Heart Size"
    range_start = 1
    range_end = 8
    default = 4
    # step = 1


class NumberOfMovementBuffs(Range):
    """Number of movement speed buffs to the player that exist as items in the pool.
    Each movement speed buff is a +25% multiplier that stacks additively"""
    internal_name = "movement_buff_number"
    display_name = "Number of Movement Buffs"
    range_start = 0
    range_end = 12
    default = 4
    # step = 1


class NumberOfLuckBuffs(Range):
    """Number of luck buffs to the player that exist as items in the pool.
    Each luck buff is a bonus to daily luck of 0.025"""
    internal_name = "luck_buff_number"
    display_name = "Number of Luck Buffs"
    range_start = 0
    range_end = 12
    default = 4
    # step = 1


class ExcludeGingerIsland(Toggle):
    """Exclude Ginger Island?
    This option will forcefully exclude everything related to Ginger Island from the slot.
    If you pick a goal that requires Ginger Island, you cannot exclude it and it will get included anyway"""
    internal_name = "exclude_ginger_island"
    display_name = "Exclude Ginger Island"
    default = 0


class TrapItems(Choice):
    """When rolling filler items, including resource packs, the game can also roll trap items.
    This setting is for choosing if traps will be in the item pool, and if so, how punishing they will be.
    """
    internal_name = "trap_items"
    display_name = "Trap Items"
    default = 2
    option_no_traps = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_hell = 4
    option_nightmare = 5


class MultipleDaySleepEnabled(Toggle):
    """Enable the ability to sleep automatically for multiple days straight?"""
    internal_name = "multiple_day_sleep_enabled"
    display_name = "Multiple Day Sleep Enabled"
    default = 1


class MultipleDaySleepCost(SpecialRange):
    """How much gold it will cost to use MultiSleep. You will have to pay that amount for each day skipped."""
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
    """How fast you want to earn skill experience. A lower setting mean less experience.
    A higher setting means more experience."""
    internal_name = "experience_multiplier"
    display_name = "Experience Multiplier"
    range_start = 25
    range_end = 800
    # step = 25
    default = 200

    special_range_names = {
        "half": 50,
        "vanilla": 100,
        "double": 200,
        "triple": 300,
        "quadruple": 400,
    }


class FriendshipMultiplier(SpecialRange):
    """How fast you want to earn friendship points with villagers.
    A lower setting mean less friendship per action.
    A higher setting means more friendship per action."""
    internal_name = "friendship_multiplier"
    display_name = "Friendship Multiplier"
    range_start = 25
    range_end = 800
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
    """How much debris will spawn on the player's farm?
    Vanilla: debris spawns normally
    Half: debris will spawn at half the normal rate
    Quarter: debris will spawn at one quarter of the normal rate
    None: No debris will spawn on the farm, ever
    Start Clear: debris will spawn at the normal rate, but the farm will be completely clear when starting the game
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


class Mods(OptionSet):
    """List of mods that will be considered for shuffling."""
    internal_name = "mods"
    display_name = "Mods"
    valid_keys = {
        ModNames.deepwoods, ModNames.tractor, ModNames.big_backpack,
        ModNames.luck_skill, ModNames.magic, ModNames.socializing_skill, ModNames.archaeology,
        ModNames.cooking_skill, ModNames.binning_skill, ModNames.juna,
        ModNames.jasper, ModNames.alec, ModNames.yoba, ModNames.eugene,
        ModNames.wellwick, ModNames.ginger, ModNames.shiko, ModNames.delores,
        ModNames.ayeisha, ModNames.riley, ModNames.skull_cavern_elevator
    }


@dataclass
class StardewValleyOptions(PerGameCommonOptions):
    goal: Goal
    starting_money: StartingMoney
    profit_margin: ProfitMargin
    bundle_randomization: BundleRandomization
    bundle_price: BundlePrice
    entrance_randomization: EntranceRandomization
    season_randomization: SeasonRandomization
    cropsanity: Cropsanity
    backpack_progression: BackpackProgression
    tool_progression: ToolProgression
    skill_progression: SkillProgression
    building_progression: BuildingProgression
    festival_locations: FestivalLocations
    elevator_progression: ElevatorProgression
    arcade_machine_locations: ArcadeMachineLocations
    special_order_locations: SpecialOrderLocations
    help_wanted_locations: HelpWantedLocations
    fishsanity: Fishsanity
    museumsanity: Museumsanity
    friendsanity: Friendsanity
    friendsanity_heart_size: FriendsanityHeartSize
    movement_buff_number: NumberOfMovementBuffs
    luck_buff_number: NumberOfLuckBuffs
    exclude_ginger_island: ExcludeGingerIsland
    trap_items: TrapItems
    multiple_day_sleep_enabled: MultipleDaySleepEnabled
    multiple_day_sleep_cost: MultipleDaySleepCost
    experience_multiplier: ExperienceMultiplier
    friendship_multiplier: FriendshipMultiplier
    debris_multiplier: DebrisMultiplier
    quick_start: QuickStart
    gifting: Gifting
    mods: Mods
    death_link: DeathLink
