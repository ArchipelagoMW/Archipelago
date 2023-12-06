from typing import Union

from ..mod_regions import SVERegion
from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...logic.combat_logic import CombatLogicMixin
from ...logic.cooking_logic import CookingLogicMixin
from ...logic.has_logic import HasLogicMixin
from ...logic.money_logic import MoneyLogicMixin
from ...logic.quest_logic import QuestLogicMixin
from ...logic.received_logic import ReceivedLogicMixin
from ...logic.region_logic import RegionLogicMixin
from ...logic.relationship_logic import RelationshipLogicMixin
from ...logic.season_logic import SeasonLogicMixin
from ...logic.time_logic import TimeLogicMixin
from ...logic.tool_logic import ToolLogicMixin
from ...strings.ap_names.mods.mod_items import SVELocation, SVERunes
from ...strings.quest_names import ModQuest
from ...stardew_rule import Or


class SVELogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sve = SVELogic(*args, **kwargs)


class SVELogic(BaseLogic[Union[HasLogicMixin, ReceivedLogicMixin, QuestLogicMixin, RegionLogicMixin, RelationshipLogicMixin, TimeLogicMixin, ToolLogicMixin,
               CookingLogicMixin, MoneyLogicMixin, CombatLogicMixin, SeasonLogicMixin]]):
    def initialize_rules(self):
        self.registry.sve_location_rules.update({
            SVELocation.tempered_galaxy_sword: self.logic.money.can_spend_at(SVERegion.alesia_shop, 350000),
            SVELocation.tempered_galaxy_dagger: self.logic.money.can_spend_at(SVERegion.isaac_shop, 600000),
            SVELocation.tempered_galaxy_hammer: self.logic.money.can_spend_at(SVERegion.isaac_shop, 400000),
        })

    def has_any_rune(self):
        rune_list = SVERunes.nexus_items
        return Or(*(self.logic.received(rune) for rune in rune_list))
