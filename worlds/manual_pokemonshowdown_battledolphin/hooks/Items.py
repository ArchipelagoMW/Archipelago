
# called after the items.json has been imported, but before ids, etc. have been assigned
# if you need access to the items after processing to add ids, etc., you should use the hooks in World.py
def before_item_table_processed(item_table: list) -> list:
    return item_table

# NOTE: Progressive items are not currently supported in Manual. Once they are, 
#       this hook will provide the ability to meaningfully change those.
def before_progressive_item_table_processed(progressive_item_table: list) -> list:
    return progressive_item_table
