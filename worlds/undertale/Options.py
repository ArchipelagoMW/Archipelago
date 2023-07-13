import typing
from Options import Choice, Option, Toggle, Range


class RouteRequired(Choice):
    """Main route of the game required to win."""
    display_name = "Required Route"
    option_neutral = 0
    option_pacifist = 1
    option_genocide = 2
    option_all_routes = 3
    default = 0


class IncludeTemy(Toggle):
    """Adds Temmy Armor to the item pool."""
    display_name = "Include Temy Armor"
    default = 1


class KeyPieces(Range):
    """How many Key Pieces are added to the pool, only matters with Key Piece Hunt enabled."""
    display_name = "Key Piece Amount"
    default = 5
    range_start = 1
    range_end = 10


class KeyHunt(Toggle):
    """Adds Key Pieces to the item pool, you need all of them to enter the last corridor."""
    display_name = "Key Piece Hunt"
    default = 0


class ProgressiveArmor(Toggle):
    """Makes the armor progressive."""
    display_name = "Progressive Armor"
    default = 0


class ProgressiveWeapons(Toggle):
    """Makes the weapons progressive."""
    display_name = "Progressive Weapons"
    default = 0


class OnlyFlakes(Toggle):
    """Replaces all non-required items, except equipment, with Temmie Flakes."""
    display_name = "Only Temmie Flakes"
    default = 0


class NoEquips(Toggle):
    """Removes all equippable items."""
    display_name = "No Equippables"
    default = 0


class RandomizeLove(Toggle):
    """Adds LOVE to the pool. GENOCIDE ONLY!"""
    display_name = "Randomize LOVE"
    default = 0


class RandomizeStats(Toggle):
    """Makes each stat increase from LV a separate item. GENOCIDE ONLY!
    Warning: This tends to spam chat with sending out checks."""
    display_name = "Randomize Stats"
    default = 0


class RandoBattleOptions(Toggle):
    """Turns the ITEM button in battle into an item you have to receive."""
    display_name = "Randomize Item Button"
    default = 0


undertale_options: typing.Dict[str, type(Option)] = {
    "route_required":                           RouteRequired,
    "key_hunt":                                 KeyHunt,
    "key_pieces":                               KeyPieces,
    "rando_love":                               RandomizeLove,
    "rando_stats":                              RandomizeStats,
    "temy_include":                             IncludeTemy,
    "no_equips":                                NoEquips,
    "only_flakes":                              OnlyFlakes,
    "prog_armor":                               ProgressiveArmor,
    "prog_weapons":                             ProgressiveWeapons,
    "rando_item_button":                     RandoBattleOptions,
}
