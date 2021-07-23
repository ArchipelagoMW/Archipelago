from rando.Items import ItemManager

start_id = 83000
lookup_id_to_name = dict((key, value.Name) for key, value in enumerate(ItemManager.Items.values(), start_id))
lookup_name_to_id = {location_name: location_id for location_id, location_name in lookup_id_to_name.items()}