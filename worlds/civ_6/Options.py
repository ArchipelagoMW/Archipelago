from dataclasses import dataclass
from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, StartInventory, StartInventoryPool, Toggle


class ProgressionStyle(Choice):
    """Determines what progressive items (if any) should be included.
    Districts Only: Each tech/civic that would normally unlock a district or district building now has a logical progression. Example: TECH_BRONZE_WORKING is now PROGRESSIVE_ENCAMPMENT
    Eras and Districts: Players will be defeated if they play until the world era advances beyond the currently unlocked maximum era.
    A notification will be shown as the end of the era approaches letting the player know if they don't have enough progressive era items.
    Unlocked eras can be seen in both the tech and civic trees. Includes all progressive districts.
    None: No progressive items will be included. This means you can get district upgrades that won't be usable until the relevant district is unlocked.
    """
    display_name = "Progression Style"
    option_districts_only = 0
    option_eras_and_districts = 1
    option_none = 2
    default = option_districts_only


class ShuffleGoodyHuts(DefaultOnToggle):
    """Shuffles the goody hut rewards. Goody huts will only contain junk items and location checks are received sequentially (GOODY_HUT_1, GOODY_HUT_2, etc)."""
    display_name = "Shuffle Goody Hut Rewards"


class BoostSanity(Toggle):
    """Boosts for Civics/Techs are location checks. Boosts can now be triggered even if the item has already been researched. If it is dependent upon a unit that is now obsolete, you can click toggle on/off the relevant tech in the tech tree."""
    display_name = "Boostsanity"


class ExcludeMissableBoosts(Toggle):
    """If Boostsanity is enabled, this will prevent any boosts that are 'missable' from having progression items. Disabling this will potentially require multiple playthroughs to complete the seed."""
    display_name = "Exclude Missable Boosts"


class ResearchCostMultiplier(Choice):
    """Multiplier for research cost of techs and civics, higher values make research more expensive. Cheap = 0.5x, Expensive = 1.5x. Default is 1. """
    display_name = "Tech/Civic Cost Multiplier"
    option_cheap = 0.5
    option_default = 1
    option_expensive = 1.5
    default = 1


class PreHintItems(Choice):
    """Controls if/what items in the tech/civics trees are pre-hinted for the multiworld.
    All : All items in the tech & civics trees are pre-hinted.
    Progression items: Only locations in the trees containing progression items are pre-hinted.
    No Junk: pre-hint the progression and useful items.
    None: No items are pre-hinted.
    """
    display_name = "Tech/Civic Tree pre-hinted Items"
    option_all = 0
    option_progression_items = 1
    option_no_junk = 2
    option_none = 3
    default = option_progression_items


class HideItemNames(Toggle):
    """Each Tech and Civic Location will have a title of 'Unrevealed' until its prereqs have been researched. Note that hints will still be precollected if that option is enabled."""
    display_name = "Hide Item Names"


class InGameFlagProgressionItems(DefaultOnToggle):
    """If enabled, an advisor icon will be added to any location that contains a progression item"""
    display_name = "Advisor Indicates Progression Items"


class DeathLinkEffect(Choice):
    """What happens when a unit dies. Default is Unit Killed.
    Faith, and Gold will be decreased by the amount specified in 'Death Link Effect Percent'.
    Era score is decreased by 1.
    Any will select any of these options any time a death link is received."""
    display_name = "Death Link Effect"
    option_unit_killed = 0
    option_era_score = 1
    option_gold = 2
    option_faith = 3
    option_any = 4
    option_any_except_era_score = 5
    default = option_unit_killed


class DeathLinkEffectPercent(Range):
    """The percentage of the effect that will be applied. Only applicable for Gold and Faith effects. Default is 20%"""
    display_name = "Death Link Effect Percent"
    default = 20
    range_start = 1
    range_end = 100


@dataclass
class CivVIOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    progression_style: ProgressionStyle
    shuffle_goody_hut_rewards: ShuffleGoodyHuts
    boostsanity: BoostSanity
    exclude_missable_boosts: ExcludeMissableBoosts
    research_cost_multiplier: ResearchCostMultiplier
    pre_hint_items: PreHintItems
    hide_item_names: HideItemNames
    advisor_show_progression_items: InGameFlagProgressionItems
    death_link: DeathLink
    death_link_effect: DeathLinkEffect
    death_link_effect_percent: DeathLinkEffectPercent
