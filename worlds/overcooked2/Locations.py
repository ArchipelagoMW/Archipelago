from BaseClasses import Location
from Overcooked2Levels import Overcooked2Level

class Overcooked2Location(Location):
    game: str = "Overcooked! 2"

    # override constructor to automatically mark event locations as such
    def __init__(self, player: int, name = "", code = None, parent = None):
        super(Overcooked2Location, self).__init__(player, name, code, parent)
        self.event = code is None

location_name_to_id = dict()
for level in Overcooked2Level():
    location_name_to_id[level.reward_name_one_star()] = level.reward_id_one_star()
    location_name_to_id[level.reward_name_two_star()] = level.reward_id_two_star()
    location_name_to_id[level.reward_name_three_star()] = level.reward_id_three_star()

location_id_to_name = dict()
for name in location_name_to_id:
    location_id_to_name[location_name_to_id[name]] = name
