from ...options import SeasonRandomization, Friendsanity, FriendsanityHeartSize
from ...test import SVTestBase


class TestFriendsanityDatingRules(SVTestBase):
    options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized_not_winter,
        Friendsanity.internal_name: Friendsanity.option_all_with_marriage,
        FriendsanityHeartSize.internal_name: 3
    }

    def test_earning_dating_heart_requires_dating(self):
        self.collect_all_the_money()
        self.multiworld.state.collect(self.create_item("Fall"))
        self.multiworld.state.collect(self.create_item("Beach Bridge"))
        self.multiworld.state.collect(self.create_item("Progressive House"))
        for i in range(3):
            self.multiworld.state.collect(self.create_item("Progressive Pickaxe"))
            self.multiworld.state.collect(self.create_item("Progressive Weapon"))
            self.multiworld.state.collect(self.create_item("Progressive Axe"))
            self.multiworld.state.collect(self.create_item("Progressive Barn"))
        for i in range(10):
            self.multiworld.state.collect(self.create_item("Foraging Level"))
            self.multiworld.state.collect(self.create_item("Farming Level"))
            self.multiworld.state.collect(self.create_item("Mining Level"))
            self.multiworld.state.collect(self.create_item("Combat Level"))
            self.multiworld.state.collect(self.create_item("Progressive Mine Elevator"))
            self.multiworld.state.collect(self.create_item("Progressive Mine Elevator"))

        npc = "Abigail"
        heart_name = f"{npc} <3"
        step = 3

        self.assert_can_reach_heart_up_to(npc, 3, step)
        self.multiworld.state.collect(self.create_item(heart_name))
        self.assert_can_reach_heart_up_to(npc, 6, step)
        self.multiworld.state.collect(self.create_item(heart_name))
        self.assert_can_reach_heart_up_to(npc, 8, step)
        self.multiworld.state.collect(self.create_item(heart_name))
        self.assert_can_reach_heart_up_to(npc, 10, step)
        self.multiworld.state.collect(self.create_item(heart_name))
        self.assert_can_reach_heart_up_to(npc, 14, step)

    def assert_can_reach_heart_up_to(self, npc: str, max_reachable: int, step: int):
        prefix = "Friendsanity: "
        suffix = " <3"
        for i in range(1, max_reachable + 1):
            if i % step != 0 and i != 14:
                continue
            location = f"{prefix}{npc} {i}{suffix}"
            can_reach = self.world.logic.region.can_reach_location(location)(self.multiworld.state)
            self.assertTrue(can_reach, f"Should be able to earn relationship up to {i} hearts")
        for i in range(max_reachable + 1, 14 + 1):
            if i % step != 0 and i != 14:
                continue
            location = f"{prefix}{npc} {i}{suffix}"
            can_reach = self.world.logic.region.can_reach_location(location)(self.multiworld.state)
            self.assertFalse(can_reach, f"Should not be able to earn relationship up to {i} hearts")
