from worlds.aquaria.test import AquariaTestBase, after_home_water_locations

class EnergyFormAccessTest(AquariaTestBase):
    options = {
        "early_energy_form": True,
    }

    def test_energy_form_location(self) -> None:
        """Test locations that require Energy form with early energy song enable"""
        locations = [
            "Home water, Nautilus Egg",
            "Naija's home, bulb after the energy door",
            "Energy temple first area, bulb in the bottom room blocked by a rock",
            "Energy temple second area, bulb under the rock",
            "Energy temple bottom entrance, Krotite armor",
            "Energy temple third area, bulb in the bottom path",
            "Energy temple boss area, Fallen god tooth",
            "Energy temple blaster room, Blaster egg",
            *after_home_water_locations
        ]
        items = [["Energy form"]]
        self.assertAccessDependency(locations, items)