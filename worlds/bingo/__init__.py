import string

from BaseClasses import Item, MultiWorld, Region, Location, Entrance, LocationProgressType
from .Items import item_table
from .Locations import location_table
from .Rules import set_rules
from ..AutoWorld import World
from .Options import bingo_options
from .Regions import create_regions
import os
from ..generic.Rules import add_item_rule
from Utils import get_location_name_from_id

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
        min_occ = world.bingo_call_minimum_occurrences[player]
        if min_occ == 2:
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
        else:
            for _ in range(0, pairs*2):
                cards.append([[None, None, None, None, None], [None, None, None, None, None],
                              [None, None, 0, None, None], [None, None, None, None, None],
                              [None, None, None, None, None]])
            remaining_placements = pairs * 48
            if min_occ == 1:
                items = list(item_table)[:pairs * 24]
                world.random.shuffle(items)
                while len(items) > 0:
                    spot = [world.random.randint(0, (pairs*2)-1), world.random.randint(0, 4), world.random.randint(0, 4)]
                    while True:
                        if cards[spot[0]][spot[2]][spot[1]] is None:
                            cards[spot[0]][spot[2]][spot[1]] = items.pop()
                            remaining_placements -= 1
                            break
                        spot[1] += 1
                        if spot[1] == 5:
                            spot[1] = 0
                            spot[2] += 1
                            if spot[2] == 5:
                                spot[2] = 0
                                spot[0] += 1
                                if spot[0] == len(cards):
                                    spot[0] = 0
            items = list(item_table)[:pairs * 24]
            spot = [0, 0, 0]
            while remaining_placements > 0:
                if cards[spot[0]][spot[2]][spot[1]] is None:
                    cards[spot[0]][spot[2]][spot[1]] = items[world.random.randint(0, len(items)-1)]
                    remaining_placements -= 1
                spot[1] += 1
                if spot[1] == 5:
                    spot[1] = 0
                    spot[2] += 1
                    if spot[2] == 5:
                        spot[2] = 0
                        spot[0] += 1
                        if spot[0] == len(cards):
                            break  # should be unnecessary
        world.worlds[player].cards[player] = cards

    def generate_basic(self):
        pool = []
        used_calls = set()
        card_pairs = self.world.card_pairs[self.player]
        for card in self.cards[self.player]:
            for row in card:
                for call in row:
                    used_calls.add(call)
        items = list(item_table)
        b = 0
        for _ in range(0, card_pairs):
            for _ in range(0, 24):
                item = BingoItem(items[b], self.player)
                if item.name not in used_calls:
                    item.advancement = False
                    item.never_exclude = True
                pool.append(item)
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
            slot_data[option_name] = option.value
        return slot_data

    def create_regions(self):
        create_regions(self.world, self.player)

    def generate_output(self, output_directory: str):
        filename = f"AP-{self.world.seed_name}-P{self.player}-{self.world.player_name[self.player]}.html"
        out_file = os.path.join(output_directory, filename)
        with open(out_file, 'w') as f:
            # Web design is my passion
            f.write("<HTML><HEAD><STYLE>body {font-family: Courier;}</STYLE></HEAD><BODY><TABLE>")
            for cardnum in range(0, len(self.cards[self.player])):
                card = self.cards[self.player][cardnum]
                f.write(f"<TR><TD>|--------------|<BR>| B I N G O &nbsp;{cardnum+1} |<BR>|--------------|<BR>")
                for row in card:
                    f.write("|")
                    for c in row:
                        if c == 0:
                            f.write("**|")
                        else:
                            f.write(str(c.split()[2]) + "|")
                    f.write("<BR>|--------------|<BR>")
                f.write("</TD></TR>")
            f.write("</TABLE></BODY></HTML>")

    def received_hint(self, ctx, team, player, hint):
        from MultiServer import notify_hints, collect_hints
        location = get_location_name_from_id(hint.location).split()
        card = ctx.slot_data[player]['cards'][int(location[1]) - 1]
        if location[2] == "Horizontal":
            line = card[int(location[3]) - 1]
        if location[2] == "Vertical":
            line = []
            for i in range(0, 5):
                line.append(card[i][int(location[3]) - 1])
        if location[2] == "Diagonal":
            line = []
            if location[3] == "1":
                for i in range(0, 5):
                    line.append(card[i][i])
            elif location[3] == "2":
                for i in range(0, 5):
                    line.append(card[i][4-i])
        hints = []
        for i in range(0,5):
            if i != 0:
                hints += collect_hints(ctx, team, player, line[i])
        notify_hints(ctx, team, hints)

    def received_checks(self, ctx, team, player):
        from MultiServer import get_received_items, register_location_checks, ClientStatus
        from Utils import get_item_name_from_id
        cards = ctx.slot_data[player]['cards']
        received_items = get_received_items(ctx, team, player, True)
        bingocalls = []
        for b in received_items:
            try:
                bingocalls.append(get_item_name_from_id(b.item))
            except:
                import logging
                logging.info(f"couldn't add {b}")
        for card in range(0, len(cards)):
            # horizontal lines
            for r in range(0, 5):
                row = cards[card][r]
                failed_line = 0
                for i in row:
                    if i != 0:
                        if i not in bingocalls:
                            failed_line = 1
                if not failed_line:
                    loc = f"Bingo Card {card + 1} Horizontal {r + 1}"
                    register_location_checks(ctx, team, player, {location_table[loc]})
            # vertical lines
            for c in range(0, 5):
                failed_line = 0
                for r in range(0, 5):
                    if cards[card][r][c] != 0:
                        if cards[card][r][c] not in bingocalls:
                            failed_line = 1
                if not failed_line:
                    loc = f"Bingo Card {card + 1} Vertical {c + 1}"
                    register_location_checks(ctx, team, player, {location_table[loc]})
            # diagonal lines
            for line in range(0, 2):
                diag = []
                if line == 0:
                    for x in range(0, 5):
                        diag.append(cards[card][x][x])
                elif line == 1:
                    for x in range(0, 5):
                        diag.append(cards[card][4 - x][x])
                failed_line = 0
                for i in diag:
                    if i != 0:
                        if i not in bingocalls:
                            failed_line = 1
                if not failed_line:
                    loc = f"Bingo Card {card + 1} Diagonal {line + 1}"
                    register_location_checks(ctx, team, player, {location_table[loc]})
        if len(bingocalls) == len(cards) * 12:
            ctx.client_game_state[team, player] = ClientStatus.CLIENT_GOAL
            finished_msg = f'{ctx.get_aliased_name(team, player)} (Team #{team + 1})' \
                           f' has been completed.'
            ctx.notify_all(finished_msg)


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        loc_count = (world.card_pairs[player] * 24)
        for location in locations:
            loc_id = location_table.get(location, 0)
            location = BingoLocation(player, location, loc_id, ret)
            if loc_id is not None:
                if loc_id - 1000 >= loc_count:
                    continue
                if (("Horizontal" in location.name and world.priority_rewards_horizontal[player])
                        or ("Vertical" in location.name and world.priority_rewards_vertical[player])
                        or ("Diagonal" in location.name and world.priority_rewards_diagonal[player])):
                    location.progress_type = LocationProgressType.PRIORITY
                    add_item_rule(location, lambda item: item.name not in world.priority_reward_item_blacklist[player])
                if world.disallow_bingo_calls[player]:
                    add_item_rule(location, lambda item: item.game != "Bingo")
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
