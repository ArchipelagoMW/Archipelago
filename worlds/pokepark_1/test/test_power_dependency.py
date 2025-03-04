from . import PokeparkTest

class TestPowerItemDependencies(PokeparkTest):
    def test_thunderbolt_upgrades(self)-> None:
        """Test all locations that require one Thunderbolt Upgrades"""
        locations = []
        items = [["Progressive Thunderbolt"]]
        self.assertAccessDependency(locations,items)

    def test_thunderbolt_upgrades2(self)-> None:
        """Test all locations that require two Thunderbolt Upgrades"""
        locations = []
        items = [["Progressive Thunderbolt"],["Progressive Thunderbolt"]]
        self.assertAccessDependency(locations,items)

    def test_thunderbolt_upgrades3(self)-> None:
        """Test all locations that require three Thunderbolt Upgrades"""
        locations = []
        items = [["Progressive Thunderbolt"],["Progressive Thunderbolt"],["Progressive Thunderbolt"]]
        self.assertAccessDependency(locations,items)

    def test_dash_upgrades(self)-> None:
        """Test all locations that require one Dash Upgrades"""
        locations = []
        items = [["Progressive Dash"]]
        self.assertAccessDependency(locations,items)

    def test_dash_upgrades2(self)-> None:
        """Test all locations that require two Dash Upgrades"""
        locations = []
        items = [["Progressive Dash"],["Progressive Dash"]]
        self.assertAccessDependency(locations,items)

    def test_dash_upgrades3(self)-> None:
        """Test all locations that require three Dash Upgrades"""
        locations = []
        items = [["Progressive Dash"],["Progressive Dash"],["Progressive Dash"]]
        self.assertAccessDependency(locations,items)

    def test_health_upgrades(self)-> None:
        """Test all locations that require one Health Upgrades"""
        locations = []
        items = [["Progressive Health"]]
        self.assertAccessDependency(locations,items)

    def test_health_upgrades2(self)-> None:
        """Test all locations that require two Health Upgrades"""
        locations = []
        items = [["Progressive Health"],["Progressive Health"]]
        self.assertAccessDependency(locations,items)

    def test_health_upgrades3(self)-> None:
        """Test all locations that require three Health Upgrades"""
        locations = []
        items = [["Progressive Health"],["Progressive Health"],["Progressive Health"]]
        self.assertAccessDependency(locations,items)
    def test_iron_tail_upgrades(self)-> None:
        """Test all locations that require one Iron Tail Upgrades"""
        locations = []
        items = [["Progressive Iron Tail"]]
        self.assertAccessDependency(locations,items)

    def test_iron_tail_upgrades2(self)-> None:
        """Test all locations that require two Iron Tail Upgrades"""
        locations = []
        items = [["Progressive Iron Tail"],["Progressive Iron Tail"]]
        self.assertAccessDependency(locations,items)

    def test_iron_tail_upgrades3(self)-> None:
        """Test all locations that require three Iron Tail Upgrades"""
        locations = []
        items = [["Progressive Iron Tail"],["Progressive Iron Tail"],["Progressive Iron Tail"]]
        self.assertAccessDependency(locations,items)