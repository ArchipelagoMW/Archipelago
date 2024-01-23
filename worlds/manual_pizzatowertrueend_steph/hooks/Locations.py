
# called after the locations.json has been imported, but before ids, etc. have been assigned
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def before_location_table_processed(location_table: list) -> list:
    return location_table
