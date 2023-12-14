from typing import List

from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
# from worlds.generic import Rules
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule
from .Options import DSTOptions
from . import Constants

from BaseClasses import Region, Entrance, Item, Tutorial, ItemClassification, Location

def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="DontStarveTogetherClient")


components.append(Component("DST Client", "DontStarveTogetherClient", func=launch_client, 
                            component_type=Type.CLIENT))

def fillgroups() -> dict:
    allitems = set()
    starteritems = set()
    prebossitems = set()
    postbossitems = set()

    for item_name in Constants.item_info["starter"]:
        allitems.add(item_name)
        starteritems.add(item_name)
    for item_name in Constants.item_info["pre_boss"]:
        allitems.add(item_name)
        prebossitems.add(item_name)
    for item_name in Constants.item_info["post_boss"]:
        allitems.add(item_name)
        postbossitems.add(item_name)
    # for item_name in Constants.item_info["traps"]:
    #     for _ in range(Constants.item_info["traps"][item_name]):
    #         prebossitems.add(item_name) #For checking pre-boss location checks which may also include traps

    return {"allitems": allitems, "pre_boss": prebossitems, "post_boss": postbossitems, "starter": starteritems}

class DST(World):
    """
    Don't Starve Together is a game where you are thrown into a strange and unexplored world full of odd creatures, 
    hidden dangers, and ancient secrets known as "The Constant". You must gather resources to craft items and build 
    strucutres and farms to help you protect yourself, survive, and most importantly, not starve.
    """
    game = "Don't Starve Together"

    item_name_to_id = Constants.item_name_to_id
    location_name_to_id = Constants.location_name_to_id

    options_dataclass = DSTOptions  # assign the options dataclass to the world
    options: DSTOptions  # typing for option results
    topology_present = False

    # web = DSTWeb()

    item_name_groups = fillgroups()
    # print(item_name_groups)



    def create_items(self) -> None:
        for item_name in Constants.item_info["starter"]:
            self.multiworld.push_precollected(self.multiworld.create_item(item_name, self.player))

        self.multiworld.get_location("Ancient Fuelweaver", self.player).place_locked_item(
                                                                        self.create_item_event("Shadow Boss Kill"))
        self.multiworld.get_location("Celestial Champion", self.player).place_locked_item(
                                                                        self.create_item_event("Lunar Boss Kill"))

        itempool = []

        for item_name in Constants.item_info["all_items"]:
            if item_name in Constants.item_info["traps"]:
                for _ in range(Constants.item_info["traps"][item_name]):
                    itempool.append(self.create_item(item_name))
            elif not item_name in Constants.item_info["starter"]:
                itempool.append(self.create_item(item_name))

        self.multiworld.itempool += itempool

    def create_item(self, name: str) -> Item:
        item_class = ItemClassification.useful # Only progression items count towards state checks
        if name in Constants.item_info["pre_boss"]:
            item_class = ItemClassification.progression
        if name in Constants.item_info["starter"]:
            item_class = ItemClassification.filler
        # elif name in Constants.item_info["useful_items"]:
        #     item_class = ItemClassification.useful
        elif name in Constants.item_info["traps"]:
            item_class = ItemClassification.trap
        # print(name, item_class, self.item_name_to_id.get(name, None), self.player)
        return DontStarveTogetherItem(name, item_class, self.item_name_to_id.get(name, None), self.player)
    
    def create_item_event(self, name: str):
        return DontStarveTogetherItem(name, ItemClassification.progression, None, self.player)
    def create_location_event(self, name: str, parent: Region):
        return DontStarveTogetherLocation(self.player, name, None, parent)

    def generate_early(self) -> None:
        # winlocations = []
        bosses = self.options.bosses.current_key
        # print(bosses)

        # if bosses == "either" or bosses == "both" or bosses == "ancient_fuelweaver":
        #     if "Ancient Fuelweaver" in self.location_names:
        #         winlocations.append("Ancient Fuelweaver")
        #     elif "Ancient Fuelweaver (1)" in self.location_names:
        #         winlocations.append("Ancient Fuelweaver (1)")
        # if bosses == "either" or bosses == "both" or bosses == "celestial_champion":
        #     if "Celestial Champion" in self.location_names:
        #         winlocations.append("Celestial Champion")
        #     elif "Celestial Champion (1)" in self.location_names:
        #         winlocations.append("Celestial Champion (1)")

        self.bosses = bosses
        # self.winlocations = winlocations
        # print(self.bosses, self.winlocations)
    
    def generate_basic(self) -> None:

        def bosscondition(state): 
            if self.bosses == "both":
                return state.has("Shadow Boss Kill", self.player) and state.has("Lunar Boss Kill", self.player)
            elif self.bosses == "either":
                return state.has("Shadow Boss Kill", self.player) or state.has("Lunar Boss Kill", self.player)
            elif self.bosses == "ancient_fuelweaver":
                return state.has("Shadow Boss Kill", self.player)
            elif self.boss == "celestial_champion":
                return state.has("Lunar Boss Kill", self.player)
            elif self.boss == "none":
                return True
        def killcondition(state): #unimplimented
            return True
            # return state

        if self.bosses != "none":
            self.multiworld.completion_condition[self.player] = lambda state: bosscondition(state)

    def create_regions(self) -> None:
        
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        
        preboss_region = Region("Pre Boss", self.player, self.multiworld)
        for loc_name in Constants.location_info["pre_boss"]:
            loc = DontStarveTogetherLocation(self.player, loc_name,
                self.location_name_to_id.get(loc_name, None), preboss_region)
            preboss_region.locations.append(loc)
        self.multiworld.regions.append(preboss_region)

        menu_region.connect(preboss_region)
        
        postboss_region = Region("Post Boss", self.player, self.multiworld)
        for loc_name in Constants.location_info["post_boss"]:
            if not (loc_name.startswith("Ancient Fuelweaver") or loc_name.startswith("Celestial Champion")):
                loc = DontStarveTogetherLocation(self.player, loc_name,
                    self.location_name_to_id.get(loc_name, None), postboss_region)
                postboss_region.locations.append(loc)
        postboss_region.locations.append(self.create_location_event("Ancient Fuelweaver", postboss_region))
        postboss_region.locations.append(self.create_location_event("Celestial Champion", postboss_region))
        self.multiworld.regions.append(postboss_region)

        connection = Entrance(self.player, "All Pre Boss", preboss_region)
        preboss_region.exits.append(connection) #Commented so we can handle progression through exits instead
        connection.connect(postboss_region)

        # endgame_region = Region("Endgame", self.player, self.multiworld)
        # self.multiworld.regions.append(endgame_region)

        # connection = Entrance(self.player, "Final Boss Kill", postboss_region)
        # postboss_region.exits.append(connection) #Commented so we can handle progression through exits instead
        # connection.connect(endgame_region)


    def set_rules(self) -> None:

        def canfightboss(state):
            return (state.has("Rope", self.player) and #I'll need to make a modular way to do this later
                    state.has("Spear", self.player) and
                    state.has("Log Suit", self.player) and
                    state.has("Football Helmet", self.player) and
                    state.has("Science Machine", self.player) and
                    state.has("Alchemy Engine", self.player) and 
                    state.has("Backpack", self.player))

        set_rule(self.multiworld.get_entrance("All Pre Boss", self.player),
             lambda state: canfightboss(state))
        # for loc_name in Constants.location_info["post_boss"]:
        #     loc = self.multiworld.get_location(loc_name, self.player)
        #     add_rule(loc, lambda state: canfightboss(state))


    def fill_slot_data(self):
        slot_data = {"death_link": bool(self.multiworld.death_link[self.player].value),
                     "bosses": str(self.bosses)
                    }
        return slot_data
    
class DontStarveTogetherLocation(Location):
    game = "Don't Starve Together"

class DontStarveTogetherItem(Item):
    game = "Don't Starve Together"