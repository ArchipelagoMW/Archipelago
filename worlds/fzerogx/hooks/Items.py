
# called after the items.json has been imported, but before ids, etc. have been assigned
# if you need access to the items after processing to add ids, etc., you should use the hooks in World.py
def before_item_table_processed(item_table: list) -> list:
    return item_table
