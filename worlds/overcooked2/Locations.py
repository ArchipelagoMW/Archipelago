from BaseClasses import Location
from .Overcooked2Levels import Overcooked2Level

class Overcooked2Location(Location):
    game: str = "Overcooked! 2"

    # override constructor to automatically mark event locations as such
    def __init__(self, player: int, name = "", code = None, parent = None):
        super(Overcooked2Location, self).__init__(player, name, code, parent)
        self.event = code is None

location_id_to_name = {level.level_name(): level.level_id() for level in Overcooked2Level()}
location_name_to_id = {level.level_id(): level.level_name() for level in Overcooked2Level()}
