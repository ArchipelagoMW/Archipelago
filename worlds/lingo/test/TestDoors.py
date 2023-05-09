from . import LingoTestBase


class TestRequiredRoomLogic(LingoTestBase):
    options = {
        "shuffle_doors": "complex"
    }

    def test_pilgrim_first(self) -> None:
        assert not self.multiworld.state.can_reach("The Seeker", "Region", self.player)
        assert not self.multiworld.state.can_reach("Pilgrim Antechamber", "Region", self.player)
        assert not self.multiworld.state.can_reach("Pilgrim Room", "Region", self.player)
        assert not self.multiworld.state.can_reach("The Seeker - Achievement", "Location", self.player)

        self.collect_by_name("Pilgrim Room - Sun Painting")
        assert not self.multiworld.state.can_reach("The Seeker", "Region", self.player)
        assert self.multiworld.state.can_reach("Pilgrim Antechamber", "Region", self.player)
        assert self.multiworld.state.can_reach("Pilgrim Room", "Region", self.player)
        assert not self.multiworld.state.can_reach("The Seeker - Achievement", "Location", self.player)

        self.collect_by_name("Pilgrim Room - Shortcut to The Seeker")
        assert self.multiworld.state.can_reach("The Seeker", "Region", self.player)
        assert self.multiworld.state.can_reach("Pilgrim Room", "Region", self.player)
        assert not self.multiworld.state.can_reach("The Seeker - Achievement", "Location", self.player)

        self.collect_by_name("Starting Room - Back Right Door")
        assert self.multiworld.state.can_reach("The Seeker - Achievement", "Location", self.player)

    def test_hidden_first(self) -> None:
        assert not self.multiworld.state.can_reach("The Seeker", "Region", self.player)
        assert not self.multiworld.state.can_reach("Pilgrim Room", "Region", self.player)
        assert not self.multiworld.state.can_reach("The Seeker - Achievement", "Location", self.player)

        self.collect_by_name("Starting Room - Back Right Door")
        assert not self.multiworld.state.can_reach("The Seeker", "Region", self.player)
        assert not self.multiworld.state.can_reach("Pilgrim Room", "Region", self.player)
        assert not self.multiworld.state.can_reach("The Seeker - Achievement", "Location", self.player)

        self.collect_by_name("Pilgrim Room - Shortcut to The Seeker")
        assert not self.multiworld.state.can_reach("The Seeker", "Region", self.player)
        assert not self.multiworld.state.can_reach("Pilgrim Room", "Region", self.player)
        assert not self.multiworld.state.can_reach("The Seeker - Achievement", "Location", self.player)

        self.collect_by_name("Pilgrim Room - Sun Painting")
        assert self.multiworld.state.can_reach("The Seeker", "Region", self.player)
        assert self.multiworld.state.can_reach("Pilgrim Room", "Region", self.player)
        assert self.multiworld.state.can_reach("The Seeker - Achievement", "Location", self.player)


class TestRequiredDoorLogic(LingoTestBase):
    options = {
        "shuffle_doors": "complex"
    }

    def test_through_rhyme(self) -> None:
        assert not self.multiworld.state.can_reach("Rhyme Room - Circle/Looped Square Wall", "Location", self.player)

        self.collect_by_name("Starting Room - Rhyme Room Entrance")
        assert not self.multiworld.state.can_reach("Rhyme Room - Circle/Looped Square Wall", "Location", self.player)

        self.collect_by_name("Rhyme Room (Looped Square) - Door to Circle")
        assert self.multiworld.state.can_reach("Rhyme Room - Circle/Looped Square Wall", "Location", self.player)

    def test_through_hidden(self) -> None:
        assert not self.multiworld.state.can_reach("Rhyme Room - Circle/Looped Square Wall", "Location", self.player)

        self.collect_by_name("Starting Room - Rhyme Room Entrance")
        assert not self.multiworld.state.can_reach("Rhyme Room - Circle/Looped Square Wall", "Location", self.player)

        self.collect_by_name("Starting Room - Back Right Door")
        assert not self.multiworld.state.can_reach("Rhyme Room - Circle/Looped Square Wall", "Location", self.player)

        self.collect_by_name("Hidden Room - Rhyme Room Entrance")
        assert self.multiworld.state.can_reach("Rhyme Room - Circle/Looped Square Wall", "Location", self.player)


class TestSimpleDoors(LingoTestBase):
    options = {
        "shuffle_doors": "simple"
    }

    def test_requirement(self):
        assert not self.multiworld.state.can_reach("Outside The Wanderer", "Region", self.player)
        assert not self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player)

        self.collect_by_name("Rhyme Room Doors")
        assert self.multiworld.state.can_reach("Outside The Wanderer", "Region", self.player)
        assert self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player)

