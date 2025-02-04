from ...options import SeasonRandomization, Fishsanity, ExcludeGingerIsland, SkillProgression, ToolProgression, ElevatorProgression, SpecialOrderLocations
from ...strings.fish_names import Fish
from ...test import SVTestBase


class TestNeedRegionToCatchFish(SVTestBase):
    options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_disabled,
        ElevatorProgression.internal_name: ElevatorProgression.option_vanilla,
        SkillProgression.internal_name: SkillProgression.option_vanilla,
        ToolProgression.internal_name: ToolProgression.option_vanilla,
        Fishsanity.internal_name: Fishsanity.option_all,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi,
    }

    def test_catch_fish_requires_region_unlock(self):
        fish_and_items = {
            Fish.crimsonfish: ["Beach Bridge"],
            Fish.void_salmon: ["Railroad Boulder Removed", "Dark Talisman"],
            Fish.woodskip: ["Glittering Boulder Removed", "Progressive Weapon"],  # For the ores to get the axe upgrades
            Fish.mutant_carp: ["Rusty Key"],
            Fish.slimejack: ["Railroad Boulder Removed", "Rusty Key"],
            Fish.lionfish: ["Boat Repair"],
            Fish.blue_discus: ["Island Obelisk", "Island West Turtle"],
            Fish.stingray: ["Boat Repair", "Island Resort"],
            Fish.ghostfish: ["Progressive Weapon"],
            Fish.stonefish: ["Progressive Weapon"],
            Fish.ice_pip: ["Progressive Weapon", "Progressive Weapon"],
            Fish.lava_eel: ["Progressive Weapon", "Progressive Weapon", "Progressive Weapon"],
            Fish.sandfish: ["Bus Repair"],
            Fish.scorpion_carp: ["Desert Obelisk"],
            # Starting the extended family quest requires having caught all the legendaries before, so they all have the rules of every other legendary
            Fish.son_of_crimsonfish: ["Beach Bridge", "Island Obelisk", "Island West Turtle", "Qi Walnut Room", "Rusty Key"],
            Fish.radioactive_carp: ["Beach Bridge", "Rusty Key", "Boat Repair", "Island West Turtle", "Qi Walnut Room"],
            Fish.glacierfish_jr: ["Beach Bridge", "Island Obelisk", "Island West Turtle", "Qi Walnut Room", "Rusty Key"],
            Fish.legend_ii: ["Beach Bridge", "Island Obelisk", "Island West Turtle", "Qi Walnut Room", "Rusty Key"],
            Fish.ms_angler: ["Beach Bridge", "Island Obelisk", "Island West Turtle", "Qi Walnut Room", "Rusty Key"],
        }
        self.original_state = self.multiworld.state.copy()
        for fish in fish_and_items:
            with self.subTest(f"Region rules for {fish}"):
                self.collect_all_the_money()
                item_names = fish_and_items[fish]
                location = self.multiworld.get_location(f"Fishsanity: {fish}", self.player)
                self.assert_cannot_reach_location(location, self.multiworld.state)
                items = []
                for item_name in item_names:
                    items.append(self.collect(item_name))
                with self.subTest(f"{fish} can be reached with {item_names}"):
                    self.assert_can_reach_location(location, self.multiworld.state)
                for item_required in items:
                    self.multiworld.state = self.original_state.copy()
                    with self.subTest(f"{fish} requires {item_required.name}"):
                        for item_to_collect in items:
                            if item_to_collect.name != item_required.name:
                                self.collect(item_to_collect)
                        self.assert_cannot_reach_location(location, self.multiworld.state)

            self.multiworld.state = self.original_state.copy()
