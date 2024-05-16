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
    copper_ore_event = event("Copper Ore (Logic event)")
    iron_ore_event = event("Iron Ore (Logic event)")
    gold_ore_event = event("Gold Ore (Logic event)")
    iridium_ore_event = event("Iridium Ore (Logic event)")
    copper_bar_event = event("Copper Bar (Logic event)")
    iron_bar_event = event("Iron Bar (Logic event)")
    gold_bar_event = event("Gold Bar (Logic event)")
    iridium_bar_event = event("Iridium Bar (Logic event)")
