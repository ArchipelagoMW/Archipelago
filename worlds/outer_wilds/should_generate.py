from .options import OuterWildsGameOptions


# logsanity only matters for locations, not items or connections
def should_generate_location(category: str | None, requires_logsanity: bool, options: OuterWildsGameOptions) -> bool:
    if requires_logsanity and not options.logsanity:
        return False
    return should_generate(category, options)


def should_generate(category: str | None, options: OuterWildsGameOptions) -> bool:
    if category is None:  # this item/location/connection gets generated no matter what the player options are
        return True
    elif '&' in category:
        return all(should_generate(c, options) for c in category.split('&'))
    elif '|' in category:
        return any(should_generate(c, options) for c in category.split('|'))
    elif category == 'base':  # is generated unless dlc_only is true
        return options.dlc_only.value == 0
    elif category == 'dlc':  # only generated if enable_eote_dlc is true
        return options.enable_eote_dlc.value == 1
    elif category == 'hn1':
        return options.enable_hn1_mod.value == 1
    elif category == 'to':
        return options.enable_outsider_mod.value == 1
    elif category == 'ac':
        return options.enable_ac_mod.value == 1
    elif category == 'hn2':
        return options.enable_hn2_mod.value == 1
    elif category == 'fq':
        return options.enable_fq_mod.value == 1
    raise ValueError(f'Invalid category: {category}')
