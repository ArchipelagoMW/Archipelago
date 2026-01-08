from random import Random
import math

class Area():
    """A loose definition for a semantic location in FF5

    Areas contain parameters that define how randomization
    should happen within that area, namely how much value should
    be allowed in that area, and how many checks that are contains.

    Args:
        area_name (str): The given name of the area.
        area_capacity (int): The total value of items allowed in the area.
        area_order (int): Int representing the rough ordering of the area when
                          traversed in the vanilla Final Fantasy 5 experience.
        num_checks (int): The number of checks in this area
                          including both (chests and events).

    Attributes:
        current_volume (int): Used to track how much value has been placed
            in this area while randomizing.
        num_placed_checks (int): Used to track the number of checks that have
            been placed in this area while randomizing.
    """
    def __init__(self, area_name, area_capacity, area_order, area_num_checks):
        self.area_name = area_name
        self.area_capacity = int(area_capacity)
        self.area_order = int(area_order)
        self.num_checks = int(area_num_checks)
        self.current_volume = 0
        self.num_placed_checks = 0

    def __str__(self):
        output = "Area: " + self.area_name
        output = output + "\nOrder: " + str(self.area_order)
        output = output + "\nCapacity: " + str(self.area_capacity)
        output = output + "\nCurr Vol: " + str(self.current_volume)
        output = output + "\nNum Checks: " + str(self.num_checks)
        output = output + "\nNum Placed: " + str(self.num_placed_checks)
        return output
        
class AreaManager():
    """A collection of Area objects and helper methods to manage them

    Args:
        data_manager (DataManager): A DataManager object to allow 
            access to data files
        random (Random): Used primarily to allow a single seeded
            random engine to be used between all the manager classes.
    """
    def __init__(self, data_manager, random=None):
        self.areas = []
        self.initialize_areas(data_manager.files["areas"])
        
        #Passing in no engine will force the AreaManager
        #to generate a new random engine.
        if random is None:
            self.random = Random()
        else:
            self.random = random

    def initialize_areas(self, data_file):
        """Reads the area data from a file and assembles objects for each.

        Args:
            data_file : A DataFrame object of a csv that
                represents the data on Areas. Each row corresponds to a
                single Area, and iterating through assembles the
                AreaManager's areas object

        Returns:
            None
        """
        for index, row in data_file.items():
            self.areas.append(Area(row['area_name'], row['capacity'],
                                   row['order'], row['num_checks']))

    def get_emptiest_area(self):
        """Retrieves the least full area, by current_volume.

        Note:
            Won't return areas where num_placed_checks > num_checks,
            even though no sorting is done on that parameter.

        Args:
            None

        Returns:
            An Area, or if all Areas are full in both volume and number of
            checks, returns None.
        """
        try:
             emptiest =  min([x for x in self.areas if x.current_volume < x.area_capacity
                        and x.num_placed_checks < x.num_checks], \
                        key=lambda item: item.current_volume)
             return emptiest
        except:
            return None
        
    def get_random_area(self):
        try:
             random_area =  self.random.choice([x for x in self.areas if x.current_volume < x.area_capacity
                        and x.num_placed_checks < x.num_checks])
             return random_area
        except:
            # print("Broken new area ")
            return None        
        
        
    def any_areas_not_full(self):
        """Determines if any areas still have checks yet to be placed

        Args:
            none

        Returns:
            True if any area has fewere placed checks than total checks, and
            False otherwise.
        """
        return any(x.num_placed_checks < x.num_checks for x in self.areas)

    def update_volume(self, reward):
        """Updates an Area object to track the new volume and check count

        Note:
            This method takes a Reward object and accepts the burden of
            determining the Area to update based on the area_name parameter
            on that reward. Reward has a string represenation of the area
            name, rather than an explicit reference to an Area object

        Args:
            reward (Reward): A Reward object fully updated with a collectible,
                and therefore a value. Rewards without placed collectibles are
                not valid inputs to this method.

        Returns:
            None
        """
        for i in self.areas:
            if reward.area == i.area_name:

                i.current_volume += reward.collectible.reward_value
                i.num_placed_checks += 1
                return

    def change_power_level(self, factor):
        """Allows for wide ranging changes to total capacity for all Areas

        Note:
            Increasing capacity corellates to an
            increase in item power in that Area.

        Args:
            factor (float): A multiplicative factor to apply to the capacity
                of each Area. The resulting value is floored.

        Returns:
            None
        """
        for i in self.areas:
            i.area_capacity = math.floor(i.area_capacity * factor)

    def get_area_by_name(self, name):
        """Gets an area with a matching name.

        Args:
            name (str): The name of the Area to get.

        Returns:
            An Area object if a matching name is found, otherwise None.
        """
        for i in self.areas:
            if i.area_name == name:
                return i