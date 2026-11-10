from .base_logic import BaseLogicMixin, BaseLogic
from ..data.shirt_data import all_considered_shirts


class ShirtLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shirt = ShirtLogic(*args, **kwargs)


class ShirtLogic(BaseLogic):

    def initialize_rules(self):
        self.registry.shirt_rules.update({
            shirt.name: self.logic.tailoring.can_tailor_shirt(shirt) for shirt in all_considered_shirts
        })
