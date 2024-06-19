from BaseClasses import CollectionState
from . import MessengerTestBase
from ..portals import PORTALS


class PortalTestBase(MessengerTestBase):
    options = {
        "available_portals": 3,
    }

    def test_portal_reqs(self) -> None:
        """tests the paths to open a portal if only that portal is closed with vanilla connections."""
        # portal and requirements to reach it if it's the only closed portal
        portal_requirements = {
            "Autumn Hills Portal": [["Wingsuit"]],  # grotto -> bamboo -> catacombs -> hills
            "Riviere Turquoise Portal": [["Candle", "Wingsuit", "Rope Dart"]],  # hills -> catacombs -> dark cave -> riviere
            "Howling Grotto Portal": [["Wingsuit"], ["Meditation", "Second Wind"]],  # crags -> quillshroom -> grotto
            "Sunken Shrine Portal": [["Seashell"]],  # crags -> quillshroom -> grotto -> shrine
            "Searing Crags Portal": [["Wingsuit"], ["Rope Dart"]],  # grotto -> quillshroom -> crags there's two separate paths
            "Glacial Peak Portal": [["Wingsuit", "Second Wind", "Meditation"], ["Rope Dart"]],  # grotto -> quillshroom -> crags -> peak or crags -> peak
        }

        for portal in PORTALS:
            name = f"{portal} Portal"
            entrance_name = f"ToTHQ {name}"
            with self.subTest(portal=name, entrance_name=entrance_name):
                entrance = self.multiworld.get_entrance(entrance_name, self.player)
                # this emulates the portal being initially closed
                entrance.access_rule = lambda state: state.has(name, self.player)
                for grouping in portal_requirements[name]:
                    test_state = CollectionState(self.multiworld)
                    self.assertFalse(entrance.can_reach(test_state), "reachable with nothing")
                    items = self.get_items_by_name(grouping)
                    for item in items:
                        test_state.collect(item)
                    self.assertTrue(entrance.can_reach(test_state), grouping)
                entrance.access_rule = lambda state: True
