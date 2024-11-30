import typing
import re
from dataclasses import make_dataclass

from .ExtractedData import logic_options, starts, pool_options
from .Rules import cost_terms
from schema import And, Schema, Optional

from Options import Option, DefaultOnToggle, Toggle, Choice, Range, OptionDict, NamedRange, DeathLink, PerGameCommonOptions
from .Charms import vanilla_costs, names as charm_names

if typing.TYPE_CHECKING:
    # avoid import during runtime
    from random import Random
else:
    Random = typing.Any

locations = {"option_" + start: i for i, start in enumerate(starts)}
# This way the dynamic start names are picked up by the MetaClass Choice belongs to
StartLocation = type("StartLocation", (Choice,), {
    "__module__": __name__,
    "auto_display_name": False,
    "display_name": "Start Location",
    "__doc__": "Choose your start location. "
               "This is currently only locked to King's Pass.",
    **locations,
})
del (locations)

option_docstrings = {
    "RandomizeDreamers": "Allow for Dreamers to be randomized into the item pool and opens their locations for "
                         "randomization.",
    "RandomizeSkills": "Allow for Skills, such as Mantis Claw or Shade Soul, to be randomized into the item pool. "
                       "Also opens their locations\n    for receiving randomized items.",
    "RandomizeFocus": "Removes the ability to focus and randomizes it into the item pool.",
    "RandomizeSwim": "Removes the ability to swim in water and randomizes it into the item pool.",
    "RandomizeCharms": "Allow for Charms to be randomized into the item pool and open their locations for "
                       "randomization. Includes Charms\n    sold in shops.",
    "RandomizeKeys": "Allow for Keys to be randomized into the item pool. Includes those sold in shops.",
    "RandomizeMaskShards": "Allow for Mask Shard to be randomized into the item pool and open their locations for"
                           " randomization.",
    "RandomizeVesselFragments": "Allow for Vessel Fragments to be randomized into the item pool and open their "
                                "locations for randomization.",
    "RandomizeCharmNotches": "Allow for Charm Notches to be randomized into the item pool. "
                             "Includes those sold by Salubra.",
    "RandomizePaleOre": "Randomize Pale Ores into the item pool and open their locations for randomization.",
    "RandomizeGeoChests": "Allow for Geo Chests to contain randomized items, "
                          "as well as their Geo reward being randomized into the item pool.",
    "RandomizeJunkPitChests": "Randomize the contents of junk pit chests into the item pool and open their locations "
                              "for randomization.",
    "RandomizeRancidEggs": "Randomize Rancid Eggs into the item pool and open their locations for randomization",
    "RandomizeRelics": "Randomize Relics (King's Idol, et al.) into the item pool and open their locations for"
                       " randomization.",
    "RandomizeWhisperingRoots": "Randomize the essence rewards from Whispering Roots into the item pool. Whispering "
                                "Roots will now grant a randomized\n    item when completed. This can be previewed by "
                                "standing on the root.",
    "RandomizeBossEssence": "Randomize boss essence drops, such as those for defeating Warrior Dreams, into the item "
                            "pool and open their locations\n    for randomization.",
    "RandomizeGrubs": "Randomize Grubs into the item pool and open their locations for randomization.",
    "RandomizeMimics": "Randomize Mimic Grubs into the item pool and open their locations for randomization.",
    "RandomizeMaps": "Randomize Maps into the item pool. This causes Cornifer to give you a message allowing you to see"
                     " and buy an item\n    that is randomized into that location as well.",
    "RandomizeStags": "Randomize Stag Stations unlocks into the item pool as well as placing randomized items "
                      "on the stag station bell/toll.",
    "RandomizeLifebloodCocoons": "Randomize Lifeblood Cocoon grants into the item pool and open their locations"
                                 " for randomization.",
    "RandomizeGrimmkinFlames": "Randomize Grimmkin Flames into the item pool and open their locations for "
                               "randomization.",
    "RandomizeJournalEntries": "Randomize the Hunter's Journal as well as the findable journal entries into the item "
                               "pool, and open their locations\n    for randomization. Does not include journal entries "
                               "gained by killing enemies.",
    "RandomizeNail": "Removes the ability to swing the nail left, right and up, and shuffles these into the item pool.",
    "RandomizeGeoRocks": "Randomize Geo Rock rewards into the item pool and open their locations for randomization.",
    "RandomizeBossGeo": "Randomize boss Geo drops into the item pool and open those locations for randomization.",
    "RandomizeSoulTotems": "Randomize Soul Refill items into the item pool and open the Soul Totem locations for"
                           " randomization.",
    "RandomizeLoreTablets": "Randomize Lore items into the itempool, one per Lore Tablet, and place randomized item "
                            "grants on the tablets themselves.\n    You must still read the tablet to get the item.",
    "PreciseMovement": "Places skips into logic which require extremely precise player movement, possibly without "
                       "movement skills such as\n    dash or claw.",
    "ProficientCombat": "Places skips into logic which require proficient combat, possibly with limited items.",
    "BackgroundObjectPogos": "Places skips into logic for locations which are reachable via pogoing off of "
                             "background objects.",
    "EnemyPogos": "Places skips into logic for locations which are reachable via pogos off of enemies.",
    "ObscureSkips": "Places skips into logic which are considered obscure enough that a beginner is not expected "
                    "to know them.",
    "ShadeSkips": "Places shade skips into logic which utilize the player's shade for pogoing or damage boosting.",
    "InfectionSkips": "Places skips into logic which are only possible after the crossroads become infected.",
    "FireballSkips": "Places skips into logic which require the use of spells to reset fall speed while in mid-air.",
    "SpikeTunnels": "Places skips into logic which require the navigation of narrow tunnels filled with spikes.",
    "AcidSkips": "Places skips into logic which require crossing a pool of acid without Isma's Tear, or water if swim "
                 "is disabled.",
    "DamageBoosts": "Places skips into logic which require you to take damage from an enemy or hazard to progress.",
    "DangerousSkips": "Places skips into logic which contain a high risk of taking damage.",
    "DarkRooms": "Places skips into logic which require navigating dark rooms without the use of the Lumafly Lantern.",
    "ComplexSkips": "Places skips into logic which require intense setup or are obscure even beyond advanced skip "
                    "standards.",
    "DifficultSkips": "Places skips into logic which are considered more difficult than typical.",
    "RemoveSpellUpgrades": "Removes the second level of all spells from the item pool."
}

default_on = {
    "RandomizeDreamers",
    "RandomizeSkills",
    "RandomizeCharms",
    "RandomizeKeys",
    "RandomizeMaskShards",
    "RandomizeVesselFragments",
    "RandomizeCharmNotches",
    "RandomizePaleOre",
    "RandomizeRancidEggs",
    "RandomizeRelics",
    "RandomizeStags",
    "RandomizeLifebloodCocoons"
}

shop_to_option = {
    "Seer": "SeerRewardSlots",
    "Grubfather": "GrubfatherRewardSlots",
    "Sly": "SlyShopSlots",
    "Sly_(Key)": "SlyKeyShopSlots",
    "Iselda": "IseldaShopSlots",
    "Salubra": "SalubraShopSlots",
    "Leg_Eater": "LegEaterShopSlots",
    "Salubra_(Requires_Charms)": "SalubraCharmShopSlots",
    "Egg_Shop": "EggShopSlots",
}

hollow_knight_randomize_options: typing.Dict[str, type(Option)] = {}

splitter_pattern = re.compile(r'(?<!^)(?=[A-Z])')
for option_name, option_data in pool_options.items():
    extra_data = {"__module__": __name__, "items": option_data[0], "locations": option_data[1]}
    if option_name in option_docstrings:
        extra_data["__doc__"] = option_docstrings[option_name]
    if option_name in default_on:
        option = type(option_name, (DefaultOnToggle,), extra_data)
    else:
        option = type(option_name, (Toggle,), extra_data)
    option.display_name = splitter_pattern.sub(" ", option_name)
    globals()[option.__name__] = option
    hollow_knight_randomize_options[option.__name__] = option

hollow_knight_logic_options: typing.Dict[str, type(Option)] = {}
for option_name in logic_options.values():
    if option_name in hollow_knight_randomize_options:
        continue
    extra_data = {"__module__": __name__}
    # some options, such as elevator pass, appear in logic_options despite explicitly being
    # handled below as classes.
    if option_name in option_docstrings:
        extra_data["__doc__"] = option_docstrings[option_name]
        option = type(option_name, (Toggle,), extra_data)
        option.display_name = splitter_pattern.sub(" ", option_name)
        globals()[option.__name__] = option
        hollow_knight_logic_options[option.__name__] = option


class RandomizeElevatorPass(Toggle):
    """Adds an Elevator Pass item to the item pool, which is then required to use the large elevators connecting
    City of Tears to the Forgotten Crossroads and Resting Grounds."""
    display_name = "Randomize Elevator Pass"
    default = False


class SplitMothwingCloak(Toggle):
    """Splits the Mothwing Cloak into left- and right-only versions of the item. Randomly adds a second left or
    right Mothwing cloak item which functions as the upgrade to Shade Cloak."""
    display_name = "Split Mothwing Cloak"
    default = False


class SplitMantisClaw(Toggle):
    """Splits the Mantis Claw into left- and right-only versions of the item."""
    display_name = "Split Mantis Claw"
    default = False


class SplitCrystalHeart(Toggle):
    """Splits the Crystal Heart into left- and right-only versions of the item."""
    display_name = "Split Crystal Heart"
    default = False


class MinimumGrubPrice(Range):
    """The minimum grub price in the range of prices that an item should cost from Grubfather."""
    display_name = "Minimum Grub Price"
    range_start = 1
    range_end = 46
    default = 1


class MaximumGrubPrice(MinimumGrubPrice):
    """The maximum grub price in the range of prices that an item should cost from Grubfather."""
    display_name = "Maximum Grub Price"
    default = 23


class MinimumEssencePrice(Range):
    """The minimum essence price in the range of prices that an item should cost from Seer."""
    display_name = "Minimum Essence Price"
    range_start = 1
    range_end = 2800
    default = 1


class MaximumEssencePrice(MinimumEssencePrice):
    """The maximum essence price in the range of prices that an item should cost from Seer."""
    display_name = "Maximum Essence Price"
    default = 1400


class MinimumEggPrice(Range):
    """The minimum rancid egg price in the range of prices that an item should cost from Jiji.
    Only takes effect if the EggSlotShops option is greater than 0."""
    display_name = "Minimum Egg Price"
    range_start = 1
    range_end = 20
    default = 1


class MaximumEggPrice(MinimumEggPrice):
    """The maximum rancid egg price in the range of prices that an item should cost from Jiji.
    Only takes effect if the EggSlotShops option is greater than 0."""
    display_name = "Maximum Egg Price"
    default = 10


class MinimumCharmPrice(Range):
    """The minimum charm price in the range of prices that an item should cost for Salubra's shop item which also
    carry a charm cost."""
    display_name = "Minimum Charm Requirement"
    range_start = 1
    range_end = 40
    default = 1


class MaximumCharmPrice(MinimumCharmPrice):
    """The maximum charm price in the range of prices that an item should cost for Salubra's shop item which also
    carry a charm cost."""
    display_name = "Maximum Charm Requirement"
    default = 20


class MinimumGeoPrice(Range):
    """The minimum geo price for items in geo shops."""
    display_name = "Minimum Geo Price"
    range_start = 1
    range_end = 200
    default = 1


class MaximumGeoPrice(Range):
    """The maximum geo price for items in geo shops."""
    display_name = "Maximum Geo Price"
    range_start = 1
    range_end = 2000
    default = 400


class RandomCharmCosts(NamedRange):
    """Total Notch Cost of all Charms together. Vanilla sums to 90.
    This value is distributed among all charms in a random fashion.
    Special Cases:
    Set to -1 or vanilla for vanilla costs.
    Set to -2 or shuffle to shuffle around the vanilla costs to different charms."""

    display_name = "Randomize Charm Notch Costs"
    range_start = 0
    range_end = 240
    default = -1
    vanilla_costs: typing.List[int] = vanilla_costs
    charm_count: int = len(vanilla_costs)
    special_range_names = {
        "vanilla": -1,
        "shuffle": -2
    }

    def get_costs(self, random_source: Random) -> typing.List[int]:
        charms: typing.List[int]
        if -1 == self.value:
            return self.vanilla_costs.copy()
        elif -2 == self.value:
            charms = self.vanilla_costs.copy()
            random_source.shuffle(charms)
            return charms
        else:
            charms = [0] * self.charm_count
            for x in range(self.value):
                index = random_source.randint(0, self.charm_count - 1)
                while charms[index] > 5:
                    index = random_source.randint(0, self.charm_count - 1)
                charms[index] += 1
            return charms


class PlandoCharmCosts(OptionDict):
    """Allows setting a Charm's Notch costs directly, mapping {name: cost}.
    This is set after any random Charm Notch costs, if applicable."""
    display_name = "Charm Notch Cost Plando"
    valid_keys = frozenset(charm_names)
    schema = Schema({
        Optional(name): And(int, lambda n: 6 >= n >= 0, error="Charm costs must be integers in the range 0-6.") for name in charm_names
        })

    def get_costs(self, charm_costs: typing.List[int]) -> typing.List[int]:
        for name, cost in self.value.items():
            charm_costs[charm_names.index(name)] = cost
        return charm_costs


class SlyShopSlots(Range):
    """For each extra slot, add a location to the Sly Shop and a filler item to the item pool."""

    display_name = "Sly Shop Slots"
    default = 8
    range_end = 16


class SlyKeyShopSlots(Range):
    """For each extra slot, add a location to the Sly Shop (requiring Shopkeeper's Key) and a filler item to the item
    pool."""

    display_name = "Sly Key Shop Slots"
    default = 6
    range_end = 16


class IseldaShopSlots(Range):
    """For each extra slot, add a location to the Iselda Shop and a filler item to the item pool."""

    display_name = "Iselda Shop Slots"
    default = 2
    range_end = 16


class SalubraShopSlots(Range):
    """For each extra slot, add a location to the Salubra Shop, and a filler item to the item pool."""

    display_name = "Salubra Shop Slots"
    default = 5
    range_start = 0
    range_end = 16


class SalubraCharmShopSlots(Range):
    """For each extra slot, add a location to the Salubra Shop (requiring Charms), and a filler item to the item
    pool."""

    display_name = "Salubra Charm Shop Slots"
    default = 5
    range_end = 16


class LegEaterShopSlots(Range):
    """For each extra slot, add a location to the Leg Eater Shop and a filler item to the item pool."""

    display_name = "Leg Eater Shop Slots"
    default = 3
    range_end = 16


class GrubfatherRewardSlots(Range):
    """For each extra slot, add a location to the Grubfather and a filler item to the item pool."""

    display_name = "Grubfather Reward Slots"
    default = 7
    range_end = 16


class SeerRewardSlots(Range):
    """For each extra slot, add a location to the Seer and a filler item to the item pool."""

    display_name = "Seer Reward Reward Slots"
    default = 8
    range_end = 16


class EggShopSlots(Range):
    """For each slot, add a location to the Egg Shop and a filler item to the item pool."""

    display_name = "Egg Shop Item Slots"
    range_end = 16


class ExtraShopSlots(Range):
    """For each extra slot, add a location to a randomly chosen shop a filler item to the item pool.

    The Egg Shop will be excluded from this list unless it has at least one item.

    Shops are capped at 16 items each.
    """

    display_name = "Additional Shop Slots"
    default = 0
    range_end = 9 * 16  # Number of shops x max slots per shop.


class Goal(Choice):
    """The goal required of you in order to complete your run in Archipelago."""
    display_name = "Goal"
    option_any = 0
    option_hollowknight = 1
    option_siblings = 2
    option_radiance = 3
    option_godhome = 4
    option_godhome_flower = 5
    option_grub_hunt = 6
    default = 0


class GrubHuntGoal(NamedRange):
    """The amount of grubs required to finish Grub Hunt.
    On 'All' any grubs from item links replacements etc. will be counted"""
    display_name = "Grub Hunt Goal"
    range_start = 1
    range_end = 46
    special_range_names = {"all": -1}
    default = 46


class WhitePalace(Choice):
    """
    Whether or not to include White Palace or not.  Note: Even if excluded, the King Fragment check may still be
    required if charms are vanilla.
    """
    display_name = "White Palace"
    option_exclude = 0  # No White Palace at all
    option_kingfragment = 1  # Include King Fragment check only
    option_nopathofpain = 2  # Exclude Path of Pain locations.
    option_include = 3  # Include all White Palace locations, including Path of Pain.
    default = 0


class ExtraPlatforms(DefaultOnToggle):
    """Places additional platforms to make traveling throughout Hallownest more convenient."""
    display_name = "Extra Platforms"


class AddUnshuffledLocations(Toggle):
    """Adds non-randomized locations to the location pool, which allows syncing
    of location state with co-op or automatic collection via collect.

    Note: This will increase the number of location checks required to purchase
    hints to the total maximum.
    """
    display_name = "Add Unshuffled Locations"


class DeathLinkShade(Choice):
    """Sets whether to create a shade when you are killed by a DeathLink and how to handle your existing shade, if any.

    vanilla: DeathLink deaths function like any other death and overrides your existing shade (including geo), if any.
    shadeless: DeathLink deaths do not spawn shades. Your existing shade (including geo), if any, is untouched.
    shade: DeathLink deaths spawn a shade if you do not have an existing shade. Otherwise, it acts like shadeless.

    * This option has no effect if DeathLink is disabled.
    ** Self-death shade behavior is not changed; if a self-death normally creates a shade in vanilla, it will override
        your existing shade, if any.
    """
    option_vanilla = 0
    option_shadeless = 1
    option_shade = 2
    default = 2
    display_name = "Deathlink Shade Handling"


class DeathLinkBreaksFragileCharms(Toggle):
    """Sets if fragile charms break when you are killed by a DeathLink.

    * This option has no effect if DeathLink is disabled.
    ** Self-death fragile charm behavior is not changed; if a self-death normally breaks fragile charms in vanilla, it
        will continue to do so.
    """
    display_name = "Deathlink Breaks Fragile Charms"


class StartingGeo(Range):
    """The amount of starting geo you have."""
    display_name = "Starting Geo"
    range_start = 0
    range_end = 1000
    default = 0


class CostSanity(Choice):
    """If enabled, most locations with costs (like stag stations) will have randomly determined costs.
    If set to shopsonly, CostSanity will only apply to shops (including Grubfather, Seer and Egg Shop).
    If set to notshops, CostSanity will only apply to non-shops (e.g. Stag stations and Cornifer locations)

    These costs can be in Geo (except Grubfather, Seer and Eggshop), Grubs, Charms, Essence and/or Rancid Eggs
    """
    option_off = 0
    alias_no = 0
    option_on = 1
    alias_yes = 1
    option_shopsonly = 2
    option_notshops = 3
    display_name = "Costsanity"


class CostSanityHybridChance(Range):
    """The chance that a CostSanity cost will include two components instead of one, e.g. Grubs + Essence"""
    range_end = 100
    default = 10
    display_name = "Costsanity Hybrid Chance"


cost_sanity_weights: typing.Dict[str, type(Option)] = {}
for term, cost in cost_terms.items():
    option_name = f"CostSanity{cost.option}Weight"
    display_name = f"Costsanity {cost.option} Weight"
    extra_data = {
        "__module__": __name__, "range_end": 1000,
        "__doc__": (
            f"The likelihood of Costsanity choosing a {cost.option} cost."
            " Chosen as a sum of all weights from other types."
        ),
        "default": cost.weight
    }
    if cost == 'GEO':
        extra_data["__doc__"] += " Geo costs will never be chosen for Grubfather, Seer, or Egg Shop."

    option = type(option_name, (Range,), extra_data)
    option.display_name = display_name
    globals()[option.__name__] = option
    cost_sanity_weights[option.__name__] = option

hollow_knight_options: typing.Dict[str, type(Option)] = {
    **hollow_knight_randomize_options,
    RandomizeElevatorPass.__name__: RandomizeElevatorPass,
    **hollow_knight_logic_options,
    **{
        option.__name__: option
        for option in (
            StartLocation, Goal, GrubHuntGoal, WhitePalace, ExtraPlatforms, AddUnshuffledLocations, StartingGeo,
            DeathLink, DeathLinkShade, DeathLinkBreaksFragileCharms,
            MinimumGeoPrice, MaximumGeoPrice,
            MinimumGrubPrice, MaximumGrubPrice,
            MinimumEssencePrice, MaximumEssencePrice,
            MinimumCharmPrice, MaximumCharmPrice,
            RandomCharmCosts, PlandoCharmCosts,
            MinimumEggPrice, MaximumEggPrice, EggShopSlots,
            SlyShopSlots, SlyKeyShopSlots, IseldaShopSlots,
            SalubraShopSlots, SalubraCharmShopSlots,
            LegEaterShopSlots, GrubfatherRewardSlots,
            SeerRewardSlots, ExtraShopSlots,
            SplitCrystalHeart, SplitMothwingCloak, SplitMantisClaw,
            CostSanity, CostSanityHybridChance
        )
    },
    **cost_sanity_weights
}

HKOptions = make_dataclass("HKOptions", [(name, option) for name, option in hollow_knight_options.items()], bases=(PerGameCommonOptions,))
