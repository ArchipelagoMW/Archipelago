from ..bases import SVTestBase
from ... import StartWithoutOptionName
from ...options import SeasonRandomization, Fishsanity, ExcludeGingerIsland, SkillProgression, ToolProgression, ElevatorProgression, SpecialOrderLocations, \
    StartWithout
from ...strings.ap_names.transport_names import Transportation
from ...strings.fish_names import Fish


class TestNeedRegionToCatchFish(SVTestBase):
    options = {
        StartWithout: frozenset({StartWithoutOptionName.landslide, StartWithoutOptionName.community_center}),
        SeasonRandomization.internal_name: SeasonRandomization.option_disabled,
        ElevatorProgression.internal_name: ElevatorProgression.option_vanilla,
        SkillProgression.internal_name: SkillProgression.option_vanilla,
        ToolProgression.internal_name: ToolProgression.option_progressive,
        Fishsanity.internal_name: Fishsanity.option_all,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi,
    }

    def test_catch_fish_requires_region_unlock(self):
        fish_and_items = {
            Fish.crimsonfish: ["Beach Bridge"],
            Fish.void_salmon: ["Railroad Boulder Removed", "Dark Talisman"],
            Fish.woodskip: ["Progressive Axe", "Progressive Axe"],
            Fish.mutant_carp: ["Rusty Key"],
            Fish.slimejack: ["Railroad Boulder Removed", "Rusty Key"],
            Fish.lionfish: [Transportation.boat_repair],
            Fish.blue_discus: ["Wizard Invitation", "Island Obelisk", "Island West Turtle"],
            Fish.stingray: [Transportation.boat_repair, "Island Resort"],
            Fish.ghostfish: ["Landslide Removed", "Progressive Weapon"],
            Fish.stonefish: ["Landslide Removed", "Progressive Weapon"],
            Fish.ice_pip: ["Landslide Removed", "Progressive Weapon", "Progressive Weapon", "Progressive Pickaxe"],
            Fish.lava_eel: ["Landslide Removed", "Progressive Weapon", "Progressive Weapon", "Progressive Weapon", "Progressive Pickaxe", "Progressive Pickaxe"],
            Fish.sandfish: [Transportation.bus_repair],
            Fish.scorpion_carp: ["Wizard Invitation", "Desert Obelisk"],
            # Starting the extended family quest requires having caught all the legendaries before, so they all have the rules of every other legendary
            Fish.son_of_crimsonfish: ["Beach Bridge", Transportation.boat_repair, "Island West Turtle", "Qi Walnut Room", "Rusty Key"],
            Fish.radioactive_carp: ["Beach Bridge", "Rusty Key", Transportation.boat_repair, "Island West Turtle", "Qi Walnut Room"],
            Fish.glacierfish_jr: ["Beach Bridge", Transportation.boat_repair, "Island West Turtle", "Qi Walnut Room", "Rusty Key"],
            Fish.legend_ii: ["Beach Bridge", "Wizard Invitation", "Island Obelisk", "Island West Turtle", "Qi Walnut Room", "Rusty Key"],
            Fish.ms_angler: ["Beach Bridge", "Wizard Invitation", "Island Obelisk", "Island West Turtle", "Qi Walnut Room", "Rusty Key"],
        }
        self.collect("Progressive Fishing Rod", 4)
        self.collect_all_the_money()
        for fish in fish_and_items:
            with self.subTest(f"Region rules for {fish}"):
                item_names = fish_and_items[fish]
                location = f"Fishsanity: {fish}"
                self.assert_cannot_reach_location(location)
                items = [self.create_item(item_name) for item_name in item_names]
                for item in items:
                    self.collect(item)
                with self.subTest(f"{fish} can be reached with {item_names}"):
                    self.assert_can_reach_location(location)
                for item_required in items:
                    with self.subTest(f"{fish} requires {item_required.name}"):
                        self.remove(item_required)
                        self.assert_cannot_reach_location(location)
                        self.collect(item_required)
                        self.assert_can_reach_location(location)
                for item in items:
                    self.remove(item)
