from BaseClasses import Item, ItemClassification

class PlateUpItem(Item):
    game = "plateup"
    
    def __init__(self, name, classification, code, player):
        super().__init__(name, classification, code, player)
        self.code = code

    def __repr__(self):
        return "<{}>".format(self.name)


ITEMS = {
    #region Appliances
    "Hob": (1001, ItemClassification.useful),
    "Safe Hob": (10012, ItemClassification.useful),
    "Danger Hob": (10013, ItemClassification.useful),
    "Starting Hob": (10014, ItemClassification.filler),
    "Oven": (10015, ItemClassification.useful),
    "Microwave": (10016, ItemClassification.useful),
    "Gas Limiter": (10017, ItemClassification.useful),
    "Gas Override": (10018, ItemClassification.useful),
    "Sink": (1002, ItemClassification.useful),
    "Power Sink": (10022, ItemClassification.useful),
    "Soaking Sink": (10023, ItemClassification.useful),
    "Starting Sink": (10024, ItemClassification.filler),
    "Dishwasher": (10025, ItemClassification.useful),
    "Wash Basin": (10026, ItemClassification.useful),
    "Counter": (1003, ItemClassification.useful),
    "Workstation": (10032, ItemClassification.useful),
    "Freezer": (10033, ItemClassification.useful),
    "Prep Station": (10034, ItemClassification.useful),
    "Frozen Prep Station": (10035, ItemClassification.useful),
    "Dining Table": (1004, ItemClassification.useful),
    "Bar Table": (10042, ItemClassification.useful),
    "Basic Cloth Table": (10043, ItemClassification.useful),
    "Cheap Metal Table": (10044, ItemClassification.filler),
    "Fancy Cloth Table": (10045, ItemClassification.useful),
    "Coffee Table": (10046, ItemClassification.useful),
    "Starter Bin": (1005, ItemClassification.filler),
    "Bin": (10052, ItemClassification.filler),
    "Compactor Bin": (10053, ItemClassification.useful),
    "Composter Bin": (10054, ItemClassification.useful),
    "Expanded Bin": (10055, ItemClassification.useful),
    "Kitchen Floor Protector": (10056, ItemClassification.filler),
    "Rolling Pin": (1006, ItemClassification.useful),
    "Sharp Knife": (10062, ItemClassification.useful),
    "Scrubbing Brush": (10063, ItemClassification.useful),
    "Breadsticks": (1007, ItemClassification.filler),
    "Candle Box": (10072, ItemClassification.filler),
    "Napkins": (10073, ItemClassification.filler),
    "Sharp Cutlery": (10074, ItemClassification.useful),
    "Specials Menu": (10075, ItemClassification.filler),
    "Leftover Bags": (10076, ItemClassification.useful),
    "Supplies": (10077, ItemClassification.useful),
    "Hosting Stand": (10078, ItemClassification.filler),
    "Flower Pot": (10079, ItemClassification.useful),
    "Mop": (1008, ItemClassification.filler),
    "Lasting Mop": (10082, ItemClassification.useful),
    "Fast Mop": (10083, ItemClassification.useful),
    "Robot Mop": (10084, ItemClassification.useful),
    "Floor Buffer": (10085, ItemClassification.useful),
    "Robot Buffer": (10086, ItemClassification.useful),
    "Dish Rack": (10087, ItemClassification.useful),
    "Conveyor": (1009, ItemClassification.useful),
    "Grabber": (10092, ItemClassification.useful),
    "Smart Grabber": (10093, ItemClassification.useful),
    "Grabber Rotating": (10094, ItemClassification.useful),
    "Combiner": (10095, ItemClassification.useful),
    "Portioner": (10096, ItemClassification.useful),
    "Mixer": (10097, ItemClassification.useful),
    "Conveyor Mixer": (10098, ItemClassification.useful),
    "Heated Mixer": (10099, ItemClassification.useful),
    "Rapid Mixer": (100992, ItemClassification.useful),
    "Blueprint Cabinet": (1011, ItemClassification.filler),
    "Research Desk": (10112, ItemClassification.useful),
    "Blueprint Desk": (10113, ItemClassification.useful),
    "Discount Desk": (10114, ItemClassification.filler),
    "Clipboard Stand": (10115, ItemClassification.filler),
    "Copying Desk": (10116, ItemClassification.useful),
    "Trainers": (1012, ItemClassification.useful),
    "Wellies": (10122, ItemClassification.filler),
    "Work Boots": (10123, ItemClassification.filler),
    "Booking Desk": (1013, ItemClassification.filler),
    "Display Stand": (10132, ItemClassification.filler),
    "Dumbwaiter": (10133, ItemClassification.filler),
    "Teleporter": (10134, ItemClassification.useful),
    "Fire Extinguisher": (10135, ItemClassification.filler),
    "Ordering Terminal": (10136, ItemClassification.filler),
    "Specials Terminal": (10137, ItemClassification.filler),
    "Starter Plates": (1014, ItemClassification.filler),
    "Plates": (10142, ItemClassification.useful),
    "Auto Plater": (10143, ItemClassification.useful),
    "Pot Stack": (10144, ItemClassification.filler),
    "Serving Boards": (10145, ItemClassification.filler),
    "Coffee Machine": (1015, ItemClassification.filler),
    "Ice Dispenser": (10152, ItemClassification.filler),
    "Milk Steamer": (10153, ItemClassification.filler),
    "Woks": (10154, ItemClassification.filler),
    "Lasagne Tray": (10155, ItemClassification.filler),
    "Taco Trays": (10156, ItemClassification.filler),
    "Mixing Bowl": (10157, ItemClassification.filler),
    "Cake Tin": (10158, ItemClassification.filler),
    "Brownie Tray": (10159, ItemClassification.filler),
    "Cookie Tray": (1016, ItemClassification.filler),
    "Cupcake Tray": (10162, ItemClassification.filler),
    "Doughnut Tray": (10163, ItemClassification.filler),
    "Extra Life": (10164, ItemClassification.useful),
    #endregion
    #region Speed
    "Speed Upgrade Player": (10, ItemClassification.progression),
    "Speed Upgrade Appliance": (11, ItemClassification.progression),
    "Speed Upgrade Cook": (12, ItemClassification.progression),
    "Speed Upgrade Chop": (13, ItemClassification.progression),
    "Speed Upgrade Clean": (14, ItemClassification.progression),
    #endregion

    #region progression
    "Day Lease": (15, ItemClassification.progression),
    "Money Cap Increase": (16, ItemClassification.useful),



    #endregion
    #region traps
    "EVERYTHING IS ON FIRE": (20000, ItemClassification.trap),
    "Super Slow": (20001, ItemClassification.trap),
    "Random Customer Card": (20002, ItemClassification.trap),
    #endregion
}

# Add unlock items for each dish from a single source of truth
try:
    from .Locations import dish_dictionary
    for dish_id, dish_name in dish_dictionary.items():
        ITEMS[f"{dish_name} Unlock"] = (30000 + dish_id, ItemClassification.progression)
except Exception:
    for dish_id, dish_name in {
        101: "Salad",
        102: "Steak",
        103: "Burger",
        104: "Coffee",
        105: "Pizza",
        106: "Dumplings",
        107: "Turkey",
        108: "Pie",
        109: "Cakes",
        110: "Spaghetti",
        111: "Fish",
        112: "Tacos",
        113: "Hot Dogs",
        114: "Breakfast",
        115: "Stir Fry",
        116: "Sandwiches",
        117: "Sundaes",
    }.items():
        ITEMS[f"{dish_name} Unlock"] = (30000 + dish_id, ItemClassification.progression)