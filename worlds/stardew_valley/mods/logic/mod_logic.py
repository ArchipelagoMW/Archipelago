from .buildings_logic import ModBuildingLogicMixin
from .deepwoods_logic import DeepWoodsLogicMixin
from .elevator_logic import ModElevatorLogicMixin
from .item_logic import ModItemLogicMixin
from .magic_logic import MagicLogicMixin
from .quests_logic import ModQuestLogicMixin
from .skills_logic import ModSkillLogicMixin
from .special_orders_logic import ModSpecialOrderLogicMixin
from .sve_logic import SVELogicMixin
from ...logic.base_logic import BaseLogicMixin


class ModLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mod = ModLogic(*args, **kwargs)


class ModLogic(ModElevatorLogicMixin, MagicLogicMixin, ModSkillLogicMixin, ModItemLogicMixin, ModQuestLogicMixin, ModBuildingLogicMixin,
               ModSpecialOrderLogicMixin, DeepWoodsLogicMixin, SVELogicMixin):
    pass
