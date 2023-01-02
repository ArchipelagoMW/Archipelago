import typing
from . import SoETestBase


class AccessTest(SoETestBase):
    @staticmethod
    def _resolveGourds(gourds: typing.Dict[str, typing.Iterable[int]]):
        return [f"{name} #{number}" for name, numbers in gourds.items() for number in numbers]

    def testBronzeAxe(self):
        gourds = {
            "Pyramid bottom": (118, 121, 122, 123, 124, 125),
            "Pyramid top": (140,)
        }
        locations = ["Rimsala"] + self._resolveGourds(gourds)
        items = [["Bronze Axe"]]
        self.assertAccessDependency(locations, items)

    def testBronzeSpearPlus(self):
        locations = ["Megataur"]
        items = [["Bronze Spear"], ["Lance (Weapon)"], ["Laser Lance"]]
        self.assertAccessDependency(locations, items)
