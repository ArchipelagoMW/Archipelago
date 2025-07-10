from typing import Dict


class Stages:
    Misc = "Misc"
    H = "Hideout"
    VH1 = "Versum Hill"
    VH2 = "Versum Hill - After Roadblock"
    VHO = "Versum Hill - Underground Mall"
    VH3 = "Versum Hill - Side Street"
    VH4 = "Versum Hill - Basketball Court"
    MS = "Millennium Square"
    BT1 = "Brink Terminal"
    BTO1 = "Brink Terminal - Underground"
    BTO2 = "Brink Terminal - Dock"
    BT2 = "Brink Terminal - Planet Plaza"
    BT3 = "Brink Terminal - Tower"
    MM1 = "Millennium Mall"
    MMO1 = "Millennium Mall - Hanging Lights"
    MM2 = "Millennium Mall - Atrium"
    MMO2 = "Millennium Mall - Race Track"
    MM3 = "Millennium Mall - Theater"
    PI1 = "Pyramid Island - Base"
    PI2 = "Pyramid Island - After Gate"
    PIO = "Pyramid Island - Maze"
    PI3 = "Pyramid Island - Upper Areas"
    PI4 = "Pyramid Island - Top"
    MA1 = "Mataan - Streets"
    MA2 = "Mataan - After Smoke Wall"
    MA3 = "Mataan - Deep City"
    MAO = "Mataan - Red Light District"
    MA4 = "Mataan - Lion Statue"
    MA5 = "Mataan - Skyscrapers"


region_exits: Dict[str, str] = {
    Stages.Misc: [Stages.H],
    Stages.H: [Stages.Misc,
               Stages.VH1,
               Stages.MS,
               Stages.MA1],
    Stages.VH1: [Stages.H,
                 Stages.VH2],
    Stages.VH2: [Stages.H,
                 Stages.VH1,
                 Stages.MS,
                 Stages.VHO,
                 Stages.VH3,
                 Stages.VH4],
    Stages.VHO: [Stages.VH2],
    Stages.VH3: [Stages.VH2],
    Stages.VH4: [Stages.VH2,
                 Stages.VH1],
    Stages.MS: [Stages.VH2,
                 Stages.BT1,
                 Stages.MM1,
                 Stages.PI1,
                 Stages.MA1],
    Stages.BT1: [Stages.MS,
                 Stages.BTO1,
                 Stages.BTO2,
                 Stages.BT2],
    Stages.BTO1: [Stages.BT1],
    Stages.BTO2: [Stages.BT1],
    Stages.BT2: [Stages.BT1,
                 Stages.BT3],
    Stages.BT3: [Stages.BT1,
                 Stages.BT2],
    Stages.MM1: [Stages.MS,
                 Stages.MMO1,
                 Stages.MM2],
    Stages.MMO1: [Stages.MM1],
    Stages.MM2: [Stages.MM1,
                 Stages.MMO2,
                 Stages.MM3],
    Stages.MMO2: [Stages.MM2],
    Stages.MM3: [Stages.MM2,
                 Stages.MM1],
    Stages.PI1: [Stages.MS,
                 Stages.PI2],
    Stages.PI2: [Stages.PI1,
                 Stages.PIO,
                 Stages.PI3],
    Stages.PIO: [Stages.PI2],
    Stages.PI3: [Stages.PI1,
                 Stages.PI2,
                 Stages.PI4],
    Stages.PI4: [Stages.PI1,
                 Stages.PI2,
                 Stages.PI3],
    Stages.MA1: [Stages.H,
                 Stages.MS,
                 Stages.MA2],
    Stages.MA2: [Stages.MA1,
                 Stages.MA3],
    Stages.MA3: [Stages.MA2,
                 Stages.MAO,
                 Stages.MA4],
    Stages.MAO: [Stages.MA3],
    Stages.MA4: [Stages.MA3,
                 Stages.MA5],
    Stages.MA5: [Stages.MA1]
}
