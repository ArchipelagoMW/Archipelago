import csv
import typing

from BaseClasses import ItemClassification


class ResourceRow(typing.NamedTuple):
    name: str


class RegionRow(typing.NamedTuple):
    name: str
    itemReq: str
    connections: typing.List[str]
    resources: typing.List[str]


class LocationRow(typing.NamedTuple):
    name: str
    category: str
    regions: typing.List[str]
    skills: typing.List[str]
    items: typing.List[str]
    qp: int


class ItemRow(typing.NamedTuple):
    name: str
    count: int
    progression: ItemClassification


def load_location_csv() -> typing.List[LocationRow]:
    location_rows = []
    with open("LogicCSV/OSRS AP Tasks - Locations.csv", newline='') as locations_csv:
        locations_reader = csv.reader(locations_csv, delimiter=',', quotechar='"')
        for row in locations_reader:
            location_rows.append(
                LocationRow(row[0], row[1], row[2].split(", "), row[3].split(", "), row[4].split(", "), int(row[5])))
        return location_rows


def load_region_csv() -> typing.List[RegionRow]:
    region_rows = []
    with open("LogicCSV/OSRS AP Tasks - Regions.csv", newline='') as regions_csv:
        regions_reader = csv.reader(regions_csv, delimiter=',', quotechar='"')
        for row in regions_reader:
            region_rows.append(RegionRow(row[0], row[1], row[2].split(", "), row[3].split(", ")))
        return region_rows


def load_resource_csv() -> typing.List[ResourceRow]:
    resource_rows = []
    with open("LogicCSV/OSRS AP Tasks - Resources.csv", newline='') as resources_csv:
        resources_reader = csv.reader(resources_csv, delimiter=',', quotechar='"')
        for row in resources_reader:
            resource_rows.append(ResourceRow(row[0]))
        return resource_rows


def load_item_csv() -> typing.List[ItemRow]:
    item_rows = []
    with open("LogicCSV/OSRS AP Tasks - Items.csv", newline='') as items_csv:
        items_reader = csv.reader(items_csv, delimiter=',', quotechar='"')
        for row in items_reader:
            progression = ItemClassification.filler
            if row[2] == "progression":
                progression = ItemClassification.progression
            elif row[2] == "useful":
                progression = ItemClassification.useful
            item_rows.append(ItemRow(row[0], int(row[1]), progression))
        return item_rows
