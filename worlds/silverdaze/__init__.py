from .Rules import set_rules, set_completion_rules
from .Regions import sd_regions
from .Items import SDItem, ItemData, item_table
from .Locations import location_table, SDLocationData
from .Options import SilverDazeOptions
from BaseClasses import Region, Entrance, Tutorial, Item
from worlds.AutoWorld import WebWorld, World
from Items import item_table
from Locations import SDLocationData
from Locations import location_table


class SDWorld(World):
    """
    This will describe Silver Daze eventually.
    """
    game = "Silver Daze"
    required_client_version = (0, 5, 4)
    options_dataclass = SilverDazeOptions

    item_name_to_id = {name: item_table.code.name for name, data in item_table.code}
    location_name_to_id = {name: SDLocationData.id for name, data in SDLocationData.id}

    def get_filler_item_name(self):
        return "Heal Token"

    def create_items(self):
        itempool = []
        for name, max_quantity in item_table:
            itempool += [name] * max_quantity

        #Starting Party Member given at game start
        starter_member = "Pinn"
        if (Options.StartingPartyMember == "option_geo"):
            starter_member = "Geo"
        if (Options.StartingPartyMember == "option_kani"):
            starter_member = "Kani"
        if (Options.StartingPartyMember == "option_random"):
            import random
            #Sawyer: Make sure this has all party members in the final game.
            member = random.randint(1,3)
            if (member == 1): starter_member = "Pinn"
            elif (member == 2): starter_member = "Geo"
            elif (member == 3): starter_member = "Kani"
        itempool.remove(starter_member)
        self.multiworld.push_precollected(self.create_item(starter_member))

        #Create Items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]
        # Fill remaining items with randomly generated junk
        while len(itempool) < len(self.multiworld.get_unfilled_locations(self.player)):
            itempool.append(self.create_filler())

        self.multiworld.itempool += itempool

    def set_rules(self):
        set_rules(self)
        set_completion_rules(self)

    def create_regions(self):
        def SDRegion(region_name: str, exits=[]):
            ret = Region(region_name, self.player, self.multiworld)
            ret.locations += [SDLocationData(ret, id)
                              ]
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.multiworld.regions += [SDRegion(*r) for r in sd_regions]

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = SDItem(name, item_data.classification, item_data.code, self.player)
        return item