from typing import Iterable


class ModNames:
    vanilla = None
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


invalid_mod_combinations = [
    # [ModNames.sve, ModNames.distant_lands] # This is going to become banned after Reptar's SVE update. For now, it's fine.
]


def mod_combination_is_valid(mods: Iterable[str]):
    for mod_combination in invalid_mod_combinations:
        if all([mod in mods for mod in mod_combination]):
            return False
    return True


def get_invalid_mod_combination(mods: Iterable[str]):
    for mod_combination in invalid_mod_combinations:
        if all([mod in mods for mod in mod_combination]):
            return mod_combination
    return None
