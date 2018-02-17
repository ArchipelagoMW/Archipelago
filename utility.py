import hashlib
import json
import sys
import random
import re
import ast

### Enums
LOCATION_WARP = 0
LOCATION_MAJOR = 1
LOCATION_MINOR = 2

"""
Variable types:
1. Locations
    - Warp locations - locations with a warp stone
    - Major locations - must have unconstrained path to warp stone
    - Minor locations - cannot have autosave or save points within
2. Items (Item Locations)
3. Additional Items (Items without locations)
4. Pseudo Items
"""

# Structs

class Item(object):
    def __init__(self, position, areaid, itemid):
        self.areaid = areaid
        self.position = position
        self.itemid = itemid
        self.name = None

    # XXXX: Delete if unneeded
    def copy(self):
        item = Item(self.position, self.areaid, self.itemid)
        item.name = self.name
        return item

    # XXXX: Delete if unneeded
    def set_location(self, item):
        self.areaid = item.areaid
        self.position = item.position

    # XXXX: Delete if unneeded
    def __str__(self):
        x, y = self.position
        return '(%d,%d) : %d : %d : %s' % (x, y, self.areaid, self.itemid, self.name)

class MapTransition(object):
    def __init__(self, origin_location, area_current, entry_current, area_target,
            entry_target, walking_right, rect):
        self.origin_location = origin_location
        self.area_current = area_current
        self.entry_current = entry_current
        self.area_target = area_target
        self.entry_target = entry_target
        self.walking_right = walking_right
        self.rect = ast.literal_eval(rect)
        rect_x, rect_y, rect_width, rect_height = self.rect
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.rect_width = rect_width
        self.rect_height = rect_height

class EdgeConstraintData(object):
    def __init__(self, from_location, to_location, prereq_expression):
        self.from_location = from_location
        self.to_location = to_location
        #self.prereq_expression = prereq_expression
        self.prereq_lambda = lambda v : prereq_expression.evaluate(v)

    def __str__(self):
        return '\n'.join([
            'From: %s' % self.from_location,
            'To: %s' % self.to_location,
            'Prereq: %s' % self.prereq_expression,
        ])

class ItemConstraintData(object):
    def __init__(self, item, from_location, entry_prereq, exit_prereq):
        self.item = item
        self.from_location = from_location
        self.entry_prereq = entry_prereq
        self.exit_prereq = exit_prereq

class GraphEdge(object):
    def __init__(self, edge_id, from_location, to_location, constraint, backtrack_cost):
        self.edge_id = edge_id
        self.from_location = from_location
        self.to_location = to_location
        self.satisfied = constraint
        self.backtrack_cost = backtrack_cost


# misc utility functions

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def deterministic_set_zip(s1, s2):
    sorted1 = sorted(s1)
    sorted2 = sorted(s2)
    random.shuffle(sorted1)
    return zip(sorted1, sorted2)

def mean(values):
    values = tuple(values)
    return float(sum(values))/len(values)

def is_potion(item_name):
    return bool(re.match('^[A-Z]*_UP', item_name))

def is_egg(item_name):
    return bool(item_name.startswith('EGG_'))



# Expression Parsing

def parse_expression_lambda(line, variable_names_set, default_expressions):
    expression = parse_expression(line, variable_names_set, default_expressions)
    return lambda v : expression.evaluate(v)

# & - and
# | - or
# !/~ - not
# ( ) - parentheses
# throws errors if parsing fails
def parse_expression(line, variable_names_set, default_expressions={}):
    try:
        # the str(line) cast is used because sometimes <line> is a u'unicode string' on unix machines.
        return parse_expression_logic(str(line), variable_names_set, default_expressions)
    except Exception as e:
        eprint('Error parsing expression:')
        eprint(line)
        raise e

# Used in string parsing. We only have either strings or expressions
isExpr = lambda s : not type(s) is str
def parse_expression_logic(line, variable_names_set, default_expressions):
    pat = re.compile('[()&|~!]')
    line = line.replace('&&', '&').replace('||', '|')
    tokens = (s.strip() for s in re.split('([()&|!~])', line))
    tokens = [s for s in tokens if s]
    # Stack-based parsing. pop from [tokens], push into [stack]
    # We push an expression into [tokens] if we want to process it next iteration.
    tokens.reverse()
    stack = []
    while len(tokens) > 0:
        next = tokens.pop()
        if isExpr(next):
            if len(stack) == 0:
                stack.append(next)
                continue
            head = stack[-1]
            if head == '&':
                stack.pop()
                exp = stack.pop()
                assert isExpr(exp)
                tokens.append(OpAnd(exp, next))
            elif head == '|':
                stack.pop()
                exp = stack.pop()
                assert isExpr(exp)
                tokens.append(OpOr(exp, next))
            elif head in '!~':
                stack.pop()
                tokens.append(OpNot(next))
            else:
                stack.append(next)
        elif next in '(&|!~':
            stack.append(next)
        elif next == ')':
            exp = stack.pop()
            assert isExpr(exp)
            assert stack.pop() == '('
            tokens.append(exp)
        else: # string literal
            # Literal parsing
            if next.startswith('BACKTRACK_'):
                nSteps = int(next[next.rfind('_')+1:])
                tokens.append(OpBacktrack(nSteps))
            elif next in default_expressions:
                tokens.append(default_expressions[next])
            else:
                if next.startswith('r'): next = next[1:]
                if next not in variable_names_set:
                    fail('Unknown variable %s in expression: %s' % (next, line))
                else:
                    tokens.append(OpLit(next))
    assert len(stack) == 1
    return stack[0]


class OpLit(object):
    def __init__(self, name):
        self.name = name
    def evaluate(self, variables):
        return variables[self.name]
    def __str__(self):
        return self.name
    __repr__ = __str__

class OpNot(object):
    def __init__(self, expr):
        self.expr = expr
    def evaluate(self, variables):
        return not self.expr.evaluate(variables)
    def __str__(self):
        return '(NOT %s)' % self.expr
    __repr__ = __str__

class OpOr(object):
    def __init__(self, exprL, exprR):
        self.exprL = exprL
        self.exprR = exprR
    def evaluate(self, variables):
        return self.exprL.evaluate(variables) or self.exprR.evaluate(variables)
    def __str__(self):
        return '(%s OR %s)' % (self.exprL, self.exprR)
    __repr__ = __str__

class OpAnd(object):
    def __init__(self, exprL, exprR):
        self.exprL = exprL
        self.exprR = exprR
    def evaluate(self, variables):
        return self.exprL.evaluate(variables) and self.exprR.evaluate(variables)
    def __str__(self):
        return '(%s AND %s)' % (self.exprL, self.exprR)
    __repr__ = __str__


class OpBacktrack(object):
    def __init__(self, nSteps):
        self.nSteps = nSteps
    def evaluate(self, variables):
        # Yes, we're cheating by putting backtrack data in variables lol.
        if not variables['IS_BACKTRACKING']: return False
        untraversable_edges, outgoing_edges, edges = variables['BACKTRACK_DATA']
        current_node, target_node = variables['BACKTRACK_GOALS']
        reachable = set()
        frontier = set((current_node,0))
        frontier_next = set()

        while len(frontier) > 0:
            for node, distance in frontier:
                for edge_id in outgoing_edges[node]:
                    if edge_id in untraversable_edges: continue
                    target_location = edges[edge_id].to_location
                    new_cost = distance + edges[edge_id].backtrack_cost
                    if new_cost > self.nSteps: continue
                    if target_location == target_node: return True
                    if target_location in reachable: continue
                    frontier_next.add((target_location, new_cost))
                    reachable.add(target_location)
            frontier.clear()
            frontier, frontier_next = frontier_next, frontier
        return False

    def __str__(self):
        return 'BACKTRACK_%d' % self.nSteps
    __repr__ = __str__


# Error Handling

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def fail(message):
    eprint(message)
    sys.exit(1)

def log(*args, **kwargs):
    print(*args, **kwargs)



# File Parsing

def print_error(error, jsondata):
    import re
    pos = int(re.findall('char ([\\d]*)', error.__str__())[0])
    VIEW_RANGE = 100
    start = max(pos-VIEW_RANGE, 0)
    end = min(pos+VIEW_RANGE, len(jsondata))
    eprint('File parsing error')
    eprint(error)
    eprint('Error location:')
    eprint(jsondata[start:pos])
    eprint(jsondata[pos:end])

def parse_json(jsondata):
    try:
        return json.loads(jsondata)
    except ValueError as e:
        print_error(e, jsondata)
        raise e

def read_file_and_strip_comments(filename):
    def strip_comments(line):
        if '//' not in line: return line
        return line[:line.find('//')]
    with open(filename) as f:
        lines = [strip_comments(line).strip() for line in f]
    return lines



# Misc commands

def string_to_integer_seed(s):
    return int(hashlib.md5(s.encode('utf-8')).hexdigest(), base=16)

def hash_map_files(areaids, maps_dir):
    hash  = hashlib.md5()

    for areaid in sorted(areaids):
        hash.update(str(areaid).encode('utf-8'))
        filename = '%s/area%d.map' % (maps_dir, areaid) 
        if not os.path.isfile(filename):
            fail('file %s does not exist!' % filename)
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash.update(chunk)
            
    digest = hash.hexdigest()
    return ('%s-%s' % (digest[:4], digest[4:8])).upper()

def reset_maps(source_dir='original_maps', output_dir='.'):
    if not os.path.isdir(output_dir):
        fail('Output directory %s does not exist' % output_dir)
    itemreader.grab_original_maps(source_dir, output_dir)
    analysis_file = '%s/analysis.txt' % output_dir
    if os.path.isfile(analysis_file):
        os.remove(analysis_file)
    print('Original maps copied to %s.' % output_dir)

def hash_maps(output_dir):
    areaids = get_default_areaids()
    hash_digest = hash_map_files(areaids, output_dir)
    print('Hash: %s' % hash_digest)



# Other Map Modification (shift to randomizer.py later)
#import musicrandomizer
#import backgroundrandomizer


def apply_fixes_for_randomizer(areaid, data):
    if areaid == 0:
        # Add warp CS trigger to enable warps from start of game.
        for y in range(79,100):
            data.tiledata_event[xy_to_index(125,y)] = 524
            data.tiledata_event[xy_to_index(126,y)] = 525
            data.tiledata_event[xy_to_index(127,y)] = 281
            data.tiledata_event[xy_to_index(128,y)] = 524

        # Remove save point and autosave point before Cocoa1
        for y in range(84,88):
            data.tiledata_event[xy_to_index(358,y)] = 0
            data.tiledata_event[xy_to_index(363,y)] = 0
            data.tiledata_event[xy_to_index(364,y)] = 0
        for y in range(85,88):
            data.tiledata_event[xy_to_index(361,y)] = 0
            data.tiledata_event[xy_to_index(365,y)] = 0

        # Add autosave point at ledge above Cocoa1
        data.tiledata_event[xy_to_index(378,80)] = 42
        data.tiledata_event[xy_to_index(378,81)] = 42
        data.tiledata_event[xy_to_index(380,80)] = 44
        data.tiledata_event[xy_to_index(380,81)] = 44
        data.tiledata_event[xy_to_index(376,80)] = 44
        data.tiledata_event[xy_to_index(376,81)] = 44
        data.tiledata_event[xy_to_index(376,82)] = 44

    if areaid == 1:
        # Remove trampoline at crisis boost location
        data.tiledata_event[xy_to_index(246,63)] = 0
        data.tiledata_event[xy_to_index(246,64)] = 0

    if areaid == 4:
        # Remove save point at slide location in lab
        for y in range(185,189):
            data.tiledata_event[xy_to_index(309,y)] = 0
        for y in range(186,189):
            data.tiledata_event[xy_to_index(310,y)] = 0

def apply_super_attack_mode(areaid, data):
    # area 0 only.
    if areaid != 0: return
    
    ATTACK_UP_COUNT = 20

    # EV_MOVEDOWN event to move erina down to start position
    data.tiledata_event[xy_to_index(111,43)] = 554

    # Place attack up get events
    for i in range(0,ATTACK_UP_COUNT):
        y = 42 - i
        data.tiledata_event[xy_to_index(111,y)] = 558
        data.tiledata_event[xy_to_index(112,y)] = 5223 - i
        data.tiledata_event[xy_to_index(113,y)] = 5001

    # Remove old start event
    data.tiledata_event[xy_to_index(113,98)] = 0
    # Place new start event
    data.tiledata_event[xy_to_index(111,42-ATTACK_UP_COUNT)] = 34

    # Add collision data
    data.tiledata_map[xy_to_index(110,44)] = 1
    data.tiledata_map[xy_to_index(111,44)] = 1
    data.tiledata_map[xy_to_index(112,44)] = 1
    for i in range(0,ATTACK_UP_COUNT+5):
        y = 43-i
        data.tiledata_map[xy_to_index(110,y)] = 1
        data.tiledata_map[xy_to_index(112,y)] = 1
    data.tiledata_map[xy_to_index(111,43-ATTACK_UP_COUNT-4)] = 1

    # Blanket with black graphical tiles
    for y in range(0,45):
        for x in range(100,120):
            data.tiledata_tiles1[xy_to_index(x,y)] = 33

    # Change room type and background
    for y in range(0,4):
        data.tiledata_roombg[to_tile_index(5,y)] = 56
        data.tiledata_roomtype[to_tile_index(5,y)] = 3



def pre_modify_map_data(mod, apply_fixes, shuffle_music, shuffle_backgrounds, no_laggy_backgrounds, no_difficult_backgrounds, super_attack_mode):
    # apply rando fixes
    if apply_fixes:
        for areaid, data in mod.stored_datas.items():
            apply_fixes_for_randomizer(areaid, data)
        print('Map fixes applied')

    # Note: because musicrandomizer requires room color info, the music
    # must be shuffled before the room colors!

    if shuffle_music:
        musicrandomizer.shuffle_music(mod.stored_datas)

    if shuffle_backgrounds:
        backgroundrandomizer.shuffle_backgrounds(mod.stored_datas, no_laggy_backgrounds, no_difficult_backgrounds)

    # super attack mode
    if super_attack_mode:
        for areaid, data in mod.stored_datas.items():
            apply_super_attack_mode(areaid, data)
        print('Super attack mode applied')