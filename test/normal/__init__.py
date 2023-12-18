from .. import WL4TestBase

class TestNormal(WL4TestBase):
    options = {'difficulty': 0}

class TestNormalOpenPortal(WL4TestBase):
    options = {'difficulty': 0, 'portal': 1}
