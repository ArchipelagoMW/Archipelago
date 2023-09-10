import os

base_id = 8675309
zillion_map = os.path.join(os.path.dirname(__file__), "empty-zillion-map-row-col-labels-281.png")


def detect_test() -> bool:
    """
    Parts of generation that are in unit tests need the rom.
    This is to detect whether we are running unit tests
    so we can work around the need for the rom.
    """
    import __main__
    try:
        if "test" in __main__.__file__:
            return True
    except AttributeError:
        # In some environments, __main__ doesn't have __file__
        # We'll assume that's not unit tests.
        pass
    return False
