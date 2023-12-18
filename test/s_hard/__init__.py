from .. import WL4TestBase

class TestSHard(WL4TestBase):
    options = {'difficulty': 2}

class TestSHardOpenPortal(WL4TestBase):
    options = {'difficulty': 2, 'portal': 1}
