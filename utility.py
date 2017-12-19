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