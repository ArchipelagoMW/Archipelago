from .has_logic import HasLogicMixin
from .skill_logic import SkillLogic
from ..stardew_rule import StardewRule, True_
from ..strings.fertilizer_names import Fertilizer


class FarmingLogic:
    player: int
    has: HasLogicMixin
    skill: SkillLogic

    def __init__(self, player: int, has: HasLogicMixin, skill: SkillLogic):
        self.player = player
        self.has = has
        self.skill = skill

    def has_fertilizer(self, tier: int) -> StardewRule:
        if tier <= 0:
            return True_()
        if tier == 1:
            return self.has(Fertilizer.basic)
        if tier == 2:
            return self.has(Fertilizer.quality)
        if tier >= 3:
            return self.has(Fertilizer.deluxe)

    def can_grow_crop_quality(self, quality: int) -> StardewRule:
        if quality <= 0:
            return True_()
        if quality == 1:
            return self.skill.has_farming_level(5) | (self.has_fertilizer(1) & self.skill.has_farming_level(2)) | (
                    self.has_fertilizer(2) & self.skill.has_farming_level(1)) | self.has_fertilizer(3)
        if quality == 2:
            return self.skill.has_farming_level(10) | (
                    self.has_fertilizer(1) & self.skill.has_farming_level(5)) | (
                    self.has_fertilizer(2) & self.skill.has_farming_level(3)) | (
                    self.has_fertilizer(3) & self.skill.has_farming_level(2))
        if quality >= 3:
            return self.has_fertilizer(3) & self.skill.has_farming_level(4)
