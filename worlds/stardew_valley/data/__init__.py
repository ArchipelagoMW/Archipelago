from dataclasses import dataclass
from typing import List

from .. import data


@dataclass(frozen=True)
class SeedData:
    name: str
    seasons: List[str]
    regions: List[str]


@dataclass(frozen=True)
class CropData:
    name: str
    farm_growth_seasons: List[str]
    seed: SeedData


def load_crop_csv():
    import csv
    from importlib.resources import path

    with path(data, "crops.csv") as resource:
        with open(resource) as file:
            reader = csv.DictReader(file)
            crops = []
            seeds = []

            for item in reader:
                seeds.append(SeedData(item["seed"],
                                      [season for season in item["seed_seasons"].split(",")]
                                      if item["seed_seasons"] else [],
                                      [region for region in item["seed_regions"].split(",")]
                                      if item["seed_regions"] else []))
                crops.append(CropData(item["crop"],
                                      [season for season in item["farm_growth_seasons"].split(",")]
                                      if item["farm_growth_seasons"] else [],
                                      seeds[-1]))
            return crops, seeds


# TODO Those two should probably be split to we can include rest of seeds
all_crops, all_purchasable_seeds = load_crop_csv()
