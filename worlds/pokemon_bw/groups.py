
def get_item_groups() -> dict[str, set[str]]:
    from .data.items import main_items, key_items, tm_hm, medicine, berries, badges, seasons

    return {
        "TMs": set(tm_hm.tm),
        "HMs": set(tm_hm.hm),
        "Main items": {*main_items.filler, *main_items.fossils, *main_items.min_once,
                       *main_items.mail, *main_items.unused},
        "Key items": {*key_items.progression, *key_items.vanilla, *key_items.useless, *key_items.special},
        "Medicine": {*medicine.table, *medicine.important},
        "Berries": {*berries.standard, *berries.niche},
        "Badges": set(badges.table),
        "Seasons": set(seasons.table),
    }


def get_location_groups() -> dict[str, set[str]]:
    from .data.locations import dexsanity
    from .data.locations.ingame_items import overworld_items, hidden_items, other, special

    return {
        "Dexsanity": set(dexsanity.location_table),
        "Overworld items": set(name for tab in (overworld_items.table, overworld_items.abyssal_ruins) for name in tab),
        "Abyssal Ruins items": set(overworld_items.abyssal_ruins),
        "Hidden items": set(hidden_items.table),
        "NPC items": {*other.table, *special.gym_badges, *special.gym_tms, *special.tm_hm_ncps},
        "Badge rewards": set(special.gym_badges),
        "Gym TM rewards": set(special.gym_tms),
        "TM/HM locations": {*special.gym_tms, *special.tm_hm_ncps},
    }
