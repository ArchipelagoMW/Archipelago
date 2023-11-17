from dataclasses import dataclass
from typing import Tuple

from .. import data


@dataclass(frozen=True)
class SeedItem:
    name: str
    seasons: Tuple[str]
    regions: Tuple[str]
    requires_island: bool


@dataclass(frozen=True)
class CropItem:
    name: str
    farm_growth_seasons: Tuple[str]
    seed: SeedItem


def load_crop_csv():
    import csv
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # noqa

    with files(data).joinpath("crops.csv").open() as file:
        reader = csv.DictReader(file)
        crops = []
        seeds = []

        for item in reader:
            seeds.append(SeedItem(item["seed"],
                                  tuple(season for season in item["seed_seasons"].split(","))
                                  if item["seed_seasons"] else tuple(),
                                  tuple(region for region in item["seed_regions"].split(","))
                                  if item["seed_regions"] else tuple(),
                                  item["requires_island"] == "True"))
            crops.append(CropItem(item["crop"],
                                  tuple(season for season in item["farm_growth_seasons"].split(","))
                                  if item["farm_growth_seasons"] else tuple(),
                                  seeds[-1]))
        return crops, seeds


# TODO Those two should probably be split to we can include rest of seeds
all_crops, all_purchasable_seeds = load_crop_csv()
crops_by_name = {crop.name: crop for crop in all_crops}
