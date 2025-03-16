from BaseClasses import Location


# a location is a check

class CandyBox2Location(Location):
    game: str = "Candy Box 2"


location_descriptions = {
    "HP Bar Unlock": ""
}

candy_box_locations = {
    "HP Bar Unlock": 1
}

village_locations = {}

village_shop_locations = {
    "Top Lollipop": 100,
    "Centre Lollipop": 101,
    "Bottom Lollipop": 102,
    "Chocolate Bar": 103,
    "Time Ring": 104,
    "Candy Merchant's Hat": 105,
    "Leather Gloves": 106,
    "Leather Boots": 107
}

village_house_1_locations = {
    "Lollipop on the bookshelf": 200,
    "Lollipop in the bookshelf": 201,
    "Lollipop under the rug": 202
}

locations = {
    **candy_box_locations,
    **village_locations,
    **village_shop_locations,
    **village_house_1_locations,
}
