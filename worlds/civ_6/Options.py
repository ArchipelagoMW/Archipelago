from dataclasses import dataclass
from Options import (
    Choice,
    DefaultOnToggle,
    OptionSet,
    PerGameCommonOptions,
    Range,
    StartInventoryPool,
    Toggle,
)
from .Enum import CivVIHintClassification


class ProgressionStyle(Choice):
    """
    **Districts Only**: Each tech/civic that would normally unlock a district or building now has a logical progression.
    Example: TECH_BRONZE_WORKING is now PROGRESSIVE_ENCAMPMENT

    **Eras and Districts**: Players will be defeated if they play until the world era advances beyond the currently unlocked maximum era.
    Unlocked eras can be seen in both the tech and civic trees. Includes all progressive districts.

    **None**: No progressive items will be included. This means you can get district upgrades that won't be usable until the relevant district is unlocked.
    """

    rich_text_doc = True
    display_name = "Progression Style"
    option_districts_only = 0
    option_eras_and_districts = 1
    option_none = 2
    default = option_districts_only


class ShuffleGoodyHuts(DefaultOnToggle):
    """Shuffles the goody hut rewards.
    Goody huts will only contain junk items and locations are checked sequentially (First goody hut gives GOODY_HUT_1, second gives GOODY_HUT_2, etc.).
    """

    display_name = "Shuffle Goody Hut Rewards"


class BoostSanity(Toggle):
    """Boosts for Civics/Techs are location checks. Boosts can now be triggered even if the item has already been
    researched.

    **Note**: If a boost is dependent upon a unit that is now obsolete, you can click to toggle on/off the relevant tech in
    the tech tree."""

    rich_text_doc = True
    display_name = "Boostsanity"


class ResearchCostMultiplier(Range):
    """Multiplier for research cost of techs and civics, higher values make research more expensive."""

    display_name = "Tech/Civic Cost Multiplier"
    range_start = 50
    range_end = 150
    default = 100


class PreHintItems(OptionSet):
    """Controls what items from the tech/civics trees are pre-hinted for the multiworld.
    **Progression**: Include Progression items in hints
    **Useful**: Include Useful items in hints
    **Filler**: Include Filler items in hints
    """

    display_name = "Tech/Civic Tree pre-hinted Items"
    valid_keys = {classification.value for classification in CivVIHintClassification}  # type: ignore


class HideItemNames(Toggle):
    """Each Tech and Civic Location will have a title of 'Unrevealed' until its prereqs have been researched. Note that
    hints will still be precollected if that option is enabled."""

    display_name = "Hide Item Names"


class InGameFlagProgressionItems(DefaultOnToggle):
    """If enabled, an advisor icon will be added to any location that contains a progression item."""

    display_name = "Advisor Indicates Progression Items"


class CivDeathLink(Toggle):
    """If enabled, losing a unit will trigger a death link effect on other players in the multiworld. When a death link is received, the player will receive the effect specified in 'Death Link Effect'."""

    display_name = "Death Link"


class DeathLinkEffect(OptionSet):
    """What happens when a unit dies.

    **Unit Killed**: A random unit will be killed when a death link is received.

    **Faith**: Faith will be decreased by the amount specified in 'Death Link Effect Percent'.

    **Gold**: Gold will be decreased by the amount specified in 'Death Link Effect Percent'.

    **Era Score**: Era score is decreased by 1.
    """

    rich_text_doc = True
    display_name = "Death Link Effect"
    valid_keys = ["Unit Killed", "Faith", "Gold", "Era Score"]  # type: ignore
    default = frozenset({"Unit Killed"})


class DeathLinkEffectPercent(Range):
    """The percentage of the effect that will be applied. Only applicable for Gold and Faith effects."""

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
    research_cost_multiplier: ResearchCostMultiplier
    pre_hint_items: PreHintItems
    hide_item_names: HideItemNames
    advisor_show_progression_items: InGameFlagProgressionItems
    death_link: CivDeathLink
    death_link_effect: DeathLinkEffect
    death_link_effect_percent: DeathLinkEffectPercent
