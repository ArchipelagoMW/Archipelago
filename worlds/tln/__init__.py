from .Items import TLNItem, item_table, item_frequencies
from .Locations import TLNAdvancement
from .Regions import tln_regions, link_tln_areas
from .Rules import set_rules
from BaseClasses import Region, Entrance, Item
from .Options import tln_options
from worlds.AutoWorld import World


class TLNWorld(World):
    """
    Touhou Luna Nights is a Metroidvania title with a heavy emphasis on exploration and action.　 
    Developed by Team Ladybug, creators of multiple fantastic action games thus far.
    """
    game = "TLN"
    option_definitions = tln_options
    topology_present = True

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in tln_regions.items()}

    data_version = 5

    def _get_tln_data(self):
        return {
            "world_seed": self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
            "client_version": self.required_client_version,
            "race": self.multiworld.is_race,
        }

    def create_items(self):
        # Generate item pool
        itempool = []
        pool_counts = item_frequencies.copy()
        # Add all required progression items

        for name in item_table.items():
            for count in range(pool_counts.get(name, 1)):
                itempool.append(self.create_item(name))

        self.multiworld.itempool += itempool

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_regions(self):
        def TLNRegion(region_name: str, exits=[]):
            ret = Region(region_name, self.player, self.multiworld)
            ret.locations = [TLNAdvancement(self.player, loc_name, loc_data.id, ret)
                             for loc_name, loc_data in tln_regions.items()
                             if loc_data.region == region_name[self.multiworld[self.player].current_key]]
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.multiworld.regions += [TLNRegion(*r) for r in tln_regions]
        link_tln_areas(self.multiworld, self.player)

    def fill_slot_data(self):
        slot_data = self._get_tln_data()

        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = TLNItem(name, item_data.classification, item_data.code, self.player)
        return item
