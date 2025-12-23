from BaseClasses import CollectionState
from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.locations.general import RAC3LOCATION
from worlds.rac3.constants.region import RAC3REGION
from worlds.rac3.test import RAC3TestBase


class TestBiobliterator(RAC3TestBase):

    def test_logic(self):
        state: CollectionState = self.multiworld.state
        self.assertTrue(self.can_reach_region(RAC3REGION.VELDIN), "Can't start on Veldin")
        self.assertFalse(self.can_reach_region(RAC3REGION.FLORANA), "Florana reachable without coordinates")
        self.assertFalse(self.can_reach_region(RAC3REGION.STARSHIP_PHOENIX),
                         "Starship Phoenix reachable without coordinates")
        self.assertFalse(self.can_reach_region(RAC3REGION.COMMAND_CENTER), "Command Center reachable from Veldin")
        self.assertFalse(self.can_reach_location(RAC3LOCATION.COMMAND_CENTER_BIOBLITERATOR),
                         "Goal location reachable from Veldin")
        self.assertBeatable(False)

        state.sweep_for_advancements()
        self.assertTrue(self.can_reach_region(RAC3REGION.FLORANA), "Can't reach Florana from Veldin")
        self.assertTrue(self.can_reach_region(RAC3REGION.STARSHIP_PHOENIX), "Can't reach Starship Phoenix from Veldin")
        self.assertFalse(self.can_reach_region(RAC3REGION.COMMAND_CENTER), "Command Center reachable from Florana")
        self.assertFalse(self.can_reach_location(RAC3LOCATION.COMMAND_CENTER_BIOBLITERATOR),
                         "Goal location reachable from Florana")
        self.assertBeatable(False)

        self.collect_by_name(RAC3ITEM.COMMAND_CENTER)
        self.assertTrue(self.can_reach_region(RAC3REGION.COMMAND_CENTER), "Can't reach Command Center with coordinates")
        self.assertFalse(self.can_reach_location(RAC3LOCATION.COMMAND_CENTER_BIOBLITERATOR),
                         "Goal location reachable with no items")
        self.assertBeatable(False)

        self.collect_by_name([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE, RAC3ITEM.HACKER,
                              RAC3ITEM.REFRACTOR])
        self.assertTrue(self.can_reach_location(RAC3LOCATION.COMMAND_CENTER_BIOBLITERATOR),
                        "Goal location not reachable with items")
        self.assertBeatable(True)
