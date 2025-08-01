class Skill:
    farming = "Farming"
    foraging = "Foraging"
    fishing = "Fishing"
    mining = "Mining"
    combat = "Combat"


class ModSkill:
    luck = "Luck"
    binning = "Binning"
    archaeology = "Archaeology"
    cooking = "Cooking"
    magic = "Magic"
    socializing = "Socializing"


all_vanilla_skills = {Skill.farming, Skill.foraging, Skill.fishing, Skill.mining, Skill.combat}
all_mod_skills = {ModSkill.luck, ModSkill.binning, ModSkill.archaeology, ModSkill.cooking, ModSkill.magic, ModSkill.socializing}
all_skills = {*all_vanilla_skills, *all_mod_skills}
