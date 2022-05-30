import typing
from Options import Toggle, Option


class AutoEquipOption(Toggle):
    # AutoEquip
    display_name = "Auto Equip"


class LockEquipOption(Toggle):
    # AutoEquip
    display_name = "Lock Equip"


class NoWeaponRequirementsOption(Toggle):
    # AutoEquip
    display_name = "No Weapon Requirements"


dark_souls_options: typing.Dict[str, type(Option)] = {
    "auto_equip": AutoEquipOption,
    "lock_equip": LockEquipOption,
    "no_weapon_requirements": NoWeaponRequirementsOption,
}

