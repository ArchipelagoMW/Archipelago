from AutoWorld import World, WebWorld
from .Options import overcooked_options
from .Overcooked2Levels import Overcooked2Level
from .Items import item_frequencies, item_table

class Overcooked2Web(WebWorld):
    pass


class Overcooked2Web(World):
    """
    Overcooked! 2 is a franticly paced cooking arcade game where
    players race against the clock to complete orders for points. Bring
    peace to the Onion Kingdom once again by recovering lost items and abilities,
    earning stars to unlock levels, and defeating the unbread horde. Levels are
    randomized to increase gameplay variety. Best enjoyed with a friend or three.
    """
    game = "Overcooked! 2"
    topology_present = False
    data_version = 7
    web = Overcooked2Web()
    option_definitions = overcooked_options

    location_id_to_name = {level.level_name(): level.level_id() for level in Overcooked2Level()}
    location_name_to_id = {level.level_id(): level.level_name() for level in Overcooked2Level()}

    def generate_basic(self) -> None:
        itempool = []
        pool_counts = item_frequencies.copy()

        for item_name in item_table:
            for _ in range(pool_counts.get(item_name, 1)):
                itempool.append(self.create_item(item_name))
