from dataclasses import dataclass
from datetime import date
from typing import Dict

from schema import And, Optional, Or, Schema

from Options import Accessibility, Choice, DeathLinkMixin, DefaultOnToggle, OptionDict, PerGameCommonOptions, Range, \
    StartInventoryPool, Toggle


class MessengerAccessibility(Accessibility):
    default = Accessibility.option_locations
    # defaulting to locations accessibility since items makes certain items self-locking
    __doc__ = Accessibility.__doc__.replace(f"default {Accessibility.default}", f"default {default}")


class Logic(Choice):
    """
    The level of logic to use when determining what locations in your world are accessible.

    Normal: Can require damage boosts, but otherwise approachable for someone who has beaten the game.
    Hard: Expects more knowledge and tighter execution. Has leashing, normal clips and much tighter d-boosting in logic.
    """
    display_name = "Logic Level"
    option_normal = 0
    option_hard = 1
    alias_oob = 1
    alias_challenging = 1


class MegaShards(Toggle):
    """Whether mega shards should be item locations."""
    display_name = "Shuffle Mega Time Shards"


class LimitedMovement(Toggle):
    """
    Removes either rope dart or wingsuit from the itempool. Forces logic to at least hard and accessibility to minimal.
    """
    display_name = "Limited Movement"


class EarlyMed(Toggle):
    """Guarantees meditation will be found early"""
    display_name = "Early Meditation"


class AvailablePortals(Range):
    """Number of portals that are available from the start. Autumn Hills, Howling Grotto, and Glacial Peak are always available. If portal outputs are not randomized, Searing Crags will also be available."""
    display_name = "Available Starting Portals"
    range_start = 3
    range_end = 6
    default = 6


class ShufflePortals(Choice):
    """
    Whether the portals lead to random places.
    Entering a portal from its vanilla area will always lead to HQ, and will unlock it if relevant.
    Supports plando.

    None: Portals will take you where they're supposed to.
    Shops: Portals can lead to any area except Music Box and Elemental Skylands, with each portal output guaranteed to not overlap with another portal's. Will only put you at a portal or a shop.
    Checkpoints: Like Shops except checkpoints without shops are also valid drop points.
    Anywhere: Like Checkpoints except it's possible for multiple portals to output to the same map.
    """
    display_name = "Shuffle Portal Outputs"
    option_none = 0
    alias_off = 0
    option_shops = 1
    option_checkpoints = 2
    option_anywhere = 3


class ShuffleTransitions(Choice):
    """
    Whether the transitions between the levels should be randomized.
    Supports plando.
    
    None: Level transitions lead where they should.
    Coupled: Returning through a transition will take you from whence you came.
    Decoupled: Any level transition can take you to any other level transition.
    """
    display_name = "Shuffle Level Transitions"
    option_none = 0
    alias_off = 0
    option_coupled = 1
    option_decoupled = 2


class Goal(Choice):
    """Requirement to finish the game. To win with the power seal hunt goal, you must enter the Music Box through the shop chest."""
    display_name = "Goal"
    option_open_music_box = 0
    option_power_seal_hunt = 1


class MusicBox(DefaultOnToggle):
    """Whether the music box gauntlet needs to be done."""
    display_name = "Music Box Gauntlet"


class NotesNeeded(Range):
    """How many notes are needed to access the Music Box."""
    display_name = "Notes Needed"
    range_start = 1
    range_end = 6
    default = range_end


class AmountSeals(Range):
    """Number of power seals that exist in the item pool when power seal hunt is the goal."""
    display_name = "Total Power Seals"
    range_start = 1
    range_end = 85
    default = 45


class RequiredSeals(Range):
    """Percentage of total seals required to open the shop chest."""
    display_name = "Percent Seals Required"
    range_start = 10
    range_end = 100
    default = range_end


class Traps(Toggle):
    """Whether traps should be included in the itempool."""
    display_name = "Include Traps"


class ShopPrices(Range):
    """Percentage modifier for shuffled item prices in shops"""
    display_name = "Shop Prices Modifier"
    range_start = 25
    range_end = 400
    default = 100


def planned_price(location: str) -> Dict[Optional, Or]:
    return {
        Optional(location): Or(
            And(int, lambda n: n >= 0),
            {
                Optional(And(int, lambda n: n >= 0)): And(int, lambda n: n >= 0)
            }
        )
    }


class PlannedShopPrices(OptionDict):
    """Plan specific prices on shop slots. Supports weighting"""
    display_name = "Shop Price Plando"
    schema = Schema({
        **planned_price("Karuta Plates"),
        **planned_price("Serendipitous Bodies"),
        **planned_price("Path of Resilience"),
        **planned_price("Kusari Jacket"),
        **planned_price("Energy Shuriken"),
        **planned_price("Serendipitous Minds"),
        **planned_price("Prepared Mind"),
        **planned_price("Meditation"),
        **planned_price("Rejuvenative Spirit"),
        **planned_price("Centered Mind"),
        **planned_price("Strike of the Ninja"),
        **planned_price("Second Wind"),
        **planned_price("Currents Master"),
        **planned_price("Aerobatics Warrior"),
        **planned_price("Demon's Bane"),
        **planned_price("Devil's Due"),
        **planned_price("Time Sense"),
        **planned_price("Power Sense"),
        **planned_price("Focused Power Sense"),
        **planned_price("Green Kappa Figurine"),
        **planned_price("Blue Kappa Figurine"),
        **planned_price("Ountarde Figurine"),
        **planned_price("Red Kappa Figurine"),
        **planned_price("Demon King Figurine"),
        **planned_price("Quillshroom Figurine"),
        **planned_price("Jumping Quillshroom Figurine"),
        **planned_price("Scurubu Figurine"),
        **planned_price("Jumping Scurubu Figurine"),
        **planned_price("Wallaxer Figurine"),
        **planned_price("Barmath'azel Figurine"),
        **planned_price("Queen of Quills Figurine"),
        **planned_price("Demon Hive Figurine"),
    })


@dataclass
class MessengerOptions(DeathLinkMixin, PerGameCommonOptions):
    accessibility: MessengerAccessibility
    start_inventory: StartInventoryPool
    logic_level: Logic
    shuffle_shards: MegaShards
    limited_movement: LimitedMovement
    early_meditation: EarlyMed
    available_portals: AvailablePortals
    shuffle_portals: ShufflePortals
    # shuffle_transitions: ShuffleTransitions
    goal: Goal
    music_box: MusicBox
    notes_needed: NotesNeeded
    total_seals: AmountSeals
    percent_seals_required: RequiredSeals
    shop_price: ShopPrices
    shop_price_plan: PlannedShopPrices

    if date.today() > date(2024, 4, 1):
        traps: Traps
