from worlds.sm.variaRandomizer.rando.Items import ItemManager

items_start_id = 83000

def gen_special_id():
    special_id_value_start = 32
    while True:
        yield special_id_value_start
        special_id_value_start += 1

gen_run = gen_special_id()

lookup_id_to_name = dict((items_start_id + (value.Id if value.Id != None else next(gen_run)), value.Name) for key, value in ItemManager.Items.items())
lookup_name_to_id = {item_name: item_id for item_id, item_name in lookup_id_to_name.items()}