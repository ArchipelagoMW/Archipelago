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
            'bingo_mode': self.world.bingo_mode[self.player],
            'cards': self.cards[self.player]
        }

    def generate_cards(self, world, player):

        cards = []
        card_count = world.number_of_rewards[player]
        rewards = world.number_of_rewards[player]
        if world.bingo_mode[player] == 1:
            card_count //= 12
            rewards //= 12
            rewards *= 12
        items = list(item_table)[:rewards]
        div = [rewards // 24 * 5, rewards // 24 * 5, rewards // 24 * 4, rewards // 24 * 5, rewards // 24 * 5]
        while sum(div) < rewards:
            for d in [2, 0, 1, 3, 4]:
                div[d] += 1
                if sum(div) == rewards:
                    break
        div = [div[0], sum(div[:2]), sum(div[:3]), sum(div[:4])]
        call_divisions = [items[:div[0]], items[div[0]:div[1]], items[div[1]:div[2]],
                          items[div[2]:div[3]], items[div[3]:]]
        card_columns = []
        for _ in range(0, card_count):
            card_columns.append([[], [], [], [], []])
            cards.append([[None, None, None, None, None], [None, None, None, None, None],
                          [None, None, 0, None, None], [None, None, None, None, None],
                          [None, None, None, None, None]])
        if not world.allow_unused_calls[player]:
            for column in range(0, 5):
                for item in call_divisions[column]:
                    while True:
                        random_card = world.random.randint(0, len(card_columns) - 1)
                        if len(card_columns[random_card][column]) < 5:
                            card_columns[random_card][column].append(item)
                            break
        for column in range(0, 5):
            for card in range(0, len(card_columns)):
                div_copy = call_divisions[column].copy()
                column_count = 4 if column == 2 else 5
                while len(card_columns[card][column]) < column_count:
                    if len(div_copy) == 0:
                        breakpoint()
                    random_call = world.random.choice(div_copy)
                    div_copy.remove(random_call)
                    if random_call not in card_columns[card][column]:
                        card_columns[card][column].append(random_call)
        for column in range(0, 5):
            for card in range(0, len(card_columns)):
                world.random.shuffle(card_columns[card][column])
                if column == 2:
                    card_columns[card][2].insert(2, 0)
                for row in range(0, 5):
                    cards[card][row][column] = card_columns[card][column][row]
        # world.worlds[player].cards[player] = cards
        self.cards[self.player] = cards

    def generate_basic(self):
        pool = []
        used_calls = set()
        rewards = self.world.number_of_rewards[self.player]
        if self.world.bingo_mode[self.player] == 1:
            rewards //= 12
            rewards *= 12
        for card in self.cards[self.player]:
            for row in card:
                for call in row:
                    used_calls.add(call)
        items = list(item_table)
        for b in range(0, rewards):
            item = BingoItem(items[b], self.player)
            if item.name not in used_calls:
                item.advancement = False
                item.never_exclude = True
            pool.append(item)
        self.world.itempool += pool
        self.world.get_location("Completed Cards", self.player).place_locked_item(BingoItem("Completion", self.player))
        self.world.completion_condition[self.player] = lambda state: state.has("Completion", self.player)

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
        if self.world.bingo_mode[player] == 0 or self.world.auto_hint[player] == 0:
            return
        location = get_location_name_from_id(hint.location).split()
        card = ctx.slot_data[player]['cards'][int(location[2]) - 1]
        if location[3] == "Horizontal":
            line = card[int(location[4]) - 1]
        if location[3] == "Vertical":
            line = []
            for i in range(0, 5):
                line.append(card[i][int(location[4]) - 1])
        if location[3] == "Diagonal":
            line = []
            if location[4] == "1":
                for i in range(0, 5):
                    line.append(card[i][i])
            elif location[4] == "2":
                for i in range(0, 5):
                    line.append(card[i][4-i])
        hints = []
        for i in line:
            if i != 0:
                hints += collect_hints(ctx, team, player, i)
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
                breakpoint()
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
                    if ctx.slot_data[player]["bingo_mode"] == 0:
                        loc = f"Bingo Card {card + 1}"
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
                    if ctx.slot_data[player]["bingo_mode"] == 0:
                        loc = f"Bingo Card {card + 1}"
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
                    if ctx.slot_data[player]["bingo_mode"] == 0:
                        loc = f"Bingo Card {card + 1}"
                    register_location_checks(ctx, team, player, {location_table[loc]})
        if ((len(bingocalls) == len(cards) * 12 and ctx.slot_data[player]["bingo_mode"] == 1) or
                (len(bingocalls) == len(cards) and ctx.slot_data[player]["bingo_mode"] == 0)):
            ctx.client_game_state[team, player] = ClientStatus.CLIENT_GOAL
            finished_msg = f'{ctx.get_aliased_name(team, player)} (Team #{team + 1})' \
                           f' has been completed.'
            ctx.notify_all(finished_msg)

    def get_filler_item_name(self) -> str:
        call = self.world.random.randint(1, len(self.cards[self.player]) * 12)
        return f"Bingo Call {call}"


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    def set_item_rules(location):
        if world.priority_rewards[player]:
            location.progress_type = LocationProgressType.PRIORITY
        add_item_rule(location, lambda item: item.name not in world.item_blacklist[player])
        # add_item_rule(location, lambda item: item.player > item.world.players) # force item link rewards?
        if world.disallow_bingo_calls[player]:
            add_item_rule(location, lambda item: item.game != "Bingo")
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        loc_count = world.number_of_rewards[player]
        if world.bingo_mode[player] == 1:
            loc_count //= 12
            loc_count *= 12
        for location in locations:
            loc_id = location_table.get(location, 0)
            location = BingoLocation(player, location, loc_id, ret)
            if loc_id is not None:
                if loc_id - 1000 >= loc_count and world.bingo_mode[player] == 1:
                    continue
                if (loc_id - 1960 >= loc_count or loc_id < 1960) and world.bingo_mode[player] == 0:
                    continue
                set_item_rules(location)

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
