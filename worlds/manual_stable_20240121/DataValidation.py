import logging
import re
import json

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
            if "region" not in location:
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
    def checkForMultipleVictoryLocations():
        victory_count = len([location["name"] for location in DataValidation.location_table if "victory" in location and location["victory"]])

        if victory_count > 1:
            raise ValidationError("There are %s victory locations defined, but there should only be 1." % (str(victory_count)))
        
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
    def checkForGameFillerMatchingAnItemName():
        filler_item = DataValidation.game_table["filler_item_name"] if "filler_item_name" in DataValidation.game_table else "Filler"
        items_matching = [item for item in DataValidation.item_table if item["name"] == filler_item]

        if len(items_matching) > 0:
            raise ValidationError("Your game's filler item name ('%s') matches an item you defined in your items.json. Item names must be unique, including the default filler item." % (filler_item))
        
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

