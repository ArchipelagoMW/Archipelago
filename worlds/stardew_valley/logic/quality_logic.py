from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .farming_logic import FarmingLogicMixin
from .skill_logic import SkillLogicMixin
from ..stardew_rule import StardewRule, True_, False_
from ..strings.quality_names import CropQuality


class QualityLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quality = QualityLogic(*args, **kwargs)


class QualityLogic(BaseLogic):

    @cache_self1
    def can_grow_crop_quality(self, quality: str) -> StardewRule:
        if quality == CropQuality.basic:
            return True_()
        if quality == CropQuality.silver:
            return self.logic.skill.has_farming_level(5) | (self.logic.farming.has_fertilizer(1) & self.logic.skill.has_farming_level(2)) | (
                    self.logic.farming.has_fertilizer(2) & self.logic.skill.has_farming_level(1)) | self.logic.farming.has_fertilizer(3)
        if quality == CropQuality.gold:
            return self.logic.skill.has_farming_level(10) | (
                    self.logic.farming.has_fertilizer(1) & self.logic.skill.has_farming_level(5)) | (
                    self.logic.farming.has_fertilizer(2) & self.logic.skill.has_farming_level(3)) | (
                    self.logic.farming.has_fertilizer(3) & self.logic.skill.has_farming_level(2))
        if quality == CropQuality.iridium:
            return self.logic.farming.has_fertilizer(3) & self.logic.skill.has_farming_level(4)
        return False_()
