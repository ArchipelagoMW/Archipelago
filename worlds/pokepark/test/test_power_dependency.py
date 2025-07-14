from . import PokeparkTest


class TestPowerItemDependenciesWithoutStartPower(PokeparkTest):
    options = {
        "power_randomizer": 4
    }

    def test_can_battle(self) -> None:
        """Test can battle Power Requirement"""
        battle_locations = ["Meadow Zone - Overworld - Croagunk"]

        items = [["Progressive Dash"], ["Progressive Thunderbolt"], ["Progressive Iron Tail"]]
        self.assertAccessDependency(battle_locations, items, True)

    def test_can_dash_overworld(self) -> None:
        """Test can dash overworld requirement"""
        battle_locations = ["Meadow Zone - Overworld - Caterpie Tree Dash"]

        items = [["Progressive Dash"]]
        self.assertAccessDependency(battle_locations, items, True)

    def test_can_play_catch(self) -> None:
        """Test can play catch requirement"""
        battle_locations = ["Meadow Zone - Overworld - Treecko"]

        items = [["Progressive Dash"]]
        self.assertAccessDependency(battle_locations, items, True)

    def test_can_play_catch_intermediate(self) -> None:
        """Test play catch intermediate requirement"""
        battle_locations = ["Cavern Zone - Overworld - Raichu"]

        items = [["Progressive Dash", "Progressive Dash"]]
        self.assertAccessDependency(battle_locations, items, True)

    def test_can_destroy_objects_overworld(self) -> None:
        """Test  can destroy objects in the overworld requirement"""
        battle_locations = ["Meadow Zone - Overworld - Shroomish Crate Dash"]

        items = [["Progressive Dash"], ["Progressive Thunderbolt"]]
        self.assertAccessDependency(battle_locations, items, True)

    def test_can_thunderbolt_overworld(self) -> None:
        """Test can use thunderbolt in the overworld requirement"""
        battle_locations = ["Meadow Zone - Overworld - Magikarp electrocuted"]

        items = [["Progressive Thunderbolt"]]
        self.assertAccessDependency(battle_locations, items, True)

    def test_can_battle_thunderbolt_immune(self) -> None:
        """Test can battle thunderbolt immune Pokemon requirement"""
        battle_locations = ["Meadow Zone - Overworld - Torterra"]

        items = [["Progressive Dash"], ["Progressive Iron Tail"]]
        self.assertAccessDependency(battle_locations, items, True)

    def test_can_farm_berries(self) -> None:
        """Test can farm berries requirement"""
        battle_locations = ["Treehouse - Iron Tail Upgrade 1"]

        items = [["Progressive Dash"]]
        self.assertAccessDependency(battle_locations, items, True)
