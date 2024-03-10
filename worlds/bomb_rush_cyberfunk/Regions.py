from enum import Enum
from typing import Dict, List


class BRCStage(Enum):
    Misc = 0
    Hideout = 1
    VersumHill = 2
    MillenniumSquare = 3
    BrinkTerminal = 4
    MillenniumMall = 5
    PyramidIsland = 6
    Mataan = 7


region_names: Dict[BRCStage, str] = {
    BRCStage.Misc: "Misc",
    BRCStage.Hideout: "Hideout",
    BRCStage.VersumHill: "Versum Hill",
    BRCStage.MillenniumSquare: "Millennium Square",
    BRCStage.BrinkTerminal: "Brink Terminal",
    BRCStage.MillenniumMall: "Millennium Mall",
    BRCStage.PyramidIsland: "Pyramid Island",
    BRCStage.Mataan: "Mataan"
}

region_exits: Dict[BRCStage, List[BRCStage]] = {
    BRCStage.Misc: [BRCStage.Hideout],
    BRCStage.Hideout: [BRCStage.Misc,
                       BRCStage.VersumHill,
                       BRCStage.MillenniumSquare,
                       BRCStage.Mataan],
    BRCStage.VersumHill: [BRCStage.Hideout,
                          BRCStage.MillenniumSquare],
    BRCStage.MillenniumSquare: [BRCStage.VersumHill,
                                BRCStage.BrinkTerminal,
                                BRCStage.MillenniumMall,
                                BRCStage.PyramidIsland,
                                BRCStage.Mataan],
    BRCStage.BrinkTerminal: [BRCStage.MillenniumSquare],
    BRCStage.MillenniumMall: [BRCStage.MillenniumSquare],
    BRCStage.PyramidIsland: [BRCStage.MillenniumSquare],
    BRCStage.Mataan: [BRCStage.MillenniumSquare,
                      BRCStage.Hideout]
}