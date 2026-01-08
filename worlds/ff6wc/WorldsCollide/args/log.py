from .. import args as args

def _log_tab(tab_name, left_groups, right_groups):
    lcolumn = []
    for lgroup in left_groups:
        lcolumn.append("")
        lcolumn.extend(args.group_modules[lgroup].log(args))

    rcolumn = []
    for rgroup in right_groups:
        rcolumn.append("")
        rcolumn.extend(args.group_modules[rgroup].log(args))

    import log
    log.section(tab_name, lcolumn, rcolumn)

def log():
    _log_tab("Game", ["settings"], [])
    args.group_modules["objectives"].log(args)
    _log_tab("Party", ["starting_party", "swdtechs", "blitzes", "lores", "rages", "dances", "steal", "sketch_control"], ["characters", "commands"])
    _log_tab("Battle", ["xpmpgp", "bosses", "boss_ai"], ["scaling", "encounters"])
    _log_tab("Magic", ["espers", "misc_magic"], ["natural_magic"])
    _log_tab("Items", ["starting_gold_items", "items"], ["shops", "chests"])
    args.group_modules["graphics"].log(args)
    _log_tab("Other", ["coliseum", "auction_house", "misc"], ["challenges", "bug_fixes"])
