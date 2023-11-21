from .buildings_logic import ModBuildingLogic
from .deepwoods_logic import DeepWoodsLogic
from .elevator_logic import ModElevatorLogicMixin
from .item_logic import ModItemLogic
from .magic_logic import MagicLogicMixin
from .quests_logic import ModQuestLogic
from .skills_logic import ModSkillLogicMixin
from .special_orders_logic import ModSpecialOrderLogic
from .sve_logic import SVELogic
from ...logic.ability_logic import AbilityLogic
from ...logic.base_logic import LogicRegistry, BaseLogicMixin
from ...logic.cooking_logic import CookingLogic
from ...logic.crafting_logic import CraftingLogic
from ...logic.fishing_logic import FishingLogic
from ...logic.mine_logic import MineLogic
from ...logic.quest_logic import QuestLogic
from ...logic.region_logic import RegionLogicMixin
from ...logic.skill_logic import SkillLogic
from ...options import SkillProgression, ElevatorProgression, Mods


class ModLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mod = None


class ModLogic(ModElevatorLogicMixin, MagicLogicMixin, ModSkillLogicMixin):
    items: ModItemLogic
    quests: ModQuestLogic
    region: RegionLogicMixin
    buildings: ModBuildingLogic
    special_orders: ModSpecialOrderLogic
    deepwoods: DeepWoodsLogic
    sve: SVELogic

    def __init__(self, player: int, registry: LogicRegistry, options, logic, skill_option: SkillProgression, elevator_option: ElevatorProgression, mods: Mods,
                 skill: SkillLogic, fishing: FishingLogic, cooking: CookingLogic, mine: MineLogic, ability: AbilityLogic,
                 quest: QuestLogic, crafting: CraftingLogic):
        super().__init__(player, registry, options, logic)
        self.item = ModItemLogic(mods, logic.combat, logic.crop, cooking, logic.has, logic.money, logic.region, logic.season, logic.relationship, logic.museum, logic.tool, crafting)
        self.quests = ModQuestLogic(mods, logic.received, logic.has, logic.region, logic.time, logic.season, logic.relationship)
        self.buildings = ModBuildingLogic(player, registry, options, logic)
        self.special_orders = ModSpecialOrderLogic(player, logic.action, logic.artisan, crafting, logic.crop, logic.has, logic.region, logic.relationship,
                                                   logic.season, logic.wallet, mods)
        self.deepwoods = DeepWoodsLogic(player, skill_option, elevator_option, logic.received, logic.has, logic.combat, logic.tool, skill, cooking)
        self.sve = SVELogic(player, skill_option, logic.received, logic.has, quest, logic.region, logic.action, logic.relationship, logic.building, logic.tool,
                            fishing, cooking, logic.money, logic.combat, logic.season, logic.time)
