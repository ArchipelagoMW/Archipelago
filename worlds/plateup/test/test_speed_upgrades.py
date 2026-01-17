from worlds.plateup.test.bases import PlateUpTestBase


class TestPlayerSpeedItemCount(PlateUpTestBase):
    options = {
        "goal": 1,  # Complete x days
        "day_count": 30,
        "player_speed_upgrade_count": 5,
        "appliance_speed_mode": 0,
        "appliance_speed_upgrade_count": 2,
    }

    def test_player_speed_item_count(self) -> None:
        items = [i for i in self.multiworld.itempool if i.player == self.player]
        player_speed = [i for i in items if i.name == "Speed Upgrade Player"]
        self.assertEqual(len(player_speed), 5)

    def test_appliance_grouped_count(self) -> None:
        items = [i for i in self.multiworld.itempool if i.player == self.player]
        grouped = [i for i in items if i.name == "Speed Upgrade Appliance"]
        self.assertEqual(len(grouped), 2)


class TestApplianceSeparateCounts(PlateUpTestBase):
    options = {
        "goal": 1,
        "day_count": 30,
        "player_speed_upgrade_count": 0,
        "appliance_speed_mode": 1,
        "appliance_speed_upgrade_count": 3,
    }

    def test_player_speed_disabled(self) -> None:
        items = [i for i in self.multiworld.itempool if i.player == self.player]
        player_speed = [i for i in items if i.name == "Speed Upgrade Player"]
        self.assertEqual(len(player_speed), 0)

    def test_appliance_separate_counts(self) -> None:
        items = [i for i in self.multiworld.itempool if i.player == self.player]
        cooks = [i for i in items if i.name == "Speed Upgrade Cook"]
        cleans = [i for i in items if i.name == "Speed Upgrade Clean"]
        chops = [i for i in items if i.name == "Speed Upgrade Chop"]
        self.assertEqual(len(cooks), 3)
        self.assertEqual(len(cleans), 3)
        self.assertEqual(len(chops), 3)
