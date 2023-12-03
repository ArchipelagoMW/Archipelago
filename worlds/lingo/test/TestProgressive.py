from . import LingoTestBase


class TestComplexProgressiveHallwayRoom(LingoTestBase):
    options = {
        "shuffle_doors": "complex"
    }

    def test_item(self):
        self.assertFalse(self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Elements Area", "Region", self.player))

        self.collect_by_name(["Second Room - Exit Door", "The Tenacious - Shortcut to Hub Room",
                              "Outside The Agreeable - Tenacious Entrance"])
        self.assertTrue(self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Elements Area", "Region", self.player))

        progressive_hallway_room = self.get_items_by_name("Progressive Hallway Room")

        self.collect(progressive_hallway_room[0])
        self.assertTrue(self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Elements Area", "Region", self.player))

        self.collect(progressive_hallway_room[1])
        self.assertTrue(self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Elements Area", "Region", self.player))

        self.collect(progressive_hallway_room[2])
        self.assertTrue(self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Elements Area", "Region", self.player))

        self.collect(progressive_hallway_room[3])
        self.assertTrue(self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Elements Area", "Region", self.player))


class TestSimpleHallwayRoom(LingoTestBase):
    options = {
        "shuffle_doors": "simple"
    }

    def test_item(self):
        self.assertFalse(self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Elements Area", "Region", self.player))

        self.collect_by_name(["Second Room - Exit Door", "Entrances to The Tenacious"])
        self.assertTrue(self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Elements Area", "Region", self.player))

        self.collect_by_name("Hallway Room Doors")
        self.assertTrue(self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Elements Area", "Region", self.player))


class TestProgressiveArtGallery(LingoTestBase):
    options = {
        "shuffle_doors": "complex",
        "shuffle_colors": "false",
    }

    def test_item(self):
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player))
        self.assertFalse(self.can_reach_location("Art Gallery - ONE ROAD MANY TURNS"))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player))

        self.collect_by_name(["Second Room - Exit Door", "Crossroads - Tower Entrance",
                              "Orange Tower Fourth Floor - Hot Crusts Door"])
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player))
        self.assertFalse(self.can_reach_location("Art Gallery - ONE ROAD MANY TURNS"))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player))

        progressive_gallery_room = self.get_items_by_name("Progressive Art Gallery")

        self.collect(progressive_gallery_room[0])
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player))
        self.assertFalse(self.can_reach_location("Art Gallery - ONE ROAD MANY TURNS"))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player))

        self.collect(progressive_gallery_room[1])
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player))
        self.assertFalse(self.can_reach_location("Art Gallery - ONE ROAD MANY TURNS"))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player))

        self.collect(progressive_gallery_room[2])
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player))
        self.assertFalse(self.can_reach_location("Art Gallery - ONE ROAD MANY TURNS"))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player))

        self.collect(progressive_gallery_room[3])
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player))
        self.assertTrue(self.can_reach_location("Art Gallery - ONE ROAD MANY TURNS"))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player))

        self.collect(progressive_gallery_room[4])
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player))
        self.assertTrue(self.can_reach_location("Art Gallery - ONE ROAD MANY TURNS"))
        self.assertTrue(self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player))


class TestNoDoorsArtGallery(LingoTestBase):
    options = {
        "shuffle_doors": "none",
        "shuffle_colors": "true"
    }

    def test_item(self):
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player))
        self.assertFalse(self.can_reach_location("Art Gallery - ONE ROAD MANY TURNS"))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player))

        self.collect_by_name("Yellow")
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player))
        self.assertFalse(self.can_reach_location("Art Gallery - ONE ROAD MANY TURNS"))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player))

        self.collect_by_name("Brown")
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player))
        self.assertFalse(self.can_reach_location("Art Gallery - ONE ROAD MANY TURNS"))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player))

        self.collect_by_name("Blue")
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player))
        self.assertFalse(self.can_reach_location("Art Gallery - ONE ROAD MANY TURNS"))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player))

        self.collect_by_name(["Orange", "Gray"])
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player))
        self.assertTrue(self.can_reach_location("Art Gallery - ONE ROAD MANY TURNS"))
        self.assertTrue(self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player))
