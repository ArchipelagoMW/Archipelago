from . import LingoTestBase


class TestDisabledPilgrimage(LingoTestBase):
    options = {
        "enable_pilgrimage": "false",
        "shuffle_colors": "false"
    }

    def test_access(self):
        self.assertFalse(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))
        
        self.collect_by_name("Pilgrim Room - Sun Painting")
        self.assertTrue(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))


class TestPilgrimageWithRoofAndPaintings(LingoTestBase):
    options = {
        "enable_pilgrimage": "true",
        "shuffle_colors": "false",
        "shuffle_doors": "doors",
        "pilgrimage_allows_roof_access": "true",
        "pilgrimage_allows_paintings": "true",
        "early_color_hallways": "false"
    }

    def test_access(self):
        doors = ["Second Room - Exit Door", "Crossroads - Roof Access", "Hub Room - Crossroads Entrance",
                 "Outside The Undeterred - Green Painting"]

        for door in doors:
            self.assertFalse(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))
            self.collect_by_name(door)
        
        self.assertTrue(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))


class TestPilgrimageNoRoofYesPaintings(LingoTestBase):
    options = {
        "enable_pilgrimage": "true",
        "shuffle_colors": "false",
        "shuffle_doors": "doors",
        "pilgrimage_allows_roof_access": "false",
        "pilgrimage_allows_paintings": "true",
        "early_color_hallways": "false"
    }

    def test_access(self):
        doors = ["Second Room - Exit Door", "Crossroads - Roof Access", "Hub Room - Crossroads Entrance",
                 "Outside The Undeterred - Green Painting", "Crossroads - Tower Entrance",
                 "Orange Tower Fourth Floor - Hot Crusts Door", "Orange Tower First Floor - Shortcut to Hub Room",
                 "Starting Room - Street Painting"]

        for door in doors:
            self.assertFalse(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))
            self.collect_by_name(door)
        
        self.assertTrue(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))


class TestPilgrimageNoRoofNoPaintings(LingoTestBase):
    options = {
        "enable_pilgrimage": "true",
        "shuffle_colors": "false",
        "shuffle_doors": "doors",
        "pilgrimage_allows_roof_access": "false",
        "pilgrimage_allows_paintings": "false",
        "early_color_hallways": "false"
    }

    def test_access(self):
        doors = ["Second Room - Exit Door", "Crossroads - Roof Access", "Hub Room - Crossroads Entrance",
                 "Outside The Undeterred - Green Painting", "Orange Tower First Floor - Shortcut to Hub Room",
                 "Starting Room - Street Painting", "Outside The Initiated - Shortcut to Hub Room",
                 "Directional Gallery - Shortcut to The Undeterred", "Orange Tower First Floor - Salt Pepper Door",
                 "Color Hunt - Shortcut to The Steady", "The Bearer - Entrance",
                 "Orange Tower Fifth Floor - Quadruple Intersection", "The Tenacious - Shortcut to Hub Room",
                 "Outside The Agreeable - Tenacious Entrance", "Crossroads - Tower Entrance",
                 "Orange Tower Fourth Floor - Hot Crusts Door"]

        for door in doors:
            self.assertFalse(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))
            self.collect_by_name(door)
        
        self.assertTrue(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))


class TestPilgrimageRequireStartingRoom(LingoTestBase):
    options = {
        "enable_pilgrimage": "true",
        "shuffle_colors": "false",
        "shuffle_doors": "complex",
        "pilgrimage_allows_roof_access": "false",
        "pilgrimage_allows_paintings": "false",
        "early_color_hallways": "false"
    }

    def test_access(self):
        doors = ["Second Room - Exit Door", "Crossroads - Roof Access", "Hub Room - Crossroads Entrance",
                 "Outside The Undeterred - Green Painting", "Outside The Undeterred - Number Hunt",
                 "Starting Room - Street Painting", "Outside The Initiated - Shortcut to Hub Room",
                 "Directional Gallery - Shortcut to The Undeterred", "Orange Tower First Floor - Salt Pepper Door",
                 "Color Hunt - Shortcut to The Steady", "The Bearer - Entrance",
                 "Orange Tower Fifth Floor - Quadruple Intersection", "The Tenacious - Shortcut to Hub Room",
                 "Outside The Agreeable - Tenacious Entrance", "Crossroads - Tower Entrance",
                 "Orange Tower Fourth Floor - Hot Crusts Door", "Challenge Room - Welcome Door",
                 "Number Hunt - Challenge Entrance", "Welcome Back Area - Shortcut to Starting Room"]

        for door in doors:
            self.assertFalse(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))
            self.collect_by_name(door)

        self.assertTrue(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))


class TestPilgrimageYesRoofNoPaintings(LingoTestBase):
    options = {
        "enable_pilgrimage": "true",
        "shuffle_colors": "false",
        "shuffle_doors": "doors",
        "pilgrimage_allows_roof_access": "true",
        "pilgrimage_allows_paintings": "false",
        "early_color_hallways": "false"
    }

    def test_access(self):
        doors = ["Second Room - Exit Door", "Crossroads - Roof Access", "Hub Room - Crossroads Entrance",
                 "Outside The Undeterred - Green Painting", "Orange Tower First Floor - Shortcut to Hub Room",
                 "Starting Room - Street Painting", "Outside The Initiated - Shortcut to Hub Room",
                 "Directional Gallery - Shortcut to The Undeterred", "Orange Tower First Floor - Salt Pepper Door",
                 "Color Hunt - Shortcut to The Steady", "The Bearer - Entrance",
                 "Orange Tower Fifth Floor - Quadruple Intersection"]

        for door in doors:
            self.assertFalse(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))
            self.collect_by_name(door)
        
        self.assertTrue(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))
