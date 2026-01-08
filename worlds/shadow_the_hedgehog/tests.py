from . import Levels, Names


def TestLevelRegions():
    print("TLR")
    region_definitions = Levels.INDIVIDUAL_LEVEL_REGIONS

    last_region = None
    for region in region_definitions:
        if last_region is None:
            last_region = region
            continue

        if region.stageId != last_region.stageId:
            last_region = region
            continue

        if region.regionIndex != (last_region.regionIndex + 1):
            print("Error with", region)

        last_region = region

    region_indicies = Names.REGION_INDICIES


    pass

TestLevelRegions()