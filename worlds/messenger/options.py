from dataclasses import dataclass
from typing import Dict

from schema import And, Optional, Or, Schema

from Options import Accessibility, Choice, DeathLink, DefaultOnToggle, OptionDict, PerGameCommonOptions, Range, \
    StartInventoryPool, Toggle


class MessengerAccessibility(Accessibility):
    default = Accessibility.option_locations
    # defaulting to locations accessibility since items makes certain items self-locking
    __doc__ = Accessibility.__doc__.replace(f"default {Accessibility.default}", f"default {default}")


class Logic(Choice):
    """
    The level of logic to use when determining what locations in your world are accessible.

    Normal: can require damage boosts, but otherwise approachable for someone who has beaten the game.
    Hard: has leashing, normal clips, time warps and turtle boosting in logic.
    OoB: places everything with the minimum amount of rules possible. Expect to do OoB. Not guaranteed completable.
    """
    display_name = "Logic Level"
    option_normal = 0
    option_hard = 1
    option_oob = 2
    alias_challenging = 1


class PowerSeals(DefaultOnToggle):
    """Whether power seal locations should be randomized."""
    display_name = "Shuffle Seals"


class MegaShards(Toggle):
    """Whether mega shards should be item locations."""
    display_name = "Shuffle Mega Time Shards"


class Goal(Choice):
    """Requirement to finish the game. Power Seal Hunt will force power seal locations to be shuffled."""
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
class MessengerOptions(PerGameCommonOptions):
    accessibility: MessengerAccessibility
    start_inventory: StartInventoryPool
    logic_level: Logic
    shuffle_seals: PowerSeals
    shuffle_shards: MegaShards
    goal: Goal
    music_box: MusicBox
    notes_needed: NotesNeeded
    total_seals: AmountSeals
    percent_seals_required: RequiredSeals
    shop_price: ShopPrices
    shop_price_plan: PlannedShopPrices
    death_link: DeathLink

