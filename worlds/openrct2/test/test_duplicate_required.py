from .base import OpenRCT2TestBase

class test_duplicate_required(OpenRCT2TestBase): #Welp, I have no idea what I'm doing. Hopefully this works!
    def test_duplicate_required(self) -> None:
        """Ensures the objective list has no duplicate items"""
        rides = objectives["UniqueRides"][0]
        self.assertEqual(len(rides), len(set(rides)), f"Duplicates found: {rides}")
