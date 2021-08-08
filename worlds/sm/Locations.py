from worlds.sm.variaRandomizer.graph.location import locationsDict

locations_start_id = 82000

def gen_boss_id():
    boss_id_value_start = 256
    while True:
        yield boss_id_value_start
        boss_id_value_start += 1

gen_run = gen_boss_id()

lookup_id_to_name = dict((locations_start_id + (value.Id if value.Id != None else next(gen_run)), key) for key, value in locationsDict.items())
lookup_name_to_id = {location_name: location_id for location_id, location_name in lookup_id_to_name.items()}