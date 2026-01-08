from . import AVTestBase
from .. import conditions

class TestCanDamage(AVTestBase):
    def test_can_damage(self):
        state, context = self.multiworld.state, self.multiworld.worlds[1].context
        self.assertFalse(conditions.can_damage(state, context))

        self.collect_by_name(("Kilver",))
        self.assertTrue(conditions.can_damage(state, context))


class TestHasPowerNodes(AVTestBase):
    def test_threshold(self):
        state, context = self.multiworld.state, self.multiworld.worlds[1].context

        self.collect(self.get_item_by_name("Power Node"))
        self.collect(self.get_item_by_name("Power Node"))
        self.assertFalse(conditions.has_power_nodes(state, context))

        self.collect(self.get_item_by_name("Power Node"))
        assert self.count("Power Node") == 3
        self.assertTrue(conditions.has_power_nodes(state, context))


class TestHasHealthNodes(AVTestBase):
    def test_threshold(self):
        state, context = self.multiworld.state, self.multiworld.worlds[1].context

        self.collect(self.get_item_by_name("Health Node"))
        self.collect(self.get_item_by_name("Health Node"))
        self.assertFalse(conditions.has_health_nodes(state, context))
        print(self.count("Health Node"))
        assert self.count("Health Node") == 2

        self.collect(self.get_item_by_name("Health Node"))
        assert self.count("Health Node") == 3
        self.assertTrue(conditions.has_health_nodes(state, context))


class TestRequireNodesDisabled(AVTestBase):
    options = {
        "require_nodes": 0,
    }

    def test_disabled(self):
        state, context = self.multiworld.state, self.multiworld.worlds[1].context

        self.assertTrue(conditions.has_health_nodes(state, context))
        self.assertTrue(conditions.has_power_nodes(state, context))
