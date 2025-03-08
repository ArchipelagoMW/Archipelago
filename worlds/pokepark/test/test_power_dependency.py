from . import PokeparkTest
from .. import REGIONS
from ..logic import PowerRequirement

class TestPowerItemDependenciesWithoutStartPower(PokeparkTest):
    options = {
        "power_randomizer": 4
    }

    def test_can_battle(self)-> None:
        """Test all locations that use the can battle requirement"""
        battle_locations = [region.display + " - "+location.name for region in REGIONS for location in region.friendship_locations if hasattr(location, 'requirements') and location.requirements and hasattr(location.requirements, 'powers') and location.requirements.powers == PowerRequirement.can_battle]

        items = [["Progressive Dash"], ["Progressive Thunderbolt"], ["Progressive Iron Tail"]]
        self.assertAccessDependency(battle_locations,items, True)

    def test_can_dash_overworld(self)-> None:
        """Test all locations that use the can dash in the overworld requirement"""
        battle_locations = [region.display + " - "+location.name for region in REGIONS for location in region.friendship_locations if hasattr(location, 'requirements') and location.requirements and hasattr(location.requirements, 'powers') and location.requirements.powers == PowerRequirement.can_dash_overworld]

        items = [["Progressive Dash"]]
        self.assertAccessDependency(battle_locations,items, True)

    def test_can_play_catch(self)-> None:
        """Test all locations that use the can play catch requirement"""
        battle_locations = [region.display + " - "+location.name for region in REGIONS for location in region.friendship_locations if hasattr(location, 'requirements') and location.requirements and hasattr(location.requirements, 'powers') and location.requirements.powers == PowerRequirement.can_play_catch]

        items = [["Progressive Dash"]]
        self.assertAccessDependency(battle_locations,items, True)

    def test_can_destroy_objects_overworld(self)-> None:
        """Test all locations that use the can destroy objects in the overworld requirement"""
        battle_locations = [region.display + " - "+location.name for region in REGIONS for location in region.friendship_locations if hasattr(location, 'requirements') and location.requirements and hasattr(location.requirements, 'powers') and location.requirements.powers == PowerRequirement.can_destroy_objects_overworld]

        items = [["Progressive Dash"], ["Progressive Thunderbolt"]]
        self.assertAccessDependency(battle_locations,items, True)

    def test_can_thunderbolt_overworld(self)-> None:
        """Test all locations that use the can use thunderbolt in the overworld requirement"""
        battle_locations = [region.display + " - "+location.name for region in REGIONS for location in region.friendship_locations if hasattr(location, 'requirements') and location.requirements and hasattr(location.requirements, 'powers') and location.requirements.powers == PowerRequirement.can_thunderbolt_overworld]

        items = [["Progressive Thunderbolt"]]
        self.assertAccessDependency(battle_locations,items, True)

    def test_can_battle_thunderbolt_immune(self)-> None:
        """Test all locations that use the can battle thunderbolt immune Pokemon requirement"""
        battle_locations = [region.display + " - "+location.name for region in REGIONS for location in region.friendship_locations if hasattr(location, 'requirements') and location.requirements and hasattr(location.requirements, 'powers') and location.requirements.powers == PowerRequirement.can_battle_thunderbolt_immune]

        items = [["Progressive Dash"], ["Progressive Iron Tail"]]
        self.assertAccessDependency(battle_locations,items, True)

    def test_can_farm_berries(self)-> None:
        """Test all locations that use the can farm berries requirement"""
        battle_locations = [region.display + " - "+location.name for region in REGIONS for location in region.friendship_locations if hasattr(location, 'requirements') and location.requirements and hasattr(location.requirements, 'powers') and location.requirements.powers == PowerRequirement.can_farm_berries]

        items = [["Progressive Dash"]]
        self.assertAccessDependency(battle_locations,items, True)
