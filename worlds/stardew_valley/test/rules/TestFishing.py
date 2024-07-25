from ...options import SeasonRandomization, Friendsanity, FriendsanityHeartSize, Fishsanity, ExcludeGingerIsland, SkillProgression, ToolProgression, \
    ElevatorProgression
from ...strings.fish_names import Fish
from ...test import SVTestBase


class TestNeedRegionToCatchFish(SVTestBase):
    options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_disabled,
        ElevatorProgression.internal_name: ElevatorProgression.option_vanilla,
        SkillProgression.internal_name: SkillProgression.option_vanilla,
        ToolProgression.internal_name: ToolProgression.option_vanilla,
        Fishsanity.internal_name: Fishsanity.option_all,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false
    }

    def test_catch_fish_requires_region_unlock(self):
        fish_and_items = {Fish.crimsonfish: ["Beach Bridge"],
                          Fish.void_salmon: ["Railroad Boulder Removed", "Dark Talisman"],
                          Fish.woodskip: ["Progressive Weapon", "Progressive Weapon"],  # Weapon to get copper and iron to get the axe upgrades
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
                          }
        for fish in fish_and_items:
            self.original_state = self.multiworld.state.copy()
            self.collect_all_the_money()
            items = fish_and_items[fish]
            with self.subTest(f"{fish} requires {items}"):
                location = self.multiworld.get_location(f"Fishsanity: {fish}", self.player)
                self.assert_reach_location_false(location, self.multiworld.state)
                for item in items:
                    self.collect(item)
                self.assert_reach_location_true(location, self.multiworld.state)
            self.multiworld.state = self.original_state
