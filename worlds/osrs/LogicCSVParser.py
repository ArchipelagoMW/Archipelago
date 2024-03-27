import csv
import typing
import pkgutil

from BaseClasses import ItemClassification

location_rows = []
region_rows = []
resource_rows = []
item_rows = []


class ResourceRow(typing.NamedTuple):
    name: str


class RegionRow(typing.NamedTuple):
    name: str
    itemReq: str
    connections: typing.List[str]
    resources: typing.List[str]


class SkillRequirement(typing.NamedTuple):
    skill: str
    level: int


class LocationRow(typing.NamedTuple):
    name: str
    category: str
    regions: typing.List[str]
    skills: typing.List[SkillRequirement]
    items: typing.List[str]
    qp: int


class ItemRow(typing.NamedTuple):
    name: str
    count: int
    progression: ItemClassification


def load_location_csv() -> typing.List[LocationRow]:
    if len(location_rows) > 0:
        return location_rows

    locations_csv = pkgutil.get_data(__name__, "LogicCSV/OSRS AP Tasks - Locations.csv")
    locations_reader = csv.reader(locations_csv.decode('utf-8').splitlines(), delimiter=',', quotechar='"')
    for row in locations_reader:
        skill_strings = row[3].split(", ")
        skill_reqs = []
        if len(skill_strings) > 0:
            split_skills = [skill.split(" ") for skill in skill_strings if skill != ""]
            if len(split_skills) > 0:
                skill_reqs = [SkillRequirement(split[0], int(split[1])) for split in split_skills]

        region_strings = row[2].split(", ") if len(row[2]) > 0 else []
        item_strings = row[4].split(", ") if len(row[4]) > 0 else []
        location_rows.append(
            LocationRow(row[0], row[1], region_strings, skill_reqs, item_strings,
                        int(row[5]) if row[5] != "" else 0))
    return location_rows


def load_region_csv() -> typing.List[RegionRow]:
    if len(region_rows) > 0:
        return region_rows
    regions_csv = pkgutil.get_data(__name__, "LogicCSV/OSRS AP Tasks - Regions.csv")
    regions_reader = csv.reader(regions_csv.decode('utf-8').splitlines(), delimiter=',', quotechar='"')
    for row in regions_reader:
        region_rows.append(RegionRow(row[0], row[1], row[2].split(", "), row[3].split(", ")))
    return region_rows


def load_resource_csv() -> typing.List[ResourceRow]:
    if len(resource_rows) > 0:
        return resource_rows
    resources_csv = pkgutil.get_data(__name__, "LogicCSV/OSRS AP Tasks - Resources.csv")
    resources_reader = csv.reader(resources_csv.decode('utf-8').splitlines(), delimiter=',', quotechar='"')
    for row in resources_reader:
        resource_rows.append(ResourceRow(row[0]))
    return resource_rows


def load_item_csv() -> typing.List[ItemRow]:
    if len(item_rows) > 0:
        return item_rows
    items_csv = pkgutil.get_data(__name__, "LogicCSV/OSRS AP Tasks - Items.csv")
    items_reader = csv.reader(items_csv.decode('utf-8').splitlines(), delimiter=',', quotechar='"')
    for row in items_reader:
        progression = ItemClassification.filler
        if row[2] == "progression":
            progression = ItemClassification.progression
        elif row[2] == "useful":
            progression = ItemClassification.useful
        item_rows.append(ItemRow(row[0], int(row[1]), progression))
    return item_rows
