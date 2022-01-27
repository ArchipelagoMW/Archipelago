import string

from BaseClasses import Item, MultiWorld, Region, Location, Entrance, LocationProgressType
from .Items import item_table
from .Locations import location_table
from .Rules import set_rules
from ..AutoWorld import World
from .Options import bingo_options
from .Regions import create_regions
import os


class BingoWorld(World):
    options = bingo_options
    game = "Bingo"
    topology_present = False
    data_version = 1

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    forced_auto_forfeit = True

    cards = {}

    def __init__(self, world: MultiWorld, player: int):
        self.world = world
        self.player = player

    def _get_slot_data(self):
        return {
            'card_pairs': self.world.card_pairs[self.player],
            'cards': self.cards[self.player]
        }

    def generate_cards(self, world, player):
        cards = []
        pairs = world.card_pairs[player]
        for _ in range(0, 2):
            items = list(item_table)[:pairs * 24]
            world.random.shuffle(items)
            for c in range(0, pairs):
                card = []
                for row in range(1, 6):
                    if row == 3:
                        card_row = items[:2] + [0] + items[2:4]
                        items = items[4:]
                    else:
                        card_row = items[:5]
                        items = items[5:]
                    card.append(card_row)
                cards.append(card)

        world.worlds[player].cards[player] = cards

    def generate_basic(self):
        pool = []
        card_pairs = self.world.card_pairs[self.player]
        items = list(item_table)
        b = 0
        for _ in range(0, card_pairs):
            for _ in range(0, 24):
                item = BingoItem(items[b], self.player)
                pool.append(item)
                if self.world.force_non_local[self.player]:
                    self.world.non_local_items[self.player].value.add(item.name)
                b += 1

        self.world.itempool += pool
        self.world.get_location("Completed Cards", self.player).place_locked_item(BingoItem("Completion", self.player))
        self.world.completion_condition[self.player] = lambda state: state.has("Completion", self.player)
        self.sending_visible = self.world.reveal_rewards[self.player]

    def set_rules(self):
        self.generate_cards(self.world, self.player)
        set_rules(self.world, self.player)

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        return Item(name, item_data.progression, item_data.code, self.player)

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in bingo_options:
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = int(option.value)
        return slot_data

    def create_regions(self):
        create_regions(self.world, self.player)

    def generate_output(self, output_directory: str):
        filename = f"AP-{self.world.seed_name}-P{self.player}-{self.world.player_name[self.player]}.html"
        out_file = os.path.join(output_directory, filename)
        with open(out_file, 'w') as f:
            # Web design is my passion
            f.write("<HTML><HEAD><STYLE>body {font-family: Courier;}</STYLE></HEAD><BODY>")
            for cardnum in range(0, len(self.cards[self.player])):
                card = self.cards[self.player][cardnum]
                f.write(f"|--------------|<BR>| B I N G O &nbsp;{cardnum+1} |<BR>|--------------|<BR>")
                for row in card:
                    f.write("|")
                    for c in row:
                        if c == 0:
                            f.write("**|")
                        else:
                            f.write(str(c.split()[2]) + "|")
                    f.write("<BR>|--------------|<BR>")
                f.write("<BR>")
            f.write("</BODY></HTML>")


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = location_table.get(location, 0)
            if loc_id is not None:
                if loc_id - 900 >= (world.card_pairs[player] * 24):
                    continue
            location = BingoLocation(player, location, loc_id, ret)
            if world.advancement_items_only[player]:
                location.progress_type = LocationProgressType.PRIORITY
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret


class BingoLocation(Location):
    game: str = "Bingo"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(BingoLocation, self).__init__(player, name, address, parent)
        if address is None:
            self.event = True
            self.locked = True


class BingoItem(Item):
    game = "Bingo"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(BingoItem, self).__init__(name, item_data.progression, item_data.code, player)
