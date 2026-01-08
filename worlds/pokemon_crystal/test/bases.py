from test.bases import WorldTestBase
from ..data import data


class PokemonCrystalTestBase(WorldTestBase):
    game = data.manifest.game


def verify_region_access(test, items_dont_collect, regions, items_collect=None):
    if items_collect is None:
        items_collect = items_dont_collect

    test.collect_all_but(items_dont_collect)
    for region in regions:
        test.assertFalse(test.can_reach_region(region),
                         f"Region {region} reachable without items {items_dont_collect}.")
    test.collect_by_name(items_collect)
    for region in regions:
        test.assertTrue(test.can_reach_region(region), f"Region {region} unreachable with items {items_collect}.")
