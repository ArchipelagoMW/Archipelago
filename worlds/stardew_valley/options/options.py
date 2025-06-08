import sys
import typing
from dataclasses import dataclass
from typing import Protocol, ClassVar

from Options import Range, NamedRange, Toggle, Choice, OptionSet, PerGameCommonOptions, DeathLink, OptionList, Visibility, Removed, OptionCounter
from ..items import items_by_group, Group
from ..mods.mod_data import ModNames
from ..strings.ap_names.ap_option_names import BuffOptionName, WalnutsanityOptionName
from ..strings.bundle_names import all_cc_bundle_names


class StardewValleyOption(Protocol):
    internal_name: ClassVar[str]


class Goal(Choice):
    """Goal for this playthrough
    Community Center: Complete the Community Center
    Grandpa's Evaluation: 4 lit candles in Grandpa's evaluation
    Bottom of the Mines: Reach level 120 in the mines
    Cryptic Note: Complete the quest "Cryptic Note" (Skull Cavern Floor 100)
    Master Angler: Catch every fish. Adapts to Fishsanity
    Complete Collection: Complete the museum collection
    Full House: Get married and have 2 children
    Greatest Walnut Hunter: Find 130 Golden Walnuts. Pairs well with Walnutsanity
    Protector of the Valley: Complete the monster slayer goals. Adapts to Monstersanity
    Full Shipment: Ship every item. Adapts to Shipsanity
    Gourmet Chef: Cook every recipe. Adapts to Cooksanity
    Craft Master: Craft every item
    Legend: Earn 10 000 000g
    Mystery of the Stardrops: Find every stardrop
    Allsanity: Complete every check in your slot
    Perfection: Attain Perfection
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
    option_protector_of_the_valley = 8
    option_full_shipment = 9
    option_gourmet_chef = 10
    option_craft_master = 11
    option_legend = 12
    option_mystery_of_the_stardrops = 13
    # option_junimo_kart =
    # option_prairie_king =
    # option_fector_challenge =
    # option_beloved_farmer =
    # option_master_of_the_five_ways =
    option_allsanity = 24
    option_perfection = 25

    @classmethod
    def get_option_name(cls, value) -> str:
        if value == cls.option_grandpa_evaluation:
            return "Grandpa's Evaluation"

        return super().get_option_name(value)


class FarmType(Choice):
    """What farm to play on?
    Custom farms are not supported"""
    internal_name = "farm_type"
    display_name = "Farm Type"
    default = "random"
    option_standard = 0
    option_riverland = 1
    option_forest = 2
    option_hill_top = 3
    option_wilderness = 4
    option_four_corners = 5
    option_beach = 6
    option_meadowlands = 7


class StartingMoney(NamedRange):
    """Amount of gold when arriving at the farm.
    Set to -1 or unlimited for infinite money"""
    internal_name = "starting_money"
    display_name = "Starting Gold"
    range_start = 0
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


class ProfitMargin(NamedRange):
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
    Remixed: Picks bundles at random from thematic, vanilla remixed and new custom ones
    Remixed Anywhere: Remixed, but bundles are not locked to specific rooms.
    Shuffled: Every bundle will require random items and follow no particular structure"""
    internal_name = "bundle_randomization"
    display_name = "Bundle Randomization"
    option_vanilla = 0
    option_thematic = 1
    option_remixed = 3
    option_remixed_anywhere = 4
    option_shuffled = 6
    default = option_remixed


class BundlePrice(Choice):
    """How many items are needed for the community center bundles?
    Minimum: Every bundle will require only one item
    Very Cheap: Every bundle will require 2 items fewer than usual
    Cheap: Every bundle will require 1 item fewer than usual
    Normal: Every bundle will require the vanilla number of items
    Expensive: Every bundle will require 1 extra item
    Very Expensive: Every bundle will require 2 extra items
    Maximum: Every bundle will require many extra items"""
    internal_name = "bundle_price"
    display_name = "Bundle Price"
    default = 0
    option_minimum = -8
    option_very_cheap = -2
    option_cheap = -1
    option_normal = 0
    option_expensive = 1
    option_very_expensive = 2
    option_maximum = 8


class EntranceRandomization(Choice):
    """Should area entrances be randomized?
    Disabled: No entrance randomization is done
    Pelican Town: Only doors in the main town area are randomized with each other
    Non Progression: Only entrances that are always available are randomized with each other
    Buildings: All entrances that allow you to enter a building are randomized with each other
    Buildings Without House: Buildings, but excluding the farmhouse
    Chaos: Same as "Buildings", but the entrances get reshuffled every single day!
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
    option_buildings_without_house = 3
    option_buildings = 4
    # option_everything = 10
    option_chaos = 12
    # option_buildings_one_way = 6
    # option_everything_one_way = 7
    # option_chaos_one_way = 8


class SeasonRandomization(Choice):
    """Should seasons be randomized?
    Disabled: Start in Spring with all seasons unlocked.
    Randomized: Start in a random season and the other 3 must be unlocked randomly.
    Randomized Not Winter: Same as randomized, but the start season is guaranteed not to be winter.
    Progressive: Start in Spring and unlock the seasons in their original order.
    """
    internal_name = "season_randomization"
    display_name = "Season Randomization"
    default = 1
    option_disabled = 0
    option_randomized = 1
    option_randomized_not_winter = 2
    option_progressive = 3


class Cropsanity(Choice):
    """
    Pierre now sells a random amount of seasonal seeds and Joja sells them without season requirements, but only in huge packs.
    Disabled: All the seeds are unlocked from the start, there are no location checks for growing and harvesting crops
    Enabled: Seeds are unlocked as archipelago items, for each seed there is a location check for growing and harvesting that crop
    """
    internal_name = "cropsanity"
    display_name = "Cropsanity"
    default = 1
    option_disabled = 0
    option_enabled = 1
    alias_shuffled = option_enabled


class BackpackProgression(Choice):
    """Shuffle the backpack?
    Vanilla: You can buy backpacks at Pierre's General Store.
    Progressive: You will randomly find Progressive Backpack upgrades.
    Early Progressive: Same as progressive, but one backpack will be placed early in the multiworld.
    """
    internal_name = "backpack_progression"
    display_name = "Backpack Progression"
    default = 2
    option_vanilla = 0
    option_progressive = 1
    option_early_progressive = 2


class ToolProgression(Choice):
    """Shuffle the tool upgrades?
    Vanilla: Clint will upgrade your tools with metal bars.
    Progressive: Your tools upgrades are randomized.
    Cheap: Tool Upgrades have a 60% discount
    Very Cheap: Tool Upgrades have an 80% discount"""
    internal_name = "tool_progression"
    display_name = "Tool Progression"
    default = 1
    option_vanilla = 0b000  # 0
    option_progressive = 0b001  # 1
    option_vanilla_cheap = 0b010  # 2
    option_vanilla_very_cheap = 0b100  # 4
    option_progressive_cheap = 0b011  # 3
    option_progressive_very_cheap = 0b101  # 5

    @property
    def is_vanilla(self):
        return not self.is_progressive

    @property
    def is_progressive(self):
        return bool(self.value & self.option_progressive)


class ElevatorProgression(Choice):
    """Shuffle the elevator?
    Vanilla: Reaching a mineshaft floor unlocks the elevator for it
    Progressive: You will randomly find Progressive Mine Elevators to go deeper.
    Progressive from previous floor: Same as progressive, but you cannot use the elevator to check elevator locations.
        You must reach elevator floors on your own."""
    internal_name = "elevator_progression"
    display_name = "Elevator Progression"
    default = 2
    option_vanilla = 0
    option_progressive = 1
    option_progressive_from_previous_floor = 2


class SkillProgression(Choice):
    """Shuffle skill levels?
    Vanilla: Leveling up skills is normal
    Progressive: Skill levels are unlocked randomly, and earning xp sends checks. Masteries are excluded
    With Masteries: Skill levels are unlocked randomly, and earning xp sends checks. Masteries are included"""
    internal_name = "skill_progression"
    display_name = "Skill Progression"
    default = 2
    option_vanilla = 0
    option_progressive = 1
    option_progressive_with_masteries = 2


class BuildingProgression(Choice):
    """Shuffle Carpenter Buildings?
    Vanilla: You can buy each building normally.
    Progressive: You will receive the buildings and will be able to build the first one of each type for free,
        once it is received. If you want more of the same building, it will cost the vanilla price.
    Cheap: Buildings will have a 50% discount
    Very Cheap: Buildings will have an 80% discount
    """
    internal_name = "building_progression"
    display_name = "Building Progression"
    default = 3
    option_vanilla = 0b000  # 0
    option_vanilla_cheap = 0b010  # 2
    option_vanilla_very_cheap = 0b100  # 4
    option_progressive = 0b001  # 1
    option_progressive_cheap = 0b011  # 3
    option_progressive_very_cheap = 0b101  # 5


class FestivalLocations(Choice):
    """Shuffle Festival Activities?
    Disabled: You do not need to attend festivals
    Easy: Every festival has checks, but they are easy and usually only require attendance
    Hard: Festivals have more checks, and many require performing well, not just attending
    """
    internal_name = "festival_locations"
    display_name = "Festival Locations"
    default = 1
    option_disabled = 0
    option_easy = 1
    option_hard = 2


class ArcadeMachineLocations(Choice):
    """Shuffle the arcade machines?
    Disabled: The arcade machines are not included.
    Victories: Each Arcade Machine will contain one check on victory
    Victories Easy: Same as Victories, but both games are made considerably easier.
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
    """Shuffle Special Orders?
    Vanilla: The special orders are not included in the Archipelago shuffling. You may need to complete some of them anyway for their vanilla rewards
    Board Only: The Special Orders on the board in town are location checks
    Board and Qi: The Special Orders from Mr Qi's walnut room are checks, in addition to the board in town
    Short: All Special Order requirements are reduced by 40%
    Very Short: All Special Order requirements are reduced by 80%
    """
    internal_name = "special_order_locations"
    display_name = "Special Order Locations"
    option_vanilla = 0b0000  # 0
    option_board = 0b0001  # 1
    value_qi = 0b0010  # 2
    value_short = 0b0100  # 4
    value_very_short = 0b1000  # 8
    option_board_qi = option_board | value_qi  # 3
    option_vanilla_short = value_short  # 4
    option_board_short = option_board | value_short  # 5
    option_board_qi_short = option_board_qi | value_short  # 7
    option_vanilla_very_short = value_very_short  # 8
    option_board_very_short = option_board | value_very_short  # 9
    option_board_qi_very_short = option_board_qi | value_very_short  # 11
    alias_disabled = option_vanilla
    alias_board_only = option_board
    default = option_board_short


class QuestLocations(NamedRange):
    """Include location checks for quests
    None: No quests are checks
    Story: Only story quests are checks
    Number: Story quests and help wanted quests are checks up to the specified amount. Multiple of 7 recommended
    Out of every 7 help wanted quests, 4 will be item deliveries, and then 1 of each for: Fishing, Gathering and Slaying Monsters.
    Extra Help wanted quests might be added if current settings don't have enough locations"""
    internal_name = "quest_locations"
    default = 7
    range_start = 0
    range_end = 56
    # step = 7
    display_name = "Quest Locations"

    special_range_names = {
        "none": -1,
        "story": 0,
        "minimum": 7,
        "normal": 14,
        "lots": 28,
        "maximum": 56,
    }

    def has_story_quests(self) -> bool:
        return self.value >= 0

    def has_no_story_quests(self) -> bool:
        return not self.has_story_quests()


class Fishsanity(Choice):
    """Locations for catching each fish the first time?
    None: There are no locations for catching fish
    Legendaries: Each of the 5 legendary fish are checks, plus the extended family if qi board is turned on
    Special: A curated selection of strong fish are checks
    Randomized: A random selection of fish are checks
    All: Every single fish in the game is a location that contains an item.
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
    All: Every single donation is a check
    """
    internal_name = "museumsanity"
    display_name = "Museumsanity"
    default = 1
    option_none = 0
    option_milestones = 1
    option_randomized = 2
    option_all = 3


class Monstersanity(Choice):
    """Locations for slaying monsters?
    None: There are no checks for slaying monsters
    One per Category: Every category visible at the adventure guild gives one check
    One per Monster: Every unique monster gives one check
    Monster Eradication Goals: The Monster Eradication Goals each contain one check
    Short Monster Eradication Goals: The Monster Eradication Goals each contain one check, but are reduced by 60%
    Very Short Monster Eradication Goals: The Monster Eradication Goals each contain one check, but are reduced by 90%
    Progressive Eradication Goals: The Monster Eradication Goals each contain 5 checks, each 20% of the way
    Split Eradication Goals: The Monster Eradication Goals are split by monsters, each monster has one check
    """
    internal_name = "monstersanity"
    display_name = "Monstersanity"
    default = 1
    option_none = 0
    option_one_per_category = 1
    option_one_per_monster = 2
    option_goals = 3
    option_short_goals = 4
    option_very_short_goals = 5
    option_progressive_goals = 6
    option_split_goals = 7


class Shipsanity(Choice):
    """Locations for shipping items?
    None: There are no checks for shipping items
    Crops: Every crop and forageable being shipped is a check
    Fish: Every fish being shipped is a check except legendaries
    Full Shipment: Every item in the Collections page is a check
    Full Shipment With Fish: Every item in the Collections page and every fish is a check
    Everything: Every item in the game that can be shipped is a check
    """
    internal_name = "shipsanity"
    display_name = "Shipsanity"
    default = 0
    option_none = 0
    option_crops = 1
    # option_quality_crops = 2
    option_fish = 3
    # option_quality_fish = 4
    option_full_shipment = 5
    # option_quality_full_shipment = 6
    option_full_shipment_with_fish = 7
    # option_quality_full_shipment_with_fish = 8
    option_everything = 9
    # option_quality_everything = 10


class Cooksanity(Choice):
    """Locations for cooking food?
    None: There are no checks for cooking
    Queen of Sauce: Every Queen of Sauce Recipe can be cooked for a check
    All: Every cooking recipe can be cooked for a check
    """
    internal_name = "cooksanity"
    display_name = "Cooksanity"
    default = 0
    option_none = 0
    option_queen_of_sauce = 1
    option_all = 2


class Chefsanity(NamedRange):
    """Locations for learning cooking recipes?
    Vanilla: All cooking recipes are learned normally
    Queen of Sauce: Every Queen of Sauce episode is a check, all Queen of Sauce recipes are items
    Purchases: Every purchasable recipe is a check
    Friendship: Recipes obtained from friendship are checks
    Skills: Recipes obtained from skills are checks
    All: Learning every cooking recipe is a check
    """
    internal_name = "chefsanity"
    display_name = "Chefsanity"
    default = 0
    range_start = 0
    range_end = 15

    option_none = 0b0000  # 0
    option_queen_of_sauce = 0b0001  # 1
    option_purchases = 0b0010  # 2
    option_qos_and_purchases = 0b0011  # 3
    option_skills = 0b0100  # 4
    option_friendship = 0b1000  # 8
    option_all = 0b1111  # 15

    special_range_names = {
        "none": 0b0000,  # 0
        "queen_of_sauce": 0b0001,  # 1
        "purchases": 0b0010,  # 2
        "qos_and_purchases": 0b0011,  # 3
        "skills": 0b0100,  # 4
        "friendship": 0b1000,  # 8
        "all": 0b1111,  # 15
    }


class Craftsanity(Choice):
    """Checks for crafting items?
    If enabled, all recipes purchased in shops will be checks as well.
    Recipes obtained from other sources will depend on their respective archipelago settings
    """
    internal_name = "craftsanity"
    display_name = "Craftsanity"
    default = 0
    option_none = 0
    option_all = 1


class Friendsanity(Choice):
    """Shuffle Friendships?
    None: Friendship hearts are earned normally
    Bachelors: Hearts with bachelors are shuffled
    Starting NPCs: Hearts for NPCs available immediately are shuffled
    All: Hearts for all npcs are shuffled, including Leo, Kent, Sandy, etc
    All With Marriage: All hearts for all npcs are shuffled, including romance hearts up to 14 when applicable
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
    """If using friendsanity, how many hearts are received per heart item, and how many hearts must be earned to send a check
    A higher value will lead to fewer heart items in the item pool, reducing bloat"""
    internal_name = "friendsanity_heart_size"
    display_name = "Friendsanity Heart Size"
    range_start = 1
    range_end = 8
    default = 4
    # step = 1


class Booksanity(Choice):
    """Shuffle Books?
    None: All books behave like vanilla
    Power: Power books are turned into checks
    Power and Skill: Power and skill books are turned into checks.
    All: Lost books are also included in the shuffling
    """
    internal_name = "booksanity"
    display_name = "Booksanity"
    default = 2
    option_none = 0
    option_power = 1
    option_power_skill = 2
    option_all = 3


class Walnutsanity(OptionSet):
    """Shuffle Walnuts?
    Puzzles: Walnuts obtained from solving a special puzzle or winning a minigame
    Bushes: Walnuts that are in a bush and can be collected by clicking it
    Dig Spots: Walnuts that are underground and must be digged up. Includes Journal scrap walnuts
    Repeatables: Random chance walnuts from normal actions (fishing, farming, combat, etc)
    """
    internal_name = "walnutsanity"
    display_name = "Walnutsanity"
    valid_keys = frozenset({
        WalnutsanityOptionName.puzzles, WalnutsanityOptionName.bushes, WalnutsanityOptionName.dig_spots,
        WalnutsanityOptionName.repeatables,
    })
    preset_none = frozenset()
    preset_all = valid_keys
    default = preset_none

    def __eq__(self, other: typing.Any) -> bool:
        if isinstance(other, OptionSet):
            return set(self.value) == other.value
        if isinstance(other, OptionList):
            return set(self.value) == set(other.value)
        else:
            return typing.cast(bool, self.value == other)


class NumberOfMovementBuffs(Range):
    """Number of movement speed buffs to the player that exist as items in the pool.
    Each movement speed buff is a +25% multiplier that stacks additively"""
    internal_name = "movement_buff_number"
    display_name = "Number of Movement Buffs"
    range_start = 0
    range_end = 12
    default = 4
    # step = 1


class EnabledFillerBuffs(OptionSet):
    """Enable various permanent player buffs to roll as filler items
    Luck: Increased daily luck
    Damage: Increased Damage %
    Defense: Increased Defense
    Immunity: Increased Immunity
    Health: Increased Max Health
    Energy: Increased Max Energy
    Bite Rate: Shorter delay to get a bite when fishing
    Fish Trap: Effect similar to the Trap Bobber, but weaker
    Fishing Bar Size: Increased Fishing Bar Size
    """
    internal_name = "enabled_filler_buffs"
    display_name = "Enabled Filler Buffs"
    valid_keys = frozenset({
        BuffOptionName.luck, BuffOptionName.damage, BuffOptionName.defense, BuffOptionName.immunity, BuffOptionName.health,
        BuffOptionName.energy, BuffOptionName.bite, BuffOptionName.fish_trap, BuffOptionName.fishing_bar,
    })
    # OptionName.buff_quality, OptionName.buff_glow}) # Disabled these two buffs because they are too hard to make on the mod side
    preset_none = frozenset()
    preset_all = valid_keys
    default = frozenset({BuffOptionName.luck, BuffOptionName.defense, BuffOptionName.bite})


class ExcludeGingerIsland(Toggle):
    """Exclude Ginger Island?
    This option will forcefully exclude everything related to Ginger Island from the slot.
    If you pick a goal that requires Ginger Island, this option will get forced to 'false'"""
    internal_name = "exclude_ginger_island"
    display_name = "Exclude Ginger Island"
    default = 0


class TrapItems(Removed):
    """Deprecated setting, replaced by TrapDifficulty
    """
    internal_name = "trap_items"
    display_name = "Trap Items"
    default = ""
    visibility = Visibility.none

    def __init__(self, value: str):
        if value:
            raise Exception("Option trap_items was replaced by trap_difficulty, please update your options file")
        super().__init__(value)


class TrapDifficulty(Choice):
    """When rolling filler items, including resource packs, the game can also roll trap items.
    Trap items are negative items that cause problems or annoyances for the player.
    This setting is for choosing how punishing traps will be.
    Lower difficulties will be on the funny annoyance side, higher difficulty will be on the extreme problems side.
    Only play Nightmare at your own risk.
    """
    internal_name = "trap_difficulty"
    display_name = "Trap Difficulty"
    default = 2
    option_no_traps = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_hell = 4
    option_nightmare = 5


trap_default_weight = 100


class TrapDistribution(OptionCounter):
    """
    Specify the weighted chance of rolling individual traps when rolling random filler items.
    The average filler item should be considered to be "100", as in 100%.
    So a trap on "200" will be twice as likely to roll as any filler item. A trap on "10" will be 10% as likely.
    You can use weight "0" to disable this trap entirely. The maximum weight is 1000, for x10 chance
    """
    internal_name = "trap_distribution"
    display_name = "Trap Distribution"
    default_weight = trap_default_weight
    visibility = Visibility.all ^ Visibility.simple_ui
    min = 0
    max = 1000
    valid_keys = frozenset({
        trap_data.name
        for trap_data in items_by_group[Group.TRAP]
        if Group.DEPRECATED not in trap_data.groups
    })
    default = {
        trap_data.name: trap_default_weight
        for trap_data in items_by_group[Group.TRAP]
        if Group.DEPRECATED not in trap_data.groups
    }


class MultipleDaySleepEnabled(Toggle):
    """Enable the ability to sleep automatically for multiple days straight?"""
    internal_name = "multiple_day_sleep_enabled"
    display_name = "Multiple Day Sleep Enabled"
    default = 1


class MultipleDaySleepCost(NamedRange):
    """How much gold it will cost to use MultiSleep. You will have to pay that amount for each day skipped."""
    internal_name = "multiple_day_sleep_cost"
    display_name = "Multiple Day Sleep Cost"
    range_start = 0
    range_end = 200
    # step = 25

    special_range_names = {
        "free": 0,
        "cheap": 10,
        "medium": 25,
        "expensive": 50,
        "very expensive": 100,
    }


class ExperienceMultiplier(NamedRange):
    """How fast you want to earn skill experience.
    A lower setting mean less experience.
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


class FriendshipMultiplier(NamedRange):
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
    """Do you want to enable gifting items to and from other Archipelago slots?
    Items can only be sent to games that also support gifting"""
    internal_name = "gifting"
    display_name = "Gifting"
    default = 1


all_mods = {ModNames.deepwoods, ModNames.tractor, ModNames.big_backpack,
            ModNames.luck_skill, ModNames.magic, ModNames.socializing_skill, ModNames.archaeology,
            ModNames.cooking_skill, ModNames.binning_skill, ModNames.juna,
            ModNames.jasper, ModNames.alec, ModNames.yoba, ModNames.eugene,
            ModNames.wellwick, ModNames.ginger, ModNames.shiko, ModNames.delores,
            ModNames.ayeisha, ModNames.riley, ModNames.skull_cavern_elevator, ModNames.sve, ModNames.distant_lands,
            ModNames.alecto, ModNames.lacey, ModNames.boarding_house}

# These mods have been disabled because either they are not updated for the current supported version of Stardew Valley,
# or we didn't find the time to validate that they work or fix compatibility issues if they do.
# Once a mod is validated to be functional, it can simply be removed from this list
disabled_mods = {ModNames.deepwoods, ModNames.magic,
                 ModNames.cooking_skill,
                 ModNames.yoba, ModNames.eugene,
                 ModNames.wellwick, ModNames.shiko, ModNames.delores, ModNames.riley,
                 ModNames.boarding_house}

enabled_mods = all_mods.difference(disabled_mods)


class Mods(OptionSet):
    """List of mods that will be included in the shuffling."""
    visibility = Visibility.all & ~Visibility.simple_ui
    internal_name = "mods"
    display_name = "Mods"
    valid_keys = enabled_mods
    # In tests, we keep even the disabled mods active, because we expect some of them to eventually get updated for SV 1.6
    # In that case, we want to maintain content and logic for them, and therefore keep testing them
    if 'unittest' in sys.modules.keys() or 'pytest' in sys.modules.keys():
        valid_keys = all_mods


class BundlePlando(OptionSet):
    """If using Remixed bundles, this guarantees some of them will show up in your community center.
    If more bundles are specified than what fits in their parent room, that room will randomly pick from only the plando ones"""
    internal_name = "bundle_plando"
    display_name = "Bundle Plando"
    visibility = Visibility.template | Visibility.spoiler
    valid_keys = set(all_cc_bundle_names)


@dataclass
class StardewValleyOptions(PerGameCommonOptions):
    goal: Goal
    farm_type: FarmType
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
    quest_locations: QuestLocations
    fishsanity: Fishsanity
    museumsanity: Museumsanity
    monstersanity: Monstersanity
    shipsanity: Shipsanity
    cooksanity: Cooksanity
    chefsanity: Chefsanity
    craftsanity: Craftsanity
    friendsanity: Friendsanity
    friendsanity_heart_size: FriendsanityHeartSize
    booksanity: Booksanity
    walnutsanity: Walnutsanity
    exclude_ginger_island: ExcludeGingerIsland
    quick_start: QuickStart
    starting_money: StartingMoney
    profit_margin: ProfitMargin
    experience_multiplier: ExperienceMultiplier
    friendship_multiplier: FriendshipMultiplier
    debris_multiplier: DebrisMultiplier
    movement_buff_number: NumberOfMovementBuffs
    enabled_filler_buffs: EnabledFillerBuffs
    trap_difficulty: TrapDifficulty
    trap_distribution: TrapDistribution
    multiple_day_sleep_enabled: MultipleDaySleepEnabled
    multiple_day_sleep_cost: MultipleDaySleepCost
    gifting: Gifting
    mods: Mods
    bundle_plando: BundlePlando
    death_link: DeathLink

    # removed:
    trap_items: TrapItems