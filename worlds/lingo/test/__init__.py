from typing import ClassVar

from test.bases import WorldTestBase


class LingoTestBase(WorldTestBase):
    game = "Lingo"
    player: ClassVar[int] = 1

    def world_setup(self, *args, **kwargs):
        super().world_setup(*args, **kwargs)

    def remove_forced_good_item(self):
        location = self.multiworld.get_location("Second Room - Good Luck", self.player)
        self.remove(location.item)
        self.multiworld.itempool.append(location.item)
        self.multiworld.state.events.add(location)
