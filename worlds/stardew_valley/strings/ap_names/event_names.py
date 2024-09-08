all_events = set()


def event(name: str):
    all_events.add(name)
    return name


class Event:
    victory = event("Victory")
    can_construct_buildings = event("Can Construct Buildings")
    start_dark_talisman_quest = event("Start Dark Talisman Quest")
    can_ship_items = event("Can Ship Items")
    can_shop_at_pierre = event("Can Shop At Pierre's")
    spring_farming = event("Spring Farming")
    summer_farming = event("Summer Farming")
    fall_farming = event("Fall Farming")
    winter_farming = event("Winter Farming")

    received_walnuts = event("Received Walnuts")
