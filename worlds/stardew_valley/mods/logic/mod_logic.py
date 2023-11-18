from typing import List, Iterable

from .buildings_logic import ModBuildingLogic
from .deepwoods_logic import DeepWoodsLogic
from .elevator_logic import ModElevatorLogic
from .item_logic import ModItemLogic
from .magic_logic import MagicLogic
from .quests_logic import ModQuestLogic
from .skills_logic import ModSkillLogic
from .special_orders_logic import ModSpecialOrderLogic
from .sve_logic import SVELogic
from ...logic.ability_logic import AbilityLogic
from ...logic.action_logic import ActionLogic
from ...logic.artisan_logic import ArtisanLogic
from ...logic.building_logic import BuildingLogic
from ...logic.combat_logic import CombatLogic
from ...logic.cooking_logic import CookingLogic
from ...logic.crafting_logic import CraftingLogic
from ...logic.crop_logic import CropLogic
from ...logic.fishing_logic import FishingLogic
from ...logic.has_logic import HasLogic
from ...logic.mine_logic import MineLogic
from ...logic.money_logic import MoneyLogic
from ...logic.museum_logic import MuseumLogic
from ...logic.quest_logic import QuestLogic
from ...logic.received_logic import ReceivedLogic
from ...logic.region_logic import RegionLogic
from ...logic.relationship_logic import RelationshipLogic
from ...logic.season_logic import SeasonLogic
from ...logic.skill_logic import SkillLogic
from ...logic.time_logic import TimeLogic
from ...logic.tool_logic import ToolLogic
from ...logic.wallet_logic import WalletLogic
from ...options import SkillProgression, ElevatorProgression, Mods


class ModLogic:
    items: ModItemLogic
    quests: ModQuestLogic
    region: RegionLogic
    magic: MagicLogic
    buildings: ModBuildingLogic
    special_orders: ModSpecialOrderLogic
    elevator: ModElevatorLogic
    deepwoods: DeepWoodsLogic
    skill: ModSkillLogic
    sve: SVELogic

    def __init__(self, player: int, skill_option: SkillProgression, elevator_option: ElevatorProgression, mods: Mods, received: ReceivedLogic, has: HasLogic, region: RegionLogic,
                 action: ActionLogic, artisan: ArtisanLogic, season: SeasonLogic, money: MoneyLogic, relationship: RelationshipLogic, museum: MuseumLogic, building: BuildingLogic, wallet: WalletLogic,
                 combat: CombatLogic, tool: ToolLogic, skill: SkillLogic, fishing: FishingLogic, cooking: CookingLogic, mine: MineLogic, ability: AbilityLogic,
                 time: TimeLogic, quest: QuestLogic, crafting: CraftingLogic, crop: CropLogic):
        self.item = ModItemLogic(mods, combat, crop, cooking, has, money, region, season, relationship, museum, tool, crafting)
        self.magic = MagicLogic(player, mods, received, region)
        self.quests = ModQuestLogic(mods, received, has, region, time, season, relationship)
        self.buildings = ModBuildingLogic(player, has, money, mods)
        self.special_orders = ModSpecialOrderLogic(player, action, artisan, crafting, crop, has, region, relationship, season, wallet, mods)
        self.elevator = ModElevatorLogic(player, elevator_option, mods, received)
        self.deepwoods = DeepWoodsLogic(player, skill_option, elevator_option, received, has, combat, tool, skill, cooking)
        self.skill = ModSkillLogic(player, skill_option, received, has, region, action, relationship, building, tool, fishing, cooking, self.magic, mods)
        self.sve = SVELogic(player, skill_option, received, has, quest, region, action, relationship, building, tool, fishing, cooking, money, combat, season, time)
        combat.set_magic(self.magic)
        tool.set_magic(self.magic)
        ability.set_magic(self.magic, self.skill)
        skill.set_mod_logic(self.magic, mods)
        mine.set_modded_elevator(self.elevator)
