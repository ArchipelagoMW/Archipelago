class Region:
    """
    Store string information for all regions
    """

    PIONEER_2 = "Pioneer 2"
    FOREST_1 = "Forest 1"
    FOREST_2 = "Forest 2"
    DRAGON = "The Dragon"
    CAVES_1 = "Caves 1"
    CAVES_2 = "Caves 2"
    CAVES_3 = "Caves 3"
    DE_ROL_LE = "De Rol Le"
    MINES_1 = "Mines 1"
    MINES_2 = "Mines 2"
    VOL_OPT = "Vol Opt"
    RUINS_ENTRANCE = "Ruins Entrance"
    RUINS_1 = "Ruins 1"
    RUINS_2 = "Ruins 2"
    RUINS_3 = "Ruins 3"
    DARK_FALZ = "Dark Falz"

    def all_regions(self) -> list[str]:
        return [
            self.PIONEER_2,
            self.FOREST_1,
            self.FOREST_2,
            self.DRAGON,
            self.CAVES_1,
            self.CAVES_2,
            self.CAVES_3,
            self.DE_ROL_LE,
            self.MINES_1,
            self.MINES_2,
            self.VOL_OPT,
            self.RUINS_ENTRANCE,
            self.RUINS_1,
            self.RUINS_2,
            self.RUINS_3,
            self.DARK_FALZ
        ]