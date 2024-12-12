from . import KH2TestBase
from ..Names import ItemName


class TestPuzzlesTrue(KH2TestBase):
    options = {
        "PuzzlePiecesLocationToggle": True
    }


class TestPuzzlesFalse(KH2TestBase):
    options = {
        "PuzzlePiecesLocationToggle": False
    }
