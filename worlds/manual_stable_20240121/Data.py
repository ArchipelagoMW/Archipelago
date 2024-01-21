import json
import os
import pkgutil

from .DataValidation import DataValidation, ValidationError

from .hooks.Data import \
    after_load_item_file, after_load_progressive_item_file, \
    after_load_location_file, after_load_region_file, after_load_category_file

# blatantly copied from the minecraft ap world because why not
def load_data_file(*args) -> dict:
    fname = os.path.join("data", *args)

    try:
        filedata = json.loads(pkgutil.get_data(__name__, fname).decode())
    except:
        filedata = []

    return filedata

game_table = load_data_file('game.json')
item_table = load_data_file('items.json')
#progressive_item_table = load_data_file('progressive_items.json')
progressive_item_table = {}
location_table = load_data_file('locations.json')
region_table = load_data_file('regions.json')
category_table = load_data_file('categories.json') or {}

# hooks
item_table = after_load_item_file(item_table)
progressive_item_table = after_load_progressive_item_file(progressive_item_table)
location_table = after_load_location_file(location_table)
region_table = after_load_region_file(region_table)
category_table = after_load_category_file(category_table)

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

# check that requires have correct item names in locations and regions
try: DataValidation.checkItemNamesInLocationRequires()
except ValidationError as e: validation_errors.append(e)

try: DataValidation.checkItemNamesInRegionRequires()
except ValidationError as e: validation_errors.append(e)

# check that region names are correct in locations
try: DataValidation.checkRegionNamesInLocations()
except ValidationError as e: validation_errors.append(e)

# check that items that are required by locations and regions are also marked required
try: DataValidation.checkItemsThatShouldBeRequired()
except ValidationError as e: validation_errors.append(e)

# check that regions that are connected to are correct
try: DataValidation.checkRegionsConnectingToOtherRegions()
except ValidationError as e: validation_errors.append(e)

# check that the apworld creator didn't specify multiple victory conditions
try: DataValidation.checkForMultipleVictoryLocations()
except ValidationError as e: validation_errors.append(e)

# check for duplicate names in items, locations, and regions
try: DataValidation.checkForDuplicateItemNames()
except ValidationError as e: validation_errors.append(e)

try: DataValidation.checkForDuplicateLocationNames()
except ValidationError as e: validation_errors.append(e)

try: DataValidation.checkForDuplicateRegionNames()
except ValidationError as e: validation_errors.append(e)

# check that starting items and starting item categories actually exist in the items json
try: DataValidation.checkStartingItemsForValidItemsAndCategories()
except ValidationError as e: validation_errors.append(e)

# check that the game's default filler item name doesn't match an item name that they defined in their items
try: DataValidation.checkForGameFillerMatchingAnItemName()
except ValidationError as e: validation_errors.append(e)

# check for regions that are set as non-starting regions and have no connectors to them (so are unreachable)
try: DataValidation.checkForNonStartingRegionsThatAreUnreachable()
except ValidationError as e: validation_errors.append(e)



############
# If there are any validation errors, display all of them at once
############

if len(validation_errors) > 0:
    print("\nValidationError(s): \n\n%s\n\n" % ("\n".join([' - ' + str(validation_error) for validation_error in validation_errors])))
    print("\n\nYou can close this window.\n")
    keeping_terminal_open = input("If you are running from a terminal, press Ctrl-C followed by ENTER to break execution.")
