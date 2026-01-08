from .bases import PseudoKeyHintsBase


class TestNoKeyHints(PseudoKeyHintsBase):
    options = {
        "major_key_hints": False,
    }
    expect_hints = False
