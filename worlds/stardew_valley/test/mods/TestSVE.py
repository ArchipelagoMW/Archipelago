from ..bases import SVTestBase
from ... import options
from ...mods.mod_data import ModNames
from ...strings.ap_names.mods.mod_items import SVEQuestItem
from ...strings.quest_names import ModQuest
from ...strings.region_names import SVERegion


class TestAuroraVineyard(SVTestBase):
    options = {
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.Mods.internal_name: frozenset({ModNames.sve})
    }

    def test_need_tablet_to_do_quest(self):
        self.collect("Starfruit Seeds")
        self.collect("Bus Repair")
        self.collect("Shipping Bin")
        self.collect("Summer")
        location_name = ModQuest.AuroraVineyard
        self.assert_cannot_reach_location(location_name, self.multiworld.state)
        self.collect(SVEQuestItem.aurora_vineyard_tablet)
        self.assert_can_reach_location(location_name, self.multiworld.state)

    def test_need_reclamation_to_go_downstairs(self):
        region_name = SVERegion.aurora_vineyard_basement
        self.assert_cannot_reach_region(region_name, self.multiworld.state)
        self.collect(SVEQuestItem.aurora_vineyard_reclamation, 1)
        self.assert_can_reach_region(region_name, self.multiworld.state)
