from . import LingoTestBase


class TestMasteryWhenVictoryIsTheEnd(LingoTestBase):
    options = {
        "mastery_achievements": "22",
        "victory_condition": "the_end",
        "shuffle_colors": "true"
    }

    def test_requirement(self):
        assert not self.multiworld.state.can_reach("Orange Tower Seventh Floor", "Region", self.player)

        self.collect_by_name("Red")
        self.collect_by_name("Blue")
        self.collect_by_name("Black")
        self.collect_by_name("Purple")
        self.collect_by_name("Orange")
        assert self.multiworld.state.can_reach("Orange Tower Seventh Floor", "Region", self.player)
        assert self.multiworld.state.can_reach("The End (Solved)", "Location", self.player)
        assert not self.multiworld.state.can_reach("Orange Tower Seventh Floor - THE MASTER", "Location", self.player)

        self.collect_by_name("Green")
        self.collect_by_name("Brown")
        self.collect_by_name("Yellow")
        assert self.multiworld.state.can_reach("Orange Tower Seventh Floor - THE MASTER", "Location", self.player)


class TestMasteryWhenVictoryIsTheMaster(LingoTestBase):
    options = {
        "mastery_achievements": "24",
        "victory_condition": "the_master",
        "shuffle_colors": "true"
    }

    def test_requirement(self):
        assert not self.multiworld.state.can_reach("Orange Tower Seventh Floor", "Region", self.player)

        self.collect_by_name("Red")
        self.collect_by_name("Blue")
        self.collect_by_name("Black")
        self.collect_by_name("Purple")
        self.collect_by_name("Orange")
        assert self.multiworld.state.can_reach("Orange Tower Seventh Floor", "Region", self.player)
        assert self.multiworld.state.can_reach("Orange Tower Seventh Floor - THE END", "Location", self.player)
        assert not self.multiworld.state.can_reach("Orange Tower Seventh Floor - Mastery Achievements", "Location",
                                                   self.player)

        self.collect_by_name("Green")
        self.collect_by_name("Gray")
        self.collect_by_name("Brown")
        self.collect_by_name("Yellow")
        assert self.multiworld.state.can_reach("Orange Tower Seventh Floor - Mastery Achievements", "Location",
                                               self.player)