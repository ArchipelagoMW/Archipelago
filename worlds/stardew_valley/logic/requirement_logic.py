import functools
from typing import Union, Iterable

from .base_logic import BaseLogicMixin, BaseLogic
from .book_logic import BookLogicMixin
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .season_logic import SeasonLogicMixin
from .skill_logic import SkillLogicMixin
from .time_logic import TimeLogicMixin
from .tool_logic import ToolLogicMixin
from ..data.game_item import Requirement
from ..data.requirement import ToolRequirement, BookRequirement, SkillRequirement, SeasonRequirement, YearRequirement


class RequirementLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requirement = RequirementLogic(*args, **kwargs)


class RequirementLogic(BaseLogic[Union[RequirementLogicMixin, HasLogicMixin, ReceivedLogicMixin, ToolLogicMixin, SkillLogicMixin, BookLogicMixin,
SeasonLogicMixin, TimeLogicMixin]]):

    def meet_all_requirements(self, requirements: Iterable[Requirement]):
        if not requirements:
            return self.logic.true_
        return self.logic.and_(*(self.logic.requirement.meet_requirement(requirement) for requirement in requirements))

    @functools.singledispatchmethod
    def meet_requirement(self, requirement: Requirement):
        raise ValueError(f"Requirements of type{type(requirement)} have no rule registered.")

    @meet_requirement.register
    def _(self, requirement: ToolRequirement):
        return self.logic.tool.has_tool(requirement.tool, requirement.tier)

    @meet_requirement.register
    def _(self, requirement: SkillRequirement):
        return self.logic.skill.has_level(requirement.skill, requirement.level)

    @meet_requirement.register
    def _(self, requirement: BookRequirement):
        return self.logic.book.has_book_power(requirement.book)

    @meet_requirement.register
    def _(self, requirement: SeasonRequirement):
        return self.logic.season.has(requirement.season)

    @meet_requirement.register
    def _(self, requirement: YearRequirement):
        return self.logic.time.has_year(requirement.year)
