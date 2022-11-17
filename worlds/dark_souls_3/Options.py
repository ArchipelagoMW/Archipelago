import typing
from Options import Toggle, Option, DeathLink


class AutoEquipOption(Toggle):
    """Automatically equips any received armor or left/right weapons."""
    display_name = "Auto-equip"


class LockEquipOption(Toggle):
    """Lock the equipment slots so you cannot change your armor or your left/right weapons. Works great with the
    Auto-equip option."""
    display_name = "Lock Equipement Slots"


class NoWeaponRequirementsOption(Toggle):
    """Disable the weapon requirements by removing any movement or damage penalties.
    Permitting you to use any weapon early"""
    display_name = "No Weapon Requirements"


class NoSpellRequirementsOption(Toggle):
    """Disable the spell requirements permitting you to use any spell"""
    display_name = "No Spell Requirements"


class NoEquipLoadOption(Toggle):
    """Disable the equip load constraint from the game"""
    display_name = "No Equip load"


class RandomizeWeaponsLevelOption(Toggle):
    """Enable this option to upgrade 33% ( based on the probability chance ) of the pool of weapons to a random value
    between +1 and +5/+10"""
    display_name = "Randomize weapons level"


class LateBasinOfVowsOption(Toggle):
    """Force the Basin of Vows to be located as a reward of defeating Pontiff Sulyvahn. It permits to ease the
    progression by preventing having to kill the Dancer of the Boreal Valley as the first boss"""
    display_name = "Late Basin of Vows"


dark_souls_options: typing.Dict[str, type(Option)] = {
    "auto_equip": AutoEquipOption,
    "lock_equip": LockEquipOption,
    "no_weapon_requirements": NoWeaponRequirementsOption,
    "randomize_weapons_level": RandomizeWeaponsLevelOption,
    "late_basin_of_vows": LateBasinOfVowsOption,
    "no_spell_requirements": NoSpellRequirementsOption,
    "no_equip_load": NoEquipLoadOption,
    "death_link": DeathLink,
}

