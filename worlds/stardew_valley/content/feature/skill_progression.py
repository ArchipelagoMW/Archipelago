from abc import ABC, abstractmethod
from typing import ClassVar, Iterable, Tuple

from ...data.skill import Skill


class SkillProgressionFeature(ABC):
    is_progressive: ClassVar[bool]
    are_masteries_shuffled: ClassVar[bool]

    @abstractmethod
    def get_randomized_level_names_by_level(self, skill: Skill) -> Iterable[Tuple[int, str]]:
        ...

    @abstractmethod
    def is_mastery_randomized(self, skill: Skill) -> bool:
        ...


class SkillProgressionVanilla(SkillProgressionFeature):
    is_progressive = False
    are_masteries_shuffled = False

    def get_randomized_level_names_by_level(self, skill: Skill) -> Iterable[Tuple[int, str]]:
        return ()

    def is_mastery_randomized(self, skill: Skill) -> bool:
        return False


class SkillProgressionProgressive(SkillProgressionFeature):
    is_progressive = True
    are_masteries_shuffled = False

    def get_randomized_level_names_by_level(self, skill: Skill) -> Iterable[Tuple[int, str]]:
        return skill.level_names_by_level

    def is_mastery_randomized(self, skill: Skill) -> bool:
        return False


class SkillProgressionProgressiveWithMasteries(SkillProgressionProgressive):
    are_masteries_shuffled = True

    def is_mastery_randomized(self, skill: Skill) -> bool:
        return skill.has_mastery
