from . import LingoTestBase


class TestRequiredRoomLogic(LingoTestBase):
    options = {
        "shuffle_doors": "complex"
    }

    def test_requirement(self) -> None:
        assert not self.multiworld.state.can_reach("The Seeker - Achievement", "Location", self.player)

        self.collect_by_name("Pilgrim Room - Sun Painting")
        assert not self.multiworld.state.can_reach("The Seeker - Achievement", "Location", self.player)

        self.collect_by_name("Pilgrim Room - Shortcut to The Seeker")
        assert not self.multiworld.state.can_reach("The Seeker - Achievement", "Location", self.player)

        self.collect_by_name("Starting Room - Back Right Door")
        assert self.multiworld.state.can_reach("The Seeker - Achievement", "Location", self.player)

        self.remove(self.get_item_by_name("Pilgrim Room - Sun Painting"))
        assert not self.multiworld.state.can_reach("The Seeker - Achievement", "Location", self.player)


class TestRequiredDoorLogic(LingoTestBase):
    options = {
        "shuffle_doors": "complex"
    }

    def test_requirement(self) -> None:
        assert not self.multiworld.state.can_reach("Rhyme Room - Circle/Looped Square Wall", "Location", self.player)

        self.collect_by_name("Starting Room - Rhyme Room Entrance")
        assert not self.multiworld.state.can_reach("Rhyme Room - Circle/Looped Square Wall", "Location", self.player)

        self.collect_by_name("Rhyme Room (Looped Square) - Door to Circle")
        assert self.multiworld.state.can_reach("Rhyme Room - Circle/Looped Square Wall", "Location", self.player)

        self.remove(self.get_item_by_name("Rhyme Room (Looped Square) - Door to Circle"))
        self.collect_by_name("Starting Room - Back Right Door")
        assert not self.multiworld.state.can_reach("Rhyme Room - Circle/Looped Square Wall", "Location", self.player)

        self.collect_by_name("Hidden Room - Rhyme Room Entrance")
        assert self.multiworld.state.can_reach("Rhyme Room - Circle/Looped Square Wall", "Location", self.player)
