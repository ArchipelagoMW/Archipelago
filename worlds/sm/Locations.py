from variaRandomizer.graph.location import locationsDict

start_id = 82000
lookup_id_to_name = dict((key, value) for key, value in enumerate(locationsDict, start_id))
lookup_name_to_id = {location_name: location_id for location_id, location_name in lookup_id_to_name.items()}