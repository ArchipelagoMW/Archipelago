# flatten values into list
def flatten(values):
    return [y for x in values for y in flatten(x)] if isinstance(values, (list, tuple, bytes)) else [values]
