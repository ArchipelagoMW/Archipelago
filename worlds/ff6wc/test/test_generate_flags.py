from worlds.ff6wc import FF6WCWorld
from worlds.ff6wc.Options import generate_flagstring
from . import FF6WCTestBase


class TestGenerateDefaultFlags(FF6WCTestBase):
    options = {}  # default

    def test_generate_flagstring(self) -> None:
        """ can generate flagstrings from options """
        assert isinstance(self.multiworld.worlds[self.player], FF6WCWorld)
        generate_flagstring(self.world.options, ["Terra", "Celes"])
