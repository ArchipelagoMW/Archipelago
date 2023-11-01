from test.TestBase import WorldTestBase


class InscryptionTestBase(WorldTestBase):
    game = "Inscryption"
    player: int = 1
    required_items_all_acts = ["Film Roll", "Camera Replica", "Pile Of Meat", "Monocle",
                               "Inspectometer Battery", "Gems Module", "Quill"]
