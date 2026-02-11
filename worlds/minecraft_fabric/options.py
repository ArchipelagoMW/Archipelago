from dataclasses import dataclass

from Options import PerGameCommonOptions, Choice, Range, ItemSet, OptionSet, OptionGroup, Toggle


########################################################################################################################
# GOAL CONDITION #######################################################################################################
########################################################################################################################

class GoalCondition(Choice):
    """
    Your Goal Condition for your game

    ender_dragon - Goal when the Ender Dragon is defeated
    wither - Goal when the Wither is defeated
    both_bosses - Goal when the Ender Dragon and Wither is defeated
    advancements_only - Goal when you collect a certain amount of Advancements
    ruby_hunt - Goal when a certain amount of rubies are collected (McGuffin hunt)
    """
    option_ender_dragon = 0
    option_wither = 1
    option_both_bosses = 2
    option_advancements_only = 3
    option_ruby_hunt = 4
    default = 0

class AdvancementsRequiredToGoal(Range):
    """
    Determines the number of advancements needed in order to beat the game! These Advancements are required for goaling
    in addition to your regular goal. If this is set to zero, no advancements will be required to goal.

    If fewer available advancements exist than this number, the number of available advancements will be used instead.
    """
    display_name = "Advancements to Goal"
    range_start = 0
    range_end = 1000
    default = 50

class ExcludedLocationTypes(OptionSet):
    """
    Determines Blacklisted Locations in the Randomizer
    If a Location Category is given here, Checks won't appear in locations categorized under it

    This Wiki Page details all locations that're blacklisted via these settings:
    https://modded.wiki/w/Fabric_Archipelago_Mod:Optional_Locations

    Options:
        "Hard" - Disables Locations that're Hard
        "Exploration" - Disables Locations that might require Exploration
        "Unreasonable" - Disables Location's that're EXTREMELY Hard
    """
    display_name = "Excluded Locations"
    default = {
        "Hard",
        "Unreasonable"
    }
    valid_keys = {
        "Hard",
        "Exploration",
        "Unreasonable"
    }

class SpeedRunnerMode(Toggle):
    """
    Makes it so Beds are a required item for defeating the Ender Dragon
    """
    display_name = "Speedrunner Mode"
    default = True

class TotalRubiesInGame(Range):
    """
    Maximum possible number of Rubies that will be in the item pool

    If fewer available locations exist in the pool than this number, the number of available locations will be used instead.

    Required Percentage of Rubies will be calculated based off of that number.

    (Only Takes Effect when going for the Ruby Hunt Goal)
    """
    display_name = "Total Rubies In Game"
    range_start = 1
    range_end = 500
    default = 16

class RubyPercentageNeeded(Range):
    """
    The Percentage of Rubies that need to be collected to Goal for Ruby Hunt.
    (Only Takes Effect when going for the Ruby Hunt Goal)
    """
    display_name = "Ruby Percentage Needed"
    range_start = 1
    range_end = 100
    default = 100

class Itemsanity(Toggle):
    """
    Enables "Itemsanity" which causes items obtainable in Survival to be checks
    """
    display_name = "Itemsanity"
    default = False

class ItemsanityLocalFill(Range):
    """
    The Percentage of Itemsanity Checks that should only contain items from your world
    (Highly recommend setting this to a high value to prevent everyone's items from being in your game)
    """
    display_name = "Itemsanity Local Fill"
    range_start = 0
    range_end = 98
    default = 90

class ExcludedFromItemsanity(OptionSet):
    """
    Determines certain Items that shouldn't appear in Itemsanity
    Primarily used to blacklist Items that are Tedious or VERY RNG heavy

    Options:
        Discs - Music Discs
        Rare Ores - Ores that are extremely rare (such as Deepslate Emerald)
        Mob Heads - Mob Heads that're only dropped from Charged Creeper Explosions
        Netherite Gear - Netherite Tools, Armor, and Netherite Smithing Template
        Trims - Smithing Templates that're used for Trims (Doesn't include Upgrade Templates)
        Sherds - Pottery Sherds
    """
    display_name = "Excluded From Itemsanity"
    default = {
        "Discs",
        "Rare Ores",
        "Mob Heads",
        "Netherite Gear",
        "Trims",
        "Sherds"
    }
    valid_keys = {
        "Discs",
        "Rare Ores",
        "Mob Heads",
        "Netherite Gear",
        "Trims",
        "Sherds"
    }

class EmptyFillPercentage(Range):
    """
    Replaces a certain amount of Non-Trap Junk Items with Items that do nothing.
    This option is primarily for preventing massive amounts of inventory clutter when Itemsanity is Enabled
    """
    display_name = "Empty Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0

########################################################################################################################
# Difficulty Options ###################################################################################################
########################################################################################################################

class DifficultyOption(OptionSet):
    """
    Base Class for Difficulty
    """
    default = {}
    valid_keys = {
        "Iron Weapons",
        "Iron Armor",
        "Bow",
        "Jump",
        "Sprint",
        "Beds"
    }

class ShouldHaveBeforeNetherAccess(DifficultyOption):
    """
    Makes it so certain Items are required in Logic before Nether Access

    Used to help make the Randomizer Easier or Harder

    Available Items
        "Iron Weapons"
        "Iron Armor"
        "Bow"
        "Jump"
        "Sprint"
        "Beds"
    """
    display_name = "Required Before Nether"
    default = {}


class ShouldHaveBeforeWitherOrDragon(DifficultyOption):
    """
    Makes it so certain Items are required in Logic before you need
    to fight the Ender Dragon or Wither

    Used to help make the Randomizer Easier or Harder

    Available Items
        "Iron Weapons"
        "Iron Armor"
        "Bow"
        "Jump"
        "Sprint"
        "Beds"
    """
    display_name = "Required Before Wither or Dragon"
    default = {
        "Iron Weapons",
        "Iron Armor",
        "Bow",
        "Jump",
        "Sprint",
        "Beds"
    }

class ShouldHaveBeforeRaids(DifficultyOption):
    """
    Makes it so certain Items are required in Logic before you need
    to fight a Raid

    Used to help make the Randomizer Easier or Harder

    Available Items
        "Iron Weapons"
        "Iron Armor"
        "Bow"
        "Jump"
        "Sprint"
        "Beds"
    """
    display_name = "Required Before Raids"
    default = {
        "Iron Weapons",
        "Iron Armor",
        "Jump"
    }

########################################################################################################################
# General Options ######################################################################################################
########################################################################################################################

class KeepInventory(Toggle):
    """
    Prevents you from dropping your items when you die!
    """
    display_name = "Keep Inventory"
    default = True

class RandomizedAbilities(OptionSet):
    """
    Determines which abilities and items will be added as items in the item pool
    If an ability is not present in the list they will be treated as unlocked from the start

    Lockable Abilities:
        "Chests" - Removes the ability to craft and use chests (and similar storage containers), and adds Chests to the Item pool.
        "Jump" - Removes the ability to jump, and adds Jumping to the Item pool.
        "Sprint" - Removes the ability to run, and adds Sprint to the Item pool.
        "Swim" - Removes the ability to enter water, and adds Swim to the Item pool.
    """
    display_name = "Ability Shuffle"
    default = {}
    valid_keys = {
        "Chests",
        "Jump",
        "Sprint",
        "Swim"
    }

class TimeSavingOptions(OptionSet):
    """
    Decrease Wait times or Increase likelihood for various events that can occur in the game

    Options:
        "Wither Skulls" - Increases the 2.5% Chance for Wither Skulls to drop to 25%
        "Rabbits Foot" - Increases the 10% Chance for Rabbit's Foot to drop to 50%
        "Drowned Items" - Increases the Chance for a Drowned to drop the items they're holding to 100%
        "Copper Oxidation" - Increases the Chance for Copper Blocks to attempt to Oxidize from 5% to 55%
    """
    display_name = "Time Saving Options"
    default = {
        "Wither Skulls",
        "Rabbits Foot",
        "Drowned Items",
        "Copper Oxidation",
    }
    valid_keys = {
        "Wither Skulls",
        "Rabbits Foot",
        "Drowned Items",
        "Copper Oxidation",
    }

########################################################################################################################
# TRAP STUFF ###########################################################################################################
########################################################################################################################

class TrapFillPercentage(Range):
    """
    Replace a percentage of junk items in the item pool with random traps
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0

class BaseTrapWeight(Choice):
    """
    Base Class for Trap Weights
    """
    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 4
    default = 2

class ReverseControlsTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes WASD, Shift, Jump, Break, and Place to Swap for a short duration
    """
    display_name = "Reverse Controls Trap Weight"

class InvertedMouseTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the Mouse to Invert for a short duration
    """
    display_name = "Inverted Mouse Trap Weight"

class IceTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes all blocks to become slippery for a short duration
    """
    display_name = "Ice Trap Weight"

class RandomEffectTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which applies a random Negative Status Effect
    """
    display_name = "Random Status Effect Trap Weight"

class StunTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap that temporarily stops movement of the player
    """
    display_name = "Stun Trap Weight"

class TNTTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap that spawns a block of lit TNT on the player's position
    """
    display_name = "TNT Trap Weight"

class TeleportTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap that Teleports the player similar to Chorus Fruit
    """
    display_name = "Teleport Trap Weight"

class BeeTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap that Spawns 6 angry bees near the player
    """
    display_name = "Bee Trap Weight"

class LiteratureTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap that Opens Literature Pop-Ups
    """
    display_name = "Literature Trap Weight"

class DeathLink(Toggle):
    """
    Enable DeathLink
    """
    display_name = "DeathLink"
    default = False

class TrapLink(Toggle):
    """
    Enable TrapLink
    """
    display_name = "TrapLink"
    default = False

@dataclass
class FMCOptions(PerGameCommonOptions):
    # Goal Related Options
    goal_condition: GoalCondition
    # Advancements
    advancements_required_for_goal: AdvancementsRequiredToGoal
    excluded_locations: ExcludedLocationTypes
    speedrunner_mode: SpeedRunnerMode
    percentage_of_rubies_needed: RubyPercentageNeeded
    total_rubies: TotalRubiesInGame
    # Sanity Options
    itemsanity: Itemsanity
    itemsanity_local_fill: ItemsanityLocalFill
    excluded_from_itemsanity: ExcludedFromItemsanity
    empty_fill_percentage: EmptyFillPercentage
    # General Settings
    required_before_nether: ShouldHaveBeforeNetherAccess
    required_before_bosses: ShouldHaveBeforeWitherOrDragon
    required_before_raids: ShouldHaveBeforeRaids
    keep_inventory: KeepInventory
    randomized_abilities: RandomizedAbilities
    time_saving_options: TimeSavingOptions
    # Traps
    trap_fill_percentage: TrapFillPercentage
    reverse_controls_trap_weight: ReverseControlsTrapWeight
    inverted_mouse_trap_weight: InvertedMouseTrapWeight
    ice_trap_weight: IceTrapWeight
    random_effect_trap_weight: RandomEffectTrapWeight
    stun_trap_weight: StunTrapWeight
    tnt_trap_weight: TNTTrapWeight
    teleport_trap_weight: TeleportTrapWeight
    bee_trap_weight: BeeTrapWeight
    literature_trap_weight: LiteratureTrapWeight
    deathlink_enabled: DeathLink
    traplink_enabled: TrapLink

