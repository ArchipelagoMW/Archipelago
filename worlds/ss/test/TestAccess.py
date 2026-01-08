from . import SSTestBase


class TestAccess(SSTestBase):
    options = {
        "treasuresanity_in_silent_realms": True,
        "trial_treasure_amount": 10,
    }

    def test_trial_entrance(self) -> None:
        """Regression test for trial entrances "no logic" bug"""
        locations = [f"Faron Silent Realm - Relic {idx + 1}" for idx in range(0, 10)]
        locations.append("Faron Silent Realm - Trial Reward")
        items = [["Farore's Courage"]]
        self.assertAccessDependency(locations, items)
