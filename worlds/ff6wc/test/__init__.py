from test.bases import WorldTestBase

from worlds.ff6wc import FF6WCWorld


class FF6WCTestBase(WorldTestBase):
    game = "Final Fantasy 6 Worlds Collide"
    world: FF6WCWorld  # type: ignore
