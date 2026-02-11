import logging
import re
import json
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, ItemClassification


class ValidationError(Exception):
    pass

class DataValidation():
    game_table = {}
    item_table = []
    location_table = []
    region_table = {}


    @staticmethod
    def checkItemNamesInLocationRequires():
        for location in DataValidation.location_table:
            if "requires" not in location:
                continue

            if isinstance(location["requires"], str):
                # parse user written statement into list of each item
                for item in re.findall(r'\|[^|]+\|', location["requires"]):
                    if item.lower() == "or" or item.lower() == "and" or item == ")" or item == "(":
                        continue
                    else:
                        # it's just a category, so ignore it
                        if '@' in item:
                            continue

                        item = item.replace("|", "")

                        item_parts = item.split(":")
                        item_name = item

                        if len(item_parts) > 1:
                            item_name = item_parts[0]

                        item_exists = len([item["name"] for item in DataValidation.item_table if item["name"] == item_name]) > 0

                        if not item_exists:
                            raise ValidationError("Item %s is required by location %s but is misspelled or does not exist." % (item_name, location["name"]))

            else:  # item access is in dict form
                for item in location["requires"]:
                    # if the require entry is an object with "or" or a list of items, treat it as a standalone require of its own
                    if (isinstance(item, dict) and "or" in item and isinstance(item["or"], list)) or (isinstance(item, list)):
                        or_items = item

                        if isinstance(item, dict):
                            or_items = item["or"]

                        for or_item in or_items:
                            or_item_parts = or_item.split(":")
                            or_item_name = or_item

                            if len(or_item_parts) > 1:
                                or_item_name = or_item_parts[0]

                            item_exists = len([item["name"] for item in DataValidation.item_table if item["name"] == or_item_name]) > 0

                            if not item_exists:
                                raise ValidationError("Item %s is required by location %s but is misspelled or does not exist." % (or_item_name, location["name"]))
                    else:
                        item_parts = item.split(":")
                        item_name = item

                        if len(item_parts) > 1:
                            item_name = item_parts[0]

                        item_exists = len([item["name"] for item in DataValidation.item_table if item["name"] == item_name]) > 0

                        if not item_exists:
                            raise ValidationError("Item %s is required by location %s but is misspelled or does not exist." % (item_name, location["name"]))

    @staticmethod
    def checkItemNamesInRegionRequires():
        for region_name in DataValidation.region_table:
            region = DataValidation.region_table[region_name]

            if "requires" not in region:
                continue

            if isinstance(region["requires"], str):
                # parse user written statement into list of each item
                for item in re.findall(r'\|[^|]+\|', region["requires"]):
                    if item.lower() == "or" or item.lower() == "and" or item == ")" or item == "(":
                        continue
                    else:
                        # it's just a category, so ignore it
                        if '@' in item:
                            continue

                        item = item.replace("|", "")

                        item_parts = item.split(":")
                        item_name = item

                        if len(item_parts) > 1:
                            item_name = item_parts[0]

                        item_exists = len([item["name"] for item in DataValidation.item_table if item["name"] == item_name]) > 0

                        if not item_exists:
                            raise ValidationError("Item %s is required by region %s but is misspelled or does not exist." % (item_name, region_name))

            else:  # item access is in dict form
                for item in region["requires"]:
                    # if the require entry is an object with "or" or a list of items, treat it as a standalone require of its own
                    if (isinstance(item, dict) and "or" in item and isinstance(item["or"], list)) or (isinstance(item, list)):
                        or_items = item

                        if isinstance(item, dict):
                            or_items = item["or"]

                        for or_item in or_items:
                            or_item_parts = or_item.split(":")
                            or_item_name = or_item

                            if len(or_item_parts) > 1:
                                or_item_name = or_item_parts[0]

                            item_exists = len([item["name"] for item in DataValidation.item_table if item["name"] == or_item_name]) > 0

                            if not item_exists:
                                raise ValidationError("Item %s is required by region %s but is misspelled or does not exist." % (or_item_name, region_name))
                    else:
                        item_parts = item.split(":")
                        item_name = item

                        if len(item_parts) > 1:
                            item_name = item_parts[0]

                        item_exists = len([item["name"] for item in DataValidation.item_table if item["name"] == item_name]) > 0

                        if not item_exists:
                            raise ValidationError("Item %s is required by region %s but is misspelled or does not exist." % (item_name, region_name))

    @staticmethod
    def checkRegionNamesInLocations():
        for location in DataValidation.location_table:
            if "region" not in location or location["region"] in ["Menu", "Manual"]:
                continue

            region_exists = len([name for name in DataValidation.region_table if name == location["region"]]) > 0

            if not region_exists:
                raise ValidationError("Region %s is set for location %s, but the region is misspelled or does not exist." % (location["region"], location["name"]))

    @staticmethod
    def checkItemsThatShouldBeRequired():
        for item in DataValidation.item_table:
            # if the item is already progression, no need to check
            if "progression" in item and item["progression"]:
                continue

            # progression_skip_balancing is also progression, so no check needed
            if "progression_skip_balancing" in item and item["progression_skip_balancing"]:
                continue

            # check location requires for the presence of item name
            for location in DataValidation.location_table:
                if "requires" not in location:
                    continue

                # convert to json so we don't have to guess the data type
                location_requires = json.dumps(location["requires"])

                # if boolean, else legacy
                if isinstance(location_requires, str):
                    if '|{}|'.format(item["name"]) in location_requires:
                        raise ValidationError("Item %s is required by location %s, but the item is not marked as progression." % (item["name"], location["name"]))
                else:
                    if item["name"] in location_requires:
                        raise ValidationError("Item %s is required by location %s, but the item is not marked as progression." % (item["name"], location["name"]))

            # check region requires for the presence of item name
            for region_name in DataValidation.region_table:
                region = DataValidation.region_table[region_name]

                if "requires" not in region:
                    continue

                # convert to json so we don't have to guess the data type
                region_requires = json.dumps(region["requires"])

                # if boolean, else legacy
                if isinstance(region_requires, str):
                    if '|{}|'.format(item["name"]) in region_requires:
                        raise ValidationError("Item %s is required by region %s, but the item is not marked as progression." % (item["name"], region_name))
                else:
                    if item["name"] in region_requires:
                        raise ValidationError("Item %s is required by region %s, but the item is not marked as progression." % (item["name"], region_name))

    @staticmethod
    def _checkLocationRequiresForItemValueWithRegex(values_requested: dict[str, int], requires) -> dict[str, int]:
        if isinstance(requires, str) and 'ItemValue' in requires:
            for result in re.findall(r'\{ItemValue\(([^:]*)\:([^)]+)\)\}', requires):
                value = result[0].lower().strip()
                count = int(result[1])
                if not values_requested.get(value):
                    values_requested[value] = count
                else:
                    values_requested[value] = max(values_requested[value], count)
        return values_requested

    @staticmethod
    def checkIfEnoughItemsForValue():
        values_available = {}
        values_requested = {}

        # First find the biggest values required by locations
        for location in DataValidation.location_table:
            if "requires" not in location:
                continue

            # convert to json so we don't have to guess the data type
            location_requires = json.dumps(location["requires"])

            DataValidation._checkLocationRequiresForItemValueWithRegex(values_requested, location_requires)
        # Second, check region requires for the presence of item name
        for region_name in DataValidation.region_table:
            region = DataValidation.region_table[region_name]

            if "requires" not in region:
                continue

            # convert to json so we don't have to guess the data type
            region_requires = json.dumps(region["requires"])

            DataValidation._checkLocationRequiresForItemValueWithRegex(values_requested, region_requires)
        # then if something is requested, we loop items
        if values_requested:

            # get all the available values with total count
            for item in DataValidation.item_table:
                # if the item is already progression, no need to check
                if not item.get("progression") and not item.get("progression_skip_balancing"):
                    continue

                item_count = item.get('count', None)
                if item_count is None: #check with none because 0 == false
                    item_count = '1'

                for key, count in item.get("value", {}).items():
                    if not values_available.get(key.lower().strip()):
                        values_available[key] = 0
                    values_available[key] += int(count) * int(item_count)

            # compare whats available vs requested
            errors = []
            for value, count in values_requested.items():
                if values_available.get(value, 0) < count:
                    errors.append(f"   '{value}': {values_available.get(value, 0)} out of the {count} {value} worth of progression items required can be found.")
            if errors:
                raise ValidationError("There are not enough progression items for the following values: \n" + "\n".join(errors))

    @staticmethod
    def preFillCheckIfEnoughItemsForValue(world: World, multiworld: MultiWorld):
        from .Helpers import get_items_with_value, get_items_for_player
        player = world.player
        values_requested = {}

        for region in multiworld.regions:
            if region.player != player:
                continue

            manualregion = DataValidation.region_table.get(region.name, {})
            if "requires" in manualregion and manualregion["requires"]:
                region_requires = json.dumps(manualregion["requires"])

                DataValidation._checkLocationRequiresForItemValueWithRegex(values_requested, region_requires)

            for location in region.locations:
                manualLocation = world.location_name_to_location.get(location.name, {})
                if "requires" in manualLocation and manualLocation["requires"]:
                    DataValidation._checkLocationRequiresForItemValueWithRegex(values_requested, manualLocation["requires"])

        # compare whats available vs requested but only if there's anything requested
        if values_requested:
            errors = []
            existing_items = [item for item in get_items_for_player(multiworld, player) if item.code is not None and
                        item.classification == ItemClassification.progression or item.classification == ItemClassification.progression_skip_balancing]

            for value, val_count in values_requested.items():
                items_value = get_items_with_value(world, multiworld, value, player, True)
                found_count = 0
                if items_value:
                    for item in existing_items:
                        if item.name in items_value:
                            found_count += items_value[item.name]

                if found_count < val_count:
                    errors.append(f"   '{value}': {found_count} out of the {val_count} {value} worth of progression items required can be found.")
            if errors:
                raise ValidationError("There are not enough progression items for the following value(s): \n" + "\n".join(errors))

    @staticmethod
    def checkRegionsConnectingToOtherRegions():
        for region_name in DataValidation.region_table:
            region = DataValidation.region_table[region_name]

            if "connects_to" not in region:
                continue

            for connecting_region in region["connects_to"]:
                region_exists = len([name for name in DataValidation.region_table if name == connecting_region]) > 0

                if not region_exists:
                    raise ValidationError("Region %s connects to a region %s, which is misspelled or does not exist." % (region_name, connecting_region))

    @staticmethod
    def checkForDuplicateItemNames():
        for item in DataValidation.item_table:
            name_count = len([i for i in DataValidation.item_table if i["name"] == item["name"]])

            if name_count > 1:
                raise ValidationError("Item %s is defined more than once." % (item["name"]))

    @staticmethod
    def checkForDuplicateLocationNames():
        for location in DataValidation.location_table:
            name_count = len([l for l in DataValidation.location_table if l["name"] == location["name"]])

            if name_count > 1:
                raise ValidationError("Location %s is defined more than once." % (location["name"]))

    @staticmethod
    def checkForDuplicateRegionNames():
        # this currently does nothing because the region name is a dict key, which will never be non-unique / limited to 1
        for region_name in DataValidation.region_table:
            name_count = len([r for r in DataValidation.region_table if r == region_name])

            if name_count > 1:
                raise ValidationError("Region %s is defined more than once." % (region_name))

    @staticmethod
    def checkStartingItemsForValidItemsAndCategories():
        if "starting_items" not in DataValidation.game_table:
            return

        starting_items = DataValidation.game_table["starting_items"]

        for starting_block in starting_items:
            if "items" in starting_block and "item_categories" in starting_block:
                raise ValidationError("One of your starting item definitions has both 'items' and 'item_categories' defined, but only one will be applied.")

            if "items" in starting_block:
                for item_name in starting_block["items"]:
                    if not item_name in [item["name"] for item in DataValidation.item_table]:
                        raise ValidationError("Item %s is set as a starting item, but is misspelled or is not defined." % (item_name))

            if "item_categories" in starting_block:
                for category_name in starting_block["item_categories"]:
                    if len([item for item in DataValidation.item_table if "category" in item and category_name in item["category"]]) == 0:
                        raise ValidationError("Item category %s is set as a starting item category, but is misspelled or is not defined on any items." % (category_name))

    @staticmethod
    def checkStartingItemsForBadSyntax():
        if not (starting_items := DataValidation.game_table.get("starting_items", False)):
            return

        for starting_block in starting_items:
            if type(starting_block) is not dict or len(starting_block.keys()) == 0:
                raise ValidationError("One of your starting item definitions is not a valid dictionary.\n   Each definition must be inside {}, as demonstrated in the Manual documentation.")

            valid_keys = ["items", "item_categories", "random", "if_previous_item", "_comment"] # _comment is provided by schema
            invalid_keys = [f'"{key}"' for key in starting_block.keys() if key not in valid_keys]

            if len(invalid_keys) > 0:
                raise ValidationError("One of your starting item definitions is invalid and may have unexpected results.\n   The invalid starting item definition specifies the following incorrect keys: {}".format(", ".join(invalid_keys)))

    @staticmethod
    def checkPlacedItemsAndCategoriesForBadSyntax():
        for location in DataValidation.location_table:
            place_item = location.get("place_item", False)
            place_item_category = location.get("place_item_category", False)

            if not place_item and not place_item_category:
                continue

            if place_item and type(place_item) is not list:
                raise ValidationError("One of your location has an incorrectly formatted place_item.\n   The items, even just one, must be inside [].")

            if place_item_category and type(place_item_category) is not list:
                raise ValidationError("One of your location has an incorrectly formatted place_item_category.\n   The categories, even just one, must be inside [].")

    @staticmethod
    def checkPlacedItemsForValidItems():
        for location in DataValidation.location_table:
            if not (place_item := location.get("place_item", False)):
                continue

            # don't bother checking for valid items if the syntax is wrong
            if type(place_item) is not list:
                continue

            for item_name in place_item:
                if not item_name in [item["name"] for item in DataValidation.item_table]:
                    raise ValidationError("Item %s is placed (using place_item) on a location, but is misspelled or is not defined." % (item_name))

    @staticmethod
    def checkPlacedItemCategoriesForValidItemCategories():
        for location in DataValidation.location_table:
            if not (place_item_category := location.get("place_item_category", False)):
                continue

            # don't bother checking for valid item categories if the syntax is wrong
            if type(place_item_category) is not list:
                continue

            for category_name in place_item_category:
                if len([item for item in DataValidation.item_table if "category" in item and category_name in item["category"]]) == 0:
                    raise ValidationError("Item category %s is placed (using place_item_category) on a location, but is misspelled or is not defined." % (category_name))

    @staticmethod
    def checkForGameBeingInvalidJSON():
        if len(DataValidation.game_table) == 0:
            raise ValidationError("No settings were found in your game.json. This likely indicates that your JSON is incorrectly formatted. Use https://jsonlint.com/ to validate your JSON files.")

    @staticmethod
    def checkForItemsBeingInvalidJSON():
        if len(DataValidation.item_table) == 0:
            raise ValidationError("No items were found in your items.json. This likely indicates that your JSON is incorrectly formatted. Use https://jsonlint.com/ to validate your JSON files.")

    @staticmethod
    def checkForLocationsBeingInvalidJSON():
        if len(DataValidation.location_table) == 0:
            raise ValidationError("No locations were found in your locations.json. This likely indicates that your JSON is incorrectly formatted. Use https://jsonlint.com/ to validate your JSON files.")

    @staticmethod
    def checkForNonStartingRegionsThatAreUnreachable():
        using_starting_regions = len([region for region in DataValidation.region_table if "starting" in DataValidation.region_table[region] and not DataValidation.region_table[region]["starting"]]) > 0

        if not using_starting_regions:
            return

        nonstarting_regions = [region for region in DataValidation.region_table if "starting" in DataValidation.region_table[region] and not DataValidation.region_table[region]["starting"]]

        for nonstarter in nonstarting_regions:
            regions_that_connect_to = [region for region in DataValidation.region_table if "connects_to" in DataValidation.region_table[region] and nonstarter in DataValidation.region_table[region]["connects_to"]]

            if len(regions_that_connect_to) == 0:
                raise ValidationError("The region '%s' is set as a non-starting region, but has no regions that connect to it. It will be inaccessible." % nonstarter)


def runPreFillDataValidation(world: World, multiworld: MultiWorld):
    validation_errors = []

    # check if there is enough items with values
    try: DataValidation.preFillCheckIfEnoughItemsForValue(world, multiworld)
    except ValidationError as e: validation_errors.append(e)

    if validation_errors:
        newline = "\n"
        raise Exception(f"\nValidationError(s) for pre_fill of player {world.player}: \n\n{newline.join([' - ' + str(validation_error) for validation_error in validation_errors])}\n\n")
# Called during stage_assert_generate
def runGenerationDataValidation() -> None:
    validation_errors = []

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

    # check if there's enough Items with values to get to every location requesting it
    try: DataValidation.checkIfEnoughItemsForValue()
    except ValidationError as e: validation_errors.append(e)

    # check that regions that are connected to are correct
    try: DataValidation.checkRegionsConnectingToOtherRegions()
    except ValidationError as e: validation_errors.append(e)

    # check for duplicate names in items, locations, and regions
    try: DataValidation.checkForDuplicateItemNames()
    except ValidationError as e: validation_errors.append(e)

    try: DataValidation.checkForDuplicateLocationNames()
    except ValidationError as e: validation_errors.append(e)

    try: DataValidation.checkForDuplicateRegionNames()
    except ValidationError as e: validation_errors.append(e)

    # check that starting items are actually valid starting item definitions
    try: DataValidation.checkStartingItemsForBadSyntax()
    except ValidationError as e: validation_errors.append(e)

    # check that starting items and starting item categories actually exist in the items json
    try: DataValidation.checkStartingItemsForValidItemsAndCategories()
    except ValidationError as e: validation_errors.append(e)

    # check that placed items are actually valid place item definitions
    try: DataValidation.checkPlacedItemsAndCategoriesForBadSyntax()
    except ValidationError as e: validation_errors.append(e)

    # check placed item and item categories for valid options for each
    try: DataValidation.checkPlacedItemsForValidItems()
    except ValidationError as e: validation_errors.append(e)

    try: DataValidation.checkPlacedItemCategoriesForValidItemCategories()
    except ValidationError as e: validation_errors.append(e)

    # check for regions that are set as non-starting regions and have no connectors to them (so are unreachable)
    try: DataValidation.checkForNonStartingRegionsThatAreUnreachable()
    except ValidationError as e: validation_errors.append(e)
    if len(validation_errors) > 0:
        raise Exception("\nValidationError(s): \n\n%s\n\n" % ("\n".join([' - ' + str(validation_error) for validation_error in validation_errors])))
