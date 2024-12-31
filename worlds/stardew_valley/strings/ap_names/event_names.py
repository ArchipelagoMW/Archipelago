all_events = set()


def event(name: str):
    all_events.add(name)
    return name


class Event:
    victory = event("Victory")
    spring_farming = event("Spring Farming")
    summer_farming = event("Summer Farming")
    fall_farming = event("Fall Farming")
    winter_farming = event("Winter Farming")

    received_walnuts = event("Received Walnuts")
