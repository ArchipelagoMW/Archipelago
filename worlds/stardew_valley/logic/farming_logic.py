from ..stardew_rule import StardewRule, True_
from .skill_logic import SkillLogic
from .crop_logic import CropLogic


class FarmingLogic:
    player: int
    crop: CropLogic
    skill: SkillLogic

    def __init__(self, player: int, crop: CropLogic, skill: SkillLogic):
        self.player = player
        self.crop = crop
        self.skill = skill

    def can_grow_gold_quality(self, quality: int) -> StardewRule:
        if quality <= 0:
            return True_()
        if quality == 1:
            return self.skill.has_farming_level(5) | (self.crop.has_fertilizer(1) & self.skill.has_farming_level(2)) | (
                    self.crop.has_fertilizer(2) & self.skill.has_farming_level(1)) | self.crop.has_fertilizer(3)
        if quality == 2:
            return self.skill.has_farming_level(10) | (
                        self.crop.has_fertilizer(1) & self.skill.has_farming_level(5)) | (
                    self.crop.has_fertilizer(2) & self.skill.has_farming_level(3)) | (
                    self.crop.has_fertilizer(3) & self.skill.has_farming_level(2))
        if quality >= 3:
            return self.crop.has_fertilizer(3) & self.skill.has_farming_level(4)

