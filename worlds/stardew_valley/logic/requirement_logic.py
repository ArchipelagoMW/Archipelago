import functools
from typing import Union, Iterable

from .base_logic import BaseLogicMixin, BaseLogic
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .tool_logic import ToolLogicMixin
from ..data.game_item import Requirement
from ..data.requirement import ToolRequirement, BookRequirement


class RequirementLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requirement = RequirementLogic(*args, **kwargs)


class RequirementLogic(BaseLogic[Union[RequirementLogicMixin, HasLogicMixin, ReceivedLogicMixin, ToolLogicMixin]]):

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
    def _(self, requirement: BookRequirement):
        book_name = requirement.book
        booksanity = self.content.features.booksanity
        if booksanity.is_included(self.content.game_items[book_name]):
            return self.logic.received(booksanity.to_item_name(book_name))
        else:
            return self.logic.has(book_name)
