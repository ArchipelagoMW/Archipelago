from BaseClasses import CollectionState
from . import MessengerTestBase
from .. import MessengerWorld
from ..portals import OUTPUT_PORTALS


class PortalTestBase(MessengerTestBase):
    def test_portal_reqs(self) -> None:
        """tests the paths to open a portal if only that portal is closed with vanilla connections."""
        # portal and requirements to reach it if it's the only closed portal
        portal_requirements = {
            "Autumn Hills Portal": [["Autumn Hills Portal", "Wingsuit"]],  # grotto -> bamboo -> catacombs -> hills
            "Riviere Turquoise Portal": [["Riviere Turquoise Portal", "Candle", "Wingsuit", "Rope Dart"]],  # hills -> catacombs -> dark cave -> riviere
            "Howling Grotto Portal": [["Howling Grotto Portal", "Wingsuit"], ["Howling Grotto Portal", "Meditation", "Second Wind"]],  # crags -> quillshroom -> grotto
            "Sunken Shrine Portal": [["Sunken Shrine Portal", "Seashell"]],  # crags -> quillshroom -> grotto -> shrine
            "Searing Crags Portal": [["Searing Crags Portal", "Wingsuit"], ["Searing Crags Portal", "Rope Dart"]],  # grotto -> quillshroom -> crags there's two separate paths
            "Glacial Peak Portal": [["Glacial Peak Portal", "Wingsuit"], ["Glacial Peak Portal", "Rope Dart"]],  # grotto -> quillshroom -> crags -> peak or crags -> peak
        }
        for portal in OUTPUT_PORTALS:
            name = f"{portal} Portal"
            entrance_name = f"ToTHQ {name}"
            with self.subTest(portal=name, entrance_name=entrance_name):
                entrance = self.multiworld.get_entrance(entrance_name, self.player)
                # this emulates the portal being initially closed
                entrance.access_rule = lambda state: state.has(name, self.player)
                self.assertAccessDependency([name], portal_requirements[name], True)
                entrance.access_rule = lambda state: True
