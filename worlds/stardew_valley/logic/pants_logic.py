from .base_logic import BaseLogicMixin, BaseLogic
from ..data.pants_data import all_considered_pants


class PantsLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pants = PantsLogic(*args, **kwargs)


class PantsLogic(BaseLogic):

    def initialize_rules(self):
        self.registry.pants_rules.update({
            pants.name: self.logic.tailoring.can_tailor_pants(pants) for pants in all_considered_pants
        })
