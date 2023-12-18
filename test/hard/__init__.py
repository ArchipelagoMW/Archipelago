from .. import WL4TestBase

class TestHard(WL4TestBase):
    options = {'difficulty': 1}

class TestHardOpenPortal(WL4TestBase):
    options = {'difficulty': 1, 'portal': 1}
