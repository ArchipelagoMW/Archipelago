from abc import ABC, abstractmethod
from typing import ClassVar, Sequence, Iterable

from ...data.skill import Skill


def to_level_item_name(skill: Skill) -> str:
    return f"{skill.name} Level"


def to_level_location_name(skill: Skill, level: int) -> str:
    assert 0 < level <= 10
    return f"Level {level} {skill.name}"


class SkillProgressionFeature(ABC):
    is_progressive: ClassVar[bool]
    are_masteries_shuffled: ClassVar[bool]

    to_level_item_name = staticmethod(to_level_item_name)
    to_level_location_name = staticmethod(to_level_location_name)

    @abstractmethod
    def get_randomized_levels(self, skill: Skill) -> Sequence[int]:
        ...

    @abstractmethod
    def get_randomized_level_names(self, skill: Skill) -> Iterable[str]:
        ...

    @abstractmethod
    def is_mastery_randomized(self, skill: Skill) -> bool:
        ...


class SkillProgressionVanilla(SkillProgressionFeature):
    is_progressive = False
    are_masteries_shuffled = False

    def get_randomized_levels(self, skill: Skill) -> Sequence[int]:
        return range(0)

    def get_randomized_level_names(self, skill: Skill) -> Iterable[str]:
        return ()

    def is_mastery_randomized(self, skill: Skill) -> bool:
        return False


class SkillProgressionProgressive(SkillProgressionFeature):
    is_progressive = True
    are_masteries_shuffled = False

    def get_randomized_levels(self, skill: Skill) -> Sequence[int]:
        return skill.levels

    def get_randomized_level_names(self, skill: Skill) -> Iterable[str]:
        return skill.level_names

    def is_mastery_randomized(self, skill: Skill) -> bool:
        return False


class SkillProgressionProgressiveWithMasteries(SkillProgressionFeature):
    is_progressive = True
    are_masteries_shuffled = True

    def get_randomized_levels(self, skill: Skill) -> Sequence[int]:
        return skill.levels

    def get_randomized_level_names(self, skill: Skill) -> Iterable[str]:
        return skill.level_names

    def is_mastery_randomized(self, skill: Skill) -> bool:
        return skill.has_mastery
