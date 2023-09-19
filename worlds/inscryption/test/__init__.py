from test.TestBase import WorldTestBase


class InscryptionTestBase(WorldTestBase):
    game = "Inscryption"
    player: int = 1
    required_items_all_acts = ["Film Roll", "Epitaph Piece 1", "Epitaph Piece 2", "Epitaph Piece 3", "Epitaph Piece 4",
                               "Epitaph Piece 5", "Epitaph Piece 6", "Epitaph Piece 7", "Epitaph Piece 8",
                               "Epitaph Piece 9", "Camera Replica", "Pile Of Meat", "Monocle",
                               "Inspectometer Battery", "Gems Module", "Quill"]
