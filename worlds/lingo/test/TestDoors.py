from . import LingoTestBase


class TestRequiredRoomLogic(LingoTestBase):
    options = {
        "shuffle_doors": "doors",
        "shuffle_colors": "false",
    }

    def test_pilgrim_first(self) -> None:
        self.assertFalse(self.multiworld.state.can_reach("The Seeker", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Pilgrim Antechamber", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Pilgrim Room", "Region", self.player))
        self.assertFalse(self.can_reach_location("The Seeker - Achievement"))

        self.collect_by_name("Pilgrim Room - Sun Painting")
        self.assertFalse(self.multiworld.state.can_reach("The Seeker", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Pilgrim Antechamber", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Pilgrim Room", "Region", self.player))
        self.assertFalse(self.can_reach_location("The Seeker - Achievement"))

        self.collect_by_name("Pilgrim Room - Shortcut to The Seeker")
        self.assertTrue(self.multiworld.state.can_reach("The Seeker", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Pilgrim Room", "Region", self.player))
        self.assertFalse(self.can_reach_location("The Seeker - Achievement"))

        self.collect_by_name("Starting Room - Back Right Door")
        self.assertTrue(self.can_reach_location("The Seeker - Achievement"))

    def test_hidden_first(self) -> None:
        self.assertFalse(self.multiworld.state.can_reach("The Seeker", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Pilgrim Room", "Region", self.player))
        self.assertFalse(self.can_reach_location("The Seeker - Achievement"))

        self.collect_by_name("Starting Room - Back Right Door")
        self.assertFalse(self.multiworld.state.can_reach("The Seeker", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Pilgrim Room", "Region", self.player))
        self.assertFalse(self.can_reach_location("The Seeker - Achievement"))

        self.collect_by_name("Pilgrim Room - Shortcut to The Seeker")
        self.assertFalse(self.multiworld.state.can_reach("The Seeker", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Pilgrim Room", "Region", self.player))
        self.assertFalse(self.can_reach_location("The Seeker - Achievement"))

        self.collect_by_name("Pilgrim Room - Sun Painting")
        self.assertTrue(self.multiworld.state.can_reach("The Seeker", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Pilgrim Room", "Region", self.player))
        self.assertTrue(self.can_reach_location("The Seeker - Achievement"))


class TestRequiredDoorLogic(LingoTestBase):
    options = {
        "shuffle_doors": "doors",
        "shuffle_colors": "false",
    }

    def test_through_rhyme(self) -> None:
        self.assertFalse(self.can_reach_location("Rhyme Room - Circle/Looped Square Wall"))

        self.collect_by_name("Starting Room - Rhyme Room Entrance")
        self.assertFalse(self.can_reach_location("Rhyme Room - Circle/Looped Square Wall"))

        self.collect_by_name("Rhyme Room (Looped Square) - Door to Circle")
        self.assertTrue(self.can_reach_location("Rhyme Room - Circle/Looped Square Wall"))

    def test_through_hidden(self) -> None:
        self.assertFalse(self.can_reach_location("Rhyme Room - Circle/Looped Square Wall"))

        self.collect_by_name("Starting Room - Rhyme Room Entrance")
        self.assertFalse(self.can_reach_location("Rhyme Room - Circle/Looped Square Wall"))

        self.collect_by_name("Starting Room - Back Right Door")
        self.assertFalse(self.can_reach_location("Rhyme Room - Circle/Looped Square Wall"))

        self.collect_by_name("Hidden Room - Rhyme Room Entrance")
        self.assertTrue(self.can_reach_location("Rhyme Room - Circle/Looped Square Wall"))


class TestSimpleDoors(LingoTestBase):
    options = {
        "shuffle_doors": "doors",
        "group_doors": "true",
        "shuffle_colors": "false",
    }

    def test_requirement(self):
        self.assertFalse(self.multiworld.state.can_reach("Outside The Wanderer", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))

        self.collect_by_name("Rhyme Room Doors")
        self.assertTrue(self.multiworld.state.can_reach("Outside The Wanderer", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))


class TestPanels(LingoTestBase):
    options = {
        "shuffle_doors": "panels"
    }

    def test_requirement(self):
        self.assertFalse(self.can_reach_location("Starting Room - HIDDEN"))
        self.assertFalse(self.can_reach_location("Hidden Room - OPEN"))
        self.assertFalse(self.can_reach_location("The Seeker - Achievement"))

        self.collect_by_name("Starting Room - HIDDEN (Panel)")
        self.assertTrue(self.can_reach_location("Starting Room - HIDDEN"))
        self.assertFalse(self.can_reach_location("Hidden Room - OPEN"))
        self.assertFalse(self.can_reach_location("The Seeker - Achievement"))

        self.collect_by_name("Hidden Room - OPEN (Panel)")
        self.assertTrue(self.can_reach_location("Starting Room - HIDDEN"))
        self.assertTrue(self.can_reach_location("Hidden Room - OPEN"))
        self.assertTrue(self.can_reach_location("The Seeker - Achievement"))


class TestGroupedPanels(LingoTestBase):
    options = {
        "shuffle_doors": "panels",
        "group_doors": "true",
        "shuffle_colors": "false",
    }

    def test_requirement(self):
        self.assertFalse(self.can_reach_location("Hub Room - SLAUGHTER"))
        self.assertFalse(self.can_reach_location("Dread Hallway - DREAD"))
        self.assertFalse(self.can_reach_location("The Tenacious - Achievement"))

        self.collect_by_name("Tenacious Entrance Panels")
        self.assertTrue(self.can_reach_location("Hub Room - SLAUGHTER"))
        self.assertFalse(self.can_reach_location("Dread Hallway - DREAD"))
        self.assertFalse(self.can_reach_location("The Tenacious - Achievement"))

        self.collect_by_name("Outside The Agreeable - BLACK (Panel)")
        self.assertTrue(self.can_reach_location("Hub Room - SLAUGHTER"))
        self.assertTrue(self.can_reach_location("Dread Hallway - DREAD"))
        self.assertFalse(self.can_reach_location("The Tenacious - Achievement"))

        self.collect_by_name("The Tenacious - Black Palindromes (Panels)")
        self.assertTrue(self.can_reach_location("Hub Room - SLAUGHTER"))
        self.assertTrue(self.can_reach_location("Dread Hallway - DREAD"))
        self.assertTrue(self.can_reach_location("The Tenacious - Achievement"))

