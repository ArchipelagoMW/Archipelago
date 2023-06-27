import typing
from Options import Choice, Option, Toggle, Range
class ProgressiveKeys(Toggle):
    """Makes the keys progressive."""
    display_name = "Progressive Keys"
    default = 0
class ProgressiveAbilities(Toggle):
    """Makes the abilities progressive."""
    display_name = "Progressive Abilities"
    default = 0
class ProgressiveSpells(Toggle):
    """Makes the spells progressive."""
    display_name = "Progressive Spells"
    default = 0


tln_options: typing.Dict[str, type(Option)] = {

    "prog_keys": ProgressiveKeys,
    "prog_abilities": ProgressiveAbilities,
    "prog_spells": ProgressiveSpells,

}
