import typing
from .ExtractedData import logic_options, starts, pool_options
from Options import Option, DefaultOnToggle, Toggle, Choice, Range

locations = {"option_" + start: i for i, start in enumerate(starts)}
# This way the dynamic start names are picked up by the MetaClass Choice belongs to
StartLocation = type("StartLocation", (Choice,), {"auto_display_name": False, **locations})
del (locations)

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
    "RandomizeFocus",
    "RandomizeSwim",
    "RandomizeMimics",
    "RandomizeNail",

}

hollow_knight_randomize_options: typing.Dict[str, type(Option)] = {}

for option_name, option_data in pool_options.items():
    extra_data = {"items": option_data[0], "locations": option_data[1]}
    if option_name in default_on:
        option = type(option_name, (DefaultOnToggle,), extra_data)
    else:
        option = type(option_name, (Toggle,), extra_data)
    hollow_knight_randomize_options[option_name] = option

hollow_knight_logic_options: typing.Dict[str, type(Option)] = {
    option_name: Toggle for option_name in logic_options.values() if
    option_name not in hollow_knight_randomize_options
    and option_name != "RandomizeCharmNotches"}


class MinimumGrubPrice(Range):
    display_name = "Minimum Grub Price"
    range_start = 1
    range_end = 46
    default = 1


class MaximumGrubPrice(MinimumGrubPrice):
    display_name = "Maximum Grub Price"
    default = 23


class MinimumEssencePrice(Range):
    display_name = "Minimum Essence Price"
    range_start = 1
    range_end = 2800
    default = 1


class MaximumEssencePrice(MinimumEssencePrice):
    display_name = "Maximum Essence Price"
    default = 1400


class MinimumEggPrice(Range):
    display_name = "Minimum Egg Price"
    range_start = 1
    range_end = 21
    default = 1


class MaximumEggPrice(MinimumEggPrice):
    display_name = "Maximum Egg Price"
    default = 10


class MinimumCharmPrice(Range):
    """For Salubra's Charm-count based locations."""
    display_name = "Minimum Charm Requirement"
    range_start = 1
    range_end = 40
    default = 1


class MaximumCharmPrice(MinimumCharmPrice):
    default = 20


class RandomCharmCosts(Range):
    """Total Cost of all Charms together. Set to -1 for vanilla costs. Vanilla sums to 90."""

    display_name = "Random Charm Costs"
    range_start = -1
    range_end = 240
    default = -1
    vanilla_costs: typing.List[int] = [1, 1, 1, 2, 2, 2, 3, 2, 3, 1, 3, 1, 3, 1, 2, 2, 1, 2, 3, 2,
                                       4, 2, 2, 2, 3, 1, 4, 2, 4, 1, 2, 3, 2, 4, 3, 5, 1, 3, 2, 2]
    charm_count: int = len(vanilla_costs)

    def get_costs(self, random_source) -> typing.List[int]:
        if -1 == self.value:
            return self.vanilla_costs
        else:
            charms = [0]*self.charm_count
            for x in range(self.value):
                index = random_source.randint(0, self.charm_count-1)
                while charms[index] > 5:
                    index = random_source.randint(0, self.charm_count-1)
                charms[index] += 1
            return charms


class EggShopSlots(Range):
    """For each slot, add a location to the Egg Shop and a Geo drop to the item pool."""

    display_name = "Egg Shop Item Slots"
    range_end = 16


hollow_knight_options: typing.Dict[str, type(Option)] = {
    **hollow_knight_randomize_options,
    **hollow_knight_logic_options,
    "start_location": StartLocation,
    "minimum_grub_price": MinimumGrubPrice,
    "maximum_grub_price": MaximumGrubPrice,
    "minimum_essence_price": MinimumEssencePrice,
    "maximum_essence_price": MaximumEssencePrice,
    "minimum_egg_price": MinimumEggPrice,
    "maximum_egg_price": MaximumEggPrice,
    "minimum_charm_price": MinimumCharmPrice,
    "maximum_charm_price": MaximumCharmPrice,
    "random_charm_costs": RandomCharmCosts,
    "egg_shop_slots": EggShopSlots,
}
