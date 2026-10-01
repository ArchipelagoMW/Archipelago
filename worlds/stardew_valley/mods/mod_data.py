from collections.abc import Iterable
from enum import StrEnum
from typing import final


class ModNames(StrEnum):
    deepwoods = "DeepWoods"
    tractor = "Tractor Mod"
    big_backpack = "Bigger Backpack"
    luck_skill = "Luck Skill"
    magic = "Magic"
    socializing_skill = "Socializing Skill"
    archaeology = "Archaeology"
    cooking_skill = "Cooking Skill"
    binning_skill = "Binning Skill"
    juna = "Juna - Roommate NPC"
    jasper = "Professor Jasper Thomas"
    alec = "Alec Revisited"
    yoba = "Custom NPC - Yoba"
    eugene = "Custom NPC Eugene"
    wellwick = "'Prophet' Wellwick"
    ginger = "Mister Ginger (cat npc)"
    shiko = "Shiko - New Custom NPC"
    delores = "Delores - Custom NPC"
    ayeisha = "Ayeisha - The Postal Worker (Custom NPC)"
    riley = "Custom NPC - Riley"
    skull_cavern_elevator = "Skull Cavern Elevator"
    sve = "Stardew Valley Expanded"
    alecto = "Alecto the Witch"
    distant_lands = "Distant Lands - Witch Swamp Overhaul"
    lacey = "Hat Mouse Lacey"
    boarding_house = "Boarding House and Bus Stop Extension"
    ginger_island = "Ginger Island"

    @staticmethod
    def disabled_mods() -> "set[ModNames]":
        return {
            ModNames.deepwoods,
            ModNames.magic,
            ModNames.cooking_skill,
            ModNames.yoba,
            ModNames.eugene,
            ModNames.wellwick,
            ModNames.shiko,
            ModNames.delores,
            ModNames.riley,
            ModNames.boarding_house,
            ModNames.sve,
            ModNames.ginger_island,  # Not a mod per se, so we can't really consider it enabled...
        }

    @staticmethod
    def enabled_mods() -> "set[ModNames]":
        return set(ModNames).difference(ModNames.disabled_mods())

    @staticmethod
    def enabled_mods_except_invalid_combinations():
        mods = ModNames.enabled_mods()
        for mod_combination in invalid_mod_combinations:
            priority_mod = mod_combination[0]
            if priority_mod not in mods:
                continue

            for mod in mod_combination[1:]:
                mods.discard(mod)

        return mods

    @property
    def is_enabled(self):
        return self not in self.disabled_mods()


invalid_mod_combinations = [
    # [ModNames.sve, ModNames.distant_lands] # This is going to become banned after Reptar's SVE update. For now, it's fine.
]

# Used to adapt content not yet moved to content packs to easily detect when SVE and Ginger Island are both enabled.
SVE_GINGER_ISLAND_PACK = ModNames.sve + "+" + ModNames.ginger_island

def mod_combination_is_valid(mods: Iterable[str]):
    for mod_combination in invalid_mod_combinations:
        if all(mod in mods for mod in mod_combination):
            return False
    return True


def get_invalid_mod_combination(mods: Iterable[str]):
    for mod_combination in invalid_mod_combinations:
        if all(mod in mods for mod in mod_combination):
            return mod_combination
    return None
