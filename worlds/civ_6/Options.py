from dataclasses import dataclass
from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle


class ProgressionStyle(Choice):
    """Determines what progressive items (if any) should be included.\n\n
    Districts Only: Each tech/civic that would normally unlock a district or district building now has a logical progression. Example: TECH_BRONZE_WORKING is now PROGRESSIVE_ENCAMPMENT\n\n
    Eras and Districts: Players will be defeated if they play until the world era advances beyond the currently unlocked maximum era.
    A notification will be shown as the end of the era approaches letting the player know if they don't have enough progressive era items.
    Unlocked eras can be seen in both the tech and civic trees. Includes all progressive districts.\n\n
    None: No progressive items will be included. This means you can get district upgrades that won't be usable until the relevant district is unlocked.
    """
    display_name = "Progression Style"
    option_districts_only = "Districts Only"
    option_eras_and_districts = "Eras and Districts"
    option_none = "None"
    default = "districts_only"


class ShuffleGoodyHuts(DefaultOnToggle):
    """Shuffles the goody hut rewards. Goody huts will only contain junk items and location checks are received sequentially (GOODY_HUT_1, GOODY_HUT_2, etc)."""
    display_name = "Shuffle Goody Hut Rewards"
    default = True


class BoostSanity(Toggle):
    """Boosts for Civics/Techs are location checks. Boosts can now be triggered even if the item has already been researched. If it is dependent upon a unit that is now obsolete, you can click toggle on/off the relevant tech in the tech tree."""
    default = False


class ExcludeMissableBoosts(Toggle):
    """If boostsanity is enabled, this will prevent any boosts that are 'missable' from having progression items. Disabling this will potentially require multiple playthroughs to complete the seed."""
    default = True


class ResearchCostMultiplier(Choice):
    """Multiplier for research cost of techs and civics, higher values make research more expensive. Cheap = 0.5x, Expensive = 1.5x. Default is 1. """
    display_name = "Tech/Civic Cost Multiplier"
    option_cheap = 0.5
    option_default = 1
    option_expensive = 1.5
    default = 1


class PreHintItems(Choice):
    """Controls if/what items in the tech/civics trees are pre hinted for the multiworld.\n
    All : All items in the tech & civics trees are pre hinted.\n
    Progression items: Only locations in the trees containing progression items are pre hinted.\n
    No Junk: Pre hint the progression and useful items.\n
    None: No items are pre hinted.
    """
    display_name = "Tech/Civic Tree Pre Hinted Items"
    option_all = "All Tree Locations"
    option_progression_items = "Progression Tree Locations"
    option_no_junk = "No Junk"
    option_none = "None"
    default = "progression_items"


class HideItemNames(Toggle):
    """Each Tech and Civic Location will have a title of 'Unrevealed' until its prereqs have been researched. Note that hints will still be pre collected if that option is enabled."""
    default = False


class InGameFlagProgressionItems(DefaultOnToggle):
    """If enabled, an advisor icon will be added to any location that contains a progression item"""
    default = True


class DeathLinkEffect(Choice):
    """What happens when a unit dies. Default is Unit Killed.\n
    Faith, and Gold will be decreased by the amount specified in 'Death Link Effect Percent'. \n
    Era score is decrased by 1.\n
    Any will select any of these options any time a death link is received."""
    display_name = "Death Link Effect"
    option_unit_killed = "Unit Killed"
    option_era_score = "Era Score"
    option_gold = "Gold"
    option_faith = "Faith"
    option_any = "Any"
    option_any_except_era_score = "Any Except Era Score"
    default = "unit_killed"


class DeathLinkEffectPercent(Range):
    """The percentage of the effect that will be applied. Only applicable for Gold and Faith effects. Default is 20%"""
    display_name = "Death Link Effect Percent"
    default = 20
    range_start = 1
    range_end = 100


@dataclass
class CivVIOptions(PerGameCommonOptions):
    progression_style: ProgressionStyle
    shuffle_goody_hut_rewards: ShuffleGoodyHuts
    boostsanity: BoostSanity
    exclude_missable_boosts: ExcludeMissableBoosts
    research_cost_multiplier: ResearchCostMultiplier
    pre_hint_items: PreHintItems
    hide_item_names: HideItemNames
    advisor_show_progression_items: InGameFlagProgressionItems
    death_link_effect: DeathLinkEffect
    death_link_effect_percent: DeathLinkEffectPercent
    death_link: DeathLink
