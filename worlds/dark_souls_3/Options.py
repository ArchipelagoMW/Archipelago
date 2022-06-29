import typing
from Options import Toggle, Option


class AutoEquipOption(Toggle):
    display_name = "Auto Equip"


class LockEquipOption(Toggle):
    display_name = "Lock Equip"


class NoWeaponRequirementsOption(Toggle):
    display_name = "No Weapon Requirements"


class RandomizeWeaponsLevelOption(Toggle):
    display_name = "Randomize weapons level"


class PriorityLocationsPresetOption(Toggle):
    display_name = "Priority locations preset"


class LateBasinOfVowsOption(Toggle):
    display_name = "Late Basin of Vows"


dark_souls_options: typing.Dict[str, type(Option)] = {
    "auto_equip": AutoEquipOption,
    "lock_equip": LockEquipOption,
    "no_weapon_requirements": NoWeaponRequirementsOption,
    "randomize_weapons_level": RandomizeWeaponsLevelOption,
    "priority_locations_preset": PriorityLocationsPresetOption,
    "late_basin_of_vows": LateBasinOfVowsOption,
}

