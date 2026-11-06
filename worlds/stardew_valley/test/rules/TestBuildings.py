from ..bases import SVTestBase
from ... import SeasonRandomization, StartWithoutOptionName, EntranceRandomization
from ...content.feature.building_progression import progressive_house
from ...options import BuildingProgression, FarmType, ToolProgression, StartWithout
from ...strings.region_names import Region


class TestBuildingLogic(SVTestBase):
    options = {
        StartWithout.internal_name: frozenset({StartWithoutOptionName.landslide}),
        SeasonRandomization.internal_name: SeasonRandomization.option_disabled,
        FarmType.internal_name: FarmType.option_standard,
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        ToolProgression.internal_name: ToolProgression.option_progressive,
    }

    def test_coop_blueprint(self):
        location = "Coop Blueprint"
        self.assert_cannot_reach_location(location)

        self.collect("Landslide Removed")
        self.collect_lots_of_money()
        self.assert_can_reach_location(location)

    def test_big_coop_blueprint(self):
        location = "Big Coop Blueprint"
        self.assert_cannot_reach_location(location)

        self.collect("Landslide Removed")
        self.collect_lots_of_money()
        self.assert_cannot_reach_location(location)

        self.multiworld.state.collect(self.create_item("Progressive Coop"))
        self.assert_can_reach_location(location)

    def test_deluxe_coop_blueprint(self):
        location = "Deluxe Coop Blueprint"
        self.assert_cannot_reach_location(location)

        self.collect("Landslide Removed")
        self.collect_lots_of_money()
        self.assert_cannot_reach_location(location)

        self.multiworld.state.collect(self.create_item("Progressive Coop"))
        self.assert_cannot_reach_location(location)

        self.multiworld.state.collect(self.create_item("Progressive Coop"))
        self.assert_can_reach_location(location)

    def test_big_shed_blueprint(self):
        location = "Big Shed Blueprint"
        self.assert_cannot_reach_location(location)

        self.collect("Landslide Removed")
        self.collect_lots_of_money()
        self.assert_cannot_reach_location(location)

        self.multiworld.state.collect(self.create_item("Progressive Shed"))
        self.assert_can_reach_location(location)


class TestStartWithHouseLogic(SVTestBase):
    options = {
        StartWithout.internal_name: frozenset({}),
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        EntranceRandomization.internal_name: EntranceRandomization.option_disabled,
    }

    def test_coop_blueprint(self):
        self.assert_can_reach_region(Region.farm_house)

        self.assert_cannot_reach_region(Region.farm_house_kitchen)
        self.collect(progressive_house)
        self.assert_can_reach_region(Region.farm_house_kitchen)

        self.assert_cannot_reach_region(Region.farm_house_crib)
        self.collect(progressive_house)
        self.assert_can_reach_region(Region.farm_house_crib)

        self.assert_cannot_reach_region(Region.cellar)
        self.collect(progressive_house)
        self.assert_can_reach_region(Region.cellar)


class TestStartWithoutHouseLogic(SVTestBase):
    options = {
        StartWithout.internal_name: frozenset({StartWithoutOptionName.house}),
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        EntranceRandomization.internal_name: EntranceRandomization.option_disabled,
    }

    def test_coop_blueprint(self):
        self.assert_cannot_reach_region(Region.farm_house)
        self.collect(progressive_house)
        self.assert_can_reach_region(Region.farm_house)

        self.assert_cannot_reach_region(Region.farm_house_kitchen)
        self.collect(progressive_house)
        self.assert_can_reach_region(Region.farm_house_kitchen)

        self.assert_cannot_reach_region(Region.farm_house_crib)
        self.collect(progressive_house)
        self.assert_can_reach_region(Region.farm_house_crib)

        self.assert_cannot_reach_region(Region.cellar)
        self.collect(progressive_house)
        self.assert_can_reach_region(Region.cellar)