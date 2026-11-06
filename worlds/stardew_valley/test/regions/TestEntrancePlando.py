from typing import ClassVar
from unittest.mock import MagicMock, Mock

from BaseClasses import MultiWorld, Region
from entrance_rando import EntranceRandomizationError
from Fill import distribute_items_restrictive

from Options import PlandoConnection

from ... import options
from ...content import StardewContent, create_content
from ...options import StardewValleyOptions
from ...regions import create_regions
from ...strings.ap_names.ap_option_names import EntranceRandomizationBehaviorOptionName
from ...strings.entrance_names import Entrance as EntranceName
from ...strings.region_names import Region as RegionName
from ..bases import SVTestCase, skip_if_no_long_tests, solo_multiworld
from ..options.utils import SVTestOptions, fill_dataclass_with_default


class EntrancePlandoTestCase(SVTestCase):
    options: ClassVar[SVTestOptions]

    __created_regions: dict[str, Region]
    __multiworld: MultiWorld

    world_options: StardewValleyOptions
    world_content: StardewContent

    def setUp(self):
        self.__created_regions = {}
        self.__multiworld = MagicMock()
        self.__multiworld.get_region = Mock(side_effect=lambda name, player: self.__created_regions[name])

        self.world_options = fill_dataclass_with_default(self.options)
        self.world_content = create_content(self.world_options, Mock())

    def create_region(self, name):
        return Region(name, 1, self.__multiworld)

    def assert_region_connections(self, expected_connections: list[tuple[str, str, str]], created_regions: dict[str, Region]):
        for plando in expected_connections:
            origin, entrance_name, destination = plando
            with self.subTest(f"{entrance_name} goes from {origin} to {destination}"):
                parent_region = created_regions[origin]
                entrance = next(e for e in parent_region.exits if e.name == entrance_name)
                connected_region: Region = entrance.connected_region
                self.assertEqual(destination, connected_region.name)


class TestEntrancePlandoCoupled(EntrancePlandoTestCase):
    options = {  # noqa: RUF012
        options.EntranceRandomization: options.EntranceRandomization.option_everywhere,
        options.EntranceRandomizationBehavior: {},
        options.EntrancePlando: [
            # sewer to beach
            PlandoConnection(EntranceName.sewer_to_forest, EntranceName.town_to_beach, "both", 100),
            # farm to railroad
            PlandoConnection(EntranceName.farm_to_backwoods, EntranceName.mountain_to_railroad, "both", 100),
            # island south to secret woods
            PlandoConnection(EntranceName.island_south_to_southeast, EntranceName.enter_secret_woods, "both", 100),
        ],
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
    }

    def test_plando_of_randomized_entrances(self):
        created_regions, forced_entrances = create_regions(self.create_region, self.world_options, self.world_content, Mock())

        self.assert_region_connections(
            [
                (RegionName.sewer, EntranceName.sewer_to_forest, RegionName.beach),
                (RegionName.farm, EntranceName.farm_to_backwoods, RegionName.railroad),
                (RegionName.island_south, EntranceName.island_south_to_southeast, RegionName.secret_woods),
                # reverse connections should be created as well
                (RegionName.beach, EntranceName.beach_to_town, RegionName.sewer),
                (RegionName.railroad, EntranceName.railroad_to_mountain, RegionName.farm),
                (RegionName.secret_woods, EntranceName.leave_secret_woods, RegionName.island_south),
            ],
            created_regions,
        )

        self.assertDictEqual(
            {
                EntranceName.sewer_to_forest: EntranceName.town_to_beach,
                EntranceName.farm_to_backwoods: EntranceName.mountain_to_railroad,
                EntranceName.island_south_to_southeast: EntranceName.enter_secret_woods,
                EntranceName.beach_to_town: EntranceName.forest_to_sewer,
                EntranceName.railroad_to_mountain: EntranceName.backwoods_to_farm,
                EntranceName.leave_secret_woods: EntranceName.island_southeast_to_south,
            },
            forced_entrances,
        )

    @skip_if_no_long_tests
    def test_can_fill(self):
        with solo_multiworld(self.options) as (multiworld, _):
            distribute_items_restrictive(multiworld)


class TestEntrancePlandoDecoupled(EntrancePlandoTestCase):
    options = {  # noqa: RUF012
        options.EntranceRandomization: options.EntranceRandomization.option_everywhere,
        options.EntranceRandomizationBehavior: {EntranceRandomizationBehaviorOptionName.decoupled},
        options.EntrancePlando: [
            # sewer to beach
            PlandoConnection(EntranceName.sewer_to_forest, EntranceName.town_to_beach, "entrance", 100),
            # farm to railroad
            PlandoConnection(EntranceName.farm_to_backwoods, EntranceName.mountain_to_railroad, "entrance", 100),
            # island south to secret woods
            PlandoConnection(EntranceName.island_south_to_southeast, EntranceName.enter_secret_woods, "entrance", 100),
        ],
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
    }

    def test_plando_of_randomized_entrances(self):
        created_regions, forced_entrances = create_regions(self.create_region, self.world_options, self.world_content, Mock())

        self.assert_region_connections(
            [
                (RegionName.sewer, EntranceName.sewer_to_forest, RegionName.beach),
                (RegionName.farm, EntranceName.farm_to_backwoods, RegionName.railroad),
                (RegionName.island_south, EntranceName.island_south_to_southeast, RegionName.secret_woods),
            ],
            created_regions,
        )

        self.assertDictEqual(
            {
                EntranceName.sewer_to_forest: EntranceName.town_to_beach,
                EntranceName.farm_to_backwoods: EntranceName.mountain_to_railroad,
                EntranceName.island_south_to_southeast: EntranceName.enter_secret_woods,
            },
            forced_entrances,
        )

    @skip_if_no_long_tests
    def test_can_fill(self):
        with solo_multiworld(self.options) as (multiworld, _):
            distribute_items_restrictive(multiworld)


class TestGivenEntrancePlandoFarmhouseAndEntranceRandoOptionDisabledWhenCreateWorldThenAllowsMovingTheFarmHouse(EntrancePlandoTestCase):
    options = {  # noqa: RUF012
        options.EntranceRandomization: options.EntranceRandomization.option_disabled,
        options.EntranceRandomizationBehavior: {},
        options.EntrancePlando: [
            # farmhouse to mountain
            PlandoConnection(EntranceName.farmhouse_to_farm, EntranceName.the_mines_to_mountain, "both", 100),
            PlandoConnection(EntranceName.the_mines_to_mountain, EntranceName.farmhouse_to_farm, "both", 100),
        ],
    }

    def test_plando_of_randomized_entrances(self):
        created_regions, forced_entrances = create_regions(self.create_region, self.world_options, self.world_content, Mock())

        self.assert_region_connections(
            [
                (RegionName.farm_house, EntranceName.farmhouse_to_farm, RegionName.outside_adventure_guild),
                (RegionName.outside_adventure_guild, EntranceName.mountain_to_the_mines, RegionName.farm_house),
                (RegionName.farm, EntranceName.farm_to_farmhouse, RegionName.mines),
                (RegionName.mines, EntranceName.the_mines_to_mountain, RegionName.farm),
            ],
            created_regions,
        )

        self.assertDictEqual(
            {
                EntranceName.farmhouse_to_farm: EntranceName.the_mines_to_mountain,
                EntranceName.the_mines_to_mountain: EntranceName.farmhouse_to_farm,
                EntranceName.mountain_to_the_mines: EntranceName.farm_to_farmhouse,
                EntranceName.farm_to_farmhouse: EntranceName.mountain_to_the_mines,
            },
            forced_entrances,
        )

    @skip_if_no_long_tests
    def test_can_fill(self):
        with solo_multiworld(self.options) as (multiworld, _):
            distribute_items_restrictive(multiworld)


class TestGivenIncompleteEntrancePlandoAndERDisabledWhenCreateWorldThenCreateRegionsFails(EntrancePlandoTestCase):
    options = {  # noqa: RUF012
        options.EntranceRandomization: options.EntranceRandomization.option_disabled,
        options.EntranceRandomizationBehavior: {},
        options.EntrancePlando: [
            PlandoConnection(EntranceName.town_to_pierre_general_store, EntranceName.town_to_jojamart, "entrance", 100),
        ],
    }

    def test_plando_of_randomized_entrances(self):
        with self.assertRaises(EntranceRandomizationError):
            create_regions(self.create_region, self.world_options, self.world_content, Mock())


class TestGivenPartialEntrancePlandoAndERDisabledWhenCreateWorldThenEntranceRandoIsCalledToCompleteEntrancePlacements(EntrancePlandoTestCase):
    options = {  # noqa: RUF012
        options.EntranceRandomization: options.EntranceRandomization.option_disabled,
        options.EntranceRandomizationBehavior: {},
        options.EntrancePlando: [
            PlandoConnection(EntranceName.town_to_pierre_general_store, EntranceName.town_to_jojamart, "both", 100),
        ],
    }

    def test_plando_of_randomized_entrances(self):
        created_regions, forced_entrances = create_regions(self.create_region, self.world_options, self.world_content, Mock())

        self.assert_region_connections(
            [
                (RegionName.town, EntranceName.town_to_pierre_general_store, RegionName.jojamart),
            ],
            created_regions,
        )

        self.assertDictEqual(
            {
                EntranceName.town_to_pierre_general_store: EntranceName.town_to_jojamart,
                EntranceName.jojamart_to_town: EntranceName.pierre_general_store_to_town,
            },
            forced_entrances,
        )

    def test_entrance_rando_places_opposite_direction(self):
        with solo_multiworld(self.options) as (_, world):
            # This validates that the ER actually placed the opposite connection.
            self.assertIn((EntranceName.town_to_jojamart, EntranceName.town_to_pierre_general_store), world.randomized_entrances.items())
            self.assertIn((EntranceName.pierre_general_store_to_town, EntranceName.jojamart_to_town), world.randomized_entrances.items())

    @skip_if_no_long_tests
    def test_can_fill(self):
        with solo_multiworld(self.options) as (multiworld, _):
            distribute_items_restrictive(multiworld)


class TestPartialEntrancePlandoAndERDisabledAndDecoupled(EntrancePlandoTestCase):
    options = {  # noqa: RUF012
        options.EntranceRandomization: options.EntranceRandomization.option_disabled,
        options.EntranceRandomizationBehavior: {EntranceRandomizationBehaviorOptionName.decoupled},
        options.EntrancePlando: [
            PlandoConnection(EntranceName.town_to_pierre_general_store, EntranceName.town_to_jojamart, "entrance", 100),
        ],
    }

    def test_plando_of_randomized_entrances(self):
        created_regions, forced_entrances = create_regions(self.create_region, self.world_options, self.world_content, Mock())

        self.assert_region_connections(
            [(RegionName.town, EntranceName.town_to_pierre_general_store, RegionName.jojamart)],
            created_regions,
        )

        self.assertDictEqual(
            {EntranceName.town_to_pierre_general_store: EntranceName.town_to_jojamart},
            forced_entrances,
        )

    @skip_if_no_long_tests
    def test_can_fill(self):
        with solo_multiworld(self.options) as (multiworld, _):
            distribute_items_restrictive(multiworld)

