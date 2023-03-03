from BaseClasses import Location

class DLCquestLocation(Location):
    game: str = "DLCquest"

offset = 120_000

location_table = {
    "Movement Pack": offset + 0
    "Animation Pack": offset + 1
    "Audio Pack": offset + 2
    "Pause Menu Pack": offset + 3
    "Time is Money Pack": offset + 4
    "Double jump Pack": offset + 5
    "Pet Pack": offset + 6
    "Sexy Outfits Pack": offset + 7
    "Top Hat Pack": offset + 8
    "Map Pack": offset + 9
    "Gun Pack": offset + 10
    "Zombie Pack": offset + 11
    "Night Map Pack": offset + 12
    "Psychological Warfare Pack": offset + 13
    "Horse Armor Pack": offset + 14
    "Finish the fight Pack": offset + 15
}