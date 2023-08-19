import csv
import typing


class ResourceRow(typing.NamedTuple):
    name: str


class RegionRow(typing.NamedTuple):
    name: str
    itemReq: str
    connections: typing.Collection[str]
    resources: typing.Collection[str]


class LocationRow(typing.NamedTuple):
    name: str
    category: str
    regions: typing.Collection[str]
    skills: typing.Collection[str]
    items: typing.Collection[str]
    qp: str


def load_logic_csvs():
    with open("LogicCSV/OSRS AP Tasks - Locations.csv", newline='') as locations_csv:
        locations_reader = csv.reader(locations_csv, delimiter=',',quotechar='"')
        location_rows = []
        for row in locations_reader:
            location_rows.append(LocationRow(row[0], row[1], row[2].split(", "), row[3].split(", "), row[4].split(", "), row[5]))
    with open("LogicCSV/OSRS AP Tasks - Regions.csv", newline='') as regions_csv:
        regions_reader = csv.reader(regions_csv, delimiter=',',quotechar='"')
        region_rows = []
        for row in regions_reader:
            region_rows.append(RegionRow(row[0], row[1], row[2].split(", "), row[3].split(", ")))
    with open("LogicCSV/OSRS AP Tasks - Resources.csv", newline='') as resources_csv:
        resources_reader = csv.reader(resources_csv, delimiter=',',quotechar='"')
        resoource_rows = []
        for row in resources_reader:
            resoource_rows.append(ResourceRow(row[0]))


if __name__ == "__main__":
    load_logic_csvs()