import json
import os
import pkgutil
from datetime import datetime


def load_data_file(*args) -> dict:
    fname = "/".join(["data", *args])
    return json.loads(pkgutil.get_data(__name__, fname).decode())


def relative_years_from_today(dt2: datetime) -> int:
    today = datetime.now()
    years = today.year - dt2.year
    if today.month < dt2.month or (today.month == dt2.month and today.day < dt2.day):
        years -= 1
    return years


location_id_offset: int = 27000
location_info = load_data_file("locations.json")
location_name_to_id = {name: location_id_offset + index for index, name in enumerate(location_info["all_locations"])}
exclusion_info = load_data_file("excluded_locations.json")
region_info = load_data_file("regions.json")
years_since_sep_30_1980 = relative_years_from_today(datetime.fromisoformat("1980-09-30"))
