from abc import ABC, abstractmethod
from typing import ClassVar

from ...data.skill import Skill


def to_level_item_name(skill: Skill) -> str:
    return f"Progressive {skill.name} Level"


def to_level_location_name(skill: Skill, level: int) -> str:
    assert 0 < level <= 10
    return f"Level {level} {skill.name}"


class SkillProgressionFeature(ABC):
    is_enabled: ClassVar[bool]

    to_level_item_name = staticmethod(to_level_item_name)
    to_level_location_name = staticmethod(to_level_location_name)

    @abstractmethod
    def is_included(self, skill: Skill) -> bool:
        ...

    @abstractmethod
    def is_mastery_included(self, skill: Skill) -> bool:
        ...


class SkillProgressionVanilla(SkillProgressionFeature):
    is_enabled = False

    def is_included(self, skill: Skill) -> bool:
        return False

    def is_mastery_included(self, skill: Skill) -> bool:
        return False


class SkillProgressionProgressive(SkillProgressionFeature):
    is_enabled = True

    def is_included(self, skill: Skill) -> bool:
        return True

    def is_mastery_included(self, skill: Skill) -> bool:
        return False


class SkillProgressionProgressiveWithMasteries(SkillProgressionFeature):
    is_enabled = True

    def is_included(self, skill: Skill) -> bool:
        return True

    def is_mastery_included(self, skill: Skill) -> bool:
        return True
