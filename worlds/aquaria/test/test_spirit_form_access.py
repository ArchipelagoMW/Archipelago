from worlds.aquaria.test import AquariaTestBase


class SpiritFormAccessTest(AquariaTestBase):

    def test_spirit_form_location(self) -> None:
        """Test locations that require spirit form"""
        locations = [
            "The veil bottom area, bulb in the spirit path",
            "Mithalas city castle, Trident head",
            "Open water skeleton path, King skull",
            "Kelp forest bottom left area, Walker baby",
            "Abyss right area, bulb behind the rock in the whale room",
            "The whale, Verse egg",
            "Ice cave, bulb in the room to the right",
            "Ice cave, First bulbs in the top exit room",
            "Ice cave, Second bulbs in the top exit room",
            "Ice cave, third bulbs in the top exit room",
            "Ice cave, bulb in the left room",
            "Bubble cave, bulb in the left cave wall",
            "Bubble cave, bulb in the right cave wall (behind the ice cristal)",
            "Bubble cave, Verse egg",
            "Sunken city left area, Girl Costume",
            "Beating Mantis Shrimp Prime",
            "First secret",
        ]
        items = [["Spirit form"]]
        self.assertAccessDependency(locations, items)
