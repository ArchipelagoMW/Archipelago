from typing import Callable, Union, Dict, Set

from BaseClasses import MultiWorld
from ..generic.Rules import add_rule, set_rule
from .Locations import location_table
from .Options import SM64Options
from .Regions import connect_regions, SM64Levels, sm64_level_to_paintings, sm64_paintings_to_level,\
sm64_level_to_secrets, sm64_secrets_to_level, sm64_entrances_to_level, sm64_level_to_entrances
from .Items import action_item_data_table

def shuffle_dict_keys(world, dictionary: dict) -> dict:
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    world.random.shuffle(keys)
    return dict(zip(keys, values))

def fix_reg(entrance_map: Dict[SM64Levels, str], entrance: SM64Levels, invalid_regions: Set[str],
            swapdict: Dict[SM64Levels, str], world):
    if entrance_map[entrance] in invalid_regions: # Unlucky :C
        replacement_regions = [(rand_entrance, rand_region) for rand_entrance, rand_region in swapdict.items()
                               if rand_region not in invalid_regions]
        rand_entrance, rand_region = world.random.choice(replacement_regions)
        old_dest = entrance_map[entrance]
        entrance_map[entrance], entrance_map[rand_entrance] = rand_region, old_dest
        swapdict[entrance], swapdict[rand_entrance] = rand_region, old_dest
    swapdict.pop(entrance)

def set_rules(world, options: SM64Options, player: int, area_connections: dict, star_costs: dict, move_rando_bitvec: int):
    randomized_level_to_paintings = sm64_level_to_paintings.copy()
    randomized_level_to_secrets = sm64_level_to_secrets.copy()
    valid_move_randomizer_start_courses = [
        "Bob-omb Battlefield", "Jolly Roger Bay", "Cool, Cool Mountain",
        "Big Boo's Haunt", "Lethal Lava Land", "Shifting Sand Land",
        "Dire, Dire Docks", "Snowman's Land"
    ]  # Excluding WF, HMC, WDW, TTM, THI, TTC, and RR
    if options.area_rando >= 1:  # Some randomization is happening, randomize Courses
        randomized_level_to_paintings = shuffle_dict_keys(world,sm64_level_to_paintings)
        # If not shuffling later, ensure a valid start course on move randomizer
        if options.area_rando < 3 and move_rando_bitvec > 0:
            swapdict = randomized_level_to_paintings.copy()
            invalid_start_courses = {course for course in randomized_level_to_paintings.values() if course not in valid_move_randomizer_start_courses}
            fix_reg(randomized_level_to_paintings, SM64Levels.BOB_OMB_BATTLEFIELD, invalid_start_courses, swapdict, world)
            fix_reg(randomized_level_to_paintings, SM64Levels.WHOMPS_FORTRESS, invalid_start_courses, swapdict, world)

    if options.area_rando == 2:  # Randomize Secrets as well
        randomized_level_to_secrets = shuffle_dict_keys(world,sm64_level_to_secrets)
    randomized_entrances = {**randomized_level_to_paintings, **randomized_level_to_secrets}
    if options.area_rando == 3:  # Randomize Courses and Secrets in one pool
        randomized_entrances = shuffle_dict_keys(world, randomized_entrances)
        # Guarantee first entrance is a course
        swapdict = randomized_entrances.copy()
        if move_rando_bitvec == 0:
            fix_reg(randomized_entrances, SM64Levels.BOB_OMB_BATTLEFIELD, sm64_secrets_to_level.keys(), swapdict, world)
        else:
            invalid_start_courses = {course for course in randomized_entrances.values() if course not in valid_move_randomizer_start_courses}
            fix_reg(randomized_entrances, SM64Levels.BOB_OMB_BATTLEFIELD, invalid_start_courses, swapdict, world)
            fix_reg(randomized_entrances, SM64Levels.WHOMPS_FORTRESS, invalid_start_courses, swapdict, world)
        # Guarantee BITFS is not mapped to DDD
        fix_reg(randomized_entrances, SM64Levels.BOWSER_IN_THE_FIRE_SEA, {"Dire, Dire Docks"}, swapdict, world)
        # Guarantee COTMC is not mapped to HMC, cuz thats impossible. If BitFS -> HMC, also no COTMC -> DDD.
        if randomized_entrances[SM64Levels.BOWSER_IN_THE_FIRE_SEA] == "Hazy Maze Cave":
            fix_reg(randomized_entrances, SM64Levels.CAVERN_OF_THE_METAL_CAP, {"Hazy Maze Cave", "Dire, Dire Docks"}, swapdict, world)
        else:
            fix_reg(randomized_entrances, SM64Levels.CAVERN_OF_THE_METAL_CAP, {"Hazy Maze Cave"}, swapdict, world)

    # Destination Format: LVL | AREA with LVL = LEVEL_x, AREA = Area as used in sm64 code
    # Cast to int to not rely on availability of SM64Levels enum. Will cause crash in MultiServer otherwise
    area_connections.update({int(entrance_lvl): int(sm64_entrances_to_level[destination]) for (entrance_lvl,destination) in randomized_entrances.items()})
    randomized_entrances_s = {sm64_level_to_entrances[entrance_lvl]: destination for (entrance_lvl,destination) in randomized_entrances.items()}

    rf = RuleFactory(world, options, player, move_rando_bitvec)

    connect_regions(world, player, "Menu", randomized_entrances_s["Bob-omb Battlefield"])
    connect_regions(world, player, "Menu", randomized_entrances_s["Whomp's Fortress"],
            rf.build_rule("", painting_lvl_name="WF", star_num_req=1))
    # JRB door is separated from JRB itself because the secret aquarium can be accessed without entering the painting
    connect_regions(world, player, "Menu", "Jolly Roger Bay Door", rf.build_rule("", star_num_req=3))
    connect_regions(world, player, "Jolly Roger Bay Door", randomized_entrances_s["Jolly Roger Bay"],
                    rf.build_rule("", painting_lvl_name="JRB"))
    connect_regions(world, player, "Menu", randomized_entrances_s["Cool, Cool Mountain"],
                    rf.build_rule("", painting_lvl_name="CCM", star_num_req=3))
    connect_regions(world, player, "Menu", randomized_entrances_s["Big Boo's Haunt"], lambda state: state.has("Power Star", player, 12))
    connect_regions(world, player, "Menu", randomized_entrances_s["The Princess's Secret Slide"], lambda state: state.has("Power Star", player, 1))
    connect_regions(world, player, "Jolly Roger Bay Door", randomized_entrances_s["The Secret Aquarium"],
                    rf.build_rule("SF/BF | TJ & LG | MOVELESS & TJ"))
    connect_regions(world, player, "Menu", randomized_entrances_s["Tower of the Wing Cap"], lambda state: state.has("Power Star", player, 10))
    connect_regions(world, player, "Menu", randomized_entrances_s["Bowser in the Dark World"],
                    lambda state: state.has("Power Star", player, star_costs["FirstBowserDoorCost"]))

    connect_regions(world, player, "Menu", "Basement", lambda state: state.has("Basement Key", player) or state.has("Progressive Key", player, 1))

    connect_regions(world, player, "Basement", randomized_entrances_s["Hazy Maze Cave"])
    connect_regions(world, player, "Basement", randomized_entrances_s["Lethal Lava Land"],
                    rf.build_rule("", painting_lvl_name="LLL"))
    connect_regions(world, player, "Basement", randomized_entrances_s["Shifting Sand Land"],
                    rf.build_rule("", painting_lvl_name="SSL"))
    connect_regions(world, player, "Basement", randomized_entrances_s["Dire, Dire Docks"],
                    rf.build_rule("", painting_lvl_name="DDD", star_num_req=star_costs["BasementDoorCost"]))
    connect_regions(world, player, "Hazy Maze Cave", randomized_entrances_s["Cavern of the Metal Cap"])
    connect_regions(world, player, "Basement", randomized_entrances_s["Vanish Cap under the Moat"],
                    rf.build_rule("GP"))
    entrance = connect_regions(world, player, "Basement", randomized_entrances_s["Bowser in the Fire Sea"],
                               lambda state: state.has("Power Star", player, star_costs["BasementDoorCost"]) and
                               state.can_reach("DDD: Board Bowser's Sub", 'Location', player))
    # Access to "DDD: Board Bowser's Sub" does not require access to other locations or regions, so the only region that
    # needs to be registered is its parent region.
    world.register_indirect_condition(world.get_location("DDD: Board Bowser's Sub", player).parent_region, entrance)

    connect_regions(world, player, "Menu", "Second Floor", lambda state: state.has("Second Floor Key", player) or state.has("Progressive Key", player, 2))

    connect_regions(world, player, "Second Floor", randomized_entrances_s["Snowman's Land"],
                    rf.build_rule("", painting_lvl_name="SL"))
    connect_regions(world, player, "Second Floor", randomized_entrances_s["Wet-Dry World"],
                    rf.build_rule("", painting_lvl_name="WDW"))
    connect_regions(world, player, "Second Floor", randomized_entrances_s["Tall, Tall Mountain"],
                    rf.build_rule("", painting_lvl_name="TTM"))
    connect_regions(world, player, "Second Floor", randomized_entrances_s["Tiny-Huge Island (Tiny)"],
                    rf.build_rule("", painting_lvl_name="THI"))
    connect_regions(world, player, "Second Floor", randomized_entrances_s["Tiny-Huge Island (Huge)"],
                    rf.build_rule("", painting_lvl_name="THI"))
    connect_regions(world, player, "Tiny-Huge Island (Tiny)", "Tiny-Huge Island")
    connect_regions(world, player, "Tiny-Huge Island (Huge)", "Tiny-Huge Island")

    connect_regions(world, player, "Second Floor", "Third Floor", lambda state: state.has("Power Star", player, star_costs["SecondFloorDoorCost"]))

    connect_regions(world, player, "Third Floor", randomized_entrances_s["Tick Tock Clock"],
                    rf.build_rule("LG/TJ/SF/BF/WK", painting_lvl_name="TTC"))
    connect_regions(world, player, "Third Floor", randomized_entrances_s["Rainbow Ride"], rf.build_rule("TJ/SF/BF"))
    connect_regions(world, player, "Third Floor", randomized_entrances_s["Wing Mario over the Rainbow"], rf.build_rule("TJ/SF/BF"))
    connect_regions(world, player, "Third Floor", "Bowser in the Sky", lambda state: state.has("Power Star", player, star_costs["StarsToFinish"]))

    # Course Rules
    # Bob-omb Battlefield
    rf.assign_rule("BoB: Island", "CANN | CANNLESS & WC & TJ | CAPLESS & CANNLESS & LJ")
    rf.assign_rule("BoB: Mario Wings to the Sky",  "CANN & WC | CAPLESS & CANN")
    rf.assign_rule("BoB: Behind Chain Chomp's Gate", "GP | MOVELESS")
    # Whomp's Fortress
    rf.assign_rule("WF: Tower", "GP")
    rf.assign_rule("WF: Chip Off Whomp's Block", "GP")
    rf.assign_rule("WF: Shoot into the Wild Blue", "WK & TJ/SF | CANN")
    rf.assign_rule("WF: Fall onto the Caged Island", "CL & {WF: Tower} | MOVELESS & TJ | MOVELESS & LJ | MOVELESS & CANN")
    rf.assign_rule("WF: Blast Away the Wall", "CANN | CANNLESS & LG")
    # Jolly Roger Bay
    rf.assign_rule("JRB: Upper", "TJ/BF/SF/WK | MOVELESS & LG")
    rf.assign_rule("JRB: Red Coins on the Ship Afloat", "CL/CANN/TJ | MOVELESS & BF/WK")
    rf.assign_rule("JRB: Blast to the Stone Pillar", "CANN+CL | CANNLESS & MOVELESS | CANN & MOVELESS")
    rf.assign_rule("JRB: Through the Jet Stream", "MC | CAPLESS")
    # Cool, Cool Mountain
    rf.assign_rule("CCM: Wall Kicks Will Work", "TJ/WK & CANN | CANNLESS & TJ/WK | MOVELESS")
    # Big Boo's Haunt
    rf.assign_rule("BBH: Third Floor", "WK+LG | MOVELESS & WK")
    rf.assign_rule("BBH: Roof", "LJ | MOVELESS")
    rf.assign_rule("BBH: Secret of the Haunted Books", "KK | MOVELESS")
    rf.assign_rule("BBH: Seek the 8 Red Coins", "BF/WK/TJ/SF")
    rf.assign_rule("BBH: Eye to Eye in the Secret Room", "VC")
    # Haze Maze Cave
    rf.assign_rule("HMC: Red Coin Area", "CL & WK/LG/BF/SF/TJ | MOVELESS & WK")
    rf.assign_rule("HMC: Pit Islands", "TJ+CL | MOVELESS & WK & TJ/LJ | MOVELESS & WK+SF+LG")
    rf.assign_rule("HMC: Metal-Head Mario Can Move!", "LJ+MC | CAPLESS & LJ+TJ | CAPLESS & MOVELESS & LJ/TJ/WK")
    rf.assign_rule("HMC: Navigating the Toxic Maze", "WK/SF/BF/TJ")
    rf.assign_rule("HMC: Watch for Rolling Rocks", "WK")
    # Lethal Lava Land
    rf.assign_rule("LLL: Upper Volcano", "CL")
    # Shifting Sand Land
    rf.assign_rule("SSL: Upper Pyramid", "CL & TJ/BF/SF/LG | MOVELESS")
    rf.assign_rule("SSL: Stand Tall on the Four Pillars", "TJ+WC+GP | CANN+WC+GP | TJ/SF/BF & CAPLESS | MOVELESS")
    rf.assign_rule("SSL: Free Flying for 8 Red Coins", "TJ+WC | CANN+WC | TJ/SF/BF & CAPLESS | MOVELESS & CAPLESS")
    # Dire, Dire Docks
    rf.assign_rule("DDD: Pole-Jumping for Red Coins", "CL & {{Bowser in the Fire Sea Key}} | TJ+DV+LG+WK & MOVELESS")
    rf.assign_rule("DDD: Through the Jet Stream", "MC | CAPLESS")
    rf.assign_rule("DDD: Collect the Caps...", "VC+MC | CAPLESS & VC")
    # Snowman's Land
    rf.assign_rule("SL: Snowman's Big Head", "BF/SF/CANN/TJ")
    rf.assign_rule("SL: In the Deep Freeze", "WK/SF/LG/BF/CANN/TJ")
    rf.assign_rule("SL: Into the Igloo", "VC & TJ/SF/BF/WK/LG | MOVELESS & VC")
    # Wet-Dry World
    rf.assign_rule("WDW: Top", "WK/TJ/SF/BF | MOVELESS")
    rf.assign_rule("WDW: Downtown", "NAR & LG & TJ/SF/BF | CANN | MOVELESS & TJ+DV")
    rf.assign_rule("WDW: Go to Town for Red Coins", "WK | MOVELESS & TJ")
    rf.assign_rule("WDW: Quick Race Through Downtown!", "VC & WK/BF | VC & TJ+LG | MOVELESS & VC & TJ")
    rf.assign_rule("WDW: Bob-omb Buddy", "TJ | SF+LG | NAR & BF/SF")
    # Tall, Tall Mountain
    rf.assign_rule("TTM: Top", "MOVELESS & TJ | LJ/DV & LG/KK | MOVELESS & WK & SF/LG | MOVELESS & KK/DV")
    rf.assign_rule("TTM: Blast to the Lonely Mushroom", "CANN | CANNLESS & LJ | MOVELESS & CANNLESS")
    # Tiny-Huge Island
    rf.assign_rule("THI: 1Up Block THI Small near Start", "NAR | {THI: Pipes}")
    rf.assign_rule("THI: Pipes", "NAR | LJ/TJ/DV/LG | MOVELESS & BF/SF/KK")
    rf.assign_rule("THI: Large Top", "NAR | LJ/TJ/DV | MOVELESS")
    rf.assign_rule("THI: Wiggler's Red Coins", "WK")
    rf.assign_rule("THI: Make Wiggler Squirm", "GP | MOVELESS & DV")
    # Tick Tock Clock
    rf.assign_rule("TTC: Lower", "LG/TJ/SF/BF/WK")
    rf.assign_rule("TTC: Upper", "CL | MOVELESS & WK")
    rf.assign_rule("TTC: Top", "TJ+LG | MOVELESS & WK/TJ")
    rf.assign_rule("TTC: Stop Time for Red Coins", "NAR | {TTC: Lower}")
    # Rainbow Ride
    rf.assign_rule("RR: Maze", "WK | LJ & SF/BF/TJ | MOVELESS & LG/TJ")
    rf.assign_rule("RR: Bob-omb Buddy", "WK | MOVELESS & LG")
    rf.assign_rule("RR: Swingin' in the Breeze", "LG/TJ/BF/SF | MOVELESS")
    rf.assign_rule("RR: Tricky Triangles!", "LG/TJ/BF/SF | MOVELESS")
    rf.assign_rule("RR: Cruiser", "WK/SF/BF/LG/TJ")
    rf.assign_rule("RR: House", "TJ/SF/BF/LG")
    rf.assign_rule("RR: Somewhere Over the Rainbow", "CANN")
    # Cavern of the Metal Cap
    rf.assign_rule("Cavern of the Metal Cap Red Coins", "MC | CAPLESS")
    # Vanish Cap Under the Moat
    rf.assign_rule("Vanish Cap Under the Moat Switch", "WK/TJ/BF/SF/LG | MOVELESS")
    rf.assign_rule("Vanish Cap Under the Moat Red Coins", "TJ/BF/SF/LG/WK & VC | CAPLESS & WK")
    # Bowser in the Fire Sea
    rf.assign_rule("BitFS: Upper", "CL")
    rf.assign_rule("Bowser in the Fire Sea Red Coins", "LG/WK")
    rf.assign_rule("Bowser in the Fire Sea 1Up Block Near Poles", "LG/WK")
    # Wing Mario Over the Rainbow
    rf.assign_rule("Wing Mario Over the Rainbow Red Coins", "TJ+WC")
    rf.assign_rule("Wing Mario Over the Rainbow 1Up Block", "TJ+WC")
    # Bowser in the Sky
    rf.assign_rule("BitS: Top", "CL+TJ | CL+SF+LG | MOVELESS & TJ+WK+LG")
    # 100 Coin Stars
    if options.enable_coin_stars:
        rf.assign_rule("BoB: 100 Coins", "CANN & WC | CANNLESS & WC & TJ")
        rf.assign_rule("WF: 100 Coins", "GP | MOVELESS")
        rf.assign_rule("JRB: 100 Coins", "GP & {JRB: Upper}")
        rf.assign_rule("HMC: 100 Coins", "GP")
        rf.assign_rule("SSL: 100 Coins", "{SSL: Upper Pyramid} | GP")
        rf.assign_rule("DDD: 100 Coins", "GP & {{DDD: Pole-Jumping for Red Coins}}")
        rf.assign_rule("SL: 100 Coins", "VC | CAPLESS")
        rf.assign_rule("WDW: 100 Coins", "GP | {WDW: Downtown}")
        rf.assign_rule("TTC: 100 Coins", "GP")
        rf.assign_rule("THI: 100 Coins", "GP")
        rf.assign_rule("RR: 100 Coins", "GP & WK")
    # Castle Stars
    add_rule(world.get_location("Toad (Basement)", player), lambda state: state.can_reach("Basement", 'Region', player) and state.has("Power Star", player, 12))
    add_rule(world.get_location("Toad (Second Floor)", player), lambda state: state.can_reach("Second Floor", 'Region', player) and state.has("Power Star", player, 25))
    add_rule(world.get_location("Toad (Third Floor)", player), lambda state: state.can_reach("Third Floor", 'Region', player) and state.has("Power Star", player, 35))

    if star_costs["MIPS1Cost"] > star_costs["MIPS2Cost"]:
        (star_costs["MIPS2Cost"], star_costs["MIPS1Cost"]) = (star_costs["MIPS1Cost"], star_costs["MIPS2Cost"])
    rf.assign_rule("MIPS 1", "DV | MOVELESS")
    rf.assign_rule("MIPS 2", "DV | MOVELESS")
    add_rule(world.get_location("MIPS 1", player), lambda state: state.can_reach("Basement", 'Region', player) and state.has("Power Star", player, star_costs["MIPS1Cost"]))
    add_rule(world.get_location("MIPS 2", player), lambda state: state.can_reach("Basement", 'Region', player) and state.has("Power Star", player, star_costs["MIPS2Cost"]))

    world.completion_condition[player] = lambda state: state.can_reach("BitS: Top", 'Region', player)

    if options.completion_type == "last_bowser_stage":
        world.completion_condition[player] = lambda state: state.can_reach("BitS: Top", 'Region', player)
    elif options.completion_type == "all_bowser_stages":
        world.completion_condition[player] = lambda state: state.can_reach("Bowser in the Dark World", 'Region', player) and \
                                                           state.can_reach("BitFS: Upper", 'Region', player) and \
                                                           state.can_reach("BitS: Top", 'Region', player)


class RuleFactory:

    world: MultiWorld
    player: int
    move_rando_bitvec: bool
    area_randomizer: bool
    capless: bool
    cannonless: bool
    moveless: bool

    token_table = {
        "TJ": "Triple Jump",
        "DJ": "Triple Jump",
        "LJ": "Long Jump",
        "BF": "Backflip",
        "SF": "Side Flip",
        "WK": "Wall Kick",
        "DV": "Dive",
        "GP": "Ground Pound",
        "KK": "Kick",
        "CL": "Climb",
        "LG": "Ledge Grab",
        "WC": "Wing Cap",
        "MC": "Metal Cap",
        "VC": "Vanish Cap"
    }

    class SM64LogicException(Exception):
        pass

    def __init__(self, world, options: SM64Options, player: int, move_rando_bitvec: int):
        self.world = world
        self.player = player
        self.move_rando_bitvec = move_rando_bitvec
        self.area_randomizer = options.area_rando > 0
        self.painting_randomizer = options.enable_locked_paintings
        self.capless = not options.strict_cap_requirements
        self.cannonless = not options.strict_cannon_requirements
        self.moveless = not options.strict_move_requirements

    def assign_rule(self, target_name: str, rule_expr: str):
        target = self.world.get_location(target_name, self.player) if target_name in location_table else self.world.get_entrance(target_name, self.player)
        cannon_name = "Cannon Unlock " + target_name.split(':')[0]
        try:
            rule = self.build_rule(rule_expr, cannon_name)
        except RuleFactory.SM64LogicException as exception:
            raise RuleFactory.SM64LogicException(
                f"Error generating rule for {target_name} using rule expression {rule_expr}: {exception}")
        if rule:
            set_rule(target, rule)

    def build_rule(self, rule_expr: str, cannon_name: str = '', painting_lvl_name: str = None, star_num_req: int = None) -> Callable:
        # Star/painting requirements are outer and'd requirements, logically (painting? star? and (rule_expr))
        base_rule = self.build_star_painting_entry_requirements(painting_lvl_name, star_num_req)
        expressions = rule_expr.split(" | ") if len(rule_expr) > 0 else []
        rules = []
        for expression in expressions:
            or_clause = self.combine_and_clauses(expression, cannon_name)
            if or_clause is True:
                return base_rule
            if or_clause is not False:
                rules.append(or_clause)
        if rules:
            if len(rules) == 1:
                return lambda state: base_rule(state) and rules[0](state)
            else:
                return lambda state: base_rule(state) and any(rule(state) for rule in rules)
        else:
            return base_rule

    def build_star_painting_entry_requirements(self, painting_lvl_name: str = None, star_num_req: int = None) -> Callable:
        nop_condition = lambda state: True
        star_rule = nop_condition
        painting_rule = nop_condition
        if painting_lvl_name is not None and self.painting_randomizer:
            painting_item_name = f"Painting Unlock {painting_lvl_name}"
            painting_rule = lambda state: state.has(painting_item_name, self.player)
        if star_num_req is not None:
            star_rule = lambda state: state.has("Power Star", self.player, star_num_req)
        return lambda state: star_rule(state) and painting_rule(state)

    def combine_and_clauses(self, rule_expr: str, cannon_name: str) -> Union[Callable, bool]:
        expressions = rule_expr.split(" & ")
        rules = []
        for expression in expressions:
            and_clause = self.make_lambda(expression, cannon_name)
            if and_clause is False:
                return False
            if and_clause is not True:
                rules.append(and_clause)
        if rules:
            if len(rules) == 1:
                return rules[0]
            return lambda state: all(rule(state) for rule in rules)
        else:
            return True

    def make_lambda(self, expression: str, cannon_name: str) -> Union[Callable, bool]:
        if '+' in expression:
            tokens = expression.split('+')
            items = set()
            for token in tokens:
                item = self.parse_token(token, cannon_name)
                if item is True:
                    continue
                if item is False:
                    return False
                items.add(item)
            if items:
                return lambda state: state.has_all(items, self.player)
            else:
                return True
        if '/' in expression:
            tokens = expression.split('/')
            items = set()
            for token in tokens:
                item = self.parse_token(token, cannon_name)
                if item is True:
                    return True
                if item is False:
                    continue
                items.add(item)
            if items:
                return lambda state: state.has_any(items, self.player)
            else:
                return False
        if '{{' in expression:
            return lambda state: state.can_reach(expression[2:-2], "Location", self.player)
        if '{' in expression:
            return lambda state: state.can_reach(expression[1:-1], "Region", self.player)
        item = self.parse_token(expression, cannon_name)
        if item in (True, False):
            return item
        return lambda state: state.has(item, self.player)

    def parse_token(self, token: str, cannon_name: str) -> Union[str, bool]:
        if token == "CANN":
            return cannon_name
        if token == "CAPLESS":
            return self.capless
        if token == "CANNLESS":
            return self.cannonless
        if token == "MOVELESS":
            return self.moveless
        if token == "NAR":
            return not self.area_randomizer
        item = self.token_table.get(token, None)
        if not item:
            raise Exception(f"Invalid token: '{item}'")
        if item in action_item_data_table:
            double_jump_bitvec_offset = action_item_data_table['Double Jump'].code
            if self.move_rando_bitvec & (1 << (action_item_data_table[item].code - double_jump_bitvec_offset)) == 0:
                # This action item is not randomized.
                return True
        return item

