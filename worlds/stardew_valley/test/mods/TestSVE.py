import random

from BaseClasses import get_seed
from .. import SVTestBase, SVTestCase, allsanity_no_mods_6_x_x, allsanity_mods_6_x_x, solo_multiworld, \
    fill_dataclass_with_default
from ..assertion import ModAssertMixin, WorldAssertMixin
from ... import items, Group, ItemClassification, create_content
from ... import options
from ...items import items_by_group
from ...mods.mod_data import ModNames
from ...options import SkillProgression, Walnutsanity
from ...regions import RandomizationFlag, randomize_connections, create_final_connections_and_regions
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
        location = self.multiworld.get_location(location_name, self.player)
        self.assert_reach_location_false(location, self.multiworld.state)
        self.collect(SVEQuestItem.aurora_vineyard_tablet, 1)
        self.assert_reach_location_true(location, self.multiworld.state)

    def test_need_reclamation_to_go_downstairs(self):
        region_name = SVERegion.aurora_vineyard_basement
        region = self.multiworld.get_region(region_name, self.player)
        self.assertFalse(region.can_reach(self.multiworld.state))
        self.collect(SVEQuestItem.aurora_vineyard_reclamation, 1)
        self.assertTrue(region.can_reach(self.multiworld.state))
