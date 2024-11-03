from BaseClasses import CollectionState
from . import GSTestBase
from .. import LocationName, ItemName


class TestRevealHiddenItem(GSTestBase):

    def test_hidden_requires_reveal(self):
        world = self.get_world()
        location = world.get_location(LocationName.Daila_Sleep_Bomb)
        self.assertFalse(location.can_reach(world.multiworld.state))
        self.collect_by_name(ItemName.Reveal)
        self.assertTrue(location.can_reach(world.multiworld.state))

class TestRevealNotRequiredForHidden(GSTestBase):
    options = {
        "reveal_hidden_item": 0
    }

    def test_hidden_available(self):
        world = self.get_world()
        location = world.get_location(LocationName.Daila_Sleep_Bomb)
        self.assertFalse(world.multiworld.state.has(ItemName.Reveal, world.player, 1))
        self.assertTrue(location.can_reach(world.multiworld.state))


# TODO: Test Omit Locations

# TODO: test add_elvenshirt_clericsring

class TestVanillaShip(GSTestBase):

    def test_no_ship(self):
        world = self.get_world()
        self.assertFalse(world.multiworld.state.has(ItemName.Ship, world.player, 1))


class TestFastShip(GSTestBase):
    options = {
        "lemurian_ship": 1
    }

    def test_no_ship(self):
        world = self.get_world()
        self.assertFalse(world.multiworld.state.has(ItemName.Ship, world.player, 1))

class TestStartWithShip(GSTestBase):
    options = {
        "lemurian_ship": 2
    }

    def test_has_ship(self):
        world = self.get_world()
        self.assertTrue(world.multiworld.state.has(ItemName.Ship, world.player, 1))

# TODO: Major Minor Option

# TODO: start with wings of anemos
# class TestNoWings(GSTestBase):
#
#     def test_no_wings(self):
#         world = self.get_world()
#         self.assertFalse(world.multiworld.state.has(ItemName))

# TODO: boss means non-junk; though tbh can't we just rely on AP priority?
# TODO: no progression in superboss
# TODO: AnemosAccess