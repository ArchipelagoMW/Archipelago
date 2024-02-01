from .data import data, BASE_OFFSET


def get_random_pokemon(random, types=None):
    pokemon_pool = []
    if types is None or types[0] is None:
        pokemon_pool = [pkmn_name for pkmn_name, _data in data.pokemon.items() if pkmn_name != "UNOWN"]
    else:
        pokemon_pool = [pkmn_name for pkmn_name, pkmn_data in data.pokemon.items()
                        if pkmn_name != "UNOWN" and pkmn_data.types == types]
    return random.choice(pokemon_pool)


def get_random_held_item(random):
    helditems = [item.item_const for item_id, item in data.items.items()
                 if "Unique" not in item.tags and "INVALID" not in item.tags]
    return random.choice(helditems)


def get_random_filler_item(random):
    helditems = [item_id for item_id, item in data.items.items()
                 if "Unique" not in item.tags and "INVALID" not in item.tags]
    return random.choice(helditems) + BASE_OFFSET


def get_random_pokemon_id(random):
    pokemon_pool = [i for i in range(1, 251) if i is not 0xC9]
    return random.choice(pokemon_pool)
