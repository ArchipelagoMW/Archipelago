from . import LingoTestBase


class TestComplexProgressiveHallwayRoom(LingoTestBase):
    options = {
        "shuffle_doors": "complex"
    }

    def test_item(self):
        assert not self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player)
        assert not self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Elements Area", "Region", self.player)

        self.collect_by_name("Starting Room - Main Door")
        self.collect_by_name("Second Room - Exit Door")
        self.collect_by_name("The Tenacious - Shortcut to Hub Room")
        self.collect_by_name("Outside The Agreeable - Tenacious Entrance")
        assert self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player)
        assert not self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Elements Area", "Region", self.player)

        progressive_hallway_room = self.get_items_by_name("Progressive Hallway Room")

        self.collect(progressive_hallway_room[0])
        assert self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player)
        assert self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Elements Area", "Region", self.player)

        self.collect(progressive_hallway_room[1])
        assert self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player)
        assert self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player)
        assert self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Elements Area", "Region", self.player)

        self.collect(progressive_hallway_room[2])
        assert self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player)
        assert self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player)
        assert self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player)
        assert self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Elements Area", "Region", self.player)

        self.collect(progressive_hallway_room[3])
        assert self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player)
        assert self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player)
        assert self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player)
        assert self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player)
        assert self.multiworld.state.can_reach("Elements Area", "Region", self.player)


class TestSimpleHallwayRoom(LingoTestBase):
    options = {
        "shuffle_doors": "simple"
    }

    def test_item(self):
        assert not self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player)
        assert not self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Elements Area", "Region", self.player)

        self.collect_by_name("Entry Doors")
        self.collect_by_name("Entrances to The Tenacious")
        assert self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player)
        assert not self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Elements Area", "Region", self.player)

        self.collect_by_name("Hallway Room Doors")
        assert self.multiworld.state.can_reach("Outside The Agreeable", "Region", self.player)
        assert self.multiworld.state.can_reach("Hallway Room (2)", "Region", self.player)
        assert self.multiworld.state.can_reach("Hallway Room (3)", "Region", self.player)
        assert self.multiworld.state.can_reach("Hallway Room (4)", "Region", self.player)
        assert self.multiworld.state.can_reach("Elements Area", "Region", self.player)


class TestProgressiveArtGallery(LingoTestBase):
    options = {
        "shuffle_doors": "complex"
    }

    def test_item(self):
        assert not self.multiworld.state.can_reach("Art Gallery", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery - ONE ROAD MANY TURNS", "Location", self.player)
        assert not self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player)

        self.collect_by_name("Starting Room - Main Door")
        self.collect_by_name("Second Room - Exit Door")
        self.collect_by_name("Crossroads - Tower Entrance")
        self.collect_by_name("Orange Tower Fourth Floor - Hot Crusts Door")
        assert self.multiworld.state.can_reach("Art Gallery", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery - ONE ROAD MANY TURNS", "Location", self.player)
        assert not self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player)

        progressive_gallery_room = self.get_items_by_name("Progressive Art Gallery")

        self.collect(progressive_gallery_room[0])
        assert self.multiworld.state.can_reach("Art Gallery", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery - ONE ROAD MANY TURNS", "Location", self.player)
        assert not self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player)

        self.collect(progressive_gallery_room[1])
        assert self.multiworld.state.can_reach("Art Gallery", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery - ONE ROAD MANY TURNS", "Location", self.player)
        assert not self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player)

        self.collect(progressive_gallery_room[2])
        assert self.multiworld.state.can_reach("Art Gallery", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery - ONE ROAD MANY TURNS", "Location", self.player)
        assert not self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player)

        self.collect(progressive_gallery_room[3])
        assert self.multiworld.state.can_reach("Art Gallery", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery - ONE ROAD MANY TURNS", "Location", self.player)
        assert not self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player)

        self.collect(progressive_gallery_room[4])
        assert self.multiworld.state.can_reach("Art Gallery", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery - ONE ROAD MANY TURNS", "Location", self.player)
        assert self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player)


class TestNoDoorsArtGallery(LingoTestBase):
    options = {
        "shuffle_doors": "none",
        "shuffle_colors": "true"
    }

    def test_item(self):
        assert not self.multiworld.state.can_reach("Art Gallery", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery - ONE ROAD MANY TURNS", "Location", self.player)
        assert not self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player)

        self.collect_by_name("Yellow")
        assert self.multiworld.state.can_reach("Art Gallery", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery - ONE ROAD MANY TURNS", "Location", self.player)
        assert not self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player)

        self.collect_by_name("Brown")
        assert self.multiworld.state.can_reach("Art Gallery", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery - ONE ROAD MANY TURNS", "Location", self.player)
        assert not self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player)

        self.collect_by_name("Blue")
        assert self.multiworld.state.can_reach("Art Gallery", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player)
        assert not self.multiworld.state.can_reach("Art Gallery - ONE ROAD MANY TURNS", "Location", self.player)
        assert not self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player)

        self.collect_by_name("Orange")
        self.collect_by_name("Gray")
        assert self.multiworld.state.can_reach("Art Gallery", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Second Floor)", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Third Floor)", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery (Fourth Floor)", "Region", self.player)
        assert self.multiworld.state.can_reach("Art Gallery - ONE ROAD MANY TURNS", "Location", self.player)
        assert self.multiworld.state.can_reach("Orange Tower Fifth Floor", "Region", self.player)
