from typing import Dict

from ..mod_regions import SVERegion
from ...logic.action_logic import ActionLogicMixin
from ...logic.building_logic import BuildingLogicMixin
from ...logic.combat_logic import CombatLogic
from ...logic.cooking_logic import CookingLogic
from ...logic.fishing_logic import FishingLogic
from ...logic.has_logic import HasLogicMixin
from ...logic.money_logic import MoneyLogicMixin
from ...logic.quest_logic import QuestLogic
from ...logic.received_logic import ReceivedLogicMixin
from ...logic.region_logic import RegionLogicMixin
from ...logic.relationship_logic import RelationshipLogic
from ...logic.season_logic import SeasonLogicMixin
from ...logic.time_logic import TimeLogicMixin
from ...logic.tool_logic import ToolLogic
from ...options import SkillProgression
from ...stardew_rule import StardewRule, Or


class SVELogic:
    player: int
    received: ReceivedLogicMixin
    has: HasLogicMixin
    quest: QuestLogic
    region: RegionLogicMixin
    relationship: RelationshipLogic
    time: TimeLogicMixin
    tool: ToolLogic
    fishing: FishingLogic
    cooking: CookingLogic
    money: MoneyLogicMixin
    combat: CombatLogic
    season: SeasonLogicMixin
    sve_location_rules: Dict[str, StardewRule]

    def __init__(self, player: int, skill_option: SkillProgression, received: ReceivedLogicMixin, has: HasLogicMixin, quest: QuestLogic,
                 region: RegionLogicMixin,
                 action: ActionLogicMixin,
                 relationship: RelationshipLogic, building: BuildingLogicMixin, tool: ToolLogic, fishing: FishingLogic, cooking: CookingLogic,
                 money: MoneyLogicMixin, combat: CombatLogic, season: SeasonLogicMixin, time: TimeLogicMixin):
        self.player = player
        self.skill_option = skill_option
        self.received = received
        self.has = has
        self.quest = quest
        self.region = region
        self.action = action
        self.relationship = relationship
        self.building = building
        self.tool = tool
        self.fishing = fishing
        self.cooking = cooking
        self.time = time
        self.money = money
        self.combat = combat
        self.season = season
        self.sve_location_rules = dict()

    def initialize_rules(self):
        self.sve_location_rules.update({
            "Alesia: Tempered Galaxy Dagger": self.region.can_reach(
                SVERegion.alesia_shop) & self.combat.has_galaxy_weapon() &
                                              self.money.can_spend(350000) & self.time.has_lived_months(3),
            "Issac: Tempered Galaxy Sword": self.region.can_reach(
                SVERegion.issac_shop) & self.combat.has_galaxy_weapon() &
                                            self.money.can_spend(600000),
            "Issac: Tempered Galaxy Hammer": self.region.can_reach(
                SVERegion.issac_shop) & self.combat.has_galaxy_weapon() &
                                             self.money.can_spend(400000),
            "Lance's Diamond Wand": self.quest.can_complete_quest("Monster Crops") & self.region.can_reach(
                SVERegion.lances_house),
        })

    def has_any_rune(self):
        rune_list = ["Nexus: Adventurer's Guild Runes", "Nexus: Junimo Woods Runes", "Nexus: Aurora Vineyard Runes", "Nexus: Sprite Spring Runes",
                     "Nexus: Outpost Runes"]
        return Or(*(self.received(rune) for rune in rune_list))
