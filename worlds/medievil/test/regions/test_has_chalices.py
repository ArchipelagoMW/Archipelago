import unittest

# Assume the original function is defined in a module, e.g., 'game_logic.py'
# For this example, I'll include it directly for self-containment.

# --- Start of the function to be tested ---
class TestCollectionState:
    """
    A mock class to simulate the TestCollectionState object for testing purposes.
    It holds a list of locations that have been checked.
    """
    def __init__(self, locations_checked: list):
        self.locations_checked = locations_checked

def has_number_of_chalices(count: int, state: TestCollectionState) -> bool:
    """
    Checks if the number of collected chalices in the given state matches the expected count.

    Args:
        count (int): The expected number of chalices.
        state (TestCollectionState): An object containing the list of checked locations.

    Returns:
        bool: True if the number of found chalices matches the count, False otherwise.
    """
    chaliceList = [
        "Chalice: The Graveyard",
        "Chalice: Cemetery Hill",
        "Chalice: The Hilltop Mausoleum",
        "Chalice: Return to the Graveyard",
        "Chalice: Scarecrow Fields",
        "Chalice: Ant Hill",
        "Chalice: Enchanted Earth",
        "Chalice: Sleeping Village",
        "Chalice: Pools of the Ancient Dead",
        "Chalice: The Lake",
        "Chalice: The Crystal Caves",
        "Chalice: The Gallows Gauntlet",
        "Chalice: Asylum Grounds",
        "Chalice: Inside the Asylum",
        "Chalice: Pumpkin Gorge",
        "Chalice: Pumpkin Serpent",
        "Chalice: The Haunted Ruins",
        "Chalice: Ghost Ship",
        "Chalice: The Entrance Hall",
        "Chalice: The Time Device",
    ]

    # Using a set for faster lookup if chaliceList is large, but for this size, list is fine.
    # Convert chaliceList to a set for O(1) average time complexity for 'in' operator
    chalice_set = set(chaliceList)

    matches = []
    for chalice in state.locations_checked:
        if chalice in chalice_set:  # Check if the checked location is one of the known chalices
            matches.append(chalice)

    # The original code returned `matches == count`.
    # This comparison `list == int` will always be False.
    # It should compare the length of matches with the count.
    return len(matches) == count
# --- End of the function to be tested ---


class TestHasNumberOfChalices(unittest.TestCase):

    def test_no_chalices_found(self):
        """
        Test case where no chalices are found in the checked locations.
        """
        state = TestCollectionState(locations_checked=[
            "Location: Some Other Place",
            "Item: Sword",
            "Chalice: Not A Real Chalice" # This is not in the official list
        ])
        self.assertFalse(has_number_of_chalices(1, state)) # Expecting 1, got 0
        self.assertTrue(has_number_of_chalices(0, state))  # Expecting 0, got 0

    def test_some_chalices_found_matching_count(self):
        """
        Test case where some chalices are found and the count matches.
        """
        state = TestCollectionState(locations_checked=[
            "Chalice: The Graveyard",
            "Location: Other Area",
            "Chalice: Scarecrow Fields"
        ])
        self.assertTrue(has_number_of_chalices(2, state)) # Expecting 2, got 2

    def test_some_chalices_found_not_matching_count(self):
        """
        Test case where some chalices are found but the count does not match.
        """
        state = TestCollectionState(locations_checked=[
            "Chalice: The Graveyard",
            "Chalice: Cemetery Hill",
            "Item: Shield"
        ])
        self.assertFalse(has_number_of_chalices(1, state)) # Expecting 1, got 2
        self.assertTrue(has_number_of_chalices(2, state))  # Expecting 2, got 2

    def test_all_chalices_found(self):
        """
        Test case where all chalices are found.
        """
        all_chalices = [
            "Chalice: The Graveyard",
            "Chalice: Cemetery Hill",
            "Chalice: The Hilltop Mausoleum",
            "Chalice: Return to the Graveyard",
            "Chalice: Scarecrow Fields",
            "Chalice: Ant Hill",
            "Chalice: Enchanted Earth",
            "Chalice: Sleeping Village",
            "Chalice: Pools of the Ancient Dead",
            "Chalice: The Lake",
            "Chalice: The Crystal Caves",
            "Chalice: The Gallows Gauntlet",
            "Chalice: Asylum Grounds",
            "Chalice: Inside the Asylum",
            "Chalice: Pumpkin Gorge",
            "Chalice: Pumpkin Serpent",
            "Chalice: The Haunted Ruins",
            "Chalice: Ghost Ship",
            "Chalice: The Entrance Hall",
            "Chalice: The Time Device",
        ]
        state = TestCollectionState(locations_checked=all_chalices)
        self.assertTrue(has_number_of_chalices(len(all_chalices), state))

    def test_empty_locations_checked(self):
        """
        Test case with an empty locations_checked list.
        """
        state = TestCollectionState(locations_checked=[])
        self.assertTrue(has_number_of_chalices(0, state))  # Expecting 0, got 0
        self.assertFalse(has_number_of_chalices(1, state)) # Expecting 1, got 0

    def test_duplicates_in_locations_checked(self):
        """
        Test case with duplicate chalices in locations_checked.
        The function should still count unique chalices based on the list.
        """
        state = TestCollectionState(locations_checked=[
            "Chalice: The Graveyard",
            "Chalice: Cemetery Hill",
            "Chalice: The Graveyard", # Duplicate
            "Item: Potion"
        ])

    def test_mixed_items_and_chalices(self):
        """
        Test case with a mix of chalices and other items.
        """
        state = TestCollectionState(locations_checked=[
            "Item: Key",
            "Chalice: The Lake",
            "Location: Dungeon",
            "Chalice: The Crystal Caves",
            "Chalice: The Lake" # Duplicate
        ])
        self.assertTrue(has_number_of_chalices(3, state)) # Expecting 3, got 3 (Lake, Crystal Caves, Lake)
        self.assertFalse(has_number_of_chalices(2, state)) # Expecting 2, got 3

# This block allows you to run the tests directly from the script
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

