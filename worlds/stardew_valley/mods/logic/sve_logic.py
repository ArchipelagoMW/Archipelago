from typing import Union

from ..mod_regions import SVERegion
from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...logic.combat_logic import CombatLogicMixin
from ...logic.cooking_logic import CookingLogicMixin
from ...logic.fishing_logic import FishingLogicMixin
from ...logic.has_logic import HasLogicMixin
from ...logic.money_logic import MoneyLogicMixin
from ...logic.quest_logic import QuestLogicMixin
from ...logic.received_logic import ReceivedLogicMixin
from ...logic.region_logic import RegionLogicMixin
from ...logic.relationship_logic import RelationshipLogicMixin
from ...logic.season_logic import SeasonLogicMixin
from ...logic.time_logic import TimeLogicMixin
from ...logic.tool_logic import ToolLogicMixin
from ...stardew_rule import Or


class SVELogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sve = SVELogic(*args, **kwargs)


class SVELogic(BaseLogic[Union[HasLogicMixin, ReceivedLogicMixin, QuestLogicMixin, RegionLogicMixin, RelationshipLogicMixin, TimeLogicMixin, ToolLogicMixin,
FishingLogicMixin, CookingLogicMixin, MoneyLogicMixin, CombatLogicMixin, SeasonLogicMixin]]):
    def initialize_rules(self):
        self.registry.sve_location_rules.update({
            "Alesia: Tempered Galaxy Dagger": self.logic.region.can_reach(
                SVERegion.alesia_shop) & self.logic.combat.has_galaxy_weapon() &
                                              self.logic.money.can_spend(350000) & self.logic.time.has_lived_months(3),
            "Issac: Tempered Galaxy Sword": self.logic.region.can_reach(
                SVERegion.issac_shop) & self.logic.combat.has_galaxy_weapon() &
                                            self.logic.money.can_spend(600000),
            "Issac: Tempered Galaxy Hammer": self.logic.region.can_reach(
                SVERegion.issac_shop) & self.logic.combat.has_galaxy_weapon() &
                                             self.logic.money.can_spend(400000),
            "Lance's Diamond Wand": self.logic.quest.can_complete_quest("Monster Crops") & self.logic.region.can_reach(
                SVERegion.lances_house),
        })

    def has_any_rune(self):
        rune_list = ["Nexus: Adventurer's Guild Runes", "Nexus: Junimo Woods Runes", "Nexus: Aurora Vineyard Runes", "Nexus: Sprite Spring Runes",
                     "Nexus: Outpost Runes", "Nexus: Farm Runes", "Nexus: Wizard Runes"]
        return Or(*(self.logic.received(rune) for rune in rune_list))
