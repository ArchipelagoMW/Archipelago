all_events = set()


def event(name: str):
    all_events.add(name)
    return name


class Event:
    victory = event("Victory")

    received_walnuts = event("Received Walnuts")
    received_progression_item = event("Received Progression Item")
    received_progression_percent = event("Received Progression Percent")
