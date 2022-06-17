import typing
from Options import Choice, Option, Toggle, DefaultOnToggle, Range, OptionList, DeathLink


class SupplyChestAmount(Range):
    """How much Psitanium should be given to the player when a Supply Chest is found."""
    display_name = "Chest Psitanium Amount"
    range_start = 1
    range_end = 200
    default = 100


#class RandomizeTags(Toggle):
#    """Randomize Emotional Baggage Tags so that they can appear anywhere."""
#    display_name = "Randomize Tags"


psychonauts2_options: typing.Dict[str, type(Option)] = {
    "supply_chest_amount": SupplyChestAmount
}