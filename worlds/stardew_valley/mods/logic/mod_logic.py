from typing import List, Iterable

from .buildings_logic import ModBuildingLogic
from .deepwoods_logic import DeepWoodsLogic
from .elevator_logic import ModElevatorLogic
from .magic_logic import MagicLogic
from .quests_logic import QuestLogic
from .skills_logic import ModSkillLogic
from .special_orders_logic import ModSpecialOrderLogic
from ...logic.ability_logic import AbilityLogic
from ...logic.action_logic import ActionLogic
from ...logic.building_logic import BuildingLogic
from ...logic.combat_logic import CombatLogic
from ...logic.cooking_logic import CookingLogic
from ...logic.fishing_logic import FishingLogic
from ...logic.has_logic import HasLogic
from ...logic.mine_logic import MineLogic
from ...logic.money_logic import MoneyLogic
from ...logic.received_logic import ReceivedLogic
from ...logic.region_logic import RegionLogic
from ...logic.relationship_logic import RelationshipLogic
from ...logic.season_logic import SeasonLogic
from ...logic.skill_logic import SkillLogic
from ...logic.tool_logic import ToolLogic
from ...logic.wallet_logic import WalletLogic
from ...options import SkillProgression, ElevatorProgression, Mods


class ModLogic:
    quests: QuestLogic
    magic: MagicLogic
    buildings: ModBuildingLogic
    special_orders: ModSpecialOrderLogic
    elevator: ModElevatorLogic
    deepwoods: DeepWoodsLogic
    skill: ModSkillLogic

    def __init__(self, player: int, skill_option: SkillProgression, elevator_option: ElevatorProgression, mods: Mods, received: ReceivedLogic, has: HasLogic, region: RegionLogic,
                 action: ActionLogic, season: SeasonLogic, money: MoneyLogic, relationship: RelationshipLogic, building: BuildingLogic, wallet: WalletLogic,
                 combat: CombatLogic, tool: ToolLogic, skill: SkillLogic, fishing: FishingLogic, cooking: CookingLogic, mine: MineLogic, ability: AbilityLogic):
        self.magic = MagicLogic(player, mods, received, region)
        self.quests = QuestLogic(mods, has, region, season, relationship)
        self.buildings = ModBuildingLogic(player, has, money, mods)
        self.special_orders = ModSpecialOrderLogic(player, has, region, relationship, wallet, mods)
        self.elevator = ModElevatorLogic(player, elevator_option, mods, received)
        self.deepwoods = DeepWoodsLogic(player, skill_option, elevator_option, received, has, combat, tool, skill, cooking)
        self.skill = ModSkillLogic(player, skill_option, received, has, region, action, relationship, building, tool, fishing, cooking, self.magic, mods)
        combat.set_magic(self.magic)
        tool.set_magic(self.magic)
        ability.set_magic(self.magic, self.skill)
        skill.set_mod_logic(self.magic, mods)
        mine.set_modded_elevator(self.elevator)
