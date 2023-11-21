from typing import Union

from .buildings_logic import ModBuildingLogic
from .deepwoods_logic import DeepWoodsLogic
from .elevator_logic import ModElevatorLogic
from .item_logic import ModItemLogic
from .magic_logic import MagicLogic, MagicLogicMixin
from .quests_logic import ModQuestLogic
from .skills_logic import ModSkillLogic
from .special_orders_logic import ModSpecialOrderLogic
from .sve_logic import SVELogic
from ...logic.ability_logic import AbilityLogic
from ...logic.action_logic import ActionLogicMixin
from ...logic.artisan_logic import ArtisanLogicMixin
from ...logic.base_logic import LogicRegistry, BaseLogic, BaseLogicMixin
from ...logic.building_logic import BuildingLogicMixin
from ...logic.combat_logic import CombatLogicMixin
from ...logic.cooking_logic import CookingLogic
from ...logic.crafting_logic import CraftingLogic
from ...logic.crop_logic import CropLogic
from ...logic.fishing_logic import FishingLogic
from ...logic.has_logic import HasLogicMixin
from ...logic.mine_logic import MineLogic
from ...logic.money_logic import MoneyLogicMixin
from ...logic.museum_logic import MuseumLogicMixin
from ...logic.quest_logic import QuestLogic
from ...logic.received_logic import ReceivedLogicMixin
from ...logic.region_logic import RegionLogicMixin
from ...logic.relationship_logic import RelationshipLogicMixin
from ...logic.season_logic import SeasonLogicMixin
from ...logic.skill_logic import SkillLogic
from ...logic.time_logic import TimeLogicMixin
from ...logic.tool_logic import ToolLogic
from ...logic.wallet_logic import WalletLogicMixin
from ...options import SkillProgression, ElevatorProgression, Mods


class ModLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mod = ModLogic(*args, **kwargs)


class ModLogic(BaseLogic[Union[TimeLogicMixin, ReceivedLogicMixin, HasLogicMixin, RegionLogicMixin, ActionLogicMixin, ArtisanLogicMixin, SeasonLogicMixin,
MoneyLogicMixin, MuseumLogicMixin, RelationshipLogicMixin, BuildingLogicMixin, WalletLogicMixin, CombatLogicMixin]], MagicLogicMixin):
    items: ModItemLogic
    quests: ModQuestLogic
    region: RegionLogicMixin
    magic: MagicLogic
    buildings: ModBuildingLogic
    special_orders: ModSpecialOrderLogic
    elevator: ModElevatorLogic
    deepwoods: DeepWoodsLogic
    skill: ModSkillLogic
    sve: SVELogic

    def __init__(self, player: int, registry: LogicRegistry, options, logic, skill_option: SkillProgression, elevator_option: ElevatorProgression, mods: Mods,
                 tool: ToolLogic, skill: SkillLogic, fishing: FishingLogic, cooking: CookingLogic, mine: MineLogic, ability: AbilityLogic,
                 quest: QuestLogic, crafting: CraftingLogic, crop: CropLogic):
        super().__init__(player, registry, options, logic)
        self.item = ModItemLogic(mods, logic.combat, crop, cooking, logic.has, logic.money, logic.region, logic.season, logic.relationship, logic.museum, tool, crafting)
        self.quests = ModQuestLogic(mods, logic.received, logic.has, logic.region, logic.time, logic.season, logic.relationship)
        self.buildings = ModBuildingLogic(player, registry, options, logic)
        self.special_orders = ModSpecialOrderLogic(player, logic.action, logic.artisan, crafting, crop, logic.has, logic.region, logic.relationship,
                                                   logic.season, logic.wallet, mods)
        self.elevator = ModElevatorLogic(player, elevator_option, mods, logic.received)
        self.deepwoods = DeepWoodsLogic(player, skill_option, elevator_option, logic.received, logic.has, logic.combat, tool, skill, cooking)
        self.skill = ModSkillLogic(player, skill_option, logic.received, logic.has, logic.region, logic.action, logic.relationship, logic.buildings, tool,
                                   fishing, cooking, self.magic, mods)
        self.sve = SVELogic(player, skill_option, logic.received, logic.has, quest, logic.region, logic.action, logic.relationship, logic.buildings, tool,
                            fishing, cooking, logic.money, logic.combat, logic.season, logic.time)
        tool.set_magic(self.magic)
        ability.set_magic(self.magic, self.skill)
        skill.set_mod_logic(self.magic, mods)
        mine.set_modded_elevator(self.elevator)
