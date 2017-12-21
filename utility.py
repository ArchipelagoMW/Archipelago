import hashlib
import random

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

def is_xx_up(item_name):
    return bool(re.match('^[A-Z]*_UP', item_name))

def is_egg(item_name):
    return bool(item_name.startswith('EGG_'))



# Expression Parsing

def parse_expression_lambda(line, variable_names_set, default_expressions):
    expression = parse_expression(variable_names_set, default_expressions)
    return lambda v : expression.evaluate(v)

# & - and
# | - or
# !/~ - not
# ( ) - parentheses
# throws errors if parsing fails
def parse_expression(line, variable_names_set, default_expressions):
    try:
        # the str(line) cast is used because sometimes <line> is a u'unicode string' on unix machines.
        return parse_expression_logic(str(line), variable_names_set, default_expressions)
    except Exception as e:
        eprint('Error parsing expression:')
        eprint(line)
        raise e

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
            if next in default_expressions:
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




# Error Handling

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def fail(message):
    eprint(message)
    sys.exit(1)

def log(*args, **kwargs):
    print(*args, **kwargs)



# File Parsing

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
import musicrandomizer
import backgroundrandomizer


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