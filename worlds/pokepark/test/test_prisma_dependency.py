from . import PokeparkTest


class TestPrismaDependencies(PokeparkTest):

    def test_bulbasaur_prisma(self) -> None:
        """Verify locations and victory conditions for Bulbasaur's Prisma unlock"""
        locations = ["Meadow Zone - Overworld - Munchlax",
                     "Meadow Zone - Overworld - Munchlax Friendship - Pokemon Unlock",
                     "Meadow Zone - Overworld - Tropius", "Meadow Zone - Overworld - Bulbasaur"]
        items = [["Bulbasaur Prisma"]]
        self.assertAccessDependency(locations, items)

    def test_pelipper_prisma(self) -> None:
        """Verify Treehouse Dash Upgrade locations and victory conditions for Pelipper's Prisma unlock"""
        locations = [f"Treehouse - Dash Upgrade {i}" for i in range(1, 4)]
        items = [["Pelipper Prisma"]]
        self.assertAccessDependency(locations, items)

    def test_dusknoir_prisma(self) -> None:
        """Verify victory conditions for Blaziken Prisma unlock"""
        locations = [
            "Haunted Zone - Overworld - Mansion - Duskull"]
        items = [["Dusknoir Prisma"]]
        self.assertAccessDependency(locations, items)

    def test_rotom_prisma(self) -> None:
        """Verify victory conditions for Blaziken Prisma unlock"""
        locations = [
            "Haunted Zone - Overworld - Drifloon",
            "Haunted Zone - Overworld - Metapod",
            "Haunted Zone - Overworld - Kakuna",
            "Haunted Zone - Overworld - Mansion - Spinarak",
            "Haunted Zone - Overworld - Mansion - Electrode"]
        items = [["Rotom Prisma"]]
        self.assertAccessDependency(locations, items)

    def test_blaziken_location(self) -> None:
        locations = ["Magma Zone - Overworld - Blaziken"]
        items = [[
            "Rayquaza Prisma"]]
        self.assertAccessDependency(locations, items, True)
