import typing
from .ExtractedData import logic_options, starts, pool_options

from Options import Option, DefaultOnToggle, Toggle, Choice, Range, OptionDict, SpecialRange
from .Charms import vanilla_costs, names as charm_names

if typing.TYPE_CHECKING:
    # avoid import during runtime
    from random import Random
else:
    Random = typing.Any


class Disabled(Toggle):
    def __init__(self, value: int):
        super(Disabled, self).__init__(0)

    @classmethod
    def from_text(cls, text: str) -> Toggle:
        return cls(0)

    @classmethod
    def from_any(cls, data: typing.Any):
        return cls(0)


locations = {"option_" + start: i for i, start in enumerate(starts)}
# This way the dynamic start names are picked up by the MetaClass Choice belongs to
StartLocation = type("StartLocation", (Choice,), {"__module__": __name__, "auto_display_name": False, **locations,
                                                  "__doc__": "Choose your start location. "
                                                             "This is currently only locked to King's Pass."})
del (locations)

option_docstrings = {
    "RandomizeDreamers": "Allow for Dreamers to be randomized into the item pool and opens their locations for "
                         "randomization.",
    "RandomizeSkills": "Allow for Skills, such as Mantis Claw or Shade Soul, to be randomized into the item pool. "
                       "Also opens their locations for receiving randomized items.",
    "RandomizeFocus": "Removes the ability to heal and adds it as a randomized item.",
    "RandomizeSwim": "All pools of water become dangerous, and a new Swim item is randomized which allows swimming in"
                     "water normally.",
    "RandomizeCharms": "Allow for Charms to be randomized into the item pool and open their locations for "
                       "randomization. Includes Charms sold in shops.",
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
                                "Roots will now grant a randomized item when completed. This can be previewed by "
                                "standing on the root.",
    "RandomizeBossEssence": "Randomize boss essence drops, such as those for defeating Warrior Dreams, into the item "
                            "pool and open their locations for randomization.",
    "RandomizeGrubs": "Randomize Grubs into the item pool and open their locations for randomization.",
    "RandomizeMaps": "Randomize Maps into the item pool. This causes Cornifer to give you a message allowing you to see"
                     " and buy an item that is randomized into that location as well.",
    "RandomizeStags": "Randomize Stag Stations unlocks into the item pool as well as placing randomized items "
                      "on the stag station bell/toll.",
    "RandomizeLifebloodCocoons": "Randomize Lifeblood Cocoon grants into the item pool and open their locations"
                                 " for randomization.",
    "RandomizeGrimmkinFlames": "Randomize Grimmkin Flames into the item pool and open their locations for "
                               "randomization.",
    "RandomizeJournalEntries": "Randomize the Hunter's Journal as well as the findable journal entries into the item "
                               "pool, and open their locations for randomization. Does not include journal entries "
                               "gained by killing enemies.",
    "RandomizeNail": "Adds three extra items to the pool that allow swinging the nail left, right and up; by default in"
                     "this mode, the nail can only be swung down.",
    "RandomizeGeoRocks": "Randomize Geo Rock rewards into the item pool and open their locations for randomization.",
    "RandomizeBossGeo": "Randomize boss Geo drops into the item pool and open those locations for randomization.",
    "RandomizeSoulTotems": "Randomize Soul Refill items into the item pool and open the Soul Totem locations for"
                           " randomization.",
    "RandomizeLoreTablets": "Randomize Lore items into the itempool, one per Lore Tablet, and place randomized item "
                            "grants on the tablets themselves. You must still read the tablet to get the item.",
    "PreciseMovement": "Places skips into logic which require extremely precise player movement, possibly without "
                       "movement skills such as dash or hook.",
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
    "RandomizePaleOre",
    "RandomizeRelics"
}

# not supported at this time
disabled = {
    "RandomizeMimics",
}

hollow_knight_randomize_options: typing.Dict[str, type(Option)] = {}

for option_name, option_data in pool_options.items():
    extra_data = {"__module__": __name__, "items": option_data[0], "locations": option_data[1]}
    if option_name in option_docstrings:
        extra_data["__doc__"] = option_docstrings[option_name]
    if option_name in disabled:
        extra_data["__doc__"] = "Disabled Option. Not implemented."
        option = type(option_name, (Disabled,), extra_data)
    if option_name in default_on:
        option = type(option_name, (DefaultOnToggle,), extra_data)
    else:
        option = type(option_name, (Toggle,), extra_data)
    globals()[option.__name__] = option
    hollow_knight_randomize_options[option.__name__] = option

hollow_knight_logic_options: typing.Dict[str, type(Option)] = {}
for option_name in logic_options.values():
    if option_name in hollow_knight_randomize_options:
        continue
    extra_data = {"__module__": __name__}
    if option_name in option_docstrings:
        extra_data["__doc__"] = option_docstrings[option_name]
        option = type(option_name, (Toggle,), extra_data)
    if option_name in disabled:
        extra_data["__doc__"] = "Disabled Option. Not implemented."
        option = type(option_name, (Disabled,), extra_data)
    globals()[option.__name__] = option
    hollow_knight_logic_options[option.__name__] = option


class SplitMothwingCloak(Toggle):
    """Replaces Mothwing Cloak with two items, a "Left Mothwing Cloak" that lets you dash to the left, and a
    "Right Mothwing Cloak" that dashes to the right. Also adds a new location dropped after defeating Hornet in
    Greenpath. Randomly adds a second left or right Mothwing cloak item which functions as the upgrade to Shade Cloak."""
    display_name = "Split Mothwing Cloak"
    default = False


class SplitMantisClaw(Toggle):
    """Replaces Mantis Claw with two items, a "Left Mantis Claw" that works only on left walls, and a "Right Mantis
    Claw" that works only on the right. Replaces the Mantis Claw location with two locations in Mantis Village."""
    display_name = "Split Mantis Claw"
    default = False


class SplitCrystalHeart(Toggle):
    """Replaces Crystal Heart with two items, a "Left Crystal Heart" that lets you superdash to the left, and a "Right
    Crystal Heart" that superdashes to the right. Also adds a new location left of the bridge next to the Crystal Heart location."""
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
    """The minimum rancid egg price in the range of prices that an item should cost from Ijii.
    Only takes effect if the EggSlotShops option is greater than 0."""
    display_name = "Minimum Egg Price"
    range_start = 1
    range_end = 21
    default = 1


class MaximumEggPrice(MinimumEggPrice):
    """The maximum rancid egg price in the range of prices that an item should cost from Ijii.
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
    default = 20


class RandomCharmCosts(SpecialRange):
    """Total Notch Cost of all Charms together. Vanilla sums to 90.
    This value is distributed among all charms in a random fashion.
    Special Cases:
    Set to -1 or vanilla for vanilla costs.
    Set to -2 or shuffle to shuffle around the vanilla costs to different charms."""

    display_name = "Randomize Charm Notch Costs"
    range_start = -2
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
            charms = [0]*self.charm_count
            for x in range(self.value):
                index = random_source.randint(0, self.charm_count-1)
                while charms[index] > 5:
                    index = random_source.randint(0, self.charm_count-1)
                charms[index] += 1
            return charms


class PlandoCharmCosts(OptionDict):
    """Allows setting a Charm's Notch costs directly, mapping {name: cost}.
    This is set after any random Charm Notch costs, if applicable."""
    display_name = "Charm Notch Cost Plando"
    valid_keys = frozenset(charm_names)

    def get_costs(self, charm_costs: typing.List[int]) -> typing.List[int]:
        for name, cost in self.value.items():
            charm_costs[charm_names.index(name)] = cost
        return charm_costs


class SlyShopSlots(Range):
    """For each extra slot, add a location to the Sly Shop and a filler item to the item pool."""

    display_name = "Sly Shop Slots"
    default = 8
    range_start = 8
    range_end = 16


class SlyKeyShopSlots(Range):
    """For each extra slot, add a location to the Sly Shop (requiring Shopkeeper's Key) and a filler item to the item pool."""

    display_name = "Sly Key Shop Slots"
    default = 6
    range_start = 6
    range_end = 16


class IseldaShopSlots(Range):
    """For each extra slot, add a location to the Iselda Shop and a filler item to the item pool."""

    display_name = "Iselda Shop Slots"
    default = 2
    range_start = 2
    range_end = 16


class SalubraShopSlots(Range):
    """For each extra slot, add a location to the Salubra Shop, and a filler item to the item pool."""

    display_name = "Salubra Shop Slots"
    default = 5
    range_start = 5
    range_end = 16


class SalubraCharmShopSlots(Range):
    """For each extra slot, add a location to the Salubra Shop (requiring Charms), and a filler item to the item pool."""

    display_name = "Salubra Charm Shop Slots"
    default = 5
    range_start = 5
    range_end = 16


class LegEaterShopSlots(Range):
    """For each extra slot, add a location to the Leg Eater Shop and a filler item to the item pool."""

    display_name = "Leg Eater Shop Slots"
    default = 3
    range_start = 3
    range_end = 16


class GrubfatherRewardSlots(Range):
    """For each extra slot, add a location to the Grubfather and a filler item to the item pool."""

    display_name = "Grubfather Reward Slots"
    default = 7
    range_start = 7
    range_end = 16


class SeerRewardSlots(Range):
    """For each extra slot, add a location to the Seer and a filler item to the item pool."""

    display_name = "Seer Reward Reward Slots"
    default = 8
    range_start = 8
    range_end = 16


class EggShopSlots(Range):
    """For each slot, add a location to the Egg Shop and a filler item to the item pool."""

    display_name = "Egg Shop Item Slots"
    range_end = 16


class Goal(Choice):
    """The goal required of you in order to complete your run in Archipelago."""
    display_name = "Goal"
    option_any = 0
    option_hollowknight = 1
    option_siblings = 2
    option_radiance = 3
    # Client support exists for this, but logic is a nightmare
    # option_godhome = 4
    default = 0


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


class StartingGeo(Range):
    """The amount of starting geo you have."""
    display_name = "Starting Geo"
    range_start = 0
    range_end = 1000
    default = 0


hollow_knight_options: typing.Dict[str, type(Option)] = {
    **hollow_knight_randomize_options,
    **hollow_knight_logic_options,
    SplitCrystalHeart.__name__: SplitCrystalHeart,
    SplitMothwingCloak.__name__: SplitMothwingCloak,
    SplitMantisClaw.__name__: SplitMantisClaw,
    StartLocation.__name__: StartLocation,
    MinimumGrubPrice.__name__: MinimumGrubPrice,
    MaximumGrubPrice.__name__: MaximumGrubPrice,
    MinimumEssencePrice.__name__: MinimumEssencePrice,
    MaximumEssencePrice.__name__: MaximumEssencePrice,
    MinimumCharmPrice.__name__: MinimumCharmPrice,
    MaximumCharmPrice.__name__: MaximumCharmPrice,
    RandomCharmCosts.__name__: RandomCharmCosts,
    PlandoCharmCosts.__name__: PlandoCharmCosts,
    MinimumEggPrice.__name__: MinimumEggPrice,
    MaximumEggPrice.__name__: MaximumEggPrice,
    SlyShopSlots.__name__: SlyShopSlots,
    SlyKeyShopSlots.__name__: SlyKeyShopSlots,
    IseldaShopSlots.__name__: IseldaShopSlots,
    SalubraShopSlots.__name__: SalubraShopSlots,
    SalubraCharmShopSlots.__name__: SalubraCharmShopSlots,
    LegEaterShopSlots.__name__: LegEaterShopSlots,
    GrubfatherRewardSlots.__name__: GrubfatherRewardSlots,
    SeerRewardSlots.__name__: SeerRewardSlots,
    EggShopSlots.__name__: EggShopSlots,
    Goal.__name__: Goal,
    WhitePalace.__name__: WhitePalace,
    StartingGeo.__name__: StartingGeo,
}
