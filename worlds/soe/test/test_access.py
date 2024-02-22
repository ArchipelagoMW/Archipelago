import typing
from . import SoETestBase


class AccessTest(SoETestBase):
    @staticmethod
    def _resolveGourds(gourds: typing.Mapping[str, typing.Iterable[int]]) -> typing.List[str]:
        return [f"{name} #{number}" for name, numbers in gourds.items() for number in numbers]

    def test_bronze_axe(self) -> None:
        gourds = {
            "Pyramid bottom": (118, 121, 122, 123, 124, 125),
            "Pyramid top": (140,)
        }
        locations = ["Rimsala"] + self._resolveGourds(gourds)
        items = [["Bronze Axe"]]
        self.assertAccessDependency(locations, items)

    def test_bronze_spear_plus(self) -> None:
        locations = ["Megataur"]
        items = [["Bronze Spear"], ["Lance (Weapon)"], ["Laser Lance"]]
        self.assertAccessDependency(locations, items)
