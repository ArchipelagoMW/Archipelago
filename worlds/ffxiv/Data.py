import logging

from .DataValidation import DataValidation, ValidationError
from .Helpers import load_data_file as helpers_load_data_file

from .hooks.Data import \
    after_load_game_file, \
    after_load_item_file, after_load_location_file, \
    after_load_region_file, after_load_category_file, \
    after_load_option_file, after_load_meta_file

# blatantly copied from the minecraft ap world because why not
def load_data_file(*args) -> dict:
    logging.warning("Deprecated usage of importing load_data_file from Data.py uses the one from Helper.py instead")
    return helpers_load_data_file(*args)

def convert_to_list(data, property_name: str) -> list:
    if isinstance(data, dict):
        data = data.get(property_name, [])
    return data

class ManualFile:
    filename: str
    data_type: dict|list

    def __init__(self, filename, data_type):
        self.filename = filename
        self.data_type = data_type

    def load(self):
        contents = helpers_load_data_file(self.filename)

        if not contents and type(contents) != self.data_type:
            return self.data_type()

        return contents


game_table = ManualFile('game.json', dict).load() #dict
item_table = convert_to_list(ManualFile('items.json', list).load(), 'data') #list
location_table = convert_to_list(ManualFile('locations.json', list).load(), 'data') #list
region_table = ManualFile('regions.json', dict).load() #dict
category_table = ManualFile('categories.json', dict).load() #dict
option_table = ManualFile('options.json', dict).load() #dict
meta_table = ManualFile('meta.json', dict).load() #dict

# Removal of schemas in root of tables
region_table.pop('$schema', '')
category_table.pop('$schema', '')

# hooks
game_table = after_load_game_file(game_table)
item_table = after_load_item_file(item_table)
location_table = after_load_location_file(location_table)
region_table = after_load_region_file(region_table)
category_table = after_load_category_file(category_table)
option_table = after_load_option_file(option_table)
meta_table = after_load_meta_file(meta_table)

# seed all of the tables for validation
DataValidation.game_table = game_table
DataValidation.item_table = item_table
DataValidation.location_table = location_table
DataValidation.region_table = region_table

validation_errors = []

# check that json files are not just invalid json
try: DataValidation.checkForGameBeingInvalidJSON()
except ValidationError as e: validation_errors.append(e)

try: DataValidation.checkForItemsBeingInvalidJSON()
except ValidationError as e: validation_errors.append(e)

try: DataValidation.checkForLocationsBeingInvalidJSON()
except ValidationError as e: validation_errors.append(e)


############
# If there are any validation errors, display all of them at once
############

if len(validation_errors) > 0:
    logging.error("\nValidationError(s): \n\n%s\n\n" % ("\n".join([' - ' + str(validation_error) for validation_error in validation_errors])))
    print("\n\nYou can close this window.\n")
    keeping_terminal_open = input("If you are running from a terminal, press Ctrl-C followed by ENTER to break execution.")
