class Region:
    """
    Store string information for all regions
    """

    pioneer_2 = "Pioneer 2"
    forest_1 = "Forest 1"
    forest_2 = "Forest 2"
    forest_boss = "Forest Boss"
    caves_1 = "Caves 1"
    caves_2 = "Caves 2"
    caves_3 = "Caves 3"
    caves_boss = "Caves Boss"
    mines_1 = "Mines 1"
    mines_2 = "Mines 2"
    mines_boss = "Mines Boss"
    ruins_entrance = "Ruins Entrance"
    ruins_1 = "Ruins 1"
    ruins_2 = "Ruins 2"
    ruins_3 = "Ruins 3"
    dark_falz = "Dark Falz"

    def all_regions(self) -> list[str]:
        return [
            self.pioneer_2,
            self.forest_1,
            self.forest_2,
            self.forest_boss,
            self.caves_1,
            self.caves_2,
            self.caves_3,
            self.caves_boss,
            self.mines_1,
            self.mines_2,
            self.mines_boss,
            self.ruins_entrance,
            self.ruins_1,
            self.ruins_2,
            self.ruins_3,
            self.dark_falz
        ]