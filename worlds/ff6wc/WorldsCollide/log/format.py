from .. import args as args

SECTION_WIDTH = 120
COLUMN_WIDTH = 60

def separator(label):
    import logging
    logging.info("")
    logging.info(get_separator(label))

def columns(lcolumn, rcolumn):
    import logging, itertools
    for column in itertools.zip_longest(lcolumn, rcolumn, fillvalue = ""):
        logging.info(f"{column[0]:<{COLUMN_WIDTH}}{column[1]:<{COLUMN_WIDTH}}".rstrip())

def section(label, lcolumn, rcolumn):
    separator(label)
    columns(lcolumn, rcolumn)

def section_entries(label, lentries, rentries):
    # log section with multi-line entries in each column as a grid

    # resize each row of entries to the minimum number of lines needed
    full_rows_count = min(len(lentries), len(rentries)) # number of entry rows with 2 entries
    for row_index in range(full_rows_count):
        if len(lentries[row_index]) > len(rentries[row_index]):
            rentries[row_index].extend([""] * (len(lentries[row_index]) - len(rentries[row_index])))
        else:
            lentries[row_index].extend([""] * (len(rentries[row_index]) - len(lentries[row_index])))
        lentries[row_index].append("")
        rentries[row_index].append("")

    if len(lentries) == len(rentries):
        # full_rows_count was the same as the number of entry rows
        # so remove the extra empty line which was added to the end of both
        lentries[-1] = lentries[-1][:-1]
        rentries[-1] = rentries[-1][:-1]

    from ..ff6wcutils.flatten import flatten
    lcolumn = flatten(lentries)
    rcolumn = flatten(rentries)

    section(label, lcolumn, rcolumn)

def get_separator(label):
    half_dash_count = SECTION_WIDTH // 2 - 1 # one space on each side of label
    side_dash_count = (half_dash_count - len(label) // 2)

    separator = ""
    separator += '-' * (side_dash_count - (len(label) % 2))
    separator += ' ' + label + ' '
    separator += '-' * side_dash_count

    return separator

def format_option(option, value, unique_name = ''):
    from ..constants.standard_flags import standard_flags
    standard_flag = standard_flags.get(unique_name)
    if(standard_flag != str(value)):
        pass # nothing for now -- uncomment once we have new standard
    #    option = f"!{option}" # prepend a ! to indicate it's non standard
        
    return f"    {option:<26} {value}"
