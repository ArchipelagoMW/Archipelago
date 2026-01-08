# WARNING: THIS FILE HAS BEEN GENERATED!
# Modifications to this file will not be kept.
# If you need to change something here, check out codegen.py and the templates directory.


from .types.condition import *

variable_definitions: dict[str, dict[str, list[Condition]]] = {
    "vtShadeLock": {
        "shades": [
            ItemCondition(item_name='Blue Ice Shade', amount=1),
            ItemCondition(item_name='Red Flame Shade', amount=1),
            ItemCondition(item_name='Purple Bolt Shade', amount=1),
            ItemCondition(item_name='Azure Drop Shade', amount=1),
        ],"bosses": [
            LocationCondition(location_name='Temple Mine Shade Statue'),
            LocationCondition(location_name="Faj'ro Shade Statue"),
            LocationCondition(location_name="Zir'vitar Shade Statue"),
            LocationCondition(location_name="So'najiz Shade Statue"),
        ],
    },
    "vwPassage": {
        "meteor": [
            ItemCondition(item_name='Meteor Shade', amount=1),
        ],
    },
    "canGrind": {
        "noShadeWarp": [
            OrCondition(subconditions=[ItemCondition(item_name='Green Leaf Shade', amount=1), ItemCondition(item_name='Red Flame Shade', amount=1)]),
        ],
    },
}