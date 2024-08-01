from BaseClasses import Location

location_descriptions = {
    # Locations
    "Level 1": "The first level, completed by delivering an unmodified shape",
    # Location Groups
    "Belt Upgrades": "All upgrades for belts, distributors, and tunnels"
}


class ShapezLocation(Location):
    game: str = "Shapez"
