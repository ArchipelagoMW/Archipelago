
# called after the regions.json has been imported, but before ids, etc. have been assigned
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def before_region_table_processed(region_table: dict) -> dict:
    return region_table
